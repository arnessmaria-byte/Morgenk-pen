#!/usr/bin/env python3
"""MANTELEN redaksjonsport.

Kontrollerer den endelige kanalversjonen av en sak, video eller e-post mot
redaksjonsordren av 25. november 2026. Porten publiserer ikke, planlegger
ikke og sender ikke. Den svarer bare PASSERER eller HOLDES, og verktøyet som
kaller den, skal la saken bli liggende som utkast når svaret er HOLDES.

Bruk:
    python port.py kontroller sak.json --fase planlegging
    python port.py kontroller sak.json --fase utsending --planlagt-versjon <sha256>
    python port.py forelegg sak.json --topp100-versjon ... --punkter 35,41 --samsvar "..."
    python port.py svar sak.json --svar ja --ord "Ja" --hvor "..."   # etter at redaktøren har svart

Bare standardbiblioteket og `openssl` (3.0 eller nyere) brukes. Ingen nettverkskode.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

REDAKTOR = "Elias Solbak Årnes"
MARIA = "Maria Solbak Årnes"
MARIA_BYLINE = "Av Maria Solbak Årnes, journalist i MANTELEN"
MARIA_AVSENDER = "Maria Solbak Årnes, MANTELEN"
MARIA_SIGNATUR = "Maria Solbak Årnes, journalist i MANTELEN"

PASSERER = "PASSERER"
HOLDES = "HOLDES"

# Kanaler der publikum møter lyd og bilde. Der må både den ferdige filen og
# all tekst i den (manus, fortellerstemme, skjermtekst, undertekster) følge med.
VIDEOKANALER = ("youtube-video", "youtube-shorts")
VIDEOTEKST = ("manus", "fortellerstemme", "undertekster")
ARTIKKELKANALER = ("ghost-artikkel", "ghost-nyhetsbrev")

NOKKEL_REDAKTOR = "redaktor.pub.pem"


# --------------------------------------------------------------------------
# Versjon: SHA-256 av alt publikum eller mottakeren får se
# --------------------------------------------------------------------------

def _norm(verdi):
    if isinstance(verdi, str):
        return unicodedata.normalize("NFC", verdi.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(verdi, list):
        return [_norm(v) for v in verdi]
    if isinstance(verdi, dict):
        return {str(k): _norm(v) for k, v in verdi.items()}
    return verdi


def _filhash(sti: Path) -> str:
    h = hashlib.sha256()
    with open(sti, "rb") as f:
        for blokk in iter(lambda: f.read(1 << 20), b""):
            h.update(blokk)
    return h.hexdigest()


def versjon(sak: dict, rot: Path) -> str:
    """Versjonshash for den endelige kanalversjonen.

    Dekker kanal, all tekst, ferdige filer (byte for byte), byline, forfatter
    og e-postens avsendernavn og signatur. Endres ett tegn, endres hashen.
    """
    filer = {}
    for navn, sti in sorted((sak.get("filer") or {}).items()):
        p = (rot / sti) if not Path(sti).is_absolute() else Path(sti)
        filer[navn] = _filhash(p) if p.is_file() else "MANGLER"
    epost = sak.get("epost") or {}
    grunnlag = {
        "kanal": sak.get("kanal", ""),
        "tekst": _norm(sak.get("tekst") or {}),
        "filer": filer,
        "byline": _norm(sak.get("byline", "")),
        "forfatter": _norm(sak.get("forfatter", "")),
        "epost": {"avsendernavn": _norm(epost.get("avsendernavn", "")),
                  "signatur": _norm(epost.get("signatur", ""))},
    }
    data = json.dumps(grunnlag, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# Innholdsskjerm: et gulv, ikke en dommer
# --------------------------------------------------------------------------

_SITAT = re.compile(r"«[^»]*»|“[^”]*”|\"[^\"]*\"")

_BOKER = (
    r"(?:[1-5]\.?\s?)?(?:Mos(?:ebok)?|Sam(?:uelsbok)?|Kong(?:ebok)?|Krøn(?:ikebok)?|Kor(?:interbrev)?|"
    r"Tess(?:alonikerbrev)?|Tim(?:oteusbrev)?|Pet(?:ersbrev)?|Joh(?:annesbrev)?|Corinthians|"
    r"Thessalonians|Timothy|Peter|John|Kings|Samuel|Chronicles)"
    r"|Matt(?:eus(?:evangeliet)?)?|Mark(?:us(?:evangeliet)?)?|Luk(?:as(?:evangeliet)?)?|"
    r"Joh(?:annes(?:evangeliet)?)?|Apg|Apostlenes gjerninger|Rom(?:erbrevet)?|Gal(?:aterbrevet)?|"
    r"Ef(?:eserbrevet)?|Fil(?:ipperbrevet)?|Kol(?:osserbrevet)?|Tit(?:usbrevet)?|Hebr(?:eerbrevet)?|"
    r"Jak(?:obs brev)?|Jud(?:asbrevet)?|Åp(?:enbaringen)?|Sal(?:me(?:ne)?)?|Ordsp(?:råkene)?|"
    r"Fork(?:ynneren)?|Jes(?:aja)?|Jer(?:emia)?|Esek(?:iel)?|Dan(?:iel)?|Hos(?:ea)?|Joel|Amos|Mika|"
    r"Sak(?:arja)?|Mal(?:aki)?|Jobs? bok|Genesis|Exodus|Leviticus|Deuteronomy|Psalms?|Proverbs|Isaiah|"
    r"Jeremiah|Ezekiel|Matthew|Luke|Acts|Romans|Galatians|Ephesians|Philippians|Colossians|Hebrews|"
    r"James|Revelation"
)
_SKRIFTSTED = re.compile(rf"(?<!\w)(?:{_BOKER})\.?\s+\d{{1,3}}\s*[,:]\s*\d{{1,3}}", re.IGNORECASE)

_MARKOR = re.compile(r"teologiske? vurdering|theological assessment", re.IGNORECASE)

_TEOLOGI = re.compile(
    r"(?<!\w)(?:frels\w*|[Gg]uds (?:rike|folk|ord|vilje|løfte\w*|nåde|trofasthet|pakt)|Skriften|"
    r"Bibelen (?:sier|lærer|viser)|bibeltro\w*|evangeliet|nåden|nådegave\w*|synden|synder|syndig\w*|"
    r"omvend\w*|vranglær\w*|kjetter\w*|utvelgelse\w*|Messias|Kristus er|Jesus (?:er|sier|lærer|sa)|"
    r"Herren|Den hellige ånd|apostelen|profeten|"
    r"salvation|saved|kingdom of God|the gospel|Scripture|God's (?:word|people|will|promise)|"
    r"repent\w*|heres\w+|the apostle|the prophet)(?!\w)"
)

_NORMATIV = re.compile(
    r"(?<!\w)(?:[Kk]irken|[Kk]ristne|[Ee]n kristen|[Dd]en som tror|[Tt]roende|[Mm]enigheten|"
    r"[Tt]he church|[Cc]hristians|[Aa] [Cc]hristian)(?!\w)[^.?!]{0,80}?(?<!\w)"
    r"(?:skylder|bør|har (?:fått )?et kall|er kalt til|k(?:an|unne) ikke tie|plikter|ought|owes?|should)(?!\w)"
)

_VERB = (r"(?:sier|sa|skriver|skrev|mener|mente|hevder|hevdet|svarer|svarte|uttaler|uttalte|forklarer|"
         r"forklarte|påpeker|påpekte|viser til|viste til|kaller|kalte|krever|krevde|opplyser|opplyste|"
         r"says|said|writes|wrote|claims|claimed|argues|argued)")
_NAVN = r"[A-ZÆØÅ][\w.'-]+"
_PRONOMEN = r"(?:[Hh]an|[Hh]un|[Dd]e|[Hh]e|[Ss]he|[Tt]hey)"
_ROLLE = r"(?:biskopen|presten|styret|kirkerådet|avisen|uttalelsen|brevet|menigheten|organisasjonen)"
_ATTRIB = re.compile(
    rf"(?:[Ii]følge|[Aa]ccording to)\s+(?P<a>{_NAVN}|{_ROLLE})"
    rf"|(?P<b>{_NAVN}|{_PRONOMEN}|{_ROLLE})\s+{_VERB}(?!\w)"
    rf"|(?<!\w){_VERB}\s+(?P<c>{_NAVN}|{_PRONOMEN}|{_ROLLE})"
)
# Bibelens forfattere og skikkelser er ikke kilder i journalistisk forstand.
# Det er heller ikke redaksjonen selv.
_IKKE_KILDE = {
    "paulus", "peter", "johannes", "jesus", "kristus", "moses", "jeremia", "jesaja", "hosea", "david",
    "lukas", "matteus", "markus", "jakob", "gud", "herren", "skriften", "bibelen", "apostelen",
    "profeten", "paul", "john", "mantelen", "redaksjonen", "vi", "we", "scripture",
    # Småord med stor forbokstav først i setningen er ikke navn på en kilde.
    "hva", "hvem", "hvor", "hvorfor", "hvordan", "det", "dette", "den", "der", "da", "så", "men", "og",
    "som", "når", "slik", "her", "nå", "likevel", "derfor", "what", "who", "why", "how", "it", "this",
    "that", "but", "and", "so", "the", "there", "then",
}
_PRON = {"han", "hun", "de", "he", "she", "they"}
# «Han viste til Matt 28,19» er referat av hva en omtalt person henviste til.
_HENVISER = re.compile(
    rf"(?:{_PRONOMEN}|{_ROLLE})\s+(?:viste|viser|henviste|henviser)\s+til|(?:referred|refers|pointed) to")


def _kilde(setning: str):
    """Returnerer 'navn', 'pronomen' eller None for hvem setningen tilskrives."""
    best = None
    for m in _ATTRIB.finditer(setning):
        hvem = (m.group("a") or m.group("b") or m.group("c") or "").strip(".,:;")
        lav = hvem.lower()
        if lav in _IKKE_KILDE:
            continue
        if lav in _PRON:
            best = best or "pronomen"
        else:
            return "navn"
    return best


def _setninger(tekst: str):
    """Gir (maskert, ordrett) for hver setning. I den maskerte er sitatene blanket ut."""
    maskert = _SITAT.sub(lambda m: m.group()[0] + "~" * (len(m.group()) - 2) + m.group()[-1], tekst)
    start = 0
    grenser = [m.span() for m in re.finditer(r"(?<=[.!?:])\s+|(?<=[»”\"])\s+(?=[A-ZÆØÅ])|\n+", maskert)] + [(len(maskert), len(maskert))]
    for a, b in grenser:
        if maskert[start:a].strip():
            yield maskert[start:a].strip(), tekst[start:a].strip()
        start = b


def skjerm(tekstfelt: dict) -> list[dict]:
    """Finner setninger som kan være MANTELENs egen teologiske vurdering.

    Sitater i anførselstegn regnes som kildens ord. En setning som tilskrives
    en navngitt kilde, regnes som gjengivelse. Skriftsteder og teologiske
    utsagn i redaksjonens egen stemme gir funn. Skjermen er et gulv: den
    fanger det åpenbare. Det den ikke fanger, er fortsatt omfattet av ordren.
    """
    funn = []
    for felt, verdi in (tekstfelt or {}).items():
        biter = verdi if isinstance(verdi, list) else [verdi]
        for bit in biter:
            if not isinstance(bit, str):
                continue
            for s, ordrett in _setninger(_norm(bit)):
                kilde = _kilde(s)
                grunn = None
                if _MARKOR.search(s):
                    grunn = "varsler egen teologisk vurdering"
                elif _SKRIFTSTED.search(s) and kilde != "navn" and not (kilde and _HENVISER.search(s)):
                    grunn = "skriftsted i redaksjonens egen stemme"
                elif kilde is None and _TEOLOGI.search(s):
                    grunn = ("spørsmål som forutsetter et teologisk svar" if s.endswith("?")
                             else "teologisk utsagn uten navngitt kilde")
                elif kilde is None and _NORMATIV.search(s):
                    grunn = "konklusjon om hva kirken eller kristne bør, uten navngitt kilde"
                if grunn:
                    funn.append({"felt": felt, "grunn": grunn, "setning": ordrett})
    return funn


# --------------------------------------------------------------------------
# Redaktørens svar: et kort ja eller nei, notert ordrett og bundet til versjonen
# --------------------------------------------------------------------------

def tillitsmappe() -> Path:
    return Path(os.environ.get("MANTELEN_TILLIT") or (Path.home() / ".mantelen" / "tillit"))


def _signert(dokument: Path, pub: Path) -> bool:
    sig = Path(str(dokument) + ".sig")
    if not (dokument.is_file() and sig.is_file() and pub.is_file()):
        return False
    try:
        r = subprocess.run(
            ["openssl", "pkeyutl", "-verify", "-pubin", "-inkey", str(pub), "-rawin",
             "-in", str(dokument), "-sigfile", str(sig)],
            capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return r.returncode == 0


def _les(sti: Path):
    try:
        return json.loads(sti.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _godkjenningsfil(sak: dict, rot: Path) -> Path:
    return rot / (sak.get("godkjenning") or f"{sak.get('id')}.godkjenning.json")


def _foreleggelsesfil(sak: dict, rot: Path) -> Path:
    return rot / f"{sak.get('id')}.foreleggelse.json"


def _godkjenning(sak: dict, rot: Path, v: str, tillit: Path) -> list[str]:
    """Tom liste betyr at ansvarlig redaktør har svart ja til nettopp denne versjonen."""
    dok = _godkjenningsfil(sak, rot)
    g = _les(dok)
    if not isinstance(g, dict):
        return ["ansvarlig redaktør har ikke svart ja til denne versjonen"]
    feil = []
    if g.get("svar") == "nei":
        feil.append("ansvarlig redaktør har svart nei")
    elif g.get("svar") != "ja":
        feil.append("redaktørens svar er ikke et tydelig ja")
    gitt = g.get("gitt") or {}
    if not (g.get("redaktorens_ord") and gitt.get("nar") and gitt.get("hvor")):
        feil.append("det er ikke notert hva redaktøren svarte, og når og hvor han svarte")
    if g.get("sak_id") != sak.get("id") or g.get("kanal") != sak.get("kanal"):
        feil.append("svaret gjelder en annen sak eller kanal")
    if g.get("versjon_sha256") != v:
        feil.append("innholdet er endret etter at redaktøren svarte, den nye versjonen må forelegges ham")
    t = g.get("topp100") or {}
    if not t.get("versjon"):
        feil.append("det er ikke oppgitt hvilken versjon av Topp 100-listen vurderingen bygger på")
    if not (t.get("punkter") or g.get("utover_listen")):
        feil.append("det er verken oppgitt punkter i Topp 100-listen eller hva som går utover listen")
    # Valgfri skjerping: har redaktøren lagt inn en nøkkel, må svaret også være signert med den.
    pub = tillit / NOKKEL_REDAKTOR
    if pub.is_file() and not _signert(dok, pub):
        feil.append("redaktørens nøkkel er registrert, men svaret er ikke signert med den")
    return feil


# --------------------------------------------------------------------------
# Selve kontrollen
# --------------------------------------------------------------------------

def _navnet_brukes(sak: dict) -> bool:
    epost = sak.get("epost") or {}
    felt = [sak.get("byline", ""), sak.get("forfatter", ""),
            epost.get("avsendernavn", ""), epost.get("signatur", "")]
    return any("Maria" in (f or "") for f in felt)


def kontroller(sak: dict, rot: Path, fase: str = "planlegging",
               planlagt_versjon: str | None = None, tillit: Path | None = None) -> dict:
    tillit = tillit or tillitsmappe()
    kanal = sak.get("kanal", "")
    tekst = sak.get("tekst") or {}
    v = versjon(sak, rot)
    grunner: list[str] = []
    merknader: list[str] = []

    if planlagt_versjon and planlagt_versjon != v:
        merknader.append("innholdet er endret siden planleggingen, hele kontrollen er kjørt på nytt")

    # 1. Er den endelige kanalversjonen lagt frem i sin helhet?
    uavklart = []
    if not sak.get("id") or not kanal:
        uavklart.append("saken mangler id eller kanal")
    if not any(isinstance(x, (str, list)) and x for x in tekst.values()):
        uavklart.append("ingen tekst er lagt frem til kontroll")
    for navn, sti in (sak.get("filer") or {}).items():
        if not ((rot / sti).is_file()):
            uavklart.append(f"filen «{navn}» finnes ikke")
    if kanal in VIDEOKANALER:
        if "video" not in (sak.get("filer") or {}):
            uavklart.append("den ferdige videofilen er ikke lagt ved")
        if not any(tekst.get(f) for f in VIDEOTEKST):
            uavklart.append("videoen mangler manus, fortellerstemme eller undertekster til kontroll")
    erklaert = sak.get("egen_teologisk_vurdering")
    if erklaert is None:
        uavklart.append("det er ikke oppgitt om innholdet har egen teologisk vurdering")

    # 2. Teologisk innhold: innholdet avgjør, ikke overskriften og ikke bylinen.
    funn = skjerm(tekst)
    teologisk = bool(funn) or erklaert is True
    if teologisk or uavklart:
        mangler = _godkjenning(sak, rot, v, tillit)
        if mangler:
            if teologisk:
                grunner.append("innholdet har eller kan ha MANTELENs egen teologiske vurdering")
            grunner.extend(uavklart)
            grunner.extend(mangler)

    # 3. Marias navn: riktig byline, forfatter, avsendernavn og signatur.
    journalist = sak.get("journalist", "")
    if journalist == MARIA:
        if kanal in ARTIKKELKANALER:
            if sak.get("byline") != MARIA_BYLINE:
                grunner.append(f"synlig byline skal være «{MARIA_BYLINE}», «Redaksjonen» alene er utilstrekkelig")
            if sak.get("forfatter") != MARIA:
                grunner.append("forfatter i Ghost skal være Maria Solbak Årnes")
        if kanal == "epost":
            epost = sak.get("epost") or {}
            if epost.get("avsendernavn") != MARIA_AVSENDER:
                grunner.append(f"avsendernavnet skal være «{MARIA_AVSENDER}»")
            kropp = _norm(tekst.get("brodtekst", "")).rstrip()
            if epost.get("signatur") != MARIA_SIGNATUR or not kropp.endswith(MARIA_SIGNATUR):
                grunner.append(f"e-posten skal signeres «{MARIA_SIGNATUR}», «Redaksjonen» alene er utilstrekkelig")
        if teologisk:
            grunner.append("teologisk vurdering i Marias tekst: hele denne versjonen skal til ansvarlig redaktør")
    elif _navnet_brukes(sak):
        grunner.append("Marias navn er brukt uten at hun er oppgitt som journalist eller avsender")
    if kanal == "epost" and not journalist:
        grunner.append("det er ikke oppgitt hvem som faktisk er avsender")

    grunner = list(dict.fromkeys(grunner))
    return {
        "sak_id": sak.get("id"),
        "kanal": kanal,
        "fase": fase,
        "versjon_sha256": v,
        "utfall": HOLDES if grunner else PASSERER,
        "grunner": grunner,
        "merknader": merknader,
        "funn": funn,
        "kontrollert": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "handling": ("kan følge ordinær publiseringsvei" if not grunner
                     else "skal bli liggende som utkast til ansvarlig redaktør har svart ja"),
    }


# --------------------------------------------------------------------------
# Foreleggelse: ett kort spørsmål redaktøren kan svare ja eller nei på
# --------------------------------------------------------------------------

def forelegg(sak: dict, rot: Path, topp100_versjon: str = "", punkter: list[str] | None = None,
             samsvar: str = "", utover: str = "") -> tuple[str, dict]:
    """Lager spørsmålet til redaktøren. Kort først, hele teksten under."""
    v = versjon(sak, rot)
    tekst = sak.get("tekst") or {}
    funn = skjerm(tekst)
    setninger = list(dict.fromkeys(f["setning"] for f in funn))
    tittel = tekst.get("tittel") or sak.get("id")
    kort = [f"TIL GODKJENNING: «{tittel}» ({sak.get('kanal')})",
            "Godkjenner du denne teologiske vurderingen? Svar ja eller nei.", ""]
    if setninger:
        kort.append("Dette sier MANTELEN selv:")
        kort += [f"  {n}. {s}" for n, s in enumerate(setninger, 1)]
    else:
        kort.append("Skjermen fant ingen enkeltsetninger. Vurderingen må pekes ut for hånd her.")
    kort.append("")
    if punkter:
        kort.append(f"Topp 100 ({topp100_versjon or 'VERSJON MANGLER'}): punkt {', '.join(punkter)}. {samsvar}".rstrip())
    if utover:
        kort.append(f"Går utover listen: {utover}")
    if not punkter and not utover:
        kort.append("GRUNNLAG MANGLER: oppgi punkter i Topp 100 eller hva som går utover listen.")
    kort.append(f"Versjon {v[:12]}. Hele teksten står under.")
    full = ["", "-" * 60]
    for felt, verdi in tekst.items():
        full.append(f"[{felt}]")
        full.extend(verdi if isinstance(verdi, list) else [str(verdi)])
        full.append("")
    for navn, sti in (sak.get("filer") or {}).items():
        full.append(f"[fil: {navn}] {sti}")
    grunnlag = {"type": "mantelen-foreleggelse", "sak_id": sak.get("id"), "kanal": sak.get("kanal"),
                "versjon_sha256": v, "sporsmal": kort[1], "setninger": setninger,
                "topp100": {"versjon": topp100_versjon, "punkter": punkter or [], "samsvar": samsvar},
                "utover_listen": utover}
    return "\n".join(kort + full), grunnlag


def noter_svar(sak: dict, rot: Path, svar: str, ordrett: str, hvor: str) -> tuple[bool, str]:
    """Noterer redaktørens svar på den foreleggelsen han faktisk så.

    Kalles først etter at ansvarlig redaktør selv har svart. `ordrett` er svaret
    slik han skrev det, og `hvor` er stedet det kan finnes igjen.
    """
    f = _les(_foreleggelsesfil(sak, rot))
    if not isinstance(f, dict):
        return False, "ingen foreleggelse funnet, kjør «forelegg» og vis den til redaktøren først"
    if f.get("versjon_sha256") != versjon(sak, rot):
        return False, "innholdet er endret siden foreleggelsen, legg den nye versjonen frem på nytt"
    if svar not in ("ja", "nei") or not ordrett.strip() or not hvor.strip():
        return False, "svaret må være ja eller nei, med redaktørens egne ord og hvor han svarte"
    g = dict(f, type="mantelen-teologisk-godkjenning", svar=svar, redaktorens_ord=ordrett.strip(),
             gitt={"nar": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "hvor": hvor.strip()},
             godkjent_av=REDAKTOR)
    _godkjenningsfil(sak, rot).write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    return True, "notert"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="MANTELEN redaksjonsport. Publiserer og sender ingenting.")
    sub = ap.add_subparsers(dest="kommando", required=True)
    k = sub.add_parser("kontroller", help="PASSERER eller HOLDES for den endelige kanalversjonen")
    k.add_argument("sak")
    k.add_argument("--fase", choices=["planlegging", "utsending"], required=True)
    k.add_argument("--planlagt-versjon")
    f = sub.add_parser("forelegg", help="lag det korte spørsmålet til redaktøren")
    f.add_argument("sak")
    f.add_argument("--topp100-versjon", default="")
    f.add_argument("--punkter", default="", help="for eksempel 35,41")
    f.add_argument("--samsvar", default="", help="én setning om hvordan vurderingen samsvarer med punktene")
    f.add_argument("--utover", default="", help="hva som går utover det listen avgjør")
    n = sub.add_parser("svar", help="noter redaktørens ja eller nei etter at han har svart")
    n.add_argument("sak")
    n.add_argument("--svar", choices=["ja", "nei"], required=True)
    n.add_argument("--ord", required=True, help="redaktørens svar, ordrett")
    n.add_argument("--hvor", required=True, help="hvor svaret ble gitt, så det kan finnes igjen")
    a = ap.parse_args(argv)

    sti = Path(a.sak)
    sak = _les(sti)
    if not isinstance(sak, dict):
        print(json.dumps({"utfall": HOLDES, "grunner": ["saksfilen kan ikke leses"]}, ensure_ascii=False))
        return 1
    if a.kommando == "forelegg":
        punkter = [x.strip() for x in a.punkter.split(",") if x.strip()]
        kort, grunnlag = forelegg(sak, sti.parent, a.topp100_versjon, punkter, a.samsvar, a.utover)
        _foreleggelsesfil(sak, sti.parent).write_text(
            json.dumps(grunnlag, ensure_ascii=False, indent=2), encoding="utf-8")
        print(kort)
        return 0
    if a.kommando == "svar":
        ok, melding = noter_svar(sak, sti.parent, a.svar, a.ord, a.hvor)
        print(melding)
        return 0 if ok else 1
    res = kontroller(sak, sti.parent, a.fase, a.planlagt_versjon)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["utfall"] == PASSERER else 1


if __name__ == "__main__":
    sys.exit(main())
