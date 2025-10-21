# Visual Flow Diagram - Dithering & Data Moshing

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         IMAGE2MELODY PIPELINE                           │
│                    Floyd-Steinberg & Data Moshing                       │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│ USER LOADS   │
│ COLOR IMAGE  │
│  (RGB/RGBA)  │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: FLOYD-STEINBERG DITHERING                                     │
│ ────────────────────────────────────────                                │
│ Status: [ DITHERING ] Applying 1-bit dithering...                      │
│ Duration: 50-200ms                                                      │
│                                                                          │
│ Step 1: Convert to Grayscale                                           │
│         RGB(r,g,b) → L(luminance)                                      │
│                                                                          │
│ Step 2: Error Diffusion                                                │
│         For each pixel:                                                │
│           • Quantize to 0 or 255                                       │
│           • Calculate error = old - new                                │
│           • Distribute error:                                          │
│                    X   7/16                                            │
│              3/16 5/16 1/16                                            │
│                                                                          │
│ Step 3: Color Mapping                                                  │
│         0 (black) → #010101                                            │
│       255 (white) → #CDBEB8 (beige)                                    │
│                                                                          │
│ Output: 1-bit RGB image (black & beige only)                           │
└─────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: PIXELATION                                                     │
│ ────────────────────────────────────────────                            │
│ • Resize dithered image to grid (e.g., 10×7)                           │
│ • Extract RGB data for each block                                      │
│ • Create empty pixelated canvas                                        │
│ • Initialize moshing_intensity = 0.0                                   │
└─────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: ANIMATED PLAYBACK WITH DATA MOSHING                           │
│ ────────────────────────────────────────────                            │
│                                                                          │
│ FOR EACH PIXEL BLOCK (0 → total_pixels):                               │
│                                                                          │
│   1. Draw pixel block on canvas                                        │
│   2. Calculate progress = current / total                              │
│   3. Update moshing intensity:                                         │
│      ┌─────────────────────────────────────────┐                       │
│      │ Intensity                               │                       │
│      │   0.21│      ╭───────╮                  │                       │
│      │       │    ╱           ╲                 │                       │
│      │   0.0 │───╯             ╰────────        │                       │
│      │       0%   30%   70%    100%             │                       │
│      │         Progress                         │                       │
│      └─────────────────────────────────────────┘                       │
│                                                                          │
│   4. IF (current_pixel % 5 == 0) AND (intensity > 0.05):               │
│      ┌────────────────────────────────────────┐                        │
│      │ APPLY DATA MOSHING                     │                        │
│      │ ──────────────────────                 │                        │
│      │ num_glitches = w×h × intensity × 0.05  │                        │
│      │                                         │                        │
│      │ For each glitch:                       │                        │
│      │   Random choice:                       │                        │
│      │                                         │                        │
│      │   [Displacement]                       │                        │
│      │   • Block: 5-20px                      │                        │
│      │   • Shift: (-30,+30), (-10,+10)       │                        │
│      │   • Copy block to new location        │                        │
│      │                                         │                        │
│      │   [Color Shift]                        │                        │
│      │   • Width: 10-50px                     │                        │
│      │   • Color: Pink or Beige               │                        │
│      │   • Horizontal streak                  │                        │
│      │                                         │                        │
│      │   [Scanline]                           │                        │
│      │   • Width: 20-100px                    │                        │
│      │   • Repeat previous pixel              │                        │
│      │   • Horizontal smear                   │                        │
│      └────────────────────────────────────────┘                        │
│                                                                          │
│   5. Display image (moshed OR clean)                                   │
│   6. Play corresponding note (HSV-based)                               │
│   7. Update status:                                                    │
│      • If intensity > 0.1: Show ⚡                                      │
│      • Display: Block coords, RGB, progress                            │
│   8. Schedule next pixel (50-100ms delay)                              │
│                                                                          │
│ VISUAL PROGRESSION:                                                     │
│ ────────────────────                                                    │
│ 0-30%:   Clean dithered blocks                                         │
│          Status: [ PLAYING ] Block (x,y) ...                           │
│                                                                          │
│ 30-70%:  Heavy glitching                                               │
│          Status: [ PLAYING ] ⚡ Block (x,y) ...                         │
│          Visible: Displacement, color streaks, smearing                │
│                                                                          │
│ 70-100%: Fading glitches                                               │
│          Status: [ PLAYING ] Block (x,y) ...                           │
│          Return to stable state                                        │
└─────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: COMPLETION                                                     │
│ ────────────────────────────────────────────                            │
│ • Display final clean frame                                            │
│ • Stop audio playback                                                  │
│ • Show SAVE MIDI and LOAD NEW buttons                                  │
│ • Status: [ COMPLETE ] Generated X notes | SAVE MELODY?                │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                          COLOR TRANSFORMATIONS                          │
└─────────────────────────────────────────────────────────────────────────┘

Original RGB Image:
┌───────────────────────┐
│ R:234 G:128 B:56      │  ─┐
│ R:12  G:89  B:234     │   │
│ R:145 G:201 B:78      │   │  Full Color
│ ...                   │   │
└───────────────────────┘  ─┘
         │
         │ Floyd-Steinberg Dithering
         ▼
1-Bit Dithered (Black & Beige):
┌───────────────────────┐
│ #CDBEB8 (beige)       │  ─┐
│ #010101 (black)       │   │  Only 2 colors
│ #CDBEB8 (beige)       │   │  + dot patterns
│ ...                   │   │
└───────────────────────┘  ─┘
         │
         │ Pixelation
         ▼
Pixelated Blocks (80×80px each):
┌─────┬─────┬─────┐
│Beige│Black│Beige│  ─┐
├─────┼─────┼─────┤   │  Large blocks
│Black│Beige│Black│   │  of solid color
├─────┼─────┼─────┤   │
│Beige│Black│Beige│   │
└─────┴─────┴─────┘  ─┘
         │
         │ Data Moshing (30-70% progress)
         ▼
Moshed/Glitched:
┌─────┬──┬──┬─────┐
│Beige│Pi│nk│Black│  ─┐ Displaced blocks
├───┬─┴──┴──┴─────┤   │ Color streaks
│Bla│Beige smeared│   │ Scanline corruption
├───┴──────┬──────┤   │
│   Beige  │Black │   │
└──────────┴──────┘  ─┘


┌─────────────────────────────────────────────────────────────────────────┐
│                      INTENSITY CURVE BREAKDOWN                          │
└─────────────────────────────────────────────────────────────────────────┘

Progress  Intensity  Glitches/Frame  Visual Effect        Status
────────  ─────────  ──────────────  ───────────────────  ─────────────
  0%       0.000          0          Clean start          No ⚡
 10%       0.030         ~15         Very light glitches  No ⚡
 20%       0.060         ~30         Light glitches       No ⚡
 30%       0.090         ~45         Moderate glitches    No ⚡
 40%       0.120         ~60         Heavy glitches       ⚡ appears
 50%       0.150         ~75         Peak glitches        ⚡
 60%       0.180         ~90         Peak glitches        ⚡
 70%       0.210        ~105         Maximum chaos        ⚡
 80%       0.140         ~70         Fading glitches      ⚡
 90%       0.070         ~35         Light glitches       No ⚡
100%       0.000          0          Clean end            No ⚡

Formula:
  if progress < 0.7:
    intensity = progress × 0.3
  else:
    intensity = (1.0 - progress) × 0.7


┌─────────────────────────────────────────────────────────────────────────┐
│                       GLITCH TYPE EXAMPLES                              │
└─────────────────────────────────────────────────────────────────────────┘

[1] DISPLACEMENT - Rectangular Block Shift
────────────────────────────────────────────

Original:                    After Glitch:
┌──────────────┐            ┌──────────────┐
│ ████░░░░     │            │ ████    ░░░░ │ ← Block moved right
│ ████░░░░     │    →       │ ████    ░░░░ │
│ ░░░░████     │            │ ░░░░    ████ │
└──────────────┘            └──────────────┘


[2] COLOR SHIFT - Horizontal Streak
────────────────────────────────────

Original:                    After Glitch:
┌──────────────┐            ┌──────────────┐
│ ████░░░░████ │            │ ████░░░░████ │
│ ░░░░████░░░░ │    →       │ 🟪🟪🟪🟪🟪🟪🟪 │ ← Pink/beige streak
│ ████░░░░████ │            │ ████░░░░████ │
└──────────────┘            └──────────────┘


[3] SCANLINE - Horizontal Smear
────────────────────────────────

Original:                    After Glitch:
┌──────────────┐            ┌──────────────┐
│ ████░░░░     │            │ ████░░░░     │
│ ░░░░████     │    →       │ ░░░░░░░░░░░░ │ ← Pixels repeated
│ ████░░░░     │            │ ████░░░░     │
└──────────────┘            └──────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                         PERFORMANCE TIMELINE                            │
└─────────────────────────────────────────────────────────────────────────┘

Example: 800×600px image, 80px blocks, 70 total blocks

Time (ms)    Event                          Details
─────────    ──────────────────────────     ────────────────────────────
    0        User clicks START              Animation begins
  100        Dithering starts               Floyd-Steinberg processing
  250        Dithering complete (+150ms)    1-bit image ready
  300        Animation frame 1              Block 1/70, no moshing
  350        Animation frame 2              Block 2/70
  400        Animation frame 3              Block 3/70
  450        Animation frame 4              Block 4/70
  500        Animation frame 5 (+20ms)      Block 5/70, MOSHING applied
  ⋮          ⋮                              ⋮
 2100        Animation frame 30 (+30ms)     Block 30/70, heavy moshing ⚡
 2150        Animation frame 31             Block 31/70
  ⋮          ⋮                              ⋮
 4200        Animation frame 60 (+25ms)     Block 60/70, light moshing
  ⋮          ⋮                              ⋮
 5600        Animation frame 70             Block 70/70, complete
 5650        Final display                  Clean frame shown
 5700        Buttons appear                 SAVE MIDI / LOAD NEW

Total: ~5.7 seconds
  Dithering: 150ms (2.6%)
  Moshing overhead: ~420ms (14 frames × 30ms) (7.4%)
  Animation: 5150ms (90%)


┌─────────────────────────────────────────────────────────────────────────┐
│                           KEY DIFFERENCES                               │
└─────────────────────────────────────────────────────────────────────────┘

BEFORE THIS UPDATE                   AFTER THIS UPDATE
──────────────────                   ─────────────────

Colors:                              Colors:
  • Full RGB spectrum                  • Only black (#010101)
  • Gradients preserved                  and beige (#CDBEB8)
  • Original colors intact             • 1-bit dithered patterns

Processing:                          Processing:
  • Direct pixelation                  • Floyd-Steinberg dithering
  • No pre-processing                  • Error diffusion algorithm
  • Instant start                      • Brief dithering phase

Animation:                           Animation:
  • Clean pixel blocks                 • Progressive glitch effects
  • No visual effects                  • 3 types of corruption
  • Consistent appearance              • Intensity curve (0→0.21→0)

Visual Style:                        Visual Style:
  • Modern dark theme                  • Mac OS Classic aesthetic
  • Digital/smooth                     • Vintage/grainy
  • No glitches                        • Intentional corruption

Status Bar:                          Status Bar:
  • Simple progress                    • Dithering indicator
  • RGB values                         • ⚡ glitch icon
  • Percentage only                    • Progressive feedback


Legend:
  ████ = Black (#010101)
  ░░░░ = Beige (#CDBEB8)
  🟪🟪 = Pink/Beige glitch colors
  ⚡   = Glitch indicator
```
