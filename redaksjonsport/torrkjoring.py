#!/usr/bin/env python3
"""Tørrkjøring av redaksjonsporten.

Alt skjer i en midlertidig mappe med testnøkler som slettes etterpå.
Ingenting publiseres, planlegges eller sendes: porten har ingen nettverkskode,
og denne filen kaller bare `kontroller`. Testnøklene er ikke redaktørens eller
Marias nøkler, og resultatene her gir ingen godkjenning av noe innhold.

    python redaksjonsport/torrkjoring.py
"""
from __future__ import annotations

import copy
import json
import subprocess
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


def _openssl(*args):
    subprocess.run(["openssl", *args], check=True, capture_output=True)


def _nokkel(mappe: Path, navn: str) -> Path:
    priv = mappe / f"{navn}.testnokkel.pem"
    _openssl("genpkey", "-algorithm", "ed25519", "-out", str(priv))
    return priv


def _signer(dok: Path, priv: Path):
    _openssl("pkeyutl", "-sign", "-inkey", str(priv), "-rawin", "-in", str(dok), "-out", str(dok) + ".sig")


def _godkjenn(rot: Path, sak: dict, priv: Path, navn: str, **endring) -> str:
    """Stiller som redaktøren med en TESTNØKKEL. I drift gjør bare redaktøren dette, med egen nøkkel."""
    g = {"type": "mantelen-teologisk-godkjenning", "sak_id": sak["id"], "kanal": sak["kanal"],
         "versjon_sha256": port.versjon(sak, rot),
         "topp100": {"fil": "Topp-100-Bibelen-og-tidligste-kirke.md", "versjon": "TESTVERSJON",
                     "punkter": [35], "samsvar": "Testtekst, ikke en reell vurdering."},
         "utover_listen": "", "godkjent_av": port.REDAKTOR, "dato": "TEST"}
    g.update(endring)
    dok = rot / navn
    dok.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    _signer(dok, priv)
    return navn


def _bekreft(rot: Path, sak: dict, priv: Path, navn: str) -> str:
    """Stiller som Maria med en TESTNØKKEL."""
    b = {"type": "mantelen-forfatterbekreftelse", "sak_id": sak["id"], "journalist": port.MARIA,
         "versjon_sha256": port.versjon(sak, rot)}
    dok = rot / navn
    dok.write_text(json.dumps(b, ensure_ascii=False, indent=2), encoding="utf-8")
    _signer(dok, priv)
    return navn


def kjor() -> int:
    rader = []

    def prov(nr, navn, sak, forventet, fase="planlegging", planlagt=None):
        res = port.kontroller(sak, rot, fase, planlagt, tillit)
        ok = res["utfall"] == forventet
        rader.append((nr, navn, fase, forventet, res["utfall"], ok, res["grunner"]))
        return res

    with tempfile.TemporaryDirectory(prefix="mantelen-torrkjoring-") as tmp:
        rot = Path(tmp)
        tillit = rot / "tillit-TEST"
        tillit.mkdir()
        red = _nokkel(rot, "redaktor")
        mar = _nokkel(rot, "maria")
        fremmed = _nokkel(rot, "fremmed")
        _openssl("pkey", "-in", str(red), "-pubout", "-out", str(tillit / port.NOKKEL_REDAKTOR))
        _openssl("pkey", "-in", str(mar), "-pubout", "-out", str(tillit / port.NOKKEL_MARIA))
        (rot / "video.mp4").write_bytes(b"TESTVIDEO versjon 1")

        # 1. Teologisk artikkel uten redaktørens ja
        art = {"id": "test-teologisk-artikkel", "kanal": "ghost-artikkel", "journalist": "redaksjonen",
               "byline": "Mantelen redaksjonen", "forfatter": "Mantelen redaksjonen",
               "egen_teologisk_vurdering": True, "tekst": TEOLOGISK_ARTIKKEL}
        prov(1, "Teologisk artikkel uten redaktørens ja", art, port.HOLDES)

        # 2. YouTube-video uten redaktørens ja
        vid = {"id": "test-video", "kanal": "youtube-video", "journalist": "redaksjonen",
               "egen_teologisk_vurdering": True, "tekst": VIDEO, "filer": {"video": "video.mp4"}}
        prov(2, "YouTube-video uten redaktørens ja", vid, port.HOLDES)
        shorts = dict(vid, id="test-shorts", kanal="youtube-shorts")
        prov(2, "Shorts-video uten redaktørens ja", shorts, port.HOLDES)

        # 3. Godkjent versjon passerer
        art_ok = dict(art, godkjenning=_godkjenn(rot, art, red, "godkjenning-artikkel.json"))
        prov(3, "Godkjent artikkelversjon", art_ok, port.PASSERER)
        vid_ok = dict(vid, godkjenning=_godkjenn(rot, vid, red, "godkjenning-video.json"))
        r_vid = prov(3, "Godkjent videoversjon", vid_ok, port.PASSERER)

        # 4. Senere innholdsendring stoppes
        art_endret = copy.deepcopy(art_ok)
        art_endret["tekst"]["brodtekst"] = art_endret["tekst"]["brodtekst"].replace("bør derfor", "må derfor")
        prov(4, "Artikkel: ett ord endret etter godkjenning", art_endret, port.HOLDES, "utsending")
        tittel_endret = copy.deepcopy(art_ok)
        tittel_endret["tekst"]["tittel"] = "Skriften avviser den nye liturgien"
        prov(4, "Artikkel: ny tittel etter godkjenning", tittel_endret, port.HOLDES, "utsending")
        (rot / "video.mp4").write_bytes(b"TESTVIDEO versjon 2, klippet om")
        prov(4, "Video: ny fil etter godkjenning", vid_ok, port.HOLDES, "utsending", r_vid["versjon_sha256"])
        (rot / "video.mp4").write_bytes(b"TESTVIDEO versjon 1")

        # 5. Ren Maria-sak med riktig byline
        maria = {"id": "test-maria-sak", "kanal": "ghost-artikkel", "journalist": port.MARIA,
                 "byline": port.MARIA_BYLINE, "forfatter": port.MARIA,
                 "egen_teologisk_vurdering": False, "tekst": REN_MARIA_SAK}
        maria["forfatterbekreftelse"] = _bekreft(rot, maria, mar, "bekreftelse-maria.json")
        prov(5, "Ren Maria-sak med riktig byline", maria, port.PASSERER)
        feil_byline = dict(maria, byline="Mantelen redaksjonen", forfatter="Mantelen redaksjonen")
        prov(5, "Maria-sak med bare «Redaksjonen» som byline", feil_byline, port.HOLDES)
        ai_tildelt = {k: v for k, v in maria.items() if k != "forfatterbekreftelse"}
        prov(5, "Maria-byline uten Marias egen bekreftelse", ai_tildelt, port.HOLDES)

        # 6. Blandingssak uten teologisk mellomtittel
        blanding = {"id": "test-blandingssak", "kanal": "ghost-artikkel", "journalist": "redaksjonen",
                    "byline": "Mantelen redaksjonen", "forfatter": "Mantelen redaksjonen",
                    "egen_teologisk_vurdering": False, "tekst": BLANDINGSSAK}
        prov(6, "Blandingssak uten teologisk mellomtittel", blanding, port.HOLDES)
        maria_blanding = {"id": "test-maria-med-ai-tillegg", "kanal": "ghost-artikkel",
                          "journalist": port.MARIA, "byline": port.MARIA_BYLINE, "forfatter": port.MARIA,
                          "egen_teologisk_vurdering": False,
                          "tekst": dict(REN_MARIA_SAK, brodtekst=REN_MARIA_SAK["brodtekst"]
                                        + "\n\nKirken skylder menighetene et klart svar etter Guds ord.")}
        maria_blanding["forfatterbekreftelse"] = _bekreft(rot, maria_blanding, mar, "bekreftelse-maria-2.json")
        prov(6, "Teologisk tillegg i Marias tekst", maria_blanding, port.HOLDES)
        bytte = dict(art, journalist=port.MARIA, byline=port.MARIA_BYLINE, forfatter=port.MARIA)
        prov(6, "Teologisk artikkel med byline byttet til Maria", bytte, port.HOLDES)

        # 7. Planlagt publisering: kontroll ved planlegging og rett før utsending
        plan = prov(7, "Planlagt Maria-sak, ved planlegging", maria, port.PASSERER, "planlegging")
        prov(7, "Samme sak uendret, rett før utsending", maria, port.PASSERER, "utsending",
             plan["versjon_sha256"])
        prov(7, "Samme sak med teologisk tillegg i køen", dict(maria, tekst=maria_blanding["tekst"]),
             port.HOLDES, "utsending", plan["versjon_sha256"])
        prov(7, "Planlagt teologisk video uten ja, ved planlegging", shorts, port.HOLDES, "planlegging")

        # 8. Kilde-e-post
        epost_red = {"id": "test-epost-redaksjonen", "kanal": "epost", "journalist": port.MARIA,
                     "egen_teologisk_vurdering": False,
                     "epost": {"avsendernavn": "MANTELEN", "signatur": "Redaksjonen"},
                     "tekst": {"emne": "Spørsmål om vedtaket", "brodtekst": EPOST_KROPP + "Redaksjonen"}}
        prov(8, "Kilde-e-post med bare «Redaksjonen» som signatur", epost_red, port.HOLDES)
        epost_ok = {"id": "test-epost-maria", "kanal": "epost", "journalist": port.MARIA,
                    "egen_teologisk_vurdering": False,
                    "epost": {"avsendernavn": port.MARIA_AVSENDER, "signatur": port.MARIA_SIGNATUR},
                    "tekst": {"emne": "Spørsmål om vedtaket", "brodtekst": EPOST_KROPP + port.MARIA_SIGNATUR}}
        epost_ok["forfatterbekreftelse"] = _bekreft(rot, epost_ok, mar, "bekreftelse-epost.json")
        prov(8, "Kilde-e-post fra Maria med riktig navn og signatur", epost_ok, port.PASSERER)
        ai_signert = {k: v for k, v in epost_ok.items() if k != "forfatterbekreftelse"}
        prov(8, "E-post signert som Maria uten hennes bekreftelse", ai_signert, port.HOLDES)

        # 9. En AI kan ikke fylle ut godkjenningen
        usignert = rot / "godkjenning-usignert.json"
        usignert.write_text((rot / "godkjenning-artikkel.json").read_text(encoding="utf-8"), encoding="utf-8")
        prov(9, "Godkjenning skrevet uten signatur", dict(art, godkjenning=usignert.name), port.HOLDES)
        prov(9, "Godkjenning signert med fremmed nøkkel",
             dict(art, godkjenning=_godkjenn(rot, art, fremmed, "godkjenning-fremmed.json")), port.HOLDES)
        prov(9, "Godkjenning uten grunnlag i Topp 100",
             dict(art, godkjenning=_godkjenn(rot, art, red, "godkjenning-uten-liste.json",
                                             topp100={"fil": "", "versjon": "", "punkter": []})), port.HOLDES)
        prov(9, "Godkjenning for artikkelen brukt på videoen",
             dict(vid, godkjenning="godkjenning-artikkel.json"), port.HOLDES)
        tom_tillit = rot / "tom-tillit"
        tom_tillit.mkdir()
        res = port.kontroller(art_ok, rot, "utsending", None, tom_tillit)
        rader.append((9, "Ingen redaktørnøkkel registrert", "utsending", port.HOLDES, res["utfall"],
                      res["utfall"] == port.HOLDES, res["grunner"]))

    # Porten skal ikke kunne sende eller publisere noe.
    kilde = Path(port.__file__).read_text(encoding="utf-8")
    forbudt = [m for m in ("import socket", "import smtplib", "import urllib", "import http", "import requests")
               if m in kilde]
    rader.append((10, "Porten har ingen nettverkskode", "kildekode", "ingen", "ingen" if not forbudt else str(forbudt),
                  not forbudt, []))

    feil = 0
    for nr, navn, fase, forventet, fikk, ok, grunner in rader:
        print(f"{'OK  ' if ok else 'FEIL'} {nr:>2}  {fikk:<9} {fase:<12} {navn}")
        if "-v" in sys.argv:
            for g in grunner:
                print(f"            - {g}")
        feil += 0 if ok else 1
    print(f"\n{len(rader) - feil} av {len(rader)} prøver ga forventet utfall. "
          "Ingenting ble publisert, planlagt eller sendt.")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(kjor())
