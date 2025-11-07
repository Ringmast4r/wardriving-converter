# Universal Wardriving Converter - Quick Start

## 🚀 Platform-Specific Instructions

### Windows 🪟

**Method 1: Drag & Drop (Easiest)**
1. Drag files/folders onto `CONVERT.bat`
2. Choose your option (1, 2, or 3)
3. Done! Check `conversion_vault` folder

**Method 2: Desktop Shortcut**
1. Right-click `CONVERT.bat` → Send To → Desktop
2. Drag files onto the desktop shortcut
3. Done!

**Method 3: Command Line**
```cmd
cd C:\path\to\kml-converter
CONVERT.bat "C:\path\to\your\files"
```

---

### Linux/Mac 🐧🍎

**Method 1: Command Line**
```bash
cd /path/to/kml-converter
./convert.sh /path/to/your/files
```

**Method 2: Make it System-Wide**
```bash
# Make executable (first time only)
chmod +x convert.sh

# Create symlink (optional)
sudo ln -s $(pwd)/convert.sh /usr/local/bin/wardrive-convert

# Now use from anywhere:
wardrive-convert ~/Downloads/wardriving_data/
```

**Method 3: Direct Python**
```bash
python3 universal_wardrive_converter.py yourfile.csv
python3 universal_wardrive_converter.py --folder ./data --merge
```

---

## 📋 What You Can Convert

✅ **Single File**
```bash
# Windows
CONVERT.bat "C:\data\scan.kml"

# Linux/Mac
./convert.sh ~/data/scan.kml
```

✅ **Multiple Files in Folder**
```bash
# Windows
CONVERT.bat "C:\data\scans\"
# Choose option 2 (merge)

# Linux/Mac
./convert.sh ~/data/scans/
# Choose option 2 (merge)
```

✅ **Folder with Subfolders**
```bash
# Windows
CONVERT.bat "C:\data\"
# Choose option 3 (recursive + merge)

# Linux/Mac
./convert.sh ~/data/
# Choose option 3 (recursive + merge)
```

---

## 📦 Output Location

All conversions are saved in timestamped folders:

```
kml-converter/
└── conversion_vault/
    ├── 20241107_093015/
    │   └── MERGED_ALL.csv
    ├── 20241107_143022/
    │   ├── file1_converted.csv
    │   ├── file2_converted.csv
    │   └── file3_converted.csv
    └── 20241107_201545/
        └── MERGED_ALL.csv
```

---

## 🎯 Supported Formats

- **KML/KMZ** (.kml, .kmz)
- **WiGLE WiFi** (.csv)
- **Kismet** (.csv, .xml, .netxml, .gpsxml)
- **Generic Text** (.txt)
- And 12+ more formats!

See `FORMATS_SUPPORTED.md` for complete list.

---

## 💡 Examples

### Example 1: Convert Large KML File
```bash
# Windows
CONVERT.bat "large_survey.kml"

# Linux/Mac
./convert.sh large_survey.kml
```

### Example 2: Merge 50 Different Format Files
```bash
# Windows
CONVERT.bat "C:\scans\2024\"
# Choose option 2

# Linux/Mac
./convert.sh ~/scans/2024/
# Choose option 2
```

### Example 3: Recursive Merge of Everything
```bash
# Windows
CONVERT.bat "C:\all_surveys\"
# Choose option 3

# Linux/Mac
./convert.sh ~/all_surveys/
# Choose option 3
```

---

## 🛠️ Troubleshooting

**Windows: "Python not found"**
- Install from: https://python.org/downloads/
- Check "Add Python to PATH" during install

**Linux: "python3: command not found"**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3

# Fedora/RHEL
sudo dnf install python3

# Arch
sudo pacman -S python
```

**Mac: "python3: command not found"**
```bash
# Install Homebrew first (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Permission denied (Linux/Mac)**
```bash
chmod +x convert.sh
```

---

## 📊 Output Format

All files converted to standardized CSV with columns:
- `ssid` - Network name
- `bssid` - MAC address
- `latitude`, `longitude`, `altitude` - GPS coordinates
- `signal` - Signal strength (dBm)
- `channel` - WiFi channel
- `encryption` - Security type (WPA2, WPA3, etc.)
- `timestamp` - Detection time

---

## ⚡ Features

✅ No size limits (handles 100MB+ files)
✅ Batch processing (convert 100+ files at once)
✅ Auto-format detection
✅ 100% offline (no internet needed)
✅ Timestamped outputs (never lose work)
✅ Cross-platform (Windows/Linux/Mac)

---

## 🆘 Need Help?

Check these files:
- `README.md` - Full documentation
- `FORMATS_SUPPORTED.md` - Format specifications
- `HOW_TO_USE.txt` - Visual guide (Windows)

---

**That's it! Drag, drop, convert. Simple.** 🚀
