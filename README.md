# 🎨 Image2Melody

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![macOS](https://img.shields.io/badge/macOS-Compatible-silver.svg)

**Transform images into 8-bit melodies with Mac OS Classic aesthetics and glitch art effects**

*将图片转换为 8-bit 风格的音乐旋律！基于 HSV 色彩空间，结合 Mac OS Classic 1-bit 美学和 glitch art 动画效果。*

<!-- 📸 Add your demo media here! -->
<!-- ![Main Interface](docs/images/interface.png) -->
<!-- ![Load Image Demo](docs/images/demo.gif) -->
<!-- ![Camera Mode](docs/images/camera_mode.gif) -->

[Quick Start](#-quick-start) • [Features](#-features) • [How to Use](#-how-to-use) • [Documentation](#-documentation)

</div>

---

## ✨ Features

### 🎨 Visual Effects
- **Mac OS Classic UI** - Retro pink borders and beige buttons inspired by vintage Mac OS
- **1-bit Pixelation** - 10×10 pixel blocks with Floyd-Steinberg dithering patterns
- **Glitch Art Animation** - RGB channel separation, scanline corruption, pixel displacement
- **Progressive Data Moshing** - Dynamic glitch intensity that follows a curve (0% → 21% → 0%)
- **Fade Trail Effects** - Gradually fading visual traces with transparency

### 🎵 Music Generation
- **Dual-Track System** - Visual track (1-bit style) + Audio track (original HSV data)
- **HSV Color Mapping**:
  - **Hue** → Pitch (musical note from pentatonic scale)
  - **Saturation** → Velocity (volume/intensity)
  - **Value** → Duration + Octave selection
- **Real-time Playback** - 8-bit square wave synthesis via pygame
- **MIDI Export** - Standard .mid format compatible with all DAWs

### ⌨️ Interactive Controls
- **Pitch Control**: `W`/`S` (±12 semitones/octave), `A`/`D` (±1 semitone)
- **Speed Control**: `↑↓` (±0.2x), `←→` (±0.1x fine tune), `R` (reset)
- **Playback Control**: `Space` (pause/resume), `ESC` (back to menu)
- **Live Display**: Real-time speed and pitch indicators in status bar
- **Auto-Reset**: Speed and pitch automatically reset after completion

---

## 🚀 Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Melos47/image2melody.git
cd image2melody

# 2. Install Python with tkinter support (macOS)
brew install python-tk@3.12

# 3. Create virtual environment and install dependencies
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application

**Method 1: Using the run script (Recommended)**

```bash
./run.sh
```

**Method 2: Manual launch**

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

---

## 🎮 How to Use

### Basic Workflow

1. **Load Image** - Click `LOAD IMAGE` button
2. **Start Animation** - Click `START ANIMATION`
3. **Live Control** - Use keyboard shortcuts to adjust pitch and speed
4. **Save Work** - Click `SAVE MIDI` to export

### Keyboard Shortcuts

| Key      | Function         | Description                  |
|----------|------------------|------------------------------|
| `W`      | Pitch Up         | +12 semitones (octave)       |
| `S`      | Pitch Down       | -12 semitones (octave)       |
| `A`      | Semitone Down    | -1 semitone                  |
| `D`      | Semitone Up      | +1 semitone                  |
| `↑`      | Speed Up         | +0.2x multiplier             |
| `↓`      | Slow Down        | -0.2x multiplier             |
| `←`      | Fine Slow        | -0.1x multiplier             |
| `→`      | Fine Fast        | +0.1x multiplier             |
| `R`      | Reset Speed      | Back to 1.0x                 |
| `Space`  | Pause/Resume     | Toggle playback              |

---

## 📂 Project Structure

```
image2melody/
├── main.py                 # Main program - GUI & animation control
├── melody_generator.py     # Melody generation - HSV to MIDI
├── image_processor.py      # Image processing - pixelation & sampling
├── requirements.txt        # Python dependencies
├── run.sh                  # Launch script
├── README.md               # This file
├── QUICKSTART.md           # Quick start guide
├── COMPLETE_GUIDE.md       # Detailed user manual
├── Jersey10-Regular.ttf    # Pixel font
└── docs/                   # Technical documentation
    ├── README.md
    ├── 8BIT_MELODY_GUIDE.md
    ├── DITHERING_AND_MOSHING_GUIDE.md
    ├── DUAL_TRACK_SYSTEM.md
    ├── EXPORT_GUIDE.md
    ├── HSV_MELODY_GUIDE.md
    ├── LIVE_PERFORMANCE_GUIDE.md
    ├── MAC_OS_CLASSIC_STYLE.md
    ├── PIXELATION_GUIDE.md
    ├── REAL_TIME_AUDIO_GUIDE.md
    ├── TESTING_GUIDE.md
    └── VISUAL_FLOW_DIAGRAM.md
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Melos47**

- GitHub: [@Melos47](https://github.com/Melos47)
- Project: [image2melody](https://github.com/Melos47/image2melody)

---

## 🙏 Acknowledgments

- **Python** - Programming language
- **tkinter** - GUI framework
- **Pillow** - Image processing library
- **pygame** - Multimedia library
- **MIDIUtil** - MIDI generation library
- **Jersey 10** - Pixel font
- **fauux.neocities.org** - Glitch art inspiration

---

<div align="center">

**🎨 Transform Visual Art into Musical Art 🎵**

Made with ❤️ by Melos47

</div>

