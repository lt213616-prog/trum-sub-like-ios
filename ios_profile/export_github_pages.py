#!/usr/bin/env python3
"""Export a PHP-free Pages site using the URL reported by actions/configure-pages."""
from pathlib import Path
import argparse
import base64
import plistlib
import struct
from urllib.parse import urlsplit, urljoin
import xml.etree.ElementTree as ET
from profile_format import create_profile, serialize_profile

HERE = Path(__file__).resolve().parent


def export(site_url, output):
    parsed = urlsplit(site_url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment or any(c.isspace() for c in site_url)):
        raise ValueError("--site-url phải là URL HTTPS của GitHub Pages, không kèm query/fragment.")
    base = site_url.rstrip("/") + "/"
    start = urljoin(base, "launch.html")
    icon = (HERE / "icon.png").read_bytes()
    if icon[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", icon[16:24]) != (512, 512):
        raise ValueError("Cần icon.png đúng PNG 512×512 từ logo Android.")
    icon_url = "data:image/png;base64," + base64.b64encode(icon).decode("ascii")
    profile = serialize_profile(create_profile(icon, start))
    # Explicit allowlist: PHP, Android, private files and build scripts are never deployed.
    files = {
        "index.html": (HERE / "install.template.html").read_text(encoding="utf-8")
            .replace("__ICON_DATA_URL__", icon_url).encode("utf-8"),
        "launch.html": (HERE / "splash.template.html").read_text(encoding="utf-8")
            .replace("__ICON_DATA_URL__", icon_url).encode("utf-8"),
        "icon.png": icon,
        "trumsublike.mobileconfig": profile.encode("utf-8"),
        ".nojekyll": b"",
    }
    if output.exists() and any(output.iterdir()):
        raise ValueError("Thư mục xuất phải mới hoặc trống, tránh đưa file cũ lên mạng.")
    output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (output / name).write_bytes(content)
    xml = ET.fromstring(files["trumsublike.mobileconfig"])
    payload = plistlib.loads(files["trumsublike.mobileconfig"])
    clip = payload["PayloadContent"][0]
    assert payload["PayloadIdentifier"] == "com.trumsublike.app.profile"
    assert clip["URL"] == start and clip["Icon"] == icon
    assert all(clip[k] is True for k in ("FullScreen", "IsRemovable", "Precomposed", "IgnoreManifestScope"))
    assert all(not any(c.isspace() for c in node.text) for node in xml.iter("data"))
    assert set(p.name for p in output.iterdir()) == set(files)
    assert 'href="./trumsublike.mobileconfig"' in files["index.html"].decode("utf-8")
    print("PASS: site PHP-free, XML/plist, embedded icon, clean Base64, Pages URL and file allowlist.")
    print("URL trang cài đặt (từ metadata Pages):", base)
    print("URL mở từ biểu tượng:", start)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    export(args.site_url, args.output)
