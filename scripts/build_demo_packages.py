#!/usr/bin/env python3
"""Build neutral public .3105 v3 demo packages without modifying 3105."""

from __future__ import annotations

import hashlib
import json
import plistlib
import uuid
from datetime import datetime
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "packages"
MAGIC = b"3105PATCH\x00"
SCHEMA_VERSION = 3
TARGET_BUNDLE = "com.test"
TARGET_PATH = "Documents/ilywd/test"
CREATED_AT = datetime(2026, 9, 7, 0, 0, 0)

PRESETS = [
    ("red", "Đỏ", "#FF3B30", "B64A0A11-25A2-4D8E-9C07-0B2F30A5E101", "2D60FA16-0372-4B2F-B90B-55A1642EA101"),
    ("blue", "Xanh dương", "#007AFF", "7B172864-C903-4D4F-882A-0CB4409BE102", "0F06DF98-F7C0-4381-BC55-0DE1EA604102"),
    ("yellow", "Vàng", "#FFCC00", "C9A272A6-5A74-4E57-A37D-E2E529664103", "BA48E2E5-22D4-4E13-A758-A1F31A3C4103"),
    ("purple", "Tím", "#AF52DE", "643566E5-59DD-4D5C-A53A-E8FDE5A06104", "356D0A39-CCF5-4211-95D4-8B478C9ED104"),
]


def binary_plist(value: dict) -> bytes:
    return plistlib.dumps(value, fmt=plistlib.FMT_BINARY, sort_keys=True)


def make_package(slug: str, label: str, color: str, project_id: str, rule_id: str) -> bytes:
    replacement = json.dumps(
        {
            "schemaVersion": 1,
            "colors": {
                "gunHex": color,
                "gunOpacity": 1.0,
                "outlineHex": "#FF3B30",
                "outlineWidth": 3.01,
            },
        },
        ensure_ascii=False,
        indent=2,
    ).encode("utf-8") + b"\n"

    project_uuid = str(uuid.UUID(project_id)).upper()
    rule_uuid = str(uuid.UUID(rule_id)).upper()
    project = {
        "id": project_uuid,
        "name": f"Color Tool Demo – {label}",
        "author": "ilywd",
        "isPrivate": False,
        "createdAt": CREATED_AT,
        "updatedAt": CREATED_AT,
        "bundleIdentifiers": [TARGET_BUNDLE],
        "directories": [],
        "rules": [
            {
                "id": rule_uuid,
                "bundleID": TARGET_BUNDLE,
                "relativePath": TARGET_PATH,
                "replacementFilename": "location-style.json",
                "replacementData": replacement,
            }
        ],
    }
    payload = {
        "project": project,
        "replacementDigests": {rule_uuid: hashlib.sha256(replacement).digest()},
    }
    payload_data = binary_plist(payload)
    # Các gói demo cần build lặp lại cho cùng một checksum trong repo công khai.
    # Khóa này không dùng để giữ bí mật: định dạng public của 3105 luôn mang khóa
    # nội dung trong envelope. Domain separator giữ key/nonce riêng cho từng preset.
    seed = hashlib.sha256(f"ilywd/3105/color-tool-demo/{slug}/v2".encode()).digest()
    content_key = hashlib.sha256(b"content-key\0" + seed).digest()
    nonce = hashlib.sha256(b"nonce\0" + seed).digest()[:12]
    aad = f"3105PATCH/v{SCHEMA_VERSION}/payload/{project_uuid}".encode("utf-8")
    encrypted_payload = nonce + AESGCM(content_key).encrypt(nonce, payload_data, aad)
    envelope = {
        "schemaVersion": SCHEMA_VERSION,
        "packageID": project_uuid,
        "isPasswordProtected": False,
        "publicContentKey": content_key,
        "keyFingerprint": hashlib.sha256(content_key).digest(),
        "encryptedPayload": encrypted_payload,
    }
    return MAGIC + binary_plist(envelope)


def validate_package(data: bytes) -> None:
    if not data.startswith(MAGIC):
        raise ValueError("Sai magic 3105")
    envelope = plistlib.loads(data[len(MAGIC):])
    key = envelope["publicContentKey"]
    if hashlib.sha256(key).digest() != envelope["keyFingerprint"]:
        raise ValueError("Sai key fingerprint")
    project_id = envelope["packageID"]
    aad = f"3105PATCH/v{envelope['schemaVersion']}/payload/{project_id}".encode("utf-8")
    combined = envelope["encryptedPayload"]
    payload_data = AESGCM(key).decrypt(combined[:12], combined[12:], aad)
    payload = plistlib.loads(payload_data)
    rule = payload["project"]["rules"][0]
    expected = payload["replacementDigests"][rule["id"]]
    if hashlib.sha256(rule["replacementData"]).digest() != expected:
        raise ValueError("Sai replacement digest")
    if rule["bundleID"] != TARGET_BUNDLE or rule["relativePath"] != TARGET_PATH:
        raise ValueError("Sai đích demo")


def main() -> None:
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    for slug, label, color, project_id, rule_id in PRESETS:
        data = make_package(slug, label, color, project_id, rule_id)
        validate_package(data)
        path = PACKAGE_DIR / f"location-color-{slug}.3105"
        path.write_bytes(data)
        print(f"{path.name}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
