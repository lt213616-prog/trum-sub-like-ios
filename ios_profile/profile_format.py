"""Apple Web Clip payload shared by the PHP-hosting and GitHub Pages exporters."""
import plistlib
import re
import uuid


def create_profile(icon, start_url):
    profile_id = "com.trumsublike.app.profile"

    def stable_uuid(identifier):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, identifier)).upper()

    return {
        "PayloadType": "Configuration",
        "PayloadVersion": 1,
        "PayloadIdentifier": profile_id,
        "PayloadUUID": stable_uuid(profile_id),
        "PayloadDisplayName": "Trùm Sub Like",
        "PayloadOrganization": "Nguyễn Công Mỹ",
        "PayloadDescription": "Thêm Trùm Sub Like vào màn hình chính. Hồ sơ chỉ cài Web Clip, không cài chứng chỉ hay quản lý thiết bị.",
        "PayloadRemovalDisallowed": False,
        "PayloadContent": [{
            "PayloadType": "com.apple.webClip.managed",
            "PayloadVersion": 1,
            "PayloadIdentifier": profile_id + ".webclip",
            "PayloadUUID": stable_uuid(profile_id + ".webclip"),
            "PayloadDisplayName": "Trùm Sub Like",
            "PayloadOrganization": "Nguyễn Công Mỹ",
            "Label": "Trùm Sub Like",
            "URL": start_url,
            "FullScreen": True,
            "IgnoreManifestScope": True,
            "IsRemovable": True,
            "Precomposed": True,
            "Icon": icon,
        }],
    }


def serialize_profile(profile):
    xml = plistlib.dumps(profile, fmt=plistlib.FMT_XML, sort_keys=False).decode("utf-8")
    return re.sub(
        r"<data>\s*([A-Za-z0-9+/=\s]*)</data>",
        lambda match: "<data>" + re.sub(r"\s", "", match[1]) + "</data>",
        xml,
    )
