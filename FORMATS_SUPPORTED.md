# Supported Wardriving File Formats

## Complete List of Supported Tools

✅ **FULLY IMPLEMENTED:**
- ✅ WiGLE WiFi Wardriving (.csv)
- ✅ Kismet (.csv, .xml, .netxml, .gpsxml)
- ✅ G-Mon (.kml, .txt)
- ✅ inSSIDer (.kml)
- ✅ Kismac (.kml, text)
- ✅ Wardrive-Android (.kml)
- ✅ WiFiFoFum (.kml, .kmz)
- ✅ WiFi-Where (.kml, .csv)

⚙️ **GENERIC PARSER (works for most):**
- ⚙️ DStumbler (text output)
- ⚙️ MacStumbler (text output)
- ⚙️ NetStumbler (text, summary)
- ⚙️ Pocket Warrior (text output)
- ⚙️ Any tab/comma/space-delimited text with SSID/BSSID/GPS data

🔧 **PLANNED ADDITIONS:**
- NetStumbler (.ns1 native format)
- MacStumbler (plist XML format)
- Kismac (.kismac native format)
- Wiscan format

---

## Format Details

### WiGLE WiFi Wardriving
**File Extensions:** `.csv`

**Sample Structure:**
```csv
# WiGLE WiFi Wardriving
MAC,SSID,AuthMode,FirstSeen,Channel,RSSI,CurrentLatitude,CurrentLongitude
AA:BB:CC:DD:EE:01,MyNetwork,WPA2,2024-11-07,6,-65,38.8977,-77.0365
```

**Fields Extracted:**
- MAC → bssid
- SSID → ssid
- AuthMode → encryption
- CurrentLatitude → latitude
- CurrentLongitude → longitude
- RSSI → signal
- Channel → channel
- FirstSeen/LastSeen → timestamp

---

### Kismet

#### CSV Format (.csv)
**Sample Structure:**
```csv
Network,ESSID,BSSID,Channel,Encryption,MaxRate,GPSBestLat,GPSBestLon
1,MyNetwork,AA:BB:CC:DD:EE:01,6,WPA2,54.0,38.8977,-77.0365
```

**Fields Extracted:**
- ESSID → ssid
- BSSID → bssid
- GPSBestLat/GPSMinLat → latitude
- GPSBestLon/GPSMinLon → longitude
- Channel → channel
- Encryption/Crypt → encryption
- BestSignal → signal

#### NetXML Format (.netxml, .xml)
**Sample Structure:**
```xml
<wireless-network>
  <SSID><essid>MyNetwork</essid></SSID>
  <BSSID>AA:BB:CC:DD:EE:01</BSSID>
  <channel>6</channel>
  <encryption>WPA2</encryption>
  <gps-info>
    <avg-lat>38.8977</avg-lat>
    <avg-lon>-77.0365</avg-lon>
  </gps-info>
</wireless-network>
```

**Fields Extracted:**
- Full XML parsing with GPS coordinates
- Signal strength, encryption, channel data
- Multiple SSID support

---

### KML-Based Formats

**Used by:** G-Mon, inSSIDer, Kismac, Wardrive-Android, WiFiFoFum, WiFi-Where

**File Extensions:** `.kml`, `.kmz`

**Sample Structure:**
```xml
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Placemark>
    <name>MyNetwork</name>
    <description>
      SSID: MyNetwork
      BSSID: AA:BB:CC:DD:EE:01
      Channel: 6
      Signal Strength: -65 dBm
    </description>
    <Point>
      <coordinates>-77.0365,38.8977,50.0</coordinates>
    </Point>
  </Placemark>
</kml>
```

**Fields Extracted:**
- name → ssid (fallback)
- Description parsed for SSID, BSSID, signal, channel, encryption
- coordinates → longitude, latitude, altitude
- Extended data fields

---

### Text-Based Formats

**Used by:** DStumbler, MacStumbler, NetStumbler, Pocket Warrior, G-Mon

**File Extensions:** `.txt`

**Supported Formats:**
- Tab-delimited
- Comma-delimited (without quotes)
- Space-delimited
- Mixed formats

**Auto-Detection:**
- MAC address patterns (AA:BB:CC:DD:EE:FF)
- GPS coordinate patterns (-90 to 90, -180 to 180)
- Signal strength patterns (negative dBm values)
- Channel numbers (1-165)

**Example:**
```
AA:BB:CC:DD:EE:01    MyNetwork    -65    6    WPA2    38.8977    -77.0365
```

---

## Output Format (Standardized CSV)

All conversions produce a **standardized CSV** with these columns (in order):

### Standard Fields (always present):
1. **ssid** - Network name/ESSID
2. **bssid** - MAC address
3. **latitude** - GPS latitude
4. **longitude** - GPS longitude
5. **altitude** - Elevation in meters
6. **signal** - Signal strength (RSSI in dBm)
7. **channel** - WiFi channel (1-165)
8. **encryption** - Security type (WPA2, WPA3, etc.)
9. **type** - Network type (802.11ac, WIFI, etc.)
10. **timestamp** - First/last seen time

### Additional Fields:
Any extra fields from the source file are preserved and added as additional columns.

---

## Usage Examples

### Convert WiGLE CSV:
```bash
python universal_wardrive_converter.py wigle_export.csv
```

### Convert Kismet NetXML:
```bash
python universal_wardrive_converter.py kismet_survey.netxml
```

### Convert any KML:
```bash
python universal_wardrive_converter.py wardrive_data.kml output.csv
```

### Convert text format:
```bash
python universal_wardrive_converter.py netstumbler_export.txt
```

---

## Auto-Detection

The converter automatically detects the format based on:
1. **File extension** (.kml, .csv, .xml, etc.)
2. **File header** (XML tags, CSV headers, etc.)
3. **Content patterns** (MAC addresses, GPS coordinates)

If the format can't be determined, it falls back to a **generic text parser** that attempts to extract common WiFi survey fields.

---

## Large File Support

- ✅ No size limits (unlike online converters)
- ✅ Progress indicators every 1000 records
- ✅ Memory-efficient streaming parsing
- ✅ Handles files with 100,000+ networks

---

## Format Request

Missing a format? Let me know:
- Tool name
- Sample export file
- Documentation/field descriptions

Most text-based formats already work with the generic parser!

---

## Testing

Test files included:
- `test_sample.kml` - KML format test
- `test_wigle.csv` - WiGLE CSV test
- `test_kismet.csv` - Kismet CSV test

Run tests:
```bash
python universal_wardrive_converter.py test_sample.kml
python universal_wardrive_converter.py test_wigle.csv
python universal_wardrive_converter.py test_kismet.csv
```
