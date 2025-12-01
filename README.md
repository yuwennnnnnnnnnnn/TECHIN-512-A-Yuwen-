# TECHIN-512-A-Yuwen-
# Squid Game ⭕️ 

The idea of this ia a 90s-style handheld electronic game inspired by Netflix's *Squid Game*, players must complete quick actions under time pressure across 10 increasingly difficult levels, with the iconic pink aesthetic and guard symbols from the show.
<img src="https://github.com/user-attachments/assets/dd8bc7f9-0776-4c0d-b54c-cfc2ffb05001" width="500" alt="squid game">

---

## 🎮 Game Overview

**Squid Game** is a reaction-based handheld game where players compete to survive 10 levels by completing random actions within strict time limits. Inspired by the deadly children's games in *Squid Game*, each level requires players to perform one of four physical actions:

- **ROTATE** - Spin the ‘circle’ （rotary encoder）
- **BUTTON** - Press the ‘star’ （rotary encoder）
- **TAP** - Tap the 'triangle' (accelerometer detection)
- **SHAKE** - Shake the 'square' (accelerometer detection)

The game features:
- 3 difficulty modes (Easy, Normal, Hard)
- Progressive difficulty with decreasing time limits
- RGB LED feedback for each action type
- Cinematic boot animation with Squid Game theming
- Score tracking (10 points per level, max 100 points)

---

## 💡 Ideation & Design Philosophy

### Squid Game Inspiration
I took inspiration from Squid Game because its simple but high pressure games match the fast reaction style I wanted. The show’s strong visual identity, like the pink lighting, the guard symbols, and the number 456, helped me set the atmosphere for my own game. I also followed its idea of rising difficulty, so the time limits get shorter and the three modes reflect different levels of players. Instead of a normal “Game Over,” I used “ELIMINATED” and added a prize money style reward screen, echoing the show’s tension and motivation.

### Why This Game Design?
I chose a Bop It style gameplay because it fits the retro vibe of the project and brings a bit of 90s nostalgia that connects naturally with the Squid Game atmosphere. The different inputs like rotating, tapping, and shaking make the interaction more physical and fun, while the time pressure keeps the same kind of tension you feel in the show. The random actions and difficulty levels also make the game more replayable and keep players excited each time they try again.

---

## 🏗️ Enclosure Design
### 6 Surface
<img width="600" height="609" alt="image" src="https://github.com/user-attachments/assets/ad96cfb7-47c5-4912-8731-454c7d0fb7fb" />
### Fushion Model
<img width="600" height="540" alt="Screenshot 2025-12-01 at 1 17 47 PM" src="https://github.com/user-attachments/assets/c7696111-309b-4f82-84c6-58c7f98963dd" />

### Design Philosophy
The enclosure balances **portability**, **accessibility**, and **thematic consistency** with Squid Game's industrial, utilitarian aesthetic.

### Enclosure Features

#### 1. **Form Factor**
- **Dimensions**: Compact handheld size 15*15 *15 cube
- **Material**: 3D printed PLA  with arclic paintt
- **Color Choice**: 
  - **Primary**: suqid game pink (Squid Game theme)
  - **Alternative**: White 

#### 2. **Accessibility Requirements**
✅ **Type-C Port Slot**: 
- Side-mounted opening for ESP32 USB-C connector
- Allows charging and code updates without opening enclosure

✅ **On/Off Switch**: 
- Top or side-mounted toggle switch
- Clearly labeled and easily accessible

✅ **Removable Lid/Panel**:
- Snap-fit or screw-attached back panel
- Provides access to perfboard for maintenance and battery replacement

#### 3. **User Interface Layout**
```
     ┌─────────────────────┐
     │   [OLED Screen]     │  ← Top section: Display
     │                     │
     │  ( Rotary Encoder ) │  ← Middle: Primary control
     │                     │
     │      [Button]       │  ← Lower: Action button
     │                     │
     │  ●●●●●●●● (LEDs)    │  ← Bottom: NeoPixel strip
     └─────────────────────┘
```

#### 4. **Internal Structure**
- **Battery Compartment**: Secure pocket for LiPo with strain relief
- **Perfboard Mount**: Standoffs or slots to hold PCB firmly
- **Cable Management**: Channels or clips to prevent wire tangles
- **Accelerometer Position**: Center-mounted for balanced shake detection

#### 5. **Aesthetic Details**
Inspired by Squid Game's props:
- **Sharp Angles**: Mimics the geometric shapes (△○□)
- **Minimal Decoration**: Industrial, functional design
- **LED Light Pipes**: Diffused pink glow through translucent sections
- **Texture**: Optional ribbed or grid pattern (like metal containers in the show)

### Design Considerations
| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Size** | Pocket-friendly | Truly portable 90s handheld experience |
| **Durability** | Thick walls (2-3mm) | Survives drops during intense gameplay |
| **Ergonomics** | Rounded edges | Comfortable for extended play sessions |
| **Assembly** | Tool-less access | Easy disassembly for troubleshooting |
| **Repairability** | Modular components | All parts removable via female headers |

---

## 🕹️ How to Play

### Starting the Game
1. **Power On**: Press the on/off switch
2. **Boot Animation**: Watch the Squid Game-inspired intro sequence
   - Pink LED flashing
   - "SQUID GAME" title zoom animation
   - Guard symbols (△ ○ □) display
   - Player #456 countdown
3. **Press Button**: Start from the splash screen

### Selecting Difficulty
- **Rotate Encoder**: Cycle through difficulty options
  - **△ EASY**: 8 seconds base time
  - **○ NORMAL**: 6 seconds base time
  - **□ HARD**: 4 seconds base time
- **Press Button**: Confirm selection

### Playing Levels
1. **Read the Action**: Screen displays "DO: [ACTION]"
2. **LED Color Hint**: 
   - 🔵 Blue = ROTATE
   - 🟢 Green = BUTTON
   - 🟡 Yellow = TAP
   - 🟣 Purple = SHAKE
3. **Perform Action**: Complete before timer runs out
4. **Time Penalty**: Each level reduces time by 0.3s (minimum 1.5s)
5. **Progress**: Complete all 10 levels to win!

### Game Over Options
- **Button**: Restart game (same difficulty)
- **Rotate Encoder**: Return to main menu

---

## 🔧 Hardware Components

### Required Components (Provided)
| Component | Model | Purpose |
|-----------|-------|---------|
| Microcontroller | Xiao ESP32-C3 | Main processor |
| Display | SSD1306 128x64 OLED | Visual interface |
| Accelerometer | ADXL345 | Tap & shake detection |
| Rotary Encoder | - | Menu navigation & rotation action |
| Button | Digital Input | Confirmation & button action |
| NeoPixel LEDs | WS2812B (8 LEDs) | Action feedback & atmosphere |
| LiPo Battery | 3.7V | Portable power |
| Power Switch | Toggle Switch | On/Off control |

### Wiring Connections
```
ESP32 Pin    →  Component
---------       ---------
D3, D2       →  Rotary Encoder (CLK, DT)
D1           →  Button
A0           →  NeoPixel Data In
SCL, SDA     →  I2C Bus (OLED + ADXL345)
3.3V, GND    →  Power Rails
BAT+, BAT-   →  LiPo Battery (via switch)
```


## 💻 Software Features

### Implemented Requirements
✅ **Three Difficulty Settings**: Easy, Normal, Hard with distinct time limits  
✅ **Four Input Actions**: Rotate, Button, Tap, Shake  
✅ **Time Limits**: Progressive difficulty with visual countdown  
✅ **Ten Levels**: Increasing challenge from level 1 to 10  
✅ **Game Over/Win Screens**: "ELIMINATED" or "YOU WIN!" with restart options  
✅ **Sensor Filtering**: Moving average filter on accelerometer (window size = 5)  
✅ **NeoPixel Integration**: Multiple colors for actions, states, and feedback  
✅ **Scoring System** 
- 10 points awarded per completed level
- Current score displayed during gameplay
- Final score shown on Game Over/Win screen
- Maximum possible score: 100 points
✅ **Animated Splash Screen** (+2 pts)
- Multi-phase boot animation on power-on only
- Includes:
  - Pink LED flashing (atmosphere building)
  - "SQUID GAME" title zoom effect
  - Guard symbols animation (△○□)
  - Player #456 countdown (3-2-1)
  - "START!" flash
- Does NOT play on game restart (only on power cycle)

---

### Game State Machine
```
BOOT_ANIMATION → SPLASH → DIFFICULTY_SELECT → GAME_PLAY → GAME_RESULT
                    ↑                                           ↓
                    └───────────────────────────────────────────┘
```

### Accelerometer Calibration
**Shake Detection Algorithm**:
- **Moving Average Filter**: Smooths raw accelerometer data over 5 samples
- **Angle Threshold**: Must exceed 30° tilt on any axis
- **Duration Requirement**: Must sustain motion for 0.2 seconds
- **Debounce Logic**: Prevents false triggers from vibrations

**Tap Detection**:
- Uses ADXL345's built-in tap detection interrupt
- Calibrated for firm but not excessive force

---

## 📝 Code Structure

### Main Components

#### 1. **Hardware Initialization** (Lines 1-75)
- Display, encoder, button, accelerometer, NeoPixels setup
- MovingAverageFilter class for sensor data smoothing

#### 2. **Game Constants** (Lines 77-95)
- State definitions, difficulty settings, color definitions
- Game variables (level, score, time)

#### 3. **Graphics Functions** (Lines 97-180)
- `draw_hollow_triangle()`, `draw_hollow_circle()`, `draw_hollow_square()`
- Boot animation sequences

#### 4. **Sensor Processing** (Lines 200-240)
- `calculate_angles()`: Convert acceleration to tilt angles
- `check_shake()`: Debounced shake detection with duration threshold

#### 5. **Game Logic** (Lines 242-290)
- `get_time_limit()`: Dynamic time calculation
- `start_level()`: Initialize new level with random action
- `check_action()`: Validate player input

#### 6. **UI Functions** (Lines 292-380)
- `create_splash_screen()`, `create_difficulty_screen()`
- `create_game_screen()`, `create_result_screen()`

#### 7. **Main Loop** (Lines 450-550)
- State machine with 5 states
- Input handling (encoder, button, accelerometer)
- Display updates and game progression

### Key Algorithms

**Moving Average Filter**:
```python
class MovingAverageFilter:
    def filter(self, x, y, z):
        # Store last N readings
        # Return average to smooth noise
```

**Shake Detection**:
```python
def check_shake(angle_x, angle_y, current_time):
    # Check if angle > 30° for 0.2 seconds
    # Prevents false positives from vibrations
```

---

## 🔮 Future Improvements

### Potential Enhancements
1. **High Score Persistence**: 
   - Save top 3 scores to ESP32 flash memory
   - Initial entry screen using rotary encoder

2. **Sound Design**:
   - Add piezo buzzer for:
     - Victory/defeat tones
     - Countdown beeps
     - Action confirmation sounds

3. **Additional Actions**:
   - Multi-tap sequences
   - Tilt-and-hold challenges
   - Combination moves (rotate + button)

4. **Multiplayer Mode**:
   - Bluetooth competition between two devices
   - Pass-and-play high score challenge

5. **Visual Enhancements**:
   - Animated sprites for guard characters
   - Particle effects on LED strip
   - Dynamic backgrounds per level

6. **Accessibility Features**:
   - Adjustable contrast settings
   - Haptic feedback option
   - Color-blind friendly LED modes
