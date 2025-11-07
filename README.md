# 🛰️ Universal Wardriving File Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/ringmast4r/wardriving-converter)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ringmast4r/wardriving-converter/pulls)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red)](https://github.com/ringmast4r)

Convert any wardriving file format to standardized CSV. Handles large files that crash online converters.

## Why This?

| Online Converters | This Tool |
|-------------------|-----------|
| ❌ Size limits | ✅ No limits |
| ❌ Upload required | ✅ 100% offline |
| ❌ One format | ✅ 12+ formats |
| ❌ Manual process | ✅ Batch processing |
| ❌ Scattered outputs | ✅ Organized vault |

## Supported Formats

**Tools:** WiGLE, Kismet, G-Mon, inSSIDer, Kismac, WiFiFoFum, Wardrive-Android, WiFi-Where, NetStumbler, MacStumbler, DStumbler, Pocket Warrior

**Files:** `.kml`, `.kmz`, `.csv`, `.xml`, `.netxml`, `.gpsxml`, `.txt`

## Quick Start

### Windows
```bash
# Double-click and drag folders into the window
Wardriving Converter.bat
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

## Features

- **Batch Processing** - Convert 100+ files at once
- **Auto-Detection** - Automatically identifies format
- **Merge Option** - Combine all into one master CSV
- **Organized Output** - Timestamped folders in `conversion_vault/`
- **Cross-Platform** - Windows, Linux, macOS
- **No Dependencies** - Just Python 3.x standard library

## Output

Standardized CSV with: `ssid`, `bssid`, `latitude`, `longitude`, `altitude`, `signal`, `channel`, `encryption`, `type`, `timestamp`

All outputs saved to: `conversion_vault/YYYYMMDD_HHMM/`

## Example

```bash
# Before: 50 different format files scattered everywhere
# After: One clean CSV with all networks combined

python3 universal_wardrive_converter.py --folder ~/wardrives --merge
# Output: conversion_vault/20241107_1430/MERGED_ALL.csv
```

## License

MIT - See [LICENSE](LICENSE)

---

Made with ❤️ by [ringmast4r](https://github.com/ringmast4r)
