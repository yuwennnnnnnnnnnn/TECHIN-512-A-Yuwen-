# TECHIN-512-A-Yuwen-
# Squid Game ⭕️ Overview

## Squid Game Inspiration
The idea of this ia a 90s-style handheld electronic game inspired by Netflix's *Squid Game*, players must complete quick actions under time pressure across 10 increasingly difficult levels, with the iconic pink aesthetic and guard symbols from the show. The show’s strong visual identity, like the pink lighting, the guard symbols, and the number 456, helped me set the atmosphere for my own game. I also followed its idea of rising difficulty, so the time limits get shorter and the three modes reflect different levels of players. Instead of a normal “Game Over,” I used “ELIMINATED” and added a prize money style reward screen, echoing the show’s tension and motivation.

## Why This Game Design?
I chose a Bop It style gameplay because it fits the retro vibe of the project and brings a bit of 90s nostalgia that connects naturally with the Squid Game atmosphere. The different inputs like rotating, tapping, and shaking make the interaction more physical and fun, while the time pressure keeps the same kind of tension you feel in the show. The random actions and difficulty levels also make the game more replayable and keep players excited each time they try again.

<img width="794" height="512" alt="Screenshot 2025-12-01 at 9 17 54 PM" src="https://github.com/user-attachments/assets/4bda3d3e-dfa2-47af-8923-02ba898e97b0" />

Inspired by the deadly children's games in *Squid Game*, each level requires players to perform one of four physical actions:
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

## Enclosure Design
### Six Surface Design
<img width="800" height="609" alt="image" src="https://github.com/user-attachments/assets/ad96cfb7-47c5-4912-8731-454c7d0fb7fb" />

### Fushion Model
<img width="800" height="540" alt="Screenshot 2025-12-01 at 1 17 47 PM" src="https://github.com/user-attachments/assets/c7696111-309b-4f82-84c6-58c7f98963dd" />

### Enclosure Features

The enclosure is a small fifteen by fifteen by fifteen cube that can be held easily. I used 3D printed PLA and painted it with acrylic to match the Squid Game pink, with white as the secondary color. I also added a Type C opening for the ESP32 so I can charge and update the code without taking it apart. The lid can be opened with four small magnets in the corners, which makes it easy to reach the perfboard and replace the battery.

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
- **Pess Star Button**: Restart game (same difficulty)
- **Rotate Circle Button**: Return to main menu

---

## Hardware Components

### Required Components (Provided)
| Component | Model | Purpose |
|-----------|-------|---------|
| Microcontroller | Xiao ESP32-C3 | Main processor |
| Display | SSD1306 128x64 OLED | Visual interface |
| Accelerometer | ADXL345 | Tap & shake detection |
| 2 Rotary Encoder | - | Menu navigation & rotation action & button action |
| NeoPixel LEDs | WS2812B (8 LEDs) | Action feedback & atmosphere |
| LiPo Battery | 3.7V | Portable power |
| Power Switch | Toggle Switch | On/Off control |

## Future Improvements

For future upgrades, I want to save the top three scores in the ESP32 memory and add simple name input. I also hope to improve the sound with countdown beeps and feedback tones. The gameplay can be expanded with new actions like multi taps, tilt moves, and combinations. A Bluetooth or pass and play mode would make it more social. I also want better visuals, such as small animations and more accessible options like contrast settings.

