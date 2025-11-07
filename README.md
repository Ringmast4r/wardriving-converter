# 🛰️ Universal Wardriving File Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/ringmast4r/kml-converter)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ringmast4r/kml-converter/pulls)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red)](https://github.com/ringmast4r)

Convert **ANY** wardriving file format to standardized CSV - handles files that online converters reject!

**Cross-Platform:** Works on Windows, Linux, and macOS

## 🎯 Supported Formats

**12+ wardriving tools supported:**
- ✅ WiGLE WiFi Wardriving
- ✅ Kismet (all formats)
- ✅ G-Mon
- ✅ inSSIDer
- ✅ Kismac
- ✅ WiFiFoFum
- ✅ Wardrive-Android
- ✅ WiFi-Where
- ✅ DStumbler
- ✅ MacStumbler
- ✅ NetStumbler
- ✅ Pocket Warrior

**File types supported:**
`.kml`, `.kmz`, `.csv`, `.xml`, `.netxml`, `.gpsxml`, `.txt`, `.nettxt`, and more!

See [FORMATS_SUPPORTED.md](FORMATS_SUPPORTED.md) for complete details.

---

## 🚀 Quick Start

### Windows 🪟

**Drag & Drop (Easiest):**
1. **Drag files/folders onto `CONVERT.bat`**
2. Choose your option (1, 2, or 3)
3. Done! Check `conversion_vault` folder

**Command Line:**
```cmd
CONVERT.bat "C:\path\to\files"
```

### Linux/Mac 🐧🍎

**Command Line:**
```bash
./convert.sh /path/to/files
```

**Direct Python (All Platforms):**
```bash
# Single file
python3 universal_wardrive_converter.py yourfile.csv

# Folder (separate files)
python3 universal_wardrive_converter.py --folder ./wardrives

# Folder (merge all)
python3 universal_wardrive_converter.py --folder ./data --merge

# Folder (recursive + merge)
python3 universal_wardrive_converter.py --folder ./data --recursive --merge
```

**See `QUICKSTART.md` for detailed platform-specific instructions!**

---

## ✨ Features

✅ **Cross-Platform** - Works on Windows, Linux, and macOS
✅ **Batch Processing** - Convert entire folders at once (mix any formats!)
✅ **Merge Option** - Combine 100+ files into one master CSV
✅ **Conversion Vault** - All outputs organized in timestamped folders
✅ **No Size Limits** - Handles 100MB+ files that crash online tools
✅ **Auto-Detection** - Automatically identifies format
✅ **Universal Output** - Standardized CSV with all fields
✅ **Offline** - 100% local, no internet needed
✅ **Fast** - Progress updates for large files
✅ **Smart Parsing** - Extracts all WiFi survey data automatically

---

## 📦 Conversion Vault

All converted files are automatically saved to the **`conversion_vault`** folder with timestamps:

```
kml-converter/
└── conversion_vault/
    ├── 20241107_0900/      ← Morning conversion
    │   └── MERGED_ALL.csv
    ├── 20241107_1430/      ← Afternoon batch
    │   ├── file1_converted.csv
    │   ├── file2_converted.csv
    │   └── file3_converted.csv
    └── 20241107_2015/      ← Evening conversion
        └── MERGED_ALL.csv
```

**Benefits:**
- 🗂️ Never lose a conversion
- 📅 Easy to find by date/time
- 🔄 Run multiple conversions without overwriting
- 🧹 Clean workspace (no scattered CSV files)

---

## 📊 Output Format

Standardized CSV with columns:
- `ssid` - Network name
- `bssid` - MAC address
- `latitude` - GPS latitude
- `longitude` - GPS longitude
- `altitude` - Elevation
- `signal` - Signal strength (RSSI)
- `channel` - WiFi channel
- `encryption` - Security type (WPA2, WPA3, etc.)
- `type` - Network type
- `timestamp` - Detection time
- *Plus any additional fields from source file*

---

## 📦 Batch Processing

Convert entire folders full of wardriving files at once!

### Drag & Drop Folder:
1. **Drag your folder** onto `convert_folder.bat`
2. Choose mode:
   - **Separate files** - Each file gets its own CSV
   - **Merged** - Combine ALL files into one master CSV
   - **Recursive** - Include subfolders
3. Done! All files converted in seconds

### Command Line Options:

**Convert folder (separate files):**
```bash
python universal_wardrive_converter.py --folder ./my_wardrives
```
Output: `./my_wardrives/converted/file1_converted.csv`, `file2_converted.csv`, etc.

**Merge all files into one:**
```bash
python universal_wardrive_converter.py --folder ./my_wardrives --merge
```
Output: `./my_wardrives/converted/merged_all.csv` (contains ALL networks)

**Include subfolders:**
```bash
python universal_wardrive_converter.py --folder ./data --recursive
```

**Combine everything (subfolders + merge):**
```bash
python universal_wardrive_converter.py --folder ./data --recursive --merge
```

### Batch Features:
- ✅ Mix any file formats (KML + CSV + XML all together!)
- ✅ Auto-skips unsupported files
- ✅ Continues on errors (one bad file won't stop the batch)
- ✅ Progress tracking for each file
- ✅ Summary report at the end

---

## 📖 Usage Examples

### WiGLE Export:
```bash
python universal_wardrive_converter.py wigle_data.csv
```
Output: `wigle_data.csv` (overwrites with normalized format)

### Kismet NetXML:
```bash
python universal_wardrive_converter.py survey.netxml networks.csv
```
Output: `networks.csv`

### Any KML/KMZ:
```bash
python universal_wardrive_converter.py wardrive.kml
```
Output: `wardrive.csv`

### Text Format:
```bash
python universal_wardrive_converter.py netstumbler.txt output.csv
```
Output: `output.csv`

---

## 🔍 How It Works

1. **Auto-detects** file format (extension + content analysis)
2. **Parses** using format-specific parser
3. **Normalizes** data to standard schema
4. **Outputs** clean CSV with all fields

If format is unknown, falls back to **generic parser** that works with most text-based exports.

---

## 💡 Why Use This?

| Problem | Solution |
|---------|----------|
| "File too large" errors | **No size limit** |
| 100+ files to convert | **Batch folder processing** |
| Need combined dataset | **Merge all into one CSV** |
| Need to upload data | **100% offline** |
| Inconsistent CSV formats | **Standardized output** |
| Multiple tool exports | **One converter for all** |
| Missing fields | **Extracts everything** |
| Slow online tools | **Fast local processing** |

---

## 🧪 Testing

Test files included:
```bash
python universal_wardrive_converter.py test_sample.kml
python universal_wardrive_converter.py test_wigle.csv
python universal_wardrive_converter.py test_kismet.csv
```

All produce standardized CSV output.

---

## 📋 Requirements

- Python 3.x (no extra packages needed!)
- Uses only Python standard library

**Install Python:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Check "Add Python to PATH" during installation
3. Done!

---

## 🐛 Troubleshooting

**"Python not found"**
- Install Python from python.org
- Make sure "Add to PATH" was checked

**"No data extracted"**
- Check file has network data (open in text editor)
- Verify file isn't corrupted
- Try opening in source tool first

**Takes a long time**
- Normal for large files! Watch progress messages
- 10,000 networks ≈ 2-3 minutes
- 100,000 networks ≈ 15-20 minutes

**Wrong format detected**
- Some formats are ambiguous (CSV, TXT)
- Specify output manually: `script.py input.csv output.csv`
- Check [FORMATS_SUPPORTED.md](FORMATS_SUPPORTED.md) for details

---

## 📁 Files Included

**Windows:**
- **`CONVERT.bat`** - ⭐ Drag & drop launcher (Windows)

**Linux/Mac:**
- **`convert.sh`** - ⭐ Shell script launcher (Linux/Mac)

**All Platforms:**
- `universal_wardrive_converter.py` - Main converter engine (all formats)
- `QUICKSTART.md` - Platform-specific quick start guide
- `README.md` - Complete documentation (this file)
- `FORMATS_SUPPORTED.md` - Format specifications
- `conversion_vault/` - Auto-created output folder (timestamped)

---

## 🎓 Technical Details

### Format Detection:
1. File extension analysis
2. Header content inspection
3. Pattern matching (XML tags, CSV headers, etc.)
4. Fallback to generic parser

### Parsing Methods:
- **XML**: ElementTree with namespace handling
- **CSV**: DictReader with format-specific field mapping
- **Text**: Regex patterns for MAC/GPS/signal data
- **KMZ**: Zip extraction + KML parsing

### Performance:
- Streaming parsing for memory efficiency
- Progress updates every 1000 records
- No intermediate file creation

---

## 🆘 Support

**Have a format that doesn't work?**
1. Check [FORMATS_SUPPORTED.md](FORMATS_SUPPORTED.md)
2. Make sure file isn't corrupted
3. Try the generic text parser (works for most formats)
4. Provide sample file for format addition

**Common Issues:**
- Most text-based formats work automatically
- KML/XML formats are fully supported
- CSV formats need proper headers

---

## 🏆 Credits

Created for efficient conversion of large WiFi survey datasets.

**No more:**
- ❌ "File too large" errors
- ❌ Uploading sensitive data
- ❌ Format compatibility issues
- ❌ Slow online converters

**Universal solution for all wardriving data!**

---

## 📝 License

Free to use for WiFi security research, mapping, and analysis.
