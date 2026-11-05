# Verification assets for C₁a / C₁b / C₁c (framework: Galois pairing–trace correspondence)

Supporting code and figures for the constant pages [1a](https://teorth.github.io/optimizationproblems/constants/1a.html), [1b](https://teorth.github.io/optimizationproblems/constants/1b.html) and [1c](https://teorth.github.io/optimizationproblems/constants/1c.html) of teorth/optimizationproblems. Per that repository's `CONTRIBUTING.md` (markdown-only changes; supporting code and data live outside the main repo), these files are hosted here, in the authors' own repository.

Paper: [doi:10.5281/zenodo.23676163](https://doi.org/10.5281/zenodo.23676163) (V5, Appendices E–F), framework DOI [10.5281/zenodo.23603555](https://doi.org/10.5281/zenodo.23603555); C₁c note [doi:10.5281/zenodo.23694729](https://doi.org/10.5281/zenodo.23694729).

## Contents

| file | purpose |
|---|---|
| `AppendixCD_RiemannSum_PowerOrder_Verification.py` | Appendices C–E: Riemann-sum ladder for the sole input $\Pi$, C₁b endpoint convergence and two-sided clamping window (decimal 60-digit). |
| `AppendixF_C1a_Scissors_Verification.py` | Appendix F: C₁a scissors structure — endpoint reverse monotonicity, analytic in-band status of $s^*=3/2$, clamping windows (decimal 60-digit). |
| `c1c_bounds_check.py` | C₁c: recomputes the upper anchor and the lower windows from the single input $\pi$ (Machin) plus the eigen-equation $\tan x = x$, in finite rational arithmetic. |
| `c1a.html`, `c1b.html` | Squeeze-figure pages (clamping windows vs $N$) cited from the constant pages. |

Usage:

```bash
python scripts/AppendixCD_RiemannSum_PowerOrder_Verification.py
python scripts/AppendixF_C1a_Scissors_Verification.py
python scripts/c1c_bounds_check.py
```

## Numerical-precision caveat (float64 rows)

The error bound quoted in the paper, $|\pi_k - \Pi| \le 1/(3N^2)$, is a **pure truncation bound** for the midpoint rule ($\max|f''| = 8$ on $[0,1]$); it does **not** include cumulative floating-point rounding. The float64 rounding floor is $\epsilon_{\mathrm{mach}} \approx 2.22\times10^{-16}$ (Kahan summation; naive summation is worse). The two effects cross at $N \approx 4\times10^{7}$:

- $N \lesssim 10^{7}$: truncation dominates; the $1/(3N^2)$ bound is tight and the measured error sits below it.
- $N \gtrsim 5\times10^{7}$ (e.g. the $N = 10^{8}$ row): rounding dominates; measured $|\pi_k - \pi| \approx 3.6\times10^{-16}$ reflects the float64 noise floor, not a failure of the quadrature.

Certified rows therefore use decimal 60-digit arithmetic (default in the scripts above); float64 rows are indicative only. The clamping-window conclusions are unaffected: for C₁a the scissors direction is fixed analytically by $\delta' = -5 - \tfrac{48}{5}\cos(\Pi/5)\sin(\Pi/5) < 0$, and a $\sim 4\times10^{-16}$ bias in $\pi_k$ is thirteen orders of magnitude below the band half-width $\sim 2.86\times10^{-3}$ (C₁a) and eight orders below the C₁b band $1.18\times10^{-8}$.

Thanks to @chessing234 (teorth/optimizationproblems#288) for prompting this clarification.
