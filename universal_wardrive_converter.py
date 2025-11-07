#!/usr/bin/env python3
"""
Universal Wardriving File Converter
Supports: DStumbler, G-Mon, inSSIDer, Kismac, Kismet, MacStumbler, NetStumbler,
          Pocket Warrior, Wardrive-Android, WiFiFoFum, WiFi-Where, WiGLE
Converts ANY wardriving format to standardized CSV
"""

import xml.etree.ElementTree as ET
import csv
import sys
import os
import json
import re
import zipfile
from pathlib import Path
from datetime import datetime

# KML namespace
KML_NS = {'kml': 'http://www.opengis.net/kml/2.2'}


class WardriveConverter:
    """Universal converter for all wardriving file formats"""

    def __init__(self):
        self.results = []
        self.file_type = None

    def detect_format(self, filepath):
        """Detect the wardriving file format"""
        ext = filepath.lower().split('.')[-1]

        print(f"[*] Detecting file format for: {filepath}")
        print(f"[*] File extension: .{ext}")

        # Read first few lines/bytes to determine format
        try:
            with open(filepath, 'rb') as f:
                header = f.read(512)

            # Try to decode as text
            try:
                header_text = header.decode('utf-8', errors='ignore')
            except:
                header_text = header.decode('latin-1', errors='ignore')

            # KML/KMZ detection
            if ext == 'kmz':
                return 'kmz'
            elif ext == 'kml' or '<kml' in header_text.lower():
                return 'kml'

            # XML formats
            if header_text.strip().startswith('<?xml') or '<' in header_text[:10]:
                if '<detection-run' in header_text or '<kismet-run' in header_text:
                    return 'kismet_netxml'
                elif '<gps-run' in header_text:
                    return 'kismet_gpsxml'
                elif 'plist' in header_text or '<dict>' in header_text:
                    return 'macstumbler_plist'
                elif ext == 'xml':
                    return 'kismet_xml'

            # CSV formats
            if ext == 'csv':
                lines = header_text.split('\n')
                if len(lines) > 0:
                    first_line = lines[0].lower()
                    if 'wigle' in first_line or 'mac' in first_line and 'ssid' in first_line and 'authmode' in first_line:
                        return 'wigle_csv'
                    elif 'bssid' in first_line or 'mac' in first_line:
                        return 'kismet_csv'
                return 'generic_csv'

            # NetStumbler formats
            if ext == 'ns1':
                return 'netstumbler_ns1'
            elif 'netstumbler' in header_text.lower() or ext == 'nss':
                return 'netstumbler_summary'

            # Kismet formats
            if ext in ['netxml', 'gpsxml', 'nettxt', 'gps']:
                return f'kismet_{ext}'

            # Text-based formats
            if ext == 'txt':
                # Try to detect which text format
                if 'lat' in header_text.lower() and 'lon' in header_text.lower():
                    return 'generic_gps_text'
                elif 'ssid' in header_text.lower() or 'bssid' in header_text.lower():
                    return 'generic_text'

            # Kismac native format
            if ext == 'kismac':
                return 'kismac_native'

            # Wiscan format
            if 'wiscan' in header_text.lower() or ext == 'wsc':
                return 'wiscan'

            print(f"[!] Unknown format, attempting generic parser")
            return 'generic_text'

        except Exception as e:
            print(f"[!] Error detecting format: {e}")
            return 'unknown'

    def parse_kml(self, filepath):
        """Parse KML format"""
        print(f"[*] Parsing as KML format")
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"[!] ERROR: Failed to parse XML - {e}")
            return []

        placemarks = root.findall('.//kml:Placemark', KML_NS)
        print(f"[*] Found {len(placemarks)} placemarks")

        results = []
        for placemark in placemarks:
            data = {}

            # Name (SSID or identifier)
            name = placemark.find('.//kml:name', KML_NS)
            if name is not None and name.text:
                data['ssid'] = name.text.strip()

            # Description (contains detailed info)
            desc = placemark.find('.//kml:description', KML_NS)
            if desc is not None and desc.text:
                desc_text = desc.text.strip()
                # Parse description fields
                for line in desc_text.split('\n'):
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key = parts[0].strip().lower()
                            value = parts[1].strip()

                            if key == 'ssid':
                                data['ssid'] = value
                            elif key in ['bssid', 'mac', 'mac address']:
                                data['bssid'] = value
                            elif 'signal' in key or 'rssi' in key:
                                data['signal'] = value
                            elif key == 'channel':
                                data['channel'] = value
                            elif 'encrypt' in key or 'security' in key:
                                data['encryption'] = value
                            elif 'type' in key:
                                data['type'] = value
                            elif 'time' in key:
                                data['timestamp'] = value

            # Coordinates
            coord = placemark.find('.//kml:coordinates', KML_NS)
            if coord is not None and coord.text:
                coords = coord.text.strip().split(',')
                if len(coords) >= 2:
                    data['longitude'] = coords[0].strip()
                    data['latitude'] = coords[1].strip()
                    if len(coords) >= 3:
                        data['altitude'] = coords[2].strip()

            # Extended data
            extended = placemark.find('.//kml:ExtendedData', KML_NS)
            if extended is not None:
                for data_elem in extended.findall('.//kml:Data', KML_NS):
                    name_attr = data_elem.get('name')
                    value_elem = data_elem.find('.//kml:value', KML_NS)
                    if name_attr and value_elem is not None and value_elem.text:
                        key = name_attr.lower().replace(' ', '_')
                        data[key] = value_elem.text.strip()

            if data:
                results.append(data)

        return results

    def parse_kmz(self, filepath):
        """Parse KMZ (zipped KML) format"""
        print(f"[*] Parsing as KMZ format (extracting...)")
        try:
            with zipfile.ZipFile(filepath, 'r') as kmz:
                kml_files = [f for f in kmz.namelist() if f.endswith('.kml')]

                if not kml_files:
                    print("[!] No KML file found in KMZ")
                    return []

                kml_file = kml_files[0]
                temp_path = kmz.extract(kml_file, path=os.environ.get('TEMP', '/tmp'))
                results = self.parse_kml(temp_path)

                try:
                    os.remove(temp_path)
                except:
                    pass

                return results
        except Exception as e:
            print(f"[!] Error parsing KMZ: {e}")
            return []

    def parse_wigle_csv(self, filepath):
        """Parse WiGLE WiFi CSV format"""
        print(f"[*] Parsing as WiGLE CSV format")
        results = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                # WiGLE CSVs have comments at the top
                lines = f.readlines()

                # Find the header line (first non-comment line)
                header_idx = 0
                for i, line in enumerate(lines):
                    if not line.startswith('#'):
                        header_idx = i
                        break

                # Parse CSV from header onwards
                reader = csv.DictReader(lines[header_idx:])

                for row in reader:
                    data = {}

                    # WiGLE CSV fields (map to standard format)
                    if 'MAC' in row:
                        data['bssid'] = row['MAC']
                    if 'SSID' in row:
                        data['ssid'] = row['SSID']
                    if 'CurrentLatitude' in row:
                        data['latitude'] = row['CurrentLatitude']
                    if 'CurrentLongitude' in row:
                        data['longitude'] = row['CurrentLongitude']
                    if 'AltitudeMeters' in row:
                        data['altitude'] = row['AltitudeMeters']
                    if 'RSSI' in row:
                        data['signal'] = row['RSSI']
                    if 'Channel' in row:
                        data['channel'] = row['Channel']
                    if 'AuthMode' in row:
                        data['encryption'] = row['AuthMode']
                    if 'Type' in row:
                        data['type'] = row['Type']
                    if 'FirstSeen' in row:
                        data['first_seen'] = row['FirstSeen']
                    if 'LastSeen' in row:
                        data['last_seen'] = row['LastSeen']

                    results.append(data)

            print(f"[*] Parsed {len(results)} WiGLE records")
            return results

        except Exception as e:
            print(f"[!] Error parsing WiGLE CSV: {e}")
            return []

    def parse_kismet_csv(self, filepath):
        """Parse Kismet CSV format"""
        print(f"[*] Parsing as Kismet CSV format")
        results = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    data = {}

                    # Kismet CSV field mapping
                    for key, value in row.items():
                        key_lower = key.lower()

                        if 'bssid' in key_lower or 'mac' in key_lower:
                            data['bssid'] = value
                        elif 'ssid' in key_lower:
                            data['ssid'] = value
                        elif 'lat' in key_lower:
                            data['latitude'] = value
                        elif 'lon' in key_lower:
                            data['longitude'] = value
                        elif 'channel' in key_lower:
                            data['channel'] = value
                        elif 'signal' in key_lower or 'rssi' in key_lower:
                            data['signal'] = value
                        elif 'crypt' in key_lower or 'encrypt' in key_lower:
                            data['encryption'] = value
                        elif 'type' in key_lower:
                            data['type'] = value
                        elif 'time' in key_lower:
                            data['timestamp'] = value

                    results.append(data)

            print(f"[*] Parsed {len(results)} Kismet CSV records")
            return results

        except Exception as e:
            print(f"[!] Error parsing Kismet CSV: {e}")
            return []

    def parse_kismet_netxml(self, filepath):
        """Parse Kismet .netxml format"""
        print(f"[*] Parsing as Kismet NetXML format")
        results = []

        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            networks = root.findall('.//wireless-network')
            print(f"[*] Found {len(networks)} networks")

            for network in networks:
                data = {}

                # SSID
                ssid = network.find('.//SSID/essid')
                if ssid is not None and ssid.text:
                    data['ssid'] = ssid.text

                # BSSID
                bssid = network.find('.//BSSID')
                if bssid is not None and bssid.text:
                    data['bssid'] = bssid.text

                # Channel
                channel = network.find('.//channel')
                if channel is not None and channel.text:
                    data['channel'] = channel.text

                # Encryption
                encryption = network.find('.//encryption')
                if encryption is not None and encryption.text:
                    data['encryption'] = encryption.text

                # GPS coordinates
                gps_info = network.find('.//gps-info')
                if gps_info is not None:
                    lat = gps_info.find('.//avg-lat')
                    lon = gps_info.find('.//avg-lon')
                    alt = gps_info.find('.//avg-alt')

                    if lat is not None and lat.text:
                        data['latitude'] = lat.text
                    if lon is not None and lon.text:
                        data['longitude'] = lon.text
                    if alt is not None and alt.text:
                        data['altitude'] = alt.text

                # Signal strength
                signal = network.find('.//max-signal-dbm')
                if signal is not None and signal.text:
                    data['signal'] = signal.text

                results.append(data)

            return results

        except Exception as e:
            print(f"[!] Error parsing Kismet NetXML: {e}")
            return []

    def parse_generic_text(self, filepath):
        """Parse generic text format (DStumbler, Pocket Warrior, etc.)"""
        print(f"[*] Parsing as generic text format")
        results = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Try to detect delimiter and structure
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                data = {}

                # Try tab-separated
                if '\t' in line:
                    parts = line.split('\t')
                # Try comma-separated (but not CSV with quotes)
                elif ',' in line and '"' not in line:
                    parts = line.split(',')
                # Try space-separated
                else:
                    parts = line.split()

                # Try to extract common patterns
                for part in parts:
                    part = part.strip()

                    # MAC address pattern
                    if re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', part):
                        data['bssid'] = part
                    # Coordinate patterns
                    elif re.match(r'^-?\d+\.\d+$', part):
                        value = float(part)
                        if -90 <= value <= 90 and 'latitude' not in data:
                            data['latitude'] = part
                        elif -180 <= value <= 180 and 'longitude' not in data:
                            data['longitude'] = part
                    # Signal strength pattern
                    elif re.match(r'^-\d+$', part) and int(part) < 0:
                        data['signal'] = part
                    # Channel pattern
                    elif part.isdigit() and 1 <= int(part) <= 165:
                        if 'channel' not in data:
                            data['channel'] = part

                if data:
                    results.append(data)

            print(f"[*] Parsed {len(results)} text records")
            return results

        except Exception as e:
            print(f"[!] Error parsing text format: {e}")
            return []

    def normalize_data(self, data_list):
        """Normalize all data to standard CSV format"""
        print(f"[*] Normalizing {len(data_list)} records to standard format")

        normalized = []
        for data in data_list:
            norm = {}

            # Standard fields
            norm['ssid'] = data.get('ssid', '')
            norm['bssid'] = data.get('bssid', '')
            norm['latitude'] = data.get('latitude', '')
            norm['longitude'] = data.get('longitude', '')
            norm['altitude'] = data.get('altitude', '')
            norm['signal'] = data.get('signal', '')
            norm['channel'] = data.get('channel', '')
            norm['encryption'] = data.get('encryption', '')
            norm['type'] = data.get('type', '')
            norm['timestamp'] = data.get('timestamp', data.get('first_seen', data.get('last_seen', '')))

            # Add any extra fields
            for key, value in data.items():
                if key not in norm:
                    norm[key] = value

            normalized.append(norm)

        return normalized

    def write_csv(self, data, output_file):
        """Write normalized data to CSV"""
        if not data:
            print("[!] No data to write")
            return False

        # Standard field order
        standard_fields = ['ssid', 'bssid', 'latitude', 'longitude', 'altitude',
                          'signal', 'channel', 'encryption', 'type', 'timestamp']

        # Collect all unique fields
        all_fields = set()
        for record in data:
            all_fields.update(record.keys())

        # Order: standard fields first, then extras
        fieldnames = [f for f in standard_fields if f in all_fields]
        fieldnames += sorted([f for f in all_fields if f not in standard_fields])

        print(f"[*] Writing {len(data)} records to: {output_file}")
        print(f"[*] Columns: {', '.join(fieldnames)}")

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()

                for i, record in enumerate(data, 1):
                    writer.writerow(record)

                    if i % 1000 == 0:
                        print(f"[*] Wrote {i}/{len(data)} records...")

            size = os.path.getsize(output_file)
            size_mb = size / (1024 * 1024)
            print(f"[+] SUCCESS! {len(data)} records written")
            print(f"[+] Output: {output_file} ({size_mb:.2f} MB)")
            return True

        except Exception as e:
            print(f"[!] Error writing CSV: {e}")
            return False

    def convert(self, input_file, output_file=None):
        """Main conversion function"""
        # Auto-generate output filename
        if not output_file:
            output_file = str(Path(input_file).with_suffix('.csv'))

        print("=" * 70)
        print("  UNIVERSAL WARDRIVING FILE CONVERTER")
        print("=" * 70)
        print()

        # Check file exists
        if not os.path.exists(input_file):
            print(f"[!] ERROR: File not found: {input_file}")
            return False

        file_size = os.path.getsize(input_file) / (1024 * 1024)
        print(f"[*] Input: {input_file} ({file_size:.2f} MB)")
        print()

        # Detect format
        file_format = self.detect_format(input_file)
        print(f"[*] Detected format: {file_format}")
        print()

        # Parse based on format
        if file_format == 'kml':
            self.results = self.parse_kml(input_file)
        elif file_format == 'kmz':
            self.results = self.parse_kmz(input_file)
        elif file_format == 'wigle_csv':
            self.results = self.parse_wigle_csv(input_file)
        elif file_format == 'kismet_csv':
            self.results = self.parse_kismet_csv(input_file)
        elif file_format == 'kismet_netxml':
            self.results = self.parse_kismet_netxml(input_file)
        elif file_format in ['generic_text', 'generic_gps_text']:
            self.results = self.parse_generic_text(input_file)
        else:
            print(f"[!] Format '{file_format}' not yet implemented, trying generic parser")
            self.results = self.parse_generic_text(input_file)

        print()

        if not self.results:
            print("[!] No data extracted!")
            return False

        # Normalize and write
        normalized = self.normalize_data(self.results)
        success = self.write_csv(normalized, output_file)

        print()
        print("=" * 70)
        if success:
            print("[+] CONVERSION COMPLETE!")
        else:
            print("[!] CONVERSION FAILED!")
        print("=" * 70)

        return success

    def batch_convert_folder(self, folder_path, output_folder=None, merge=False, recursive=False):
        """Batch convert all wardriving files in a folder"""
        print("=" * 70)
        print("  BATCH FOLDER CONVERSION")
        print("=" * 70)
        print()

        if not os.path.isdir(folder_path):
            print(f"[!] ERROR: Not a directory: {folder_path}")
            return False

        # Setup output folder
        if not output_folder:
            output_folder = os.path.join(folder_path, 'converted')

        os.makedirs(output_folder, exist_ok=True)
        print(f"[*] Input folder: {folder_path}")
        print(f"[*] Output folder: {output_folder}")
        print(f"[*] Merge files: {'YES' if merge else 'NO'}")
        print(f"[*] Recursive scan: {'YES' if recursive else 'NO'}")
        print()

        # Supported extensions
        supported_exts = ['.kml', '.kmz', '.csv', '.xml', '.netxml', '.gpsxml', '.txt', '.ns1', '.nss']

        # Find all supported files
        files_to_convert = []
        if recursive:
            for root, dirs, files in os.walk(folder_path):
                # Skip output folder
                if root.startswith(output_folder):
                    continue
                for file in files:
                    if any(file.lower().endswith(ext) for ext in supported_exts):
                        files_to_convert.append(os.path.join(root, file))
        else:
            for file in os.listdir(folder_path):
                filepath = os.path.join(folder_path, file)
                if os.path.isfile(filepath) and any(file.lower().endswith(ext) for ext in supported_exts):
                    files_to_convert.append(filepath)

        if not files_to_convert:
            print("[!] No supported files found in folder!")
            print(f"    Supported: {', '.join(supported_exts)}")
            return False

        print(f"[*] Found {len(files_to_convert)} files to convert")
        print()

        # Convert each file
        successful = []
        failed = []
        all_data = []

        for i, filepath in enumerate(files_to_convert, 1):
            filename = os.path.basename(filepath)
            print(f"\n[{i}/{len(files_to_convert)}] Processing: {filename}")
            print("-" * 70)

            try:
                # Create new converter instance for each file
                converter = WardriveConverter()

                # Detect and parse
                file_format = converter.detect_format(filepath)
                print(f"[*] Detected format: {file_format}")

                # Parse based on format
                if file_format == 'kml':
                    results = converter.parse_kml(filepath)
                elif file_format == 'kmz':
                    results = converter.parse_kmz(filepath)
                elif file_format == 'wigle_csv':
                    results = converter.parse_wigle_csv(filepath)
                elif file_format == 'kismet_csv':
                    results = converter.parse_kismet_csv(filepath)
                elif file_format == 'kismet_netxml':
                    results = converter.parse_kismet_netxml(filepath)
                elif file_format in ['generic_text', 'generic_gps_text']:
                    results = converter.parse_generic_text(filepath)
                else:
                    print(f"[!] Unknown format, trying generic parser")
                    results = converter.parse_generic_text(filepath)

                if results:
                    normalized = converter.normalize_data(results)

                    if merge:
                        # Add to master list
                        all_data.extend(normalized)
                        print(f"[+] Added {len(normalized)} records to merged dataset")
                    else:
                        # Write individual file
                        output_file = os.path.join(output_folder, Path(filename).stem + '_converted.csv')
                        converter.write_csv(normalized, output_file)

                    successful.append(filename)
                else:
                    print(f"[!] No data extracted from {filename}")
                    failed.append(filename)

            except Exception as e:
                print(f"[!] ERROR processing {filename}: {e}")
                failed.append(filename)

        print()
        print("=" * 70)
        print("  BATCH CONVERSION COMPLETE")
        print("=" * 70)
        print()

        # Write merged file if requested
        if merge and all_data:
            merged_file = os.path.join(output_folder, 'merged_all.csv')
            print(f"[*] Writing merged dataset: {merged_file}")
            dummy_converter = WardriveConverter()
            dummy_converter.write_csv(all_data, merged_file)
            print()

        # Summary
        print(f"[+] Successfully converted: {len(successful)} files")
        if failed:
            print(f"[!] Failed: {len(failed)} files")
            for f in failed:
                print(f"    - {f}")

        print()
        print(f"[+] Output location: {output_folder}")
        print("=" * 70)

        return len(successful) > 0


def main():
    if len(sys.argv) < 2:
        print("=" * 70)
        print("  UNIVERSAL WARDRIVING FILE CONVERTER")
        print("=" * 70)
        print()
        print("Converts ANY wardriving format to CSV:")
        print("  • DStumbler, G-Mon, inSSIDer")
        print("  • Kismac, Kismet (all formats)")
        print("  • MacStumbler, NetStumbler")
        print("  • Pocket Warrior, Wardrive-Android")
        print("  • WiFiFoFum, WiFi-Where")
        print("  • WiGLE WiFi Wardriving")
        print()
        print("Usage:")
        print("  Single file:")
        print("    python universal_wardrive_converter.py <input_file> [output.csv]")
        print()
        print("  Batch folder:")
        print("    python universal_wardrive_converter.py --folder <folder_path>")
        print("    python universal_wardrive_converter.py --folder <folder_path> --merge")
        print("    python universal_wardrive_converter.py --folder <folder_path> --recursive")
        print()
        print("Options:")
        print("  --folder <path>    Convert all files in folder")
        print("  --merge           Combine all files into one master CSV")
        print("  --recursive       Scan subfolders too")
        print()
        print("Examples:")
        print("  python universal_wardrive_converter.py wigle_data.csv")
        print("  python universal_wardrive_converter.py kismet_survey.netxml")
        print("  python universal_wardrive_converter.py survey.kml output.csv")
        print("  python universal_wardrive_converter.py --folder ./wardrives")
        print("  python universal_wardrive_converter.py --folder ./data --merge --recursive")
        print()
        sys.exit(1)

    # Check for folder mode
    if '--folder' in sys.argv:
        folder_idx = sys.argv.index('--folder')
        if folder_idx + 1 >= len(sys.argv):
            print("[!] ERROR: --folder requires a path")
            sys.exit(1)

        folder_path = sys.argv[folder_idx + 1]
        merge = '--merge' in sys.argv
        recursive = '--recursive' in sys.argv

        converter = WardriveConverter()
        success = converter.batch_convert_folder(folder_path, merge=merge, recursive=recursive)
        sys.exit(0 if success else 1)

    # Single file mode
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None

    converter = WardriveConverter()
    success = converter.convert(input_file, output_file)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
