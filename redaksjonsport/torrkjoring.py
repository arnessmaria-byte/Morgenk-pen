#!/usr/bin/env python3
"""Tørrkjøring av redaksjonsporten.

Alt skjer i en midlertidig mappe som slettes etterpå. Ingenting publiseres,
planlegges eller sendes: porten har ingen nettverkskode. Svarene som noteres
her, er merket TEST og gir ingen godkjenning av noe innhold.

    python redaksjonsport/torrkjoring.py
"""
from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import port  # noqa: E402

TEOLOGISK_ARTIKKEL = {
    "tittel": "Bispemøtet behandlet ny liturgi",
    "ingress": "Bispemøtet vedtok tirsdag en ny ordning. MANTELEN vurderer vedtaket.",
    "brodtekst": (
        "Bispemøtet vedtok ordningen med ni mot tre stemmer.\n\n"
        "Herfra følger MANTELENs teologiske vurdering.\n\n"
        "Paulus skriver i Romerbrevet 12,2 at menigheten ikke skal skikke seg lik denne verden. "
        "Kirken bør derfor avvise ordningen."
    ),
}

BLANDINGSSAK = {
    "tittel": "Bispemøtet behandlet ny liturgi",
    "ingress": "Bispemøtet vedtok tirsdag en ny ordning med ni mot tre stemmer.",
    "brodtekst": (
        "Biskop Kari Nordmann sier til MANTELEN at vedtaket var nødvendig.\n\n"
        "Vedtaket bryter med det Skriften sier om saken. Den som tror, har fått et kall til å si fra."
    ),
    "bildetekster": ["Bispemøtet var samlet i Oslo tirsdag."],
}

REN_MARIA_SAK = {
    "tittel": "Bispemøtet vedtok ny liturgi med ni mot tre stemmer",
    "ingress": "Tre biskoper stemte imot. En av dem varsler at hun vil ta saken videre til Kirkemøtet.",
    "brodtekst": (
        "Bispemøtet vedtok tirsdag en ny ordning for dåpsliturgien med ni mot tre stemmer.\n\n"
        "Biskop Kari Nordmann sier til MANTELEN at vedtaket var nødvendig: «Skriften gir oss "
        "rom for dette.»\n\n"
        "Biskop Ola Hansen stemte imot. Han viste til Matt 28,19 og sier at ordningen bryter "
        "med kirkens lære. Ifølge Kirkerådet trer ordningen i kraft 1. januar."
    ),
    "bildetekster": ["Bispemøtet var samlet i Oslo tirsdag. Foto: MANTELEN"],
}

VIDEO = {
    "tittel": "Hva sier Paulus om staten?",
    "beskrivelse": "En gjennomgang av Romerbrevet 13.",
    "manus": "I Romerbrevet 13,1 skriver Paulus at enhver skal være lydig mot øvrigheten.",
    "fortellerstemme": "Paulus skriver om øvrigheten. Kirken bør lese ham på nytt.",
    "skjermtekst": ["Rom 13,1", "Hva skylder en kristen staten?"],
    "undertekster": "I Romerbrevet 13,1 skriver Paulus at enhver skal være lydig mot øvrigheten.",
}

EPOST_KROPP = (
    "Hei,\n\nJeg arbeider med en sak om vedtaket i Bispemøtet og har to spørsmål:\n"
    "1. Hvorfor stemte du imot?\n2. Vil du ta saken videre til Kirkemøtet?\n\n"
    "Svarfrist er torsdag klokken 12.\n\nVennlig hilsen\n"
)


TEST_HVOR = "TEST i tørrkjøring, ikke et svar fra redaktøren"


def _ja(rot: Path, sak: dict, svar: str = "ja", punkter=("35",), utover: str = "") -> tuple[bool, str]:
    """Forelegger og noterer et TESTSVAR. I drift svarer bare redaktøren selv."""
    _, grunnlag = port.forelegg(sak, rot, "TESTVERSJON", list(punkter), "Testtekst.", utover)
    port._foreleggelsesfil(sak, rot).write_text(json.dumps(grunnlag, ensure_ascii=False), encoding="utf-8")
    return port.noter_svar(sak, rot, svar, "Ja" if svar == "ja" else "Nei", TEST_HVOR)


def kjor() -> int:
    rader = []

    def prov(nr, navn, sak, forventet, fase="planlegging", planlagt=None):
        res = port.kontroller(sak, rot, fase, planlagt, tillit)
        rader.append((nr, navn, fase, res["utfall"], res["utfall"] == forventet, res["grunner"]))
        return res

    with tempfile.TemporaryDirectory(prefix="mantelen-torrkjoring-") as tmp:
        rot = Path(tmp)
        tillit = rot / "ingen-nokler"
        tillit.mkdir()
        (rot / "video.mp4").write_bytes(b"TESTVIDEO versjon 1")

        art = {"id": "test-teologisk-artikkel", "kanal": "ghost-artikkel", "journalist": "redaksjonen",
               "byline": "Mantelen redaksjonen", "forfatter": "Mantelen redaksjonen",
               "egen_teologisk_vurdering": True, "tekst": TEOLOGISK_ARTIKKEL}
        vid = {"id": "test-video", "kanal": "youtube-video", "journalist": "redaksjonen",
               "egen_teologisk_vurdering": True, "tekst": VIDEO, "filer": {"video": "video.mp4"}}
        shorts = dict(vid, id="test-shorts", kanal="youtube-shorts")

        # 1 og 2. Uten redaktørens ja
        prov(1, "Teologisk artikkel uten redaktørens ja", art, port.HOLDES)
        prov(2, "YouTube-video uten redaktørens ja", vid, port.HOLDES)
        prov(2, "Shorts-video uten redaktørens ja", shorts, port.HOLDES)

        # 3. Redaktøren svarer ja: versjonen passerer
        _ja(rot, art)
        prov(3, "Artikkel etter redaktørens ja", art, port.PASSERER)
        _ja(rot, vid)
        r_vid = prov(3, "Video etter redaktørens ja", vid, port.PASSERER)
        _ja(rot, shorts, "nei")
        prov(3, "Shorts etter redaktørens nei", shorts, port.HOLDES)

        # 4. Senere innholdsendring stoppes
        endret = copy.deepcopy(art)
        endret["tekst"]["brodtekst"] = endret["tekst"]["brodtekst"].replace("bør derfor", "må derfor")
        prov(4, "Artikkel: ett ord endret etter ja", endret, port.HOLDES, "utsending")
        ny_tittel = copy.deepcopy(art)
        ny_tittel["tekst"]["tittel"] = "Skriften avviser den nye liturgien"
        prov(4, "Artikkel: ny tittel etter ja", ny_tittel, port.HOLDES, "utsending")
        (rot / "video.mp4").write_bytes(b"TESTVIDEO versjon 2, klippet om")
        prov(4, "Video: ny fil etter ja", vid, port.HOLDES, "utsending", r_vid["versjon_sha256"])
        (rot / "video.mp4").write_bytes(b"TESTVIDEO versjon 1")
        ok, _ = port.noter_svar(endret, rot, "ja", "Ja", TEST_HVOR)
        rader.append((4, "Gammelt ja kan ikke noteres på endret tekst", "svar", "avvist" if not ok else "notert",
                      not ok, []))

        # 5. Ren Maria-sak med riktig byline: trenger ikke redaktøren
        maria = {"id": "test-maria-sak", "kanal": "ghost-artikkel", "journalist": port.MARIA,
                 "byline": port.MARIA_BYLINE, "forfatter": port.MARIA,
                 "egen_teologisk_vurdering": False, "tekst": REN_MARIA_SAK}
        prov(5, "Ren Maria-sak med riktig byline", maria, port.PASSERER)
        prov(5, "Maria-sak med bare «Redaksjonen» som byline",
             dict(maria, byline="Mantelen redaksjonen", forfatter="Mantelen redaksjonen"), port.HOLDES)
        prov(5, "Marias navn i byline, men hun er ikke journalisten",
             dict(maria, journalist="redaksjonen"), port.HOLDES)

        # 6. Blandingssak uten teologisk mellomtittel
        blanding = {"id": "test-blandingssak", "kanal": "ghost-artikkel", "journalist": "redaksjonen",
                    "byline": "Mantelen redaksjonen", "forfatter": "Mantelen redaksjonen",
                    "egen_teologisk_vurdering": False, "tekst": BLANDINGSSAK}
        prov(6, "Blandingssak uten teologisk mellomtittel", blanding, port.HOLDES)
        maria_tillegg = dict(maria, id="test-maria-med-tillegg",
                             tekst=dict(REN_MARIA_SAK, brodtekst=REN_MARIA_SAK["brodtekst"]
                                        + "\n\nKirken skylder menighetene et klart svar etter Guds ord."))
        prov(6, "Teologisk tillegg i Marias tekst", maria_tillegg, port.HOLDES)
        prov(6, "Teologisk artikkel med byline byttet til Maria",
             dict(art, id="test-byttet-byline", journalist=port.MARIA, byline=port.MARIA_BYLINE,
                  forfatter=port.MARIA), port.HOLDES)

        # 7. Planlagt publisering: kontroll ved planlegging og rett før utsending
        plan = prov(7, "Planlagt Maria-sak, ved planlegging", maria, port.PASSERER, "planlegging")
        prov(7, "Samme sak uendret, rett før utsending", maria, port.PASSERER, "utsending",
             plan["versjon_sha256"])
        prov(7, "Samme sak med teologisk tillegg i køen", dict(maria, tekst=maria_tillegg["tekst"]),
             port.HOLDES, "utsending", plan["versjon_sha256"])
        prov(7, "Planlagt teologisk video uten ja", dict(vid, id="test-planlagt-video"), port.HOLDES)

        # 8. Kilde-e-post
        prov(8, "Kilde-e-post med bare «Redaksjonen» som signatur",
             {"id": "test-epost-redaksjonen", "kanal": "epost", "journalist": port.MARIA,
              "egen_teologisk_vurdering": False,
              "epost": {"avsendernavn": "MANTELEN", "signatur": "Redaksjonen"},
              "tekst": {"emne": "Spørsmål om vedtaket", "brodtekst": EPOST_KROPP + "Redaksjonen"}}, port.HOLDES)
        prov(8, "Kilde-e-post fra Maria med riktig navn og signatur",
             {"id": "test-epost-maria", "kanal": "epost", "journalist": port.MARIA,
              "egen_teologisk_vurdering": False,
              "epost": {"avsendernavn": port.MARIA_AVSENDER, "signatur": port.MARIA_SIGNATUR},
              "tekst": {"emne": "Spørsmål om vedtaket", "brodtekst": EPOST_KROPP + port.MARIA_SIGNATUR}},
             port.PASSERER)

        # 9. Et ja som ikke holder
        annen = dict(art, id="test-annen-sak")
        port._godkjenningsfil(annen, rot).write_text(
            port._godkjenningsfil(art, rot).read_text(encoding="utf-8"), encoding="utf-8")
        prov(9, "Ja til en annen sak brukt på nytt", annen, port.HOLDES)
        uten_ord = dict(art, id="test-uten-ord")
        g = json.loads(port._godkjenningsfil(art, rot).read_text(encoding="utf-8"))
        g.update(sak_id="test-uten-ord", redaktorens_ord="", gitt={})
        port._godkjenningsfil(uten_ord, rot).write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
        prov(9, "Ja uten redaktørens ord, tid og sted", uten_ord, port.HOLDES)
        uten_liste = dict(art, id="test-uten-liste")
        _ja(rot, uten_liste, punkter=())
        prov(9, "Ja uten grunnlag i Topp 100", uten_liste, port.HOLDES)
        utover = dict(art, id="test-utover-listen")
        _ja(rot, utover, punkter=(), utover="Spørsmålet er ikke behandlet i listen.")
        prov(9, "Ja til noe som åpent går utover listen", utover, port.PASSERER)

    kilde = Path(port.__file__).read_text(encoding="utf-8")
    forbudt = [m for m in ("import socket", "import smtplib", "import urllib", "import http", "import requests")
               if m in kilde]
    rader.append((10, "Porten har ingen nettverkskode", "kildekode", "ingen" if not forbudt else str(forbudt),
                  not forbudt, []))

    feil = 0
    for nr, navn, fase, fikk, ok, grunner in rader:
        print(f"{'OK  ' if ok else 'FEIL'} {nr:>2}  {fikk:<9} {fase:<12} {navn}")
        if "-v" in sys.argv:
            for grunn in grunner:
                print(f"            - {grunn}")
        feil += 0 if ok else 1
    print(f"\n{len(rader) - feil} av {len(rader)} prøver ga forventet utfall. "
          "Ingenting ble publisert, planlagt eller sendt.")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(kjor())
