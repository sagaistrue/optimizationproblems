"""Verifier / certificate issuer.

Merges raw_arb.json (L3 primary) + raw_mpmath.json (L2 cross-check) +
raw_ef.json (appendix rows), applies the pre-registered rules of the scheme
  R1  the two independent enclosures overlap;
  R2  the primary (Arb) radius is below the registered threshold;
  R3  the published decimal lies inside the primary ball
      (the published decimal itself carries an implied rounding of
      half a unit in its last place, which is added to the ball radius);
then writes claims/<ID>.json per claim and results/latest/summary.md.

Failure discipline (scheme sec.1): a FAIL can only be resolved by re-running
at higher precision or by correcting the paper -- never by relaxing a
threshold.
"""
import json, os, hashlib, datetime
from mpmath import mpf, mp

mp.dps = 80
HERE = os.path.dirname(__file__)
RES = os.path.join(HERE, "..", "results")
CLAIMS = os.path.join(HERE, "..", "claims")

REGISTRY = {
    "DELTA-OPEN":    {"tex": "delta_open = 6*Phi^2 - 5*pi",
                      "published": "2.4066e-4", "radius": 1e-18},
    "C1A-UPPER":     {"tex": "3/2*(1 + 2*sqrt(5*pi)*delta)",
                      "published": "1.50286149714653", "radius": 1e-15},
    "C1A-LOWER":     {"tex": "3/2*(1 - 2*sqrt(6*Phi^2)*delta)",
                      "published": "1.49713848093279", "radius": 1e-15},
    "C1B-UPPER":     {"tex": "((3-sqrt5) - (1+sqrt5)*sqrt(5*pi)*delta)/2",
                      "published": "0.380422678036171", "radius": 1e-16},
    # published = canonical Appendix Pi-table value (18 dp). The v5 §3.2 display
    # (...373) carries a 1-ulp typo documented by the 2026-11-06 erratum.
    "C1B-LOWER":     {"tex": "((3-sqrt5) - (3+sqrt5)*sqrt6*delta)/2",
                      "published": "0.380422666213372492", "radius": 1e-16},
    "C1B-BANDWIDTH": {"tex": "Phi*delta^2/(sqrt(6*Phi^2)+sqrt(5*pi))",
                      "published": "1.18228e-8", "radius": 1e-12},
    "C84-WINDOW":    {"tex": "5/4 - delta_open",
                      "published": "1.2497593", "radius": 1e-15},
    "C84-GAP":       {"tex": "(5/4 - delta_open) - (1 + 1/4.116)",
                      "published": "6.8e-3", "radius": 1e-12},
    "C84-GAP-DELTA": {"tex": "gap/delta_open (window basis; anchor basis)",
                      "published": ["28.3", "29.3"], "radius": 1e-4},
    "END-ORDER":     {"tex": "6*Phi^2 > 5*pi  (sign certificate)",
                      "published": None, "radius": None},
}


def half_ulp(s):
    s = s.strip().lower()
    if "e" in s:
        mant, ex = s.split("e")
        dec = len(mant.split(".")[1]) if "." in mant else 0
        return mpf(10) ** (int(ex) - dec - 1) / 2 * 10
    dec = len(s.split(".")[1]) if "." in s else 0
    return mpf(10) ** mpf(-(dec + 1)) * 5


def code_hash():
    h = hashlib.sha256()
    for fn in ("claims_arb.py", "claims_mpmath.py", "appendix_EF_rows.py"):
        with open(os.path.join(HERE, fn), "rb") as f:
            h.update(f.read())
    return h.hexdigest()


def main():
    arb = json.load(open(os.path.join(RES, "raw_arb.json"), encoding="utf-8"))
    imm = json.load(open(os.path.join(RES, "raw_mpmath.json"), encoding="utf-8"))
    ef_path = os.path.join(RES, "raw_ef.json")
    ef = json.load(open(ef_path, encoding="utf-8")) if os.path.exists(ef_path) else None
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    chash = code_hash()
    os.makedirs(CLAIMS, exist_ok=True)
    os.makedirs(os.path.join(RES, "latest"), exist_ok=True)
    summary = ["# Certificate summary", "",
               f"- issued: {ts}",
               f"- primary: {arb['tool']}", f"- cross-check: {imm['tool']}",
               f"- code_sha256: {chash}", "",
               "| claim | published | Arb mid | radius | R1 | R2 | R3 | verdict |",
               "|---|---|---|---|---|---|---|---|"]
    all_pass = True
    for cid, meta in REGISTRY.items():
        pa, pm = arb["claims"][cid], imm["claims"][cid]
        if cid == "END-ORDER":
            r1 = pa["delta_open_positive_certified"] and pm["delta_open_positive_certified"]
            rules, verdict = {"R1_overlap": r1, "R2_radius": None, "R3_published_inside": None}, r1
            cert = {"cert_id": cid, "claim_tex": meta["tex"], "published_value": None,
                    "precision_bits": 200,
                    "primary": {"tool": arb["tool"], "sign_certified": pa["delta_open_positive_certified"]},
                    "crosscheck": {"tool": imm["tool"], "sign_certified": pm["delta_open_positive_certified"]},
                    "rules": rules, "verdict": "PASS" if verdict else "FAIL",
                    "code_sha256": chash, "timestamp_utc": ts}
            summary.append(f"| {cid} | (sign) | delta_open>0 | - | {r1} | - | - | {'PASS' if verdict else 'FAIL'} |")
        else:
            subs = ("window_basis", "anchor_basis") if cid == "C84-GAP-DELTA" else (None,)
            for si, sub in enumerate(subs):
                ba = pa[sub] if sub else pa
                bm = pm[sub] if sub else pm
                mid, rad = mpf(ba["mid"]), mpf(ba["radius"])
                a_lo, a_hi = mid - rad, mid + rad
                i_lo, i_hi = mpf(bm["lo"]), mpf(bm["hi"])
                r1 = max(a_lo, i_lo) <= min(a_hi, i_hi)
                r2 = True if meta["radius"] is None else float(rad) < meta["radius"]
                pubs = meta["published"] if isinstance(meta["published"], list) else [meta["published"]]
                pub = mpf(pubs[si] if sub else pubs[0])
                r3 = abs(pub - mid) <= rad + half_ulp(str(pubs[si] if sub else pubs[0]))
                verdict = r1 and r2 and r3
                name = cid + (f" ({sub})" if sub else "")
                cert = {"cert_id": name, "claim_tex": meta["tex"], "published_value": str(pub),
                        "precision_bits": 200,
                        "primary": {"tool": arb["tool"], "mid": ba["mid"], "radius": ba["radius"]},
                        "crosscheck": {"tool": imm["tool"], "lo": bm["lo"], "hi": bm["hi"]},
                        "rules": {"R1_overlap": r1, "R2_radius": r2, "R3_published_inside": r3},
                        "verdict": "PASS" if verdict else "FAIL",
                        "code_sha256": chash, "timestamp_utc": ts}
                fn = name.replace(" ", "_").replace("(", "").replace(")", "") + ".json"
                json.dump(cert, open(os.path.join(CLAIMS, fn), "w", encoding="utf-8"),
                          ensure_ascii=False, indent=2)
                summary.append(f"| {name} | {pub} | {ba['mid'][:28]}... | {ba['radius']:.2e} | {r1} | {r2} | {r3} | {'PASS' if verdict else 'FAIL'} |")
                all_pass &= verdict
            continue
        fn = cid + ".json"
        json.dump(cert, open(os.path.join(CLAIMS, fn), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        all_pass &= verdict
    if ef:
        summary += ["", "## Appendix E/F rows (Arb-certified)", "",
                    "| N | E err mid | trunc bound 1/(3N^2) | r_IA | E certified | E-window in band | F contains 3/2 |",
                    "|---|---|---|---|---|---|---|"]
        for r in ef["rows"]:
            summary.append(
                f"| {r['N']} | {r['E']['err_ball']['mid'][:14]} | {r['E']['trunc_bound']:.2e} | "
                f"{r['E']['r_ia']:.2e} | {r['E']['certified']} | {r['E_window']['inside_band']} | {r['F']['contains_3/2']} |")
            all_pass &= r["E"]["certified"] and r["F"]["contains_3/2"]
    summary += ["", f"**overall: {'ALL PASS' if all_pass else 'FAIL PRESENT'}**", "",
                "Rules pre-registered in the scheme; FAIL => re-run at higher precision or correct the paper, never relax thresholds."]
    open(os.path.join(RES, "latest", "summary.md"), "w", encoding="utf-8").write("\n".join(summary))
    print("\n".join(summary))
    raise SystemExit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
