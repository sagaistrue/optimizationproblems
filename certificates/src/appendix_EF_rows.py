"""Appendix E/F rows of the v5 paper, certified with Arb ball arithmetic.

E rows (C1b): pi_k = (4/N) * sum_{i=1..N} 1/(1+x_i^2), x_i = (i-1/2)/N.
  Certified statement: |pi_k - pi| <= 1/(3N^2) + r_IA,
  where 1/(3N^2) is the paper's analytic truncation bound (max|f''|=8,
  midpoint rule) and r_IA is the self-certified ball radius.
  This supersedes the float64 row at N=1e8 (measured 3.62e-16 there was
  float64 noise; the true error is ~8.3e-18).

E-window rows (C1b): one-sided window [L0(p_hi), U0(p_lo)] (both endpoints
  increase with Pi), certified to lie inside the true band when nonempty.

F rows (C1a scissors): window [lo(p_lo), up(p_lo)] (lo increasing, up
  decreasing in Pi) certified to contain s* = 3/2; width reported.

Usage: python appendix_EF_rows.py [--big]   (--big adds the N=1e8 rows)
"""
import json, os, sys, datetime
from flint import arb, ctx

ctx.prec = 200

PI = arb.pi()
SQRT5 = arb(5).sqrt()
PHI = (1 + SQRT5) / 2
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "raw_ef.json")


def lo_edge(b):
    return b.mid() - b.rad()


def hi_edge(b):
    return b.mid() + b.rad()


def ball(x):
    return {"mid": x.mid().str(70, radius=False), "radius": float(x.rad())}


def pi_k_ball(N):
    s = arb(0)
    twoN = arb(2 * N)
    for i in range(1, N + 1):
        x = arb(2 * i - 1) / twoN
        s += 1 / (1 + x * x)
    return 4 * s / N


def c1b_lo_at(p):
    return ((3 - SQRT5) - (3 + SQRT5) * arb(6).sqrt() * (6 * PHI**2 - 5 * p)) / 2


def c1b_up_at(p):
    return ((3 - SQRT5) - (1 + SQRT5) * (5 * p).sqrt() * (6 * PHI**2 - 5 * p)) / 2


def c1a_lo_at(p):
    return arb(3) / 2 * (1 - 2 * (6 * PHI**2).sqrt() * (6 * PHI**2 - 5 * p))


def c1a_up_at(p):
    return arb(3) / 2 * (1 + 2 * (5 * p).sqrt() * (6 * PHI**2 - 5 * p))


def main():
    big = "--big" in sys.argv
    Ns = [10**3, 10**4, 10**5, 10**6, 10**7] + ([10**8] if big else [])
    true_lo, true_up = c1b_lo_at(PI), c1b_up_at(PI)
    s_star_c1b = arb("0.380422672124771778")
    three_half = arb(3) / 2
    rows = []
    for N in Ns:
        print(f"N = {N} ...", flush=True)
        pk = pi_k_ball(N)
        e = abs(pk - PI)
        trunc = arb(1) / (3 * arb(N) ** 2)
        r_ia = pk.rad() + PI.rad()
        # E row: |pi_k - pi| <= trunc + r_IA, all balls, certified compare
        e_pass = bool(e <= trunc + r_ia)
        # certified one-sided enclosures of pi (sum radius + truncation bound):
        #   p_lo <= pi <= p_hi   (pi_k is biased high by ~1/(12N^2), so the
        #   truncation bound must be subtracted to obtain a lower enclosure)
        p_lo = lo_edge(pk) - trunc
        p_hi = hi_edge(pk) + trunc
        # E-window (C1b): [L0(p_hi), U0(p_lo)] inside true band, contains s*
        wl, wu = c1b_lo_at(p_hi), c1b_up_at(p_lo)
        ew_nonempty = bool(wl < wu)
        ew_contained = bool((wl - true_lo > 0) and (true_up - wu > 0)) if ew_nonempty else False
        ew_sstar = bool((s_star_c1b - wl >= 0) and (wu - s_star_c1b >= 0)) if ew_nonempty else False
        # F row (C1a scissors): window at p_lo contains 3/2
        fl, fu = c1a_lo_at(p_lo), c1a_up_at(p_lo)
        f_contains = bool((fl < three_half) and (fu > three_half))
        rows.append({
            "N": N,
            "E": {"err_ball": ball(e), "trunc_bound": float(trunc.mid()),
                  "r_ia": float(r_ia), "certified": e_pass},
            "E_window": {"lo": ball(wl), "hi": ball(wu),
                         "nonempty": ew_nonempty, "inside_band": ew_contained,
                         "contains_s_star": ew_sstar},
            "F": {"lo": ball(fl), "hi": ball(fu), "width": ball(fu - fl),
                  "contains_3/2": f_contains},
        })
        print(f"  E err ~ {e.mid().str(12, radius=False)} (bound {trunc.mid().str(6, radius=False)}) pass={e_pass}; "
              f"E-window contained={ew_contained}; F contains 3/2={f_contains}", flush=True)
    res = {"tool": "python-flint 0.9.0 (Arb), prec=200 bits",
           "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "rows": rows}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
