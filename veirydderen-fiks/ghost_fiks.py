#!/usr/bin/env python3
"""Rydder Veirydderen-dataene i Ghost (oktober 2026).

1. Morgenkåpen utgave 13 mister taggen «Veirydderen», så den forsvinner fra tidslinjen.
2. Del 37 får den interne taggen #veirydder-kvinne, slik alle andre samtaler har.
3. Del 44 og 45 får publiseringsdatoen i stedet for plassholderteksten i bylinjen.

Uten --apply vises bare hva som ville blitt endret (leser via det offentlige Content API).
Med --apply kreves GHOST_ADMIN_API_KEY (format id:hemmelighet) fra en Custom Integration
i Ghost Admin (Settings, Integrations).

    python3 ghost_fiks.py            # prøvekjøring
    python3 ghost_fiks.py --apply    # skriver til Ghost
"""
import base64, hashlib, hmac, json, os, sys, time, urllib.request

GHOST = "https://mantelen.ghost.io"
CONTENT_KEY = "0955b9c6309f5a277bab4f7bc9"  # offentlig nøkkel, står i sidens HTML

FJERN_TAG = {"morgenkapen-utgave-13-4-oktober-2026": "veirydderen"}
LEGG_TIL_TAG = {"mest-opptatt-av-motet-med-mennesker": "#veirydder-kvinne"}
PLASSHOLDERE = {
    "i-dont-have-a-paper-signed-by-jesus": ("[PUBLICATION DATE TO BE SET]", "2 October 2026"),
    "vad-jesus-gor-ar-viktigare-an-vad-paulus-tycker": ("[PUBLISERINGSDATO SETTES]", "3. oktober 2026"),
}


def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def admin_token(key):
    kid, secret = key.split(":")
    now = int(time.time())
    header = b64(json.dumps({"alg": "HS256", "typ": "JWT", "kid": kid}).encode())
    payload = b64(json.dumps({"iat": now, "exp": now + 300, "aud": "/admin/"}).encode())
    sig = hmac.new(bytes.fromhex(secret), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    return f"{header}.{payload}.{b64(sig)}"


def request(url, method="GET", body=None, key=None):
    headers = {"Accept-Version": "v5.0", "Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Ghost " + admin_token(key)
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(urllib.request.Request(url, data, headers, method=method)) as r:
        return json.load(r)


def hent(slug, key):
    if key:
        url = f"{GHOST}/ghost/api/admin/posts/slug/{slug}/?formats=lexical&include=tags"
        return request(url, key=key)["posts"][0]
    url = f"{GHOST}/ghost/api/content/posts/slug/{slug}/?key={CONTENT_KEY}&formats=html&include=tags"
    return request(url)["posts"][0]


def lagre(post, endringer, key):
    url = f"{GHOST}/ghost/api/admin/posts/{post['id']}/"
    body = {"posts": [dict(endringer, updated_at=post["updated_at"])]}
    request(url, "PUT", body, key)


def main():
    apply = "--apply" in sys.argv
    key = os.environ.get("GHOST_ADMIN_API_KEY")
    if apply and not key:
        sys.exit("GHOST_ADMIN_API_KEY mangler.")
    key = key if apply else None

    for slug, tag in FJERN_TAG.items():
        post = hent(slug, key)
        tags = [{"id": t["id"]} for t in post["tags"] if t["slug"] != tag]
        if len(tags) == len(post["tags"]):
            print(f"OK      {slug}: har ikke taggen {tag}")
            continue
        print(f"ENDRE   {slug}: fjerner taggen {tag}")
        if apply:
            lagre(post, {"tags": tags}, key)

    for slug, navn in LEGG_TIL_TAG.items():
        post = hent(slug, key)
        if any(t["name"] == navn for t in post["tags"]):
            print(f"OK      {slug}: har allerede {navn}")
            continue
        print(f"ENDRE   {slug}: legger til {navn}")
        if apply:
            lagre(post, {"tags": [{"id": t["id"]} for t in post["tags"]] + [{"name": navn}]}, key)

    for slug, (gammel, ny) in PLASSHOLDERE.items():
        post = hent(slug, key)
        tekst = post.get("lexical") or post.get("html") or ""
        if gammel not in tekst:
            print(f"OK      {slug}: plassholderen er borte")
            continue
        print(f"ENDRE   {slug}: {gammel} -> {ny}")
        if apply:
            lagre(post, {"lexical": post["lexical"].replace(gammel, ny)}, key)

    if not apply:
        print("\nPrøvekjøring. Kjør med --apply og GHOST_ADMIN_API_KEY for å skrive endringene.")


if __name__ == "__main__":
    main()
