#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
REPO_PATH = ROOT / "repo.json"
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Không đọc được JSON {path.relative_to(ROOT)}: {error}")


def validate_download(package: dict) -> None:
    raw_download = package.get("download")
    if not isinstance(raw_download, str) or not raw_download:
        fail(f"Package {package.get('identifier')} thiếu download")

    parsed = urlparse(raw_download)
    if parsed.scheme:
        if parsed.scheme != "https" or not parsed.hostname:
            fail(f"URL tải không phải HTTPS hợp lệ: {raw_download}")
        return

    file_path = (ROOT / raw_download).resolve()
    if ROOT not in file_path.parents:
        fail(f"Đường dẫn tải thoát khỏi repository: {raw_download}")
    if not file_path.is_file():
        fail(f"Không tìm thấy package: {raw_download}")

    data = file_path.read_bytes()
    actual_hash = hashlib.sha256(data).hexdigest()
    actual_size = len(data)
    if package.get("sha256", "").lower() != actual_hash:
        fail(f"SHA-256 không khớp: {raw_download}")
    if package.get("size") != actual_size:
        fail(f"Dung lượng không khớp: {raw_download}")


def main() -> None:
    repo = load_json(REPO_PATH)
    if repo.get("schemaVersion") != 1:
        fail("schemaVersion của repo phải bằng 1")
    if not IDENTIFIER_PATTERN.fullmatch(str(repo.get("identifier", ""))):
        fail("identifier của repo không hợp lệ")
    if not isinstance(repo.get("name"), str) or not repo["name"].strip():
        fail("repo thiếu name")

    packages = repo.get("packages")
    if not isinstance(packages, list):
        fail("packages phải là một mảng")

    seen = set()
    for package in packages:
        identifier = str(package.get("identifier", ""))
        if not IDENTIFIER_PATTERN.fullmatch(identifier):
            fail(f"Package identifier không hợp lệ: {identifier}")
        if identifier in seen:
            fail(f"Package identifier bị trùng: {identifier}")
        seen.add(identifier)
        if package.get("kind", "patch") not in {"patch", "wallpaper"}:
            fail(f"kind không hợp lệ: {identifier}")
        if not SHA_PATTERN.fullmatch(str(package.get("sha256", ""))):
            fail(f"SHA-256 không hợp lệ: {identifier}")
        supported_os = package.get("supportedOS")
        if not isinstance(supported_os, list) or not supported_os:
            fail(f"supportedOS bị thiếu: {identifier}")
        validate_download(package)

    print(f"OK: repo hợp lệ, {len(packages)} package")


if __name__ == "__main__":
    main()
