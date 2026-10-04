"""Lager Solnes_Palerad, en kort rad med påler uten terrengendring, for PlanBuild.

    python bp_palerad.py

Fem påler med 2,2 m mellom, samme avstand og retning som i Grav 22 m.
Pålene står i siktehøyden, og PlanBuild fester dem ikke til bakken. Raden er
derfor bare 9 m lang, slik at den ikke svever eller går i jorda i hellinger.
"""
import os

from bp_hage import piece, write

HER = os.path.dirname(os.path.abspath(__file__))


def palerad():
    deler = [piece('piece_sharpstakes', 'Building', x, -0.05, 0) for x in (-4.4, -2.2, 0, 2.2, 4.4)]
    write('Solnes_Palerad.blueprint', 'Pålerad',
          'Fem påler på rad, 9 m lang, uten terrengendring. Sikt på bakken der pålene skal stå, med framsiden mot vollgrava, '
          'så peker pålene utover som i Grav 22 m. Legg neste rad i forlengelsen, og sikt på nytt der bakken heller. '
          'Hver rad trenger 30 Wood og 20 Core wood, og en arbeidsbenk innen 20 m.',
          [], deler)


if __name__ == '__main__':
    palerad()
