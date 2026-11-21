# A polydrafter with Heesch number 5, a polykite with Heesch number 4, and a census of Heesch numbers of polykites and polydrafters

The *Heesch number* of a shape that does not tile the plane is the largest number of complete
rings (coronas) of copies of the shape that can surround it. For polyominoes, polyhexes and
polyiamonds, C. S. Kaplan computed Heesch numbers exhaustively ([Heesch numbers of unmarked
polyforms](https://arxiv.org/abs/2105.09438)); the largest value found is 4. This repository extends that
computation to **polykites** (unions of kites of the [3.4.6.4] Laves tiling, the family of the "hat"
monotile), **polydrafters**, and four other grids supported by Kaplan's software (half-Cairo,
trihex, octasquare, bevelhex), using that software.

The main finding is a **22-drafter polydrafter with Heesch number 5**: it can be surrounded by five
complete hole-free coronas (126 copies), but not by six. It is the only one among the 33,078,305
holeless free 22-drafters. For unmarked polyforms, the largest Heesch number previously reported is 4
(Kaplan); Mann and Thomas reached 5 with edge-marked polyforms, and Bašić's record 6 is not a polyform.
We also found a **16-kite polykite with Heesch number 4** (four coronas, 61 copies), the only one among
the 15,032,772 holeless free 16-kites.

> **Status.** Not checked by a third party; novelty not confirmed (unpublished computations may
> exist). Heesch numbers are computed, as in Kaplan's work, for copies placed on the underlying grid.
> The four coronas are re-checked by an independent program (`verification/`); the impossibility
> of a fifth corona relies on the SAT solver used by `heesch-sat`. Corrections and pointers to
> prior work are welcome: please open an issue.

*Résumé en français : un polydrafter de 22 drafters de nombre de Heesch 5 (cinq couronnes, pas six) et un polykite de 16 cerfs-volants de nombre de Heesch 4 (quatre couronnes
complètes, pas cinq), et le recensement des nombres de Heesch des polykites (jusqu'à 17 cerfs-volants),
des polydrafters (jusqu'à 22) et de quatre autres grilles (maximum 3). Pas encore vérifié par un tiers ;
nouveauté non confirmée.*

Interactive figure (French): https://totocaedres.fransys.io/pistes/heesch/notre-travail

## Files

- `results/drafter22_heesch5.txt` and `results/kite16_heesch4.txt` — each shape and its witness patch, in the text format of
  [heesch-sat](https://github.com/isohedral/heesch-sat): first line, the 16 kite cells (`D …` drafter-grid or `K …`
  kite-grid coordinates); then `~ 4 4 1` (Heesch numbers without/with holes in the outer corona);
  then the number of copies and, for each copy, its corona index and the affine map
  `<a,b,c,d,e,f>` : `(x, y) ↦ (a x + b y + c, d x + e y + f)` applied to the cells.
- `results/census.csv` — per grid and size: number of holeless free shapes, isohedral tilers,
  inconclusive shapes (anisohedral or aperiodic tilers, or shapes too slow to classify), non-tilers,
  and the number of non-tilers with each hole-free Heesch number `hc0` … `hc5`.
- `verification/verify_coronas.py` — independent check of the witness (Python 3, no dependency).

## Census summary

| Grid | Sizes | Shapes classified | Largest Heesch number |
|---|---|---|---|
| polykites | 1–17 | 73,392,986 | **4** (one 16-kite) |
| polydrafters | 1–22 | 56,414,167 | **5** (one 22-drafter) |
| poly-half-Cairos | 1–15 | 2,644,550 | 1 |
| poly-(3.6.3.6)-tiles (trihex) | 1–13 | 1,289,367 | 2 |
| poly-(4.8.8)-tiles (octasquare) | 1–11 | 1,761,672 | 3 |
| poly-(4.6.12)-tiles (bevelhex) | 1–10 | 2,030,603 | 2 |

Checks: for polykites up to 17 kites, the numbers of holeless shapes and of non-tilers coincide
exactly with the independent table of [J. Myers](https://www.polyomino.org.uk/mathematics/polyform-tiling/);
on 6-cell polyhexes the run reproduces Kaplan's published result.

## Verify

```bash
python3 verification/verify_coronas.py results/drafter22_heesch5.txt
python3 verification/verify_coronas.py results/kite16_heesch4.txt
```

The script checks that all copies are isometric to the shape, that no two copies overlap,
and that for each k the union of coronas 0..k contains the union of coronas 0..k−1 in its interior
and has no hole. It rejects deliberately corrupted witnesses (a missing, duplicated or shifted copy).

To recompute: build [heesch-sat](https://github.com/isohedral/heesch-sat) (C++, CryptoMiniSat) and run
`gen -kite -size 16 -free` then `sat -isohedral -show` on each shape.

## Licence

Code: MIT (`LICENSE`). Data: CC BY 4.0 (`LICENSE-DATA.md`).
