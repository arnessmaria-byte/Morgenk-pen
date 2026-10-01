"""PlanBuild-tegninger for Solnes (Kongesalen, Vestporten, Grav).

Koordinater: x = øst/høyre, y = opp, z = nord/forover (Unity, venstrehendt).
Tegningens origo (0,0,0) = punktet du sikter på når du plasserer.
yaw i grader rundt y; lokal +z peker da mot (sin yaw, 0, cos yaw).

Geometri (snappunkter lest fra spillets egne prefabs, Valheim 1.0.16):
  stone_wall_1x1/2x1/4x2  pivot i senter, 1 m tykke
  stone_pillar            1 x 2 x 1, pivot i senter
  stone_floor_2x2         2 x 1 x 2, pivot i senter (topp = +0.5)
  wood_floor              snapplan = pivot, kollider -0.035..+0.095
  wood_pole_log_4         pivot i senter, 4 m
  wood_roof (26 grader)   lav kant (±1, 0, +1), høy kant (±1, 1, -1)
  wood_roof_top           nedre kanter (±1, 0, ±1), møne (±1, 0.5, 0)
  wood_door               åpning 2 x 2, pivot i senter
  iron_grate              åpning 2 x 3, pivot 1 m over bunnen
  wood_stepladder         bunn (±0.5, 0, +1), topp (±0.5, 2, -1)
  piece_sharpstakes       pivot på bakken, piggene peker mot lokal -z
"""
import math
import json
import os

SINK = 0.05   # murer og steingulv senkes 5 cm så de sikkert står i bakken
FLOOR = 0.0   # tregulvets kollider går 3,5 cm ned i bakken og 9,5 cm opp
FURN = 0.08   # møbler står 1,5 cm ned i tregulvet


def quat(yaw):
    r = math.radians(yaw) / 2.0
    return (0.0, math.sin(r), 0.0, math.cos(r))


def num(v):
    v = round(v, 4)
    if v == 0:
        v = 0.0
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'


class Blueprint:
    def __init__(self, name, description, category='Solnes'):
        self.name = name
        self.description = description
        self.category = category
        self.pieces = []
        self.terrain = []
        self.snaps = []

    def add(self, prefab, x, y, z, yaw=0, cat='Building', sink=True):
        self.pieces.append((prefab, cat, x, y - (SINK if sink else 0), z, yaw))

    def level(self, shape, x, y, z, radius, rotation=0, smooth=0.0, paint=''):
        self.terrain.append((shape, x, y, z, radius, rotation, smooth, paint))

    def lines(self):
        out = ['#Name:' + self.name,
               '#Creator:Claude for Elias',
               '#Description:' + json.dumps(self.description, ensure_ascii=False),
               '#Category:' + self.category]
        if self.snaps:
            out.append('#SnapPoints')
            out += [';'.join(num(c) for c in p) for p in self.snaps]
        if self.terrain:
            out.append('#Terrain')
            for shape, x, y, z, r, rot, sm, paint in self.terrain:
                out.append(';'.join([shape, num(x), num(y), num(z), num(r), str(int(rot)), num(sm), paint]))
        out.append('#Pieces')
        for prefab, cat, x, y, z, yaw in self.pieces:
            qx, qy, qz, qw = quat(yaw)
            out.append(';'.join([prefab, cat, num(x), num(y), num(z),
                                 num(qx), num(qy), num(qz), num(qw), '']))
        return out

    def write(self, folder, filename=None):
        path = os.path.join(folder, (filename or self.name) + '.blueprint')
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(self.lines()) + '\n')
        return path

    def count(self):
        c = {}
        for p in self.pieces:
            c[p[0]] = c.get(p[0], 0) + 1
        return c


# ---------------------------------------------------------------- byggeklosser

def wall_run_4x2(bp, axis, fixed, start, end, rows, skip=()):
    """Steinmur av 4x2-blokker langs en linje. axis 'x' eller 'z'."""
    yaw = 0 if axis == 'x' else 90
    c = start + 2
    while c + 2 <= end + 1e-6:
        if c not in skip:
            for y in rows:
                if axis == 'x':
                    bp.add('stone_wall_4x2', c, y, fixed, yaw)
                else:
                    bp.add('stone_wall_4x2', fixed, y, c, yaw)
        c += 4


def roof_side(bp, ridge_x, eave_x, eave_y, zs, overhang=True):
    """26-graders stråtak fra eave_x (veggens senterlinje) opp til mønet ved ridge_x.
    Mønet går langs z. Taket stiger 1 m per 2 m."""
    d = 1 if ridge_x > eave_x else -1          # retning inn mot mønet (i x)
    yaw = 270 if d > 0 else 90                 # lokal -z (oppover) skal peke mot mønet
    steps = int(round(abs(ridge_x - eave_x) / 2))
    for z in zs:
        if overhang:
            bp.add('wood_roof', eave_x - d * 1, eave_y - 1, z, yaw)
        for k in range(steps):
            bp.add('wood_roof', eave_x + d * (2 * k + 1), eave_y + k, z, yaw)


# ---------------------------------------------------------------- Kongesalen

def kongesalen():
    bp = Blueprint(
        'Kongesalen',
        'Borgens storsal, 12 x 18 m: steinmurer med trappegavler, stråtak, '
        'hearth i midten, Raven throne på steinpodium, seng i øst og langbord i vest. '
        'Sikt på bakken midt i salen, der gulvet skal ligge. Roter med scrollhjulet '
        'til døra peker mot landsbyen. Bakken jevnes 21 x 21 m og brolegges.')

    # terreng: jevnt 21 x 21 m med 4,5 m slak overgang ut til 30 x 30 m
    bp.level('square', 0, 0, 0, 15, 0, 0.3, '')
    bp.level('square', 0, 0, 0, 10.5, 0, 0.0, 'Paved')

    EAVE = 4
    zs_long = (-7, -3, 3, 7)  # 4x2-blokker langs langveggene
    for x in (-6, 6):
        for z in zs_long:
            for y in (1, 3):
                bp.add('stone_wall_4x2', x, y, z, 90)
        for y in (0.5, 1.5, 2.5, 3.5):           # midtfeltet (2 m)
            bp.add('stone_wall_2x1', x, y, 0, 90)

    # sorveggen (trone)
    for x in (-4, 0, 4):
        for y in (1, 3):
            bp.add('stone_wall_4x2', x, y, -9, 0)
    # nordveggen (inngang, 2 m dor i midten)
    for x in (-4, 4):
        bp.add('stone_wall_4x2', x, 1, 9, 0)
    for x in (-1.5, 1.5):
        for y in (0.5, 1.5):
            bp.add('stone_wall_1x1', x, y, 9, 0)
    for x in (-4, 0, 4):
        bp.add('stone_wall_4x2', x, 3, 9, 0)
    bp.add('wood_door', 0, 1, 9, 0)
    # hjørnesteiner fyller hakket der to 1 m tykke murer møtes
    for x in (-6, 6):
        for z in (-9, 9):
            for y in (1, 3):
                bp.add('stone_pillar', x, y, z, 0)

    # trappegavler over takfoten (4 m) i begge ender
    for z in (-9, 9):
        for y in (5, 7):
            bp.add('stone_wall_4x2', 0, y, z, 0)
        for x in (-3, 3):
            for y in (4.5, 5.5, 6.5):
                bp.add('stone_wall_2x1', x, y, z, 0)
        for x in (-5, 5):
            for y in (4.5, 5.5):
                bp.add('stone_wall_2x1', x, y, z, 0)

    # tak: monet langs z, 9 plater per rad, med takutstikk
    zs_roof = [-8, -6, -4, -2, 0, 2, 4, 6, 8]
    roof_side(bp, 0, 6, EAVE, zs_roof)
    roof_side(bp, 0, -6, EAVE, zs_roof)
    for z in zs_roof:
        bp.add('wood_roof_top', 0, EAVE + 2.5, z, 90)

    # tregulv, unntatt under podiet
    for x in (-5, -3, -1, 1, 3, 5):
        for z in range(-8, 9, 2):
            if x in (-1, 1) and z in (-8, -6):
                continue
            bp.add('wood_floor', x, FLOOR, z, 0, sink=False)
    # steinpodium 4 x 4 m, 0,5 m hoyt
    for x in (-1, 1):
        for z in (-8, -6):
            bp.add('stone_floor_2x2', x, 0, z, 0)

    # tommerstolper inne langs veggene
    for x in (-5.35, 5.35):
        for z in (-8.35, -5, -1, 1, 5, 8.35):
            bp.add('wood_pole_log_4', x, 2, z, 0)
    for x in (-2, 2):
        bp.add('wood_pole_log_4', x, 2, 8.35, 0)           # rammer inn døra
        bp.add('wood_pole_log_4', x * 1.15, 2, -8.35, 0)   # rammer inn podiet

    # innredning (står 2 cm ned i gulvet så de får støtte)
    F = FURN
    bp.add('hearth', 0, F, 0, 0, 'Furniture', sink=False)
    bp.add('piece_throne01', 0, 0.5 - 0.02, -7.5, 0, 'Furniture')
    bp.add('rug_Bjorn', 0, F, -3.8, 0, 'Furniture', sink=False)
    bp.add('bed', 4.4, F, 0, 90, 'Furniture', sink=False)
    bp.add('piece_table_oak', -4.2, F, 0, 90, 'Furniture', sink=False)
    for x in (2.4, 3.5, 4.6):
        bp.add('ArmorStand', x, F, 7.8, 180, 'Furniture', sink=False)
    for x in (-3.2, 3.2):
        bp.add('piece_groundtorch_wood', x, F, -7.6, 0, 'Furniture', sink=False)
    for x in (-1.8, 1.8):
        bp.add('piece_groundtorch_wood', x, 0, 10.2, 0, 'Furniture')

    # byggestasjoner utenfor vestveggen (planer trenger dem innen rekkevidde)
    bp.add('piece_workbench', -9.2, 0, -2.5, 90, 'Crafting')
    bp.add('piece_stonecutter', -9.2, 0, 2.5, 90, 'Crafting')
    return bp


# ---------------------------------------------------------------- Vestporten

def vestporten():
    bp = Blueprint(
        'Vestporten',
        'Porthus med to steintårn, skyteplattform med murtinder (4 m), portgård '
        'og steinbro over grava. Sikt på fakkellinja midt i porten og '
        'roter til broa peker ut mot havet. Graver også 12 m grav på hver side av broa.')

    # terreng
    bp.level('square', 0, 0, 4.5, 8.5, 0, 0.25, '')
    bp.level('square', 0, 0, 4.5, 6.4, 0, 0.0, 'Paved')
    for x in (-11, -5, 5, 11):
        bp.level('square', x, -6, -6, 3, 0, 0.0, '')
    for z in (-4.5, -7.5):
        bp.level('square', 0, 0, z, 2, 0, 0.0, 'Paved')
    bp.level('square', 0, 0, -11, 2, 0, 0.5, 'Paved')
    stake_x = (-12.3, -10.1, -7.9, -5.7, -3.5, 3.5, 5.7, 7.9, 10.1, 12.3)
    for x in stake_x:
        bp.level('square', x, 0, -10.5, 1.5, 0, 0.6, '')

    # steinbro og porthull
    # steinplatene stikker 5 cm opp av bakken så de synes
    for z in (-8, -6, -4, -2, 0):
        bp.add('stone_floor_2x2', 0, -0.45, z, 0, sink=False)
    bp.add('stone_floor_2x2', 0, -0.45, 10, 0, sink=False)

    # to taarn, 4 x 4 m, 4 m hoye
    for sx in (-1, 1):
        cx = 4 * sx
        for y in (1, 3):
            bp.add('stone_wall_4x2', cx, y, 0, 0)       # front
            bp.add('stone_wall_4x2', cx, y, 4, 0)       # bak
            bp.add('stone_wall_4x2', 6 * sx, y, 2, 90)  # ytterside
            bp.add('stone_wall_4x2', 2 * sx, y, 2, 90)  # mot portrommet
        for y in (0.5, 1.5, 2.5):
            bp.add('stone_wall_1x1', 1.5 * sx, y, 0, 0)  # porthullets kanter
        for (x, z) in ((6, 0), (6, 4), (2, 4), (4, 10)):  # hjørnesteiner
            for y in (1, 3):
                bp.add('stone_pillar', x * sx, y, z, 0)
    bp.add('stone_wall_4x2', 0, 4, 0, 0)                 # overligger over port 1, brystvern over porten
    bp.add('iron_grate', 0, 1, 0, 0)                     # port 1 (2 x 3 m)

    # plattform og murtinder
    for x in (-5, -3, -1, 1, 3, 5):
        for z in (1, 3):
            bp.add('wood_floor', x, 4, z, 0)
    for x in (-5.5, -3.5, 3.5, 5.5):
        bp.add('stone_wall_1x1', x, 4.5, 0, 0)
    for x in (-6, 6):
        for z in (1.5, 3.5):
            bp.add('stone_wall_1x1', x, 4.5, z, 90)

    # portgaarden: sidemurer og indre mur med port 2
    for sx in (-1, 1):
        for y in (1, 3):
            bp.add('stone_wall_4x2', 4 * sx, y, 6, 90)
        for y in (0.5, 1.5, 2.5, 3.5):
            bp.add('stone_wall_2x1', 4 * sx, y, 9, 90)
            bp.add('stone_wall_2x1', 3 * sx, y, 10, 0)
        for y in (0.5, 1.5, 2.5):
            bp.add('stone_wall_1x1', 1.5 * sx, y, 10, 0)
    bp.add('stone_wall_4x2', 0, 4, 10, 0)                # overligger over port 2
    bp.add('iron_grate', 0, 1, 10, 0)                    # port 2

    # stige opp til plattformen, bak det ostre taarnet (utenfor portgaarden)
    bp.add('wood_stepladder', 5.2, 0, 7, 0)
    bp.add('wood_stepladder', 5.2, 2, 5, 0)

    # lys og arbeidsbenk
    for x in (-4.8, -1.2, 1.2, 4.8):
        bp.add('piece_groundtorch_wood', x, 4, 0.9, 0, 'Furniture')
    bp.add('piece_workbench', -5.6, 0, 7, 90, 'Crafting')
    bp.add('piece_stonecutter', -5.6, 0, 9.8, 90, 'Crafting')

    # paaler langs ytterkanten av grava
    for x in stake_x:
        bp.add('piece_sharpstakes', x, 0, -10.5, 0)
    return bp


# ---------------------------------------------------------------- Grav

def grav():
    bp = Blueprint(
        'Grav 22 m',
        'Tørr vollgrav, 22 m lang, 6 m bred og 6 m dyp, med påler langs ytterkanten. '
        'Sikt på fakkellinja og roter til pålene peker utover. Grava havner 3–9 m '
        'utenfor. Legg neste bit i forlengelsen, gjerne med litt overlapp.')
    for x in (-8.25, -2.75, 2.75, 8.25):
        bp.level('square', x, -6, -6, 3, 0, 0.0, '')
    xs = [round(-9.9 + 2.2 * i, 2) for i in range(10)]
    for x in xs:
        bp.level('square', x, 0, -10.5, 1.5, 0, 0.6, '')
    for x in xs:
        bp.add('piece_sharpstakes', x, 0, -10.5, 0)
    return bp


COSTS = {
    'stone_wall_4x2': {'Stone': 6}, 'stone_wall_2x1': {'Stone': 4},
    'stone_wall_1x1': {'Stone': 3}, 'stone_floor_2x2': {'Stone': 6},
    'wood_floor': {'Wood': 2}, 'wood_roof': {'Wood': 2}, 'wood_roof_top': {'Wood': 2},
    'wood_pole_log_4': {'Core wood': 2}, 'wood_stepladder': {'Wood': 2},
    'hearth': {'Stone': 15}, 'bed': {'Wood': 8},
    'piece_throne01': {'Fine wood': 20, 'Iron nails': 10},
    'piece_table_oak': {'Fine wood': 20, 'Tar': 2, 'Iron nails': 20},
    'rug_Bjorn': {'Bear hide': 1, 'Bear paw': 2, 'Bear trophy': 1},
    'ArmorStand': {'Fine wood': 8, 'Iron nails': 4, 'Leather scraps': 2},
    'piece_groundtorch_wood': {'Wood': 2, 'Resin': 2},
    'piece_workbench': {'Wood': 10},
    'piece_stonecutter': {'Wood': 10, 'Iron': 2, 'Stone': 4},
    'piece_sharpstakes': {'Wood': 6, 'Core wood': 4},
    'stone_pillar': {'Stone': 5}, 'wood_door': {'Wood': 4}, 'iron_grate': {'Iron': 4},
}


def materials(bp):
    tot = {}
    for prefab, n in bp.count().items():
        for item, amt in COSTS[prefab].items():
            tot[item] = tot.get(item, 0) + amt * n
    return tot


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Skriv Solnes-tegningene som .blueprint-filer')
    ap.add_argument('--out', default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--preview', action='store_true', help='skriv også preview.js for 3D-visningen')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    preview = {}
    for bp, fn in ((kongesalen(), 'Solnes_Kongesalen'), (vestporten(), 'Solnes_Vestporten'),
                   (grav(), 'Solnes_Grav22m')):
        path = bp.write(args.out, fn)
        preview[fn] = {'pieces': [[p[0], p[2], p[3], p[4], p[5]] for p in bp.pieces], 'terrain': bp.terrain}
        print(os.path.basename(path), len(bp.pieces), 'deler,', len(bp.terrain), 'terrengoperasjoner')
        print('   ', materials(bp))
    if args.preview:
        with open(os.path.join(args.out, 'preview.js'), 'w') as f:
            f.write('window.BP = ' + json.dumps(preview) + ';\n')
