# Certificate summary

- issued: 2026-11-05T22:57:02.982771+00:00
- primary: python-flint 0.9.0 (Arb), prec=200 bits
- cross-check: mpmath 1.4.1 iv, prec=200 bits
- code_sha256: bcff4d80ba658b2a933c8539c29d8b8524efde48e45ca24d3574485745109fcd

| claim | published | Arb mid | radius | R1 | R2 | R3 | verdict |
|---|---|---|---|---|---|---|---|
| DELTA-OPEN | 0.00024066 | 0.00024066455040289691430408... | 6.52e-59 | True | True | True | PASS |
| C1A-UPPER | 1.50286149714653 | 1.50286149714653363716921306... | 7.78e-58 | True | True | True | PASS |
| C1A-LOWER | 1.49713848093279 | 1.49713848093279228344940175... | 7.78e-58 | True | True | True | PASS |
| C1B-UPPER | 0.380422678036171 | 0.38042267803617106403095165... | 4.20e-58 | True | True | True | PASS |
| C1B-LOWER | 0.380422666213372492 | 0.38042266621337249178165438... | 4.20e-58 | True | True | True | PASS |
| C1B-BANDWIDTH | 1.18228e-08 | 1.18227985722492972671208047... | 6.41e-63 | True | True | True | PASS |
| C84-WINDOW | 1.2497593 | 1.24975933544959710308569591... | 6.52e-59 | True | True | True | PASS |
| C84-GAP | 0.0068 | 0.00680501086261945488355791... | 6.67e-59 | True | True | True | PASS |
| C84-GAP-DELTA (window_basis) | 28.3 | 28.2759170439816547863791460... | 7.94e-54 | True | True | True | PASS |
| C84-GAP-DELTA (anchor_basis) | 29.3 | 29.2759170439816547863791460... | 7.94e-54 | True | True | True | PASS |
| END-ORDER | (sign) | delta_open>0 | - | True | - | - | PASS |

## Appendix E/F rows (Arb-certified)

| N | E err mid | trunc bound 1/(3N^2) | r_IA | E certified | E-window in band | F contains 3/2 |
|---|---|---|---|---|---|---|
| 1000 | 8.333333333333 | 3.33e-07 | 1.62e-57 | True | False | True |
| 10000 | 8.333333333333 | 3.33e-09 | 1.46e-56 | True | False | True |
| 100000 | 8.333333333333 | 3.33e-11 | 1.64e-55 | True | True | True |
| 1000000 | 8.333333333333 | 3.33e-13 | 1.62e-54 | True | True | True |
| 10000000 | 8.333333333333 | 3.33e-15 | 1.48e-53 | True | True | True |
| 100000000 | 8.333333333333 | 3.33e-17 | 1.71e-52 | True | True | True |

**overall: ALL PASS**

Rules pre-registered in the scheme; FAIL => re-run at higher precision or correct the paper, never relax thresholds.