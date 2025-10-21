# Mac OS Classic 1-Bit Dithering Style Guide

## Overview
The Image2Melody application has been redesigned with a complete Mac OS Classic 1-bit dithering aesthetic, inspired by vintage Macintosh applications like Scrapbook.

## Color Scheme

### Primary Colors
- **Background Black**: `#010101` - Main background color
- **Primary Pink**: `#C87488` (r:200 g:116 b:136) - Borders, title bar, and text
- **Hover Beige**: `#CDBEB8` (r:205 g:190 b:184) - Selection, hover states, and buttons

### Color Usage
```python
self.bg_black = "#010101"        # Background
self.primary_pink = "#C87488"    # Borders/text/title bar
self.hover_beige = "#CDBEB8"     # Hover/selection/buttons
```

## UI Components

### 1. Title Bar (Mac OS Classic Striped Style)
- Height: 32px
- Background: Pink (#C87488) with vertical black stripes (every 2px)
- Title: "Scrapbook - Image2Melody"
- Font: Jersey 10 (pixel font), medium size
- Text Color: Black (#010101)

### 2. Control Bar
- Background: Beige (#CDBEB8)
- Border: Pink (#C87488), 2px
- Height: 48px
- Contents:
  - Control hints: `[W]↑ [S]↓ [A]← [D]→ [SPACE]⏸`
  - Pitch display: `PITCH: +0`
- Font: Jersey 10, small size
- Text Color: Black

### 3. Main Canvas Area
- Background: Black (#010101)
- Border: Pink (#C87488), 3px with RIDGE relief
- Inner padding: 2px black border
- Contains pixelated image display

### 4. Status Bar
- Background: Beige (#CDBEB8)
- Border: Pink (#C87488), 1px
- Height: 32px
- Font: Jersey 10, small size
- Text Color: Black
- Example text: `[ READY ] Load image to start`

### 5. Buttons

#### Load Image Button (Initial State)
- Size: 240×80px
- Background: Beige (#CDBEB8)
- Border: Pink (#C87488), 3px
- Text: "LOAD IMAGE"
- Subtext: "Click to select"
- Hover: Background changes to Pink

#### Action Buttons (After Animation)
**SAVE MIDI Button:**
- Size: 200×50px
- Background: Beige (#CDBEB8)
- Border: Pink (#C87488), 3px
- Text: "SAVE MIDI"
- Text Color: Black

**LOAD NEW Button:**
- Size: 200×50px
- Background: Beige (#CDBEB8)
- Border: Pink (#C87488), 3px
- Text: "LOAD NEW"
- Text Color: Black

### 6. Popup Windows (Fourth Wall Breaking)

#### Start Animation Popup
- Title: "Scrapbook"
- Size: 450×280px
- Background: Black with Pink border (3px RIDGE)
- Inner area: Beige (#CDBEB8)
- Components:
  - Title: "IMAGE LOADED" (black text)
  - Image info and instructions
  - START ANIMATION button (pink background)
  - CANCEL button (beige background)

## Font Configuration

### Jersey 10 Font
The application uses the Jersey 10 pixel font (system name: "Jersey 10" with space).

Font sizes:
```python
self.pixel_font_large = ("Jersey 10", 28, "normal")   # Title text
self.pixel_font_medium = ("Jersey 10", 20, "normal")  # Button text
self.pixel_font_small = ("Jersey 10", 14, "normal")   # Status/controls
```

### Fallback Fonts
1. Silkscreen
2. Monaco (macOS built-in)
3. Menlo (macOS built-in)
4. Courier New

## Dithering Patterns

### Pattern Implementation (Planned)
Two dithering patterns are prepared for future 1-bit effects:

1. **50% Dithering** (Checkerboard):
   - 4×4 pixel pattern
   - Alternating pixels: `(x + y) % 2`

2. **25% Dithering** (Sparse):
   - 4×4 pixel pattern
   - Pattern: `(x % 2 == 0 and y % 2 == 0)`

## Interaction Design

### Cursor Feedback
- Default cursor on normal UI
- Hand cursor (`hand2`) on interactive elements:
  - Load Image button
  - Save MIDI button
  - Load New button
  - Popup window buttons

### Hover States
- Buttons change background from Beige to Pink on hover
- Maintains 3px border throughout

## Data Moshing Effect (Planned)

State variables prepared for glitch animation:
```python
self.glitch_frames = []          # Store corrupted frames
self.moshing_intensity = 0       # Control corruption level
```

### Implementation Plan
During melody generation animation:
1. Capture animation frames
2. Apply pixel displacement/corruption
3. Progressively increase moshing intensity
4. Create visual glitch effect synchronized with audio

## Technical Details

### Canvas-Based UI
Unlike the previous version using tkinter Labels, the new design uses Canvas widgets for:
- Precise positioning
- Custom drawing (stripes, patterns)
- Better control over visual effects
- Easy state updates without widget recreation

### Status Updates
All status updates now use canvas itemconfig:
```python
self.status_canvas.itemconfig(self.status_text_id, text="New status")
self.octave_canvas.itemconfig(self.octave_display_id, text="PITCH: +2")
```

## Visual Reference
The design is inspired by the classic Mac OS Scrapbook application, featuring:
- Striped title bars
- Chunky bordered windows
- 1-bit black & white aesthetic with dithering
- Pink and beige accent colors
- Pixel-perfect typography

## Future Enhancements

### Planned Features
1. **Full Dithering Implementation**
   - Apply Floyd-Steinberg or Bayer matrix dithering
   - Convert images to 1-bit before pixelation
   - Create authentic Mac OS Classic visual effect

2. **Data Moshing Animation**
   - Frame buffer corruption during playback
   - Glitch effects synchronized with notes
   - Progressive intensity increase

3. **Enhanced Window Chrome**
   - Close box widget (top-left corner)
   - Resize handle (bottom-right corner)
   - Classic Mac window controls

4. **Desktop Icon Integration**
   - Small pixel icons on the right side
   - Mimicking classic Mac desktop layout

## Color Accessibility

While maintaining the retro aesthetic, the color choices ensure:
- High contrast between text and background (black on beige/pink)
- Clear visual hierarchy
- Readable at different screen sizes
- Nostalgic yet functional design

---

Last Updated: 2025-10-21
Style: Mac OS Classic 1-Bit Dithering
Reference: Vintage Macintosh Scrapbook Application
