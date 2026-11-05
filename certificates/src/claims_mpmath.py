"""L2 cross-check implementation: the same core claims via mpmath interval
arithmetic (independent code path). Writes lo/hi enclosures; the verifier
checks overlap with the Arb balls (rule R1).
"""
import json, os, datetime
from mpmath import iv

iv.prec = 200  # bits, matching the Arb primary

PI = iv.pi
SQRT5 = iv.sqrt(5)
PHI = (1 + SQRT5) / 2

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "raw_mpmath.json")


def enc(x):
    # ctx_iv endpoints are ivmpf point-intervals; repr carries full precision
    return {"lo": repr(x.a).split("'")[1], "hi": repr(x.b).split("'")[1]}


def main():
    delta = 6 * PHI**2 - 5 * PI
    c1a_up = iv.mpf(3) / 2 * (1 + 2 * iv.sqrt(5 * PI) * delta)
    c1a_lo = iv.mpf(3) / 2 * (1 - 2 * iv.sqrt(6 * PHI**2) * delta)
    c1b_up = ((3 - SQRT5) - (1 + SQRT5) * iv.sqrt(5 * PI) * delta) / 2
    c1b_lo = ((3 - SQRT5) - (3 + SQRT5) * iv.sqrt(6) * delta) / 2
    c1b_bw = PHI * delta**2 / (iv.sqrt(6 * PHI**2) + iv.sqrt(5 * PI))
    win_lo = iv.mpf(5) / 4 - delta
    ceiling = 1 + 1 / iv.mpf("4.116")
    gap = win_lo - ceiling
    res = {
        "tool": "mpmath 1.4.1 iv, prec=200 bits",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "claims": {
            "DELTA-OPEN": enc(delta),
            "C1A-UPPER": enc(c1a_up),
            "C1A-LOWER": enc(c1a_lo),
            "C1B-UPPER": enc(c1b_up),
            "C1B-LOWER": enc(c1b_lo),
            "C1B-BANDWIDTH": enc(c1b_bw),
            "C84-WINDOW": enc(win_lo),
            "C84-GAP": enc(gap),
            "C84-GAP-DELTA": {"window_basis": enc(gap / delta),
                              "anchor_basis": enc((iv.mpf(5) / 4 - ceiling) / delta)},
            "END-ORDER": {"delta_open_positive_certified": bool(delta > 0),
                          "note": "certified sign of 6*Phi^2 - 5*pi"},
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
