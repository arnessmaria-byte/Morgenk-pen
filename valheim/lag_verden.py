"""Lager en ny Valheim 1.0-verden (mappe med _main.0.fwl2) fra en seed.

Formatet følger World.SaveWorldMetaData i assembly_valheim, slik det er
dokumentert i MakeFwl (https://github.com/CrystalFerrai/MakeFwl, Apache 2.0).
Spillet genererer resten av verdenen selv første gang den lastes.
"""

import os
import random
import struct
import sys

WORLD_VERSION = 41  # Version.c_WorldVersion i Valheim 1.0
GEN_VERSION = 2  # Version.World (Ashlands-generatoren)

# Spillets "Hardcore"-preset, oversatt til globale nøkler
HARDCORE = [
    "playerdamage 70",
    "enemydamage 200",
    "enemyspeedsize 120",
    "enemyleveluprate 140",
    "eventrate 60",
    "nomap",
    "deathdeleteitems",
    "deathskillsreset",
    "nobossportals",
    "preset combat_veryhard:deathpenalty_hardcore:resources_default:raids_more:portals_hard",
]


def stable_hash(s):
    """StringExtensionMethods.GetStableHashCode fra assembly_utils (int32)."""
    def i32(x):
        x &= 0xFFFFFFFF
        return x - 0x100000000 if x & 0x80000000 else x

    a = b = 5381
    i = 0
    while i < len(s) and s[i] != "\0":
        a = i32(((a << 5) + a) ^ ord(s[i]))
        if i == len(s) - 1 or s[i + 1] == "\0":
            break
        b = i32(((b << 5) + b) ^ ord(s[i + 1]))
        i += 2
    return i32(a + b * 1566083941)


def write_string(s):
    """BinaryWriter.Write(string): 7-bit-kodet lengde + bytes."""
    data = s.encode("ascii")
    n, prefix = len(data), bytearray()
    while n >= 0x80:
        prefix.append((n & 0x7F) | 0x80)
        n >>= 7
    prefix.append(n)
    return bytes(prefix) + data


def build_fwl(name, seed, modifiers, uid):
    body = struct.pack("<i", WORLD_VERSION)
    body += write_string(name) + write_string(seed)
    body += struct.pack("<iqi?", stable_hash(seed), uid, GEN_VERSION, False)
    body += struct.pack("<i", len(modifiers))
    for key in modifiers:
        body += write_string(key)
    body += struct.pack("<i", 0)  # spillerhistorikk
    return struct.pack("<i", len(body)) + body


def make_world(out_dir, name, seed, modifiers):
    assert 5 <= len(name) <= 20 and 1 <= len(seed) <= 10
    folder = os.path.join(out_dir, name)
    os.makedirs(folder, exist_ok=True)
    uid = stable_hash(name) + random.randint(1, 2**31 - 1)
    with open(os.path.join(folder, "_main.0.fwl2"), "wb") as f:
        f.write(build_fwl(name, seed, modifiers, uid))
    return folder


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "worlds_local")
    print(make_world(out, "Bossrush", "HHcLC5acQt", []))
    print(make_world(out, "BossrushViking", "HHcLC5acQt", HARDCORE))
