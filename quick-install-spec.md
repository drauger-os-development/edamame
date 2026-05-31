# Quick Install File Format Specification

**Version:** 2.1
**Status:** Draft
**Maintainer:** Thomas Castleman \<batcastle@draugeros.org\>

---

## Overview

A Quick Install file captures system configuration so that an installer
(such as Edamame) can reproduce that configuration on a fresh installation
with minimal user interaction. It is designed to be simple enough that a
technically literate user can write one by hand in under 15 minutes without
any tooling.

Quick Install files come in two formats depending on whether carry-over
assets (network profiles, wallpaper) are included:

| Situation | Format | Extension | Name |
|---|---|---|---|
| Settings only | JSON text file | `.json` | Quick Install File |
| Settings + assets | XZ-compressed tar archive | `.tar.xz` | Advanced Quick Install File |

---

## JSON Format

### Top-level structure

The JSON file may be structured in one of two equivalent ways.

**With a `DATA` wrapper** (recommended for human-authored files):

```json
{
    "DATA": {
        "LANG": "en",
        ...
    },
    "COMMENTS": [
        "Any comments go here as an array of strings.",
        "This field is entirely optional and ignored by all tooling."
    ]
}
```

**Flat structure** (produced by Edamame's built-in export):

```json
{
    "LANG": "en",
    ...
}
```

Both are valid. When a `DATA` key is present, all tooling discards the
rest of the top-level object and reads only `DATA`. The `COMMENTS` field
is always ignored by tooling and exists solely for human readers.

---

### Fields

All fields listed below live either directly at the top level (flat
format) or inside `DATA` (wrapped format).

#### Partitioning

| Field | Type | Required | Description |
|---|---|---|---|
| `AUTO_PART` | `bool` | Yes | If `true`, the installer partitions the target drive automatically. All partition fields below are ignored when this is `true`. |
| `ROOT` | `string \| null` | Yes | Device path for the root (`/`) partition. e.g. `/dev/sda2`. `null` when `AUTO_PART` is `true`. |
| `EFI` | `string \| null` | Yes | Device path for the EFI System Partition. e.g. `/dev/sda1`. `null` on BIOS systems or when `AUTO_PART` is `true`. Treated as absent when set to `"NULL"`, `""`, or `false`. |
| `HOME` | `string \| null` | Yes | Device path for a separate `/home` partition. `null` if no separate home partition is desired. Treated as absent when set to `"NULL"` or `""`. The special value `"MAKE"` (only valid when `AUTO_PART` is `true`) instructs the auto-partitioner to create a dedicated home partition on the same target drive. |
| `SWAP` | `string \| null` | Yes | Device path for a swap partition (e.g. `/dev/sda3`), or the special string `"FILE"` to instruct the installer to create a swap file on the root partition. When `"FILE"` is used the installer is responsible for computing the swap file size using the formula recommended by the Linux kernel developers: `SWAP_SIZE = RAM_SIZE + √RAM_SIZE`. This size enables both full suspend and Hybrid Sleep. `null` if no swap is desired. **Note:** Edamame always sets this field to either `"FILE"` or a device path — it requires some form of swap for system stability and will not generate a Quick Install file with `null` here. Setting `SWAP` to `null` in a hand-authored file may bypass this, but correct behaviour with Edamame is not guaranteed. Other installers are encouraged to follow the same convention and require swap for consistency. |

**Note on BTRFS RAID home partitions:** When a home partition lives on a
drive formatted entirely with BTRFS as part of a RAID array (i.e. no
partition table), `HOME` may be set to a bare drive path such as
`/dev/sdb`. This is the only situation where a bare drive path is valid
for any partition field.

#### RAID Array

The `raid_array` field is an object with the following structure:

```json
"raid_array": {
    "raid_type": null,
    "disks": {
        "1": null,
        "2": null,
        "3": null,
        "4": null
    }
}
```

| Field | Type | Description |
|---|---|---|
| `raid_type` | `string \| null` | RAID level as a string: `"0"`, `"1"`, or `"10"`. These are the only levels supported, as they are the only RAID modes BTRFS supports. `null` if RAID is not in use. |
| `disks` | `object` | Object with string integer keys (starting from `"1"`) mapping to device path strings. A minimum of two disks must be defined. RAID 0 and RAID 1 require at least 2 disks; RAID 10 requires at least 4. The list may be longer than 4 entries if the array spans more drives. Unused slots should be set to `null`. The default template provides 4 slots to encourage RAID 10 for its balance of speed and redundancy. |

#### Locale and Input

| Field | Type | Required | Description |
|---|---|---|---|
| `LANG` | `string` | Yes | Two-letter ISO 639-1 language code. e.g. `"en"`, `"fr"`, `"de"`. |
| `TIME_ZONE` | `string` | Yes | IANA timezone string in `Region/SubRegion` format. e.g. `"US/Eastern"`, `"Europe/London"`. |
| `LAYOUT` | `string` | Yes | Human-readable keyboard layout label. e.g. `"English(US)"`. |
| `VARIENT` | `string` | Yes | Human-readable keyboard variant label. e.g. `"English(US) - English(US, euro on 5)"`. Note: this key is intentionally spelled `VARIENT` (not `VARIANT`) for historical compatibility. |
| `MODEL` | `string` | Yes | Keyboard model identifier. e.g. `"pc105"`, `"pc104"`. |

#### User Account

| Field | Type | Required | Description |
|---|---|---|---|
| `USERNAME` | `string` | Yes | Username for the primary user account created during installation. |
| `PASSWORD` | `string` | Yes | Plaintext password for the primary user account. **This value is not encrypted or hashed. Do not share this file without removing this field.** |
| `COMPUTER_NAME` | `string` | Yes | Hostname for the installed system. |

#### Installation Behaviour

| Field | Type | Required | Description |
|---|---|---|---|
| `EXTRAS` | `bool` | Yes | If `true`, install restricted extras during setup: proprietary media codecs (MP3, AAC, H.264) and proprietary GPU drivers (NVIDIA, AMD). |
| `UPDATES` | `bool` | Yes | If `true`, run a full system update as part of the installation process. |
| `LOGIN` | `bool` | Yes | If `true`, enable automatic login for the primary user at boot. |
| `COMPAT_MODE` | `bool` | No | Bootloader Compatibility Mode. If `true`, installs systemd-boot in its standard EFI location and additionally places the bootloader at the Windows Boot Manager path (`EFI/Microsoft/Boot/bootmgfw.efi`), allowing Linux to boot on locked-down UEFI firmware that only permits the Windows bootloader. Defaults to `false` if absent (for backwards compatibility with older files). |

#### OEM Mode

If any field value is the string `"OEM"`, the installer treats this as
an OEM pre-configuration installation. In this mode, certain steps are
skipped during the initial install and handled later when the end user
first boots the machine. Tooling that generates Quick Install files for
end users should not set any field to `"OEM"`.

---

### Minimal valid example

```json
{
    "DATA": {
        "LANG": "en",
        "TIME_ZONE": "US/Eastern",
        "AUTO_PART": true,
        "ROOT": null,
        "EFI": null,
        "HOME": null,
        "SWAP": null,
        "USERNAME": "alice",
        "PASSWORD": "changeme",
        "COMPUTER_NAME": "my-computer",
        "EXTRAS": true,
        "UPDATES": false,
        "LOGIN": false,
        "COMPAT_MODE": false,
        "MODEL": "pc105",
        "LAYOUT": "English(US)",
        "VARIENT": "English(US) - English(US, euro on 5)",
        "raid_array": {
            "raid_type": null,
            "disks": {
                "1": null,
                "2": null,
                "3": null,
                "4": null
            }
        }
    },
    "COMMENTS": [
        "Remove or leave the COMMENTS field as you prefer.",
        "Remember to remove the PASSWORD field before sharing this file."
    ]
}
```

---

## Advanced Quick Install File Format (`.tar.xz`)

When network settings or wallpaper are to be carried over, the Quick
Install file becomes an XZ-compressed tar archive. The JSON settings file
lives inside the archive alongside any assets.

### Directory structure

```
<archive>.tar.xz
├── settings/
│   ├── installation-settings.json   ← the JSON config described above
│   ├── network-settings/            ← NetworkManager connection profiles
│   │   └── <profile-name>           ← one file per saved connection
│   └── network-settings-NP/         ← netplan configuration
│       └── *.yaml
└── assets/
    ├── screens.list                  ← present only with a single wallpaper
    └── master/                       ← single wallpaper (all monitors)
        └── wallpaper.<ext>
```

**Multi-monitor wallpaper variant:** when different monitors use different
wallpapers, `assets/master/` is absent and each monitor gets its own
directory instead:

```
assets/
└── <monitor-name>/
    └── wallpaper.<ext>
```

In this case `screens.list` is not present, and the directory name
corresponds to the monitor identifier as reported by the desktop
environment.

### Field details

#### `settings/installation-settings.json`

The full Quick Install JSON config as described above. Either the flat or
`DATA`-wrapped format is valid here.

#### `settings/network-settings/`

Contains NetworkManager system connection profile files copied verbatim
from `/etc/NetworkManager/system-connections/` on the source machine.
These are applied to the live environment during installation, before
the network is used to download packages.

May be absent if network carry-over was not selected.

#### `settings/network-settings-NP/`

Contains netplan configuration files (`.yaml`) copied from `/etc/netplan/`
on the source machine. On systems not using netplan, this directory will
be absent or empty, and the installer silently ignores it.

On Windows source machines, this directory may contain synthesized netplan
files generated from the Windows network configuration.

May be absent if network carry-over was not selected.

#### `assets/master/wallpaper.<ext>`

The desktop wallpaper image. The file extension is preserved from the
original file. Any image format the target desktop environment supports is
valid here. The installer does not validate the format — it copies the
file to `/user-data/wallpaper.<ext>` on the new installation for the
post-install setup to consume.

On Windows source machines where the wallpaper is sourced from the
`TranscodedWallpaper` cache (which has no extension), `.jpg` is assumed
since Windows always transcodes wallpapers to JPEG in that cache location.

#### `assets/screens.list`

Plain text file, one monitor identifier per line, listing which monitors
should use the `master` wallpaper. Present only alongside `assets/master/`.

#### `assets/<monitor-name>/wallpaper.<ext>`

Per-monitor wallpaper, used when different monitors have different
wallpapers. The directory name is the monitor identifier as reported by
the desktop environment on the source machine.

---

## Backwards Compatibility

- **`COMPAT_MODE` absent:** treated as `false`. Files generated before
  this field was introduced continue to work without modification.
- **Flat vs. wrapped JSON:** both have been valid since the format's
  introduction. Do not rely on the presence of `DATA` to detect file
  version.
- **`EFI`, `HOME` set to `"NULL"`, `""`, or `false`:** all treated
  identically to `null` by the installer for historical reasons. New
  files should use `null`.

---


