#!/usr/bin/env python
"""VPM リスティングの index.json を、GitHub のリリースから組み立て直す。

使い方:
    python tools/build_index.py

このリスティングに載せるパッケージは PACKAGE_REPOS に書く。
各リポジトリのリリース資産（zip）を GitHub API から拾い、
zip の中の package.json をそのまま版情報として index.json に展開する。
zipSHA256 は実際にダウンロードして計算する（手で書かない）。
"""
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
import zipfile
from collections import OrderedDict
from pathlib import Path

LISTING = OrderedDict([
    ("name", "you5248 VPM Listing"),
    ("id", "com.you5248.vpm"),
    ("url", "https://you5248.github.io/vpm-listing/index.json"),
    ("author", "you5248"),
    ("description", "you5248 の VRChat ワールド向けパッケージ"),
])

# ここに載せたいパッケージのリポジトリを書く（public のみ。private は VCC から取得できない）
PACKAGE_REPOS = ["you5248/dhk-shaders"]


def gh_json(path):
    out = subprocess.run(["gh", "api", path], capture_output=True, check=True)
    return json.loads(out.stdout.decode("utf-8"))


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "vpm-listing-builder"})
    with urllib.request.urlopen(req) as r:
        return r.read()


def main():
    packages = OrderedDict()
    for repo in PACKAGE_REPOS:
        for rel in gh_json("repos/{}/releases".format(repo)):
            # ドラフトと prerelease は載せない（壊れた版を prerelease に落として除外する運用）
            if rel.get("draft") or rel.get("prerelease"):
                continue
            for asset in rel.get("assets", []):
                if not asset["name"].endswith(".zip"):
                    continue
                url = asset["browser_download_url"]
                blob = fetch(url)
                try:
                    with zipfile.ZipFile(io.BytesIO(blob)) as z:
                        manifest = json.loads(z.read("package.json").decode("utf-8"),
                                              object_pairs_hook=OrderedDict)
                except (KeyError, zipfile.BadZipFile):
                    print("  スキップ（zip のルートに package.json が無い）: " + url, file=sys.stderr)
                    continue

                manifest["url"] = url
                manifest["zipSHA256"] = hashlib.sha256(blob).hexdigest()

                name = manifest["name"]
                version = manifest["version"]
                packages.setdefault(name, OrderedDict([("versions", OrderedDict())]))
                packages[name]["versions"][version] = manifest
                print("  {} {}  ({} bytes)".format(name, version, len(blob)))

    listing = OrderedDict(LISTING)
    listing["packages"] = packages
    out = Path(__file__).resolve().parent.parent / "index.json"
    out.write_text(json.dumps(listing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("書き出し: {}".format(out))


if __name__ == "__main__":
    main()
