"""Lager PlanBuild-tegningene til Nedre gård: Stabburet, Mjødstua, Tingstua og Lysthuset.

Bruk: python bp_nedre.py [--out MAPPE] [--preview FIL.js]

Koordinatene er lokale. Origo er punktet du sikter på i spillet, og +z er framsiden
(døra eller den åpne siden). Målene bygger på de samme snappunktene som Kongesalen:
woodwall 2 x 2 m med midtpivot, wood_floor 2 x 2 m med pivot i gulvflaten, wood_roof
med pivot midt på i lav kant, wood_roof_top med pivot i lav kant og stone_floor_2x2
og stone_pillar med midtpivot.
"""
import argparse
import collections
import json
import math
import os

FURN = 0.08      # møbler på tregulv (gulvflaten ligger 0,095 over pivot)
SINK = 0.05      # stein senkes litt ned i bakken så den står på terrenget


def quat(yaw):
    t = math.radians(yaw) / 2
    return (0.0, math.sin(t), 0.0, math.cos(t))


def num(v):
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


class Blueprint:
    def __init__(self, name, desc):
        self.name, self.desc = name, desc
        self.pieces, self.terrain = [], []

    def add(self, prefab, x, y, z, yaw=0, cat='Building'):
        self.pieces.append((prefab, cat, x, y, z, yaw % 360))

    def level(self, r, smooth=0.3, paint=''):
        self.terrain.append(('square', 0, 0, 0, r, 0, smooth, paint))

    def text(self):
        out = ['#Name:' + self.name, '#Creator:Claude for Elias',
               '#Description:' + json.dumps(self.desc, ensure_ascii=False),
               '#Category:Solnes', '#Terrain']
        for t in self.terrain:
            out.append(';'.join([t[0]] + [num(v) for v in t[1:7]] + [t[7]]))
        out.append('#Pieces')
        for prefab, cat, x, y, z, yaw in self.pieces:
            q = quat(yaw)
            out.append(';'.join([prefab, cat, num(x), num(y), num(z)] + [num(v) for v in q]) + ';')
        return '\n'.join(out) + '\n'

    def counts(self):
        return collections.Counter(p[0] for p in self.pieces)


# ---------- byggeklosser ----------

def floor_grid(bp, xs, zs, y=0.0, stone=None):
    """Tregulv 2 x 2 m. Ruter i `stone` blir stone_floor_2x2 med toppen i y."""
    for x in xs:
        for z in zs:
            if stone and (x, z) in stone:
                bp.add('stone_floor_2x2', x, y - 0.5, z)
            else:
                bp.add('wood_floor', x, y, z)


def stone_floor(bp, xs, zs, top=0.0):
    for x in xs:
        for z in zs:
            bp.add('stone_floor_2x2', x, top - 0.5, z)


def walls(bp, half, rows, base, sides, skip=()):
    """Vegger av woodwall rundt et kvadrat på 2*half m. sides: 'L','R','B','F' (venstre, høyre, bak, front)."""
    cells = [c for c in range(-half + 1, half, 2)]
    for r in range(rows):
        y = base + 1.0 + 2.0 * r
        for c in cells:
            if 'L' in sides and ('L', c, r) not in skip:
                bp.add('woodwall', -half, y, c, 90)
            if 'R' in sides and ('R', c, r) not in skip:
                bp.add('woodwall', half, y, c, 90)
            if 'B' in sides and ('B', c, r) not in skip:
                bp.add('woodwall', c, y, -half, 0)
            if 'F' in sides and ('F', c, r) not in skip:
                bp.add('woodwall', c, y, half, 0)


def gable_roof(bp, half, eave, zs):
    """26-graders saltak med mønet langs z. Bredden 2*half er 4 eller 6 m.
    4 m: ett takstykke per side, mønekappe over toppen.
    6 m: ett takstykke per side og en mønekappe som dekker midtre 2 m."""
    for z in zs:
        bp.add('wood_roof', -half - 1, eave - 1, z, 270)     # utstikk venstre
        bp.add('wood_roof', half + 1, eave - 1, z, 90)       # utstikk høyre
        bp.add('wood_roof', -half + 1, eave, z, 270)
        bp.add('wood_roof', half - 1, eave, z, 90)
        if half == 2:
            bp.add('wood_roof_top', 0, eave + 0.5, z, 90)
        else:
            bp.add('wood_roof_top', 0, eave + 1.0, z, 90)


def chairs_round(bp, r, y):
    for x, z, yaw in [(0, -r, 0), (0, r, 180), (-r, 0, 90), (r, 0, 270)]:
        bp.add('piece_chair02', x, y, z, yaw, 'Furniture')


# ---------- tegningene ----------

def stabburet():
    bp = Blueprint('Stabburet', 'Stabbur på 4 x 4 m, løftet en meter opp på fire steinsøyler. '
                   'Saltak med utstikk over døra og bakveggen, fem kister og et steintrinn foran døra. '
                   'Døra vender fram, mot veien.')
    bp.level(3.5)
    for x in (-1.5, 1.5):
        for z in (-1.5, 1.5):
            bp.add('stone_pillar', x, 0.0, z)            # 1 x 2 x 1 m, toppen 1 m over bakken
    floor_grid(bp, (-1, 1), (-1, 1), y=1.0)
    walls(bp, 2, 1, 1.0, 'LRBF', skip={('F', 1, 0)})
    bp.add('wood_door', 1, 2.0, 2)
    gable_roof(bp, 2, 3.0, (-3, -1, 1, 3))
    for x in (-1.1, 0.0, 1.1):
        bp.add('piece_chest_wood', x, 1.0 + FURN, -1.45, 0, 'Furniture')
    for z in (0.0, 1.1):
        bp.add('piece_chest_wood', -1.45, 1.0 + FURN, z, 90, 'Furniture')
    bp.add('stone_floor_2x2', 1, 0.0 - SINK, 3.2)      # trinn, toppen 0,5 m
    for x in (-0.4, 2.4):
        bp.add('piece_groundtorch', x, 0.0, 3.6, 0, 'Furniture')
    return bp


def mjodstua():
    bp = Blueprint('Mjødstua', 'Bryggerhus på 6 x 6 m med fem fermentere, langbord, stoler og et bål på steinheller midt i rommet. '
                   'Vegger i to høyder og saltak med takoverheng over døra. Fermenterne står under tak, og røyken går ut gjennom gavlene.')
    bp.level(4.5)
    floor_grid(bp, (-2, 0, 2), (-2, 0, 2), y=0.0, stone={(0, 0)})
    walls(bp, 3, 2, 0.0, 'LRBF', skip={('F', 0, 0)})
    bp.add('wood_door', 0, 1.0, 3)
    gable_roof(bp, 3, 4.0, (-2, 0, 2, 4))
    bp.add('fire_pit', 0, 0.0, 0, 0, 'Furniture')
    for z in (-1.9, 0.0, 1.9):
        bp.add('fermenter', -2.0, FURN, z, 90, 'Furniture')
    for x in (0.0, 1.9):
        bp.add('fermenter', x, FURN, -2.0, 0, 'Furniture')
    bp.add('piece_table', 1.9, FURN, 1.2, 90, 'Furniture')
    for z in (0.7, 1.8):
        bp.add('piece_chair02', 1.0, FURN, z, 90, 'Furniture')
    bp.add('piece_chest_barrel', 2.3, FURN, -0.6, 0, 'Furniture')
    bp.add('rug_deer', 0, FURN, 2.0, 0, 'Furniture')
    for x in (-1.6, 1.6):
        bp.add('piece_groundtorch', x, 0.0, 3.8, 0, 'Furniture')
    return bp


def tingstua():
    bp = Blueprint('Tingstua', 'Tingsted på 6 x 6 m for torget: steingulv, vegger i to høyder på tre sider og åpen front med to tømmerstolper. '
                   'Bål i midten, fire stoler, et banner og et teppe. Taket går ut over den åpne siden. '
                   'Den åpne siden vender fram.')
    bp.level(4.5)
    bp.level(4.0, 0.0, 'Paved')
    stone_floor(bp, (-2, 0, 2), (-2, 0, 2))
    walls(bp, 3, 2, 0.0, 'LRB')
    for x in (-3, 3):
        bp.add('wood_pole_log_4', x, 2.0, 3)
    gable_roof(bp, 3, 4.0, (-2, 0, 2, 4))
    bp.add('fire_pit', 0, 0.0, 0, 0, 'Furniture')
    chairs_round(bp, 1.9, 0.0)
    bp.add('piece_banner02', 0, 3.0, -2.8, 0, 'Furniture')
    bp.add('rug_deer', 0, 0.0, 2.6, 0, 'Furniture')
    for x in (-3.6, 3.6):
        bp.add('piece_groundtorch', x, 0.0, 3.6, 0, 'Furniture')
    return bp


def lysthuset():
    bp = Blueprint('Lysthuset', 'Lysthus på 6 x 6 m til Kongshagen: steingulv, lave vegger på tre sider og åpen front. '
                   'Bål i midten, fire stoler og et teppe. Heng opp lysgirlander selv. Den åpne siden vender fram, mot porten.')
    bp.level(4.0)
    stone_floor(bp, (-2, 0, 2), (-2, 0, 2))
    walls(bp, 3, 1, 0.0, 'LRB')
    gable_roof(bp, 3, 2.0, (-2, 0, 2))
    bp.add('fire_pit', 0, 0.0, 0, 0, 'Furniture')
    chairs_round(bp, 1.9, 0.0)
    bp.add('rug_deer', 0, 0.0, 2.4, 0, 'Furniture')
    for x in (-3.4, 3.4):
        bp.add('piece_groundtorch', x, 0.0, 3.4, 0, 'Furniture')
    return bp


ALL = {'Solnes_Stabburet': stabburet, 'Solnes_Mjodstua': mjodstua,
       'Solnes_Tingstua': tingstua, 'Solnes_Lysthuset': lysthuset}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--preview')
    a = ap.parse_args()
    prev = {}
    for fname, fn in ALL.items():
        bp = fn()
        with open(os.path.join(a.out, fname + '.blueprint'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(bp.text())
        print(fname, len(bp.pieces), 'deler:', dict(bp.counts()))
        prev[fname] = {'pieces': [[p[0], p[2], p[3], p[4], p[5]] for p in bp.pieces], 'terrain': [list(t) for t in bp.terrain]}
    if a.preview:
        with open(a.preview, 'w', encoding='utf-8') as f:
            f.write('window.BP = ' + json.dumps(prev) + ';\n')


if __name__ == '__main__':
    main()
