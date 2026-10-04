"""Lager tegningene til hagene i Nedre gård (Økt 2B) for PlanBuild.

    python bp_hage.py

Skriver Solnes_Akerbed, Solnes_Bigarden, Solnes_Folden og Solnes_Kongebordet.
Framsiden er +z i alle fire. Mål i meter, og y = 0 er bakken der du sikter.

PlanBuild jevner bakken til siktehøyden under hver terrenglinje og maler
den etterpå (Cultivate, Paved eller Dirt). Delene står i faste høyder over
siktepunktet, så alt som står på bakken, står på den jevnede flata.
"""
import math
import os

HER = os.path.dirname(os.path.abspath(__file__))


def quat(yaw):
    """Rotasjon om y-aksen i grader, som PlanBuild-kvaternion (x;y;z;w)."""
    h = math.radians(yaw) / 2
    return (0.0, round(math.sin(h), 4), 0.0, round(math.cos(h), 4))


def num(v):
    v = round(v, 3)
    return str(int(v)) if v == int(v) else str(v)


def piece(name, cat, x, y, z, yaw=0):
    q = quat(yaw)
    return ';'.join([name, cat, num(x), num(y), num(z)] + [num(c) for c in q]) + ';'


def square(x, z, r, paint='', smooth=0):
    return 'square;%s;0;%s;%s;0;%s;%s' % (num(x), num(z), num(r), num(smooth), paint)


def write(fil, navn, beskrivelse, terreng, deler):
    linjer = ['#Name:' + navn, '#Creator:Claude for Elias', '#Description:"%s"' % beskrivelse,
              '#Category:Solnes', '#Terrain'] + terreng + ['#Pieces'] + deler
    with open(os.path.join(HER, fil), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(linjer) + '\n')
    print('%-28s %3d terrenglinjer, %3d deler' % (fil, len(terreng), len(deler)))


def akerbed():
    # Bed 4 x 10 m (x -3..1) og sti 2 x 10 m (x 1..3). Ruter på 2 x 2 m.
    terreng = []
    for z in (-4, -2, 0, 2, 4):
        terreng.append(square(-2, z, 1, 'Cultivate'))
        terreng.append(square(0, z, 1, 'Cultivate'))
        terreng.append(square(2, z, 1, 'Paved'))
    deler = [piece('piece_groundtorch_wood', 'Furniture', 2, 0, 4.6)]
    write('Solnes_Akerbed.blueprint', 'Åkerbed',
          'Åkermodul på 6 x 10 m: et dyrket bed på 4 x 10 m og en brolagt sti på 2 m langs høyre side, med en fakkel ved enden av stien. '
          'Bakken jevnes til der du sikter. Sett modulene side om side, så får du bed, sti, bed, sti. Legg bedene på tvers av bakken, så blir trinnene små.',
          terreng, deler)


def bigarden():
    # Brolagt flate 12 x 6 m med åtte kuber i to rader og to fakler.
    terreng = [square(x, z, 1, 'Paved') for x in (-5, -3, -1, 1, 3, 5) for z in (-2, 0, 2)]
    deler = [piece('piece_beehive', 'Misc', x, 0, z) for z in (-1.4, 1.4) for x in (-4.2, -1.4, 1.4, 4.2)]
    deler += [piece('piece_groundtorch_wood', 'Furniture', x, 0, 2.6) for x in (-5.6, 5.6)]
    write('Solnes_Bigarden.blueprint', 'Bigården',
          'Åtte bikuber i to rader på en brolagt flate på 12 x 6 m, med 2,8 m mellom kubene og en fakkel i hvert fremre hjørne. '
          'Kubene står under åpen himmel. Hver kube trenger 10 Wood og 1 Queen bee, så planene står til du har funnet dronninger.',
          terreng, deler)


def folden():
    # Innhegning 8 x 20 m (x -4..4, z -10..10) av tremur, med dør midt på framsiden.
    terreng = [square(x, z, 2, 'Dirt') for x in (-2, 2) for z in (-8, -4, 0, 4, 8)]
    deler = []
    for x in (-3, -1, 1, 3):
        deler.append(piece('woodwall', 'Building', x, 1, -10))
        if x != 1:
            deler.append(piece('woodwall', 'Building', x, 1, 10))
    deler.append(piece('wood_door', 'Building', 1, 1, 10))
    for z in range(-9, 10, 2):
        deler.append(piece('woodwall', 'Building', -4, 1, z, 90))
        deler.append(piece('woodwall', 'Building', 4, 1, z, 90))
    deler += [piece('piece_groundtorch_wood', 'Furniture', x, 0, 10.8) for x in (-0.4, 2.4)]
    write('Solnes_Folden.blueprint', 'Folden',
          'Innhegning for tamme villsvin på 8 x 20 m med tremur på 2 m og en dør midt på framsiden, med en fakkel på hver side av døra. '
          'Bakken inni jevnes og blir jord.',
          terreng, deler)


def kongebordet():
    # To bord på 2 m ende mot ende, to stoler på hver langside og én ved hodeenden, og et teppe under.
    deler = [piece('rug_deer', 'Furniture', 0, 0, 0)]
    deler += [piece('piece_table', 'Furniture', x, 0, 0) for x in (-1, 1)]
    deler += [piece('piece_chair02', 'Furniture', x, 0, -0.9, 0) for x in (-1, 1)]
    deler += [piece('piece_chair02', 'Furniture', x, 0, 0.9, 180) for x in (-1, 1)]
    deler.append(piece('piece_chair02', 'Furniture', -2.7, 0, 0, 90))
    write('Solnes_Kongebordet.blueprint', 'Kongebordet',
          'Langbord på 4 m med fem stoler og et hjorteteppe under, til midten av Velkomsthallen under det hengende fyrfatet. '
          'Bordet gir komfort sammen med bålet og teppet når du kommer hjem gjennom portalene.',
          [], deler)


if __name__ == '__main__':
    akerbed()
    bigarden()
    folden()
    kongebordet()
