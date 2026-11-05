# Interval-arithmetic certificates for the C₁a / C₁b / C₈₄ registered claims

Certified numerical layer for the constant pages [1a](https://teorth.github.io/optimizationproblems/constants/1a.html), [1c](https://teorth.github.io/optimizationproblems/constants/1c.html) and [84a](https://teorth.github.io/optimizationproblems/constants/84a.html) of teorth/optimizationproblems, hosted in the authors' repository per that project's CONTRIBUTING.md. The scripts in [`../scripts/`](../scripts/) are the decimal 60-digit indicative layer; this directory is the rigorous layer, using interval arithmetic with self-certified radii.

Papers: V5 [doi:10.5281/zenodo.23676163](https://doi.org/10.5281/zenodo.23676163) (C₁a/C₁b, Appendices E–F); V1A [doi:10.5281/zenodo.23990285](https://doi.org/10.5281/zenodo.23990285) (C₈₄).

## Layers and pre-registered rules

- **L3 (primary)**: Arb ball arithmetic via python-flint 0.9.0, precision 200 bits. Radii are self-certified by the library.
- **L2 (cross-check)**: mpmath 1.4.1 interval arithmetic (`iv`), precision 200 bits, independent implementation.
- **R1**: the L3 ball and the L2 interval intersect.
- **R2**: the L3 radius is below the claim's registered threshold (10⁻¹⁸ … 10⁻¹² per the registry in `src/verify_certificates.py`).
- **R3**: the published value lies in the ball within half a ulp of its printed precision.
- Discipline: a FAIL is resolved by re-running at higher precision or by correcting the paper — thresholds are never relaxed.

## Status: ALL PASS (2026-11-06)

Twelve core verdicts: `DELTA-OPEN`, `C1A-UPPER/LOWER`, `C1B-UPPER/LOWER`, `C1B-BANDWIDTH`, `C84-WINDOW`, `C84-GAP`, `C84-GAP-DELTA` (window and anchor bases), `END-ORDER` (certified sign of $\delta_{\mathrm{open}}=6\Phi^2-5\pi$). Radii ≈ 10⁻⁵⁸ … 10⁻⁶³.

Appendix E rows N = 10³ … 10⁸: the certified error is exactly 1/(12N²) at every level — for N = 10⁸ it is 8.33×10⁻¹⁸ with interval radius 1.71×10⁻⁵². This separates the pure truncation term from the float64 noise floor (~3.6×10⁻¹⁶) discussed in [`../scripts/README.md`](../scripts/README.md) and resolves the question raised in teorth/optimizationproblems#288. Appendix F: the clamping window contains $s^* = 3/2$ at every N, and the C₁b two-sided window enters the band width from N = 10⁵, matching the paper.

Per-claim verdict records: `claims/*.json`; human-readable summary: `results/latest/summary.md`.

## Erratum (2026-11-06): C1B-LOWER

The value displayed in v5 §3.2 (0.380422666213373) carries a 1-ulp rounding typo in the last digit. The certified value is 0.38042266621337249178… (Arb and mpmath-iv agree to 200 bits), so the correct 15-digit rounding is …372. The Appendix Π-table value 0.380422666213372492… was already correct and is the canonical published value used by the registry (`claims/C1B-LOWER.json`). The 1-ulp difference is far below any measured window width and does not affect the kill-line semantics; the paper carries a matching erratum note at §3.2.

## Reproduce

```bash
pip install python-flint==0.9.0 mpmath==1.4.1
cd certificates
python src/claims_arb.py                 # L3 balls   -> results/raw_arb.json
python src/claims_mpmath.py              # L2 intervals -> results/raw_mpmath.json
python src/appendix_EF_rows.py           # E/F rows up to N = 1e7 -> results/raw_ef.json
python src/appendix_EF_rows.py --big     # additionally the N = 1e8 row (slow)
python src/verify_certificates.py        # verdicts -> claims/*.json + results/latest/summary.md
```

Exit code 0 ⇔ ALL PASS; exit code 1 if any claim fails.

## Integrity binding

`results/latest/summary.md` records `code_sha256` over the three generator scripts (`claims_arb.py`, `claims_mpmath.py`, `appendix_EF_rows.py`). This directory is pinned to LF line endings (`.gitattributes`) so the hash is stable across clones and platforms.

Prepared by sagaistrue with AI assistance (Trae).
