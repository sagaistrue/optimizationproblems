"""L3 primary implementation: Arb ball-arithmetic values for the core claims.

Scheme: verification/区间算术认证证书方案.md (sections 1, 3, 4.1).
Every output number is a ball [mid-radius, mid+radius]; the radius is
self-certified by Arb's ball arithmetic (no external error analysis).
"""
import json, os, datetime
from flint import arb, ctx

ctx.prec = 200  # bits (~60 decimal digits); scheme requires >= 134 bits

PI = arb.pi()
SQRT5 = arb(5).sqrt()
PHI = (1 + SQRT5) / 2

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "raw_arb.json")


def ball(x):
    # print far more digits than the radius so the printing truncation
    # (~0.5 ulp of the last printed digit) stays far below the true radius
    return {"mid": x.mid().str(70, radius=False), "radius": float(x.rad())}


def main():
    delta = 6 * PHI**2 - 5 * PI                                  # DELTA-OPEN
    c1a_up = arb(3) / 2 * (1 + 2 * (5 * PI).sqrt() * delta)      # C1A-UPPER
    c1a_lo = arb(3) / 2 * (1 - 2 * (6 * PHI**2).sqrt() * delta)  # C1A-LOWER
    c1b_up = ((3 - SQRT5) - (1 + SQRT5) * (5 * PI).sqrt() * delta) / 2   # C1B-UPPER
    c1b_lo = ((3 - SQRT5) - (3 + SQRT5) * arb(6).sqrt() * delta) / 2     # C1B-LOWER
    c1b_bw = PHI * delta**2 / ((6 * PHI**2).sqrt() + (5 * PI).sqrt())    # C1B-BANDWIDTH
    win_lo = arb(5) / 4 - delta                                  # C84-WINDOW
    ceiling = 1 + 1 / arb("4.116")                               # Sawin family ceiling (rounded c)
    gap = win_lo - ceiling                                       # C84-GAP
    res = {
        "tool": f"python-flint 0.9.0 (Arb), prec=200 bits",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "claims": {
            "DELTA-OPEN": ball(delta),
            "C1A-UPPER": ball(c1a_up),
            "C1A-LOWER": ball(c1a_lo),
            "C1B-UPPER": ball(c1b_up),
            "C1B-LOWER": ball(c1b_lo),
            "C1B-BANDWIDTH": ball(c1b_bw),
            "C84-WINDOW": ball(win_lo),
            "C84-GAP": ball(gap),
            "C84-GAP-DELTA": {"window_basis": ball(gap / delta),
                              "anchor_basis": ball((arb(5) / 4 - ceiling) / delta)},
            "END-ORDER": {"delta_open_positive_certified": bool(delta > 0),
                          "note": "certified sign of 6*Phi^2 - 5*pi (equivalently 5*pi < 6*Phi^2)"},
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("wrote", OUT)
    for k, v in res["claims"].items():
        print(k, v)


if __name__ == "__main__":
    main()
