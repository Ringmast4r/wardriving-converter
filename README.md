<div align="center">

<img width="100%" alt="WARDRIVING CONVERTER" src="https://capsule-render.vercel.app/api?type=waving&color=0:000000,100:80246C&height=220&section=header&text=WARDRIVING%20CONVERTER&fontSize=57&fontColor=ffffff&animation=twinkling&fontAlignY=35&desc=Cross-platform%20%7C%20Python%20%7C%20GIS%20%7C%20Wardriving&descSize=16&descAlignY=58"/>

`Cross-platform` [`Python`](https://www.python.org/) `GIS` `Wardriving` - Universal wardriving file converter - supports 12+ formats (WiGLE, Kismet, KML), cross-platform, batch processing

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=20&pause=1000&color=80246C&center=true&vCenter=true&multiline=true&repeat=true&width=950&height=90&lines=Universal+wardriving+file+converter+-+supports+12%2B+formats+%28WiGLE%2C+Kismet%2C...%3BCross-platform+%2F+Python+%2F+GIS+%2F+Wardriving)](https://git.io/typing-svg)

<br>

[![Project](https://img.shields.io/badge/Project-wardriving--converter-80246C?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ringmast4r/wardriving-converter)
[![Format](https://img.shields.io/badge/Format-Python-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ringmast4r/wardriving-converter/tree/main)

[![Stars](https://img.shields.io/github/stars/Ringmast4r/wardriving-converter?style=flat-square&color=80246C)](https://github.com/Ringmast4r/wardriving-converter/stargazers)
[![Forks](https://img.shields.io/github/forks/Ringmast4r/wardriving-converter?style=flat-square&color=80246C)](https://github.com/Ringmast4r/wardriving-converter/network/members)
[![Repo Size](https://img.shields.io/github/repo-size/Ringmast4r/wardriving-converter?style=flat-square&color=80246C)](https://github.com/Ringmast4r/wardriving-converter)
[![Last Commit](https://img.shields.io/github/last-commit/Ringmast4r/wardriving-converter?style=flat-square&color=80246C)](https://github.com/Ringmast4r/wardriving-converter/commits/main)

</div>

---

# 🛰️ Universal Wardriving File Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/ringmast4r/wardriving-converter)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ringmast4r/wardriving-converter/pulls)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red)](https://github.com/ringmast4r)

Convert any wardriving file format to standardized CSV. Handles large files that crash online converters.

<a id="why-this"></a>
## `> why_this`

| Online Converters | This Tool |
|-------------------|-----------|
| ❌ Size limits | ✅ No limits |
| ❌ Upload required | ✅ 100% offline |
| ❌ One format | ✅ 12+ formats |
| ❌ Manual process | ✅ Batch processing |
| ❌ Scattered outputs | ✅ Organized vault |

<a id="supported-formats"></a>
## `> supported_formats`

**Tools:** WiGLE, Kismet, G-Mon, inSSIDer, Kismac, WiFiFoFum, Wardrive-Android, WiFi-Where, NetStumbler, MacStumbler, DStumbler, Pocket Warrior

**Files:** `.kml`, `.kmz`, `.csv`, `.xml`, `.netxml`, `.gpsxml`, `.txt`

<a id="quick-start"></a>
## `> quick_start`

### Windows (Drag & Drop!)
```bash
# 1. Double-click to launch
Wardriving Converter.bat

# 2. Drag any folder into the CMD window - done!
```

### Linux/Mac
```bash
chmod +x convert.sh
./convert.sh /path/to/folder
```

### Python (All Platforms)
```bash
# Single file
python3 universal_wardrive_converter.py file.kml

# Merge entire folder
python3 universal_wardrive_converter.py --folder ./data --merge
```

<a id="features"></a>
## `> features`

- **🎯 Drag & Drop** - Just drag folders into CMD window (Windows)
- **Batch Processing** - Convert 100+ files at once
- **Auto-Detection** - Automatically identifies format
- **Merge Option** - Combine all into one master CSV
- **Organized Output** - Timestamped folders in `conversion_vault/`
- **Cross-Platform** - Windows, Linux, macOS
- **No Dependencies** - Just Python 3.x standard library

<a id="output"></a>
## `> output`

Standardized CSV with: `ssid`, `bssid`, `latitude`, `longitude`, `altitude`, `signal`, `channel`, `encryption`, `type`, `timestamp`

All outputs saved to: `conversion_vault/YYYYMMDD_HHMM/`

<a id="example"></a>
## `> example`

```bash
# Before: 50 different format files scattered everywhere
# After: One clean CSV with all networks combined

python3 universal_wardrive_converter.py --folder ~/wardrives --merge
# Output: conversion_vault/20241107_1430/MERGED_ALL.csv
```

<a id="license"></a>
## `> license`

MIT - See [LICENSE](LICENSE)

---

Made with ❤️ by [ringmast4r](https://github.com/ringmast4r)

---

<div align="center">

<img width="100%" alt="WARDRIVING CONVERTER footer" src="https://capsule-render.vercel.app/api?type=waving&color=0:80246C,100:000000&height=120&section=footer&text=RINGMAST4R%20%2F%2F%20WARDRIVING&fontSize=18&fontColor=ffffff&fontAlignY=65"/>

</div>
