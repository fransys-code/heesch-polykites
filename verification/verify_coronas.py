#!/usr/bin/env python3
"""Independent check of a Heesch witness patch for a polykite or a polydrafter (output of `sat -show` from heesch-sat).
Only the file format follows Kaplan's conventions (cell coordinates on the kite or drafter grid); the checks are
redone here: every copy is isometric to the base shape, copies do not overlap, and for each k the union of
coronas 0..k contains the union of coronas 0..k-1 in its interior (every cell touching the previous union, even
at a single vertex, belongs to it) and has no hole.
Usage: verify_coronas.py WITNESS.txt (grid read from the first letter: K kites, D drafters)"""
import itertools, math, sys
from collections import defaultdict

ORIENT = [7, 0, 7, 7, 7, 3, 1, 7, 4, 5, 7, 2, 7, 3, 7, 0, 7, 7, 7, 2, 1, 7, 4, 5, 7, 7, 7, 3, 7, 0, 4, 5, 7, 2, 1, 7]
ORIGINES = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
SOMMETS = [[(0, 0), (2, -1), (2, 0), (1, 1)], [(0, 0), (1, 1), (0, 2), (-1, 2)], [(0, 0), (-1, 2), (-2, 2), (-2, 1)],
           [(0, 0), (-2, 1), (-2, 0), (-1, -1)], [(0, 0), (-1, -1), (0, -2), (1, -2)], [(0, 0), (1, -2), (2, -2), (2, -1)]]


D_TYPES = [None, None, None, None, None, None, None, None, None, 0, None, 5, None, None, None, 1, None, None, 4, None, None, None, None, None, None, None, 3, 2, None, 8, 9, None, None, None, None, None, None, None, 10, None, None, 7, None, None, None, 11, None, 6, None]
D_LOS = [(-2, -1), (-1, -2), (1, -3), (2, -3), (3, -2), (3, -1), (2, 1), (1, 2), (-1, 3), (-2, 3), (-3, 2), (-3, 1)]
D_SOMMETS = [[(0, 0), (6, 0), (4, 4)], [(4, 4), (0, 6), (0, 0)], [(0, 0), (0, 6), (-4, 8)], [(0, 0), (-4, 8), (-6, 6)],
             [(0, 0), (-6, 6), (-8, 4)], [(0, 0), (-8, 4), (-6, 0)], [(0, 0), (-6, 0), (-4, -4)], [(0, 0), (-4, -4), (0, -6)],
             [(0, 0), (0, -6), (4, -8)], [(0, 0), (4, -8), (6, -6)], [(0, 0), (6, -6), (8, -4)], [(0, 0), (8, -4), (6, 0)]]
GRILLE = "K"


def orient(x, y):
    if GRILLE == "K":
        o = ORIENT[(y % 6) * 6 + (x % 6)]
        return -1 if o == 7 else o
    t = D_TYPES[(y % 7) * 7 + (x % 7)]
    return -1 if t is None else t


def kite(x, y):
    o = orient(x, y)
    assert o >= 0, (x, y)
    if GRILLE == "K":
        cx, cy = x - ORIGINES[o][0], y - ORIGINES[o][1]
        return tuple((cx + a, cy + b) for a, b in SOMMETS[o])
    px, py = x + D_LOS[o][0], y + D_LOS[o][1]
    assert px % 7 == 0 and py % 7 == 0
    cx, cy = px * 12 // 7, py * 12 // 7
    return tuple((cx + a, cy + b) for a, b in D_SOMMETS[o])


def page(p):
    if GRILLE == "D":
        p = (p[0] * 3.5 / 6, p[1] * 3.5 / 6)
    return (p[0] + 0.5 * p[1], math.sqrt(3) / 2 * p[1])


def aire2(poly):
    """Twice the area in grid coordinates (integer), up to the factor sqrt(3)/2."""
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def empreinte(cells):
    pts = sorted({page(v) for c in cells for v in kite(*c)})
    d = sorted(round(math.dist(p, q), 6) for p, q in itertools.combinations(pts, 2))
    return len(pts), tuple(d)


lignes = open(sys.argv[1]).read().split("\n")
GRILLE = lignes[0][0]
nums = list(map(int, lignes[0].split()[1:]))
base = [(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)]
statut = lignes[1].split()
n = int(lignes[2])
copies = []
for l in lignes[3:3 + n]:
    c, t = l.split(" ", 1)
    a, b, cc, d, e, f = map(int, t.strip("<>").split(","))
    copies.append((int(c), [(a * x + b * y + cc, d * x + e * y + f) for x, y in base]))
print(f"shape of {len(base)} cells ({GRILLE}), status {statut}, {n} copies")
for x, y in base:
    assert orient(x, y) >= 0
assert len({abs(aire2(kite(x, y))) for x, y in base}) == 1
ref = empreinte(base)
for k, (c, cells) in enumerate(copies):
    assert all(orient(x, y) >= 0 for x, y in cells), f"copy {k}: cell outside the grid"
    assert empreinte(cells) == ref, f"copy {k} is not isometric to the shape"
print("all copies are isometric to the shape (identical vertex distances)")
vus = {}
for k, (c, cells) in enumerate(copies):
    for x in cells:
        assert x not in vus, f"overlap between copies {vus[x]} and {k}"
        vus[x] = k
print("no overlap:", len(vus), "cells covered")
xs = [x for x, _ in vus]; ys = [y for _, y in vus]
X0, X1, Y0, Y1 = min(xs) - 12, max(xs) + 12, min(ys) - 12, max(ys) + 12
toutes = [(x, y) for x in range(X0, X1 + 1) for y in range(Y0, Y1 + 1) if orient(x, y) >= 0]
par_sommet = defaultdict(set)
par_arete = defaultdict(set)
for c in toutes:
    P = kite(*c)
    for v in P:
        par_sommet[v].add(c)
    for i in range(len(P)):
        par_arete[frozenset((P[i], P[(i + 1) % len(P)]))].add(c)
voisins_s = defaultdict(set); voisins_a = defaultdict(set)
for s in par_sommet.values():
    for c in s:
        voisins_s[c] |= s
for s in par_arete.values():
    for c in s:
        voisins_a[c] |= s
kmax = max(c for c, _ in copies)
for k in range(1, kmax + 1):
    U0 = {x for c, cells in copies if c < k for x in cells}
    U1 = {x for c, cells in copies if c <= k for x in cells}
    bord = {v for c in U0 for v in voisins_s[c]} - U0
    manque = bord - U1
    assert not manque, f"corona {k} incomplete: {len(manque)} cells touching the previous union are missing"
    for c, cells in copies:
        if c == k:
            assert any(v in U0 for x in cells for v in voisins_s[x]), "a copy of the corona does not touch the previous union"
    dehors = set(toutes) - U1
    bordure = [c for c in dehors if c[0] in (X0, X1) or c[1] in (Y0, Y1) or len(voisins_a[c]) < len(kite(*c)) + 1]
    vu = set(bordure); pile = list(bordure)
    while pile:
        c = pile.pop()
        for v in voisins_a[c]:
            if v in dehors and v not in vu:
                vu.add(v); pile.append(v)
    trous = dehors - vu
    assert not trous, f"the union of coronas 0..{k} has a hole ({len(trous)} cells)"
    print(f"corona {k}: complete, {sum(1 for c, _ in copies if c == k)} copies, union without holes")
print(f"VERIFIED: {kmax} complete coronas around the shape")
