import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import i2cdisplaybus
import adafruit_displayio_ssd1306
import time
from rotary_encoder import RotaryEncoder
import digitalio
import adafruit_adxl34x
import math
import neopixel
from random import choice
import vectorio

# Initialize display
displayio.release_displays()
i2c = busio.I2C(board.SCL, board.SDA)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Initialize rotary encoder
encoder = RotaryEncoder(board.D3, board.D2, pulses_per_detent=1)

# Initialize button
button = digitalio.DigitalInOut(board.D1)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Initialize accelerometer
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_tap_detection()

# Initialize NeoPixel
pixel_pin = board.A0
num_pixels = 8
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

# ==================== 新增：加速度计滤波器类 ====================
# 插入位置：在初始化硬件之后，游戏状态定义之前

class MovingAverageFilter:
    """
    移动平均滤波器 - 用于平滑加速度计数据
    
    原理：保存最近N个读数，返回它们的平均值
    优点：可以有效减少噪声和抖动
    
    参数：
        size: 滤波窗口大小（保存多少个历史数据）
              size越大越平滑，但响应越慢
              建议值：3-10
    """
    def __init__(self, size=5):
        self.size = size
        self.values_x = []  # X轴历史数据
        self.values_y = []  # Y轴历史数据
        self.values_z = []  # Z轴历史数据
    
    def filter(self, x, y, z):
        """
        对新的加速度数据进行滤波
        
        参数：
            x, y, z: 加速度计原始读数
        
        返回：
            滤波后的 (x, y, z) 数据
        """
        # 添加新数据到历史记录
        self.values_x.append(x)
        self.values_y.append(y)
        self.values_z.append(z)
        
        # 如果历史数据超过窗口大小，删除最旧的数据
        if len(self.values_x) > self.size:
            self.values_x.pop(0)
            self.values_y.pop(0)
            self.values_z.pop(0)
        
        # 计算平均值
        avg_x = sum(self.values_x) / len(self.values_x)
        avg_y = sum(self.values_y) / len(self.values_y)
        avg_z = sum(self.values_z) / len(self.values_z)
        
        return avg_x, avg_y, avg_z
    
    def reset(self):
        """重置滤波器（清空历史数据）"""
        self.values_x = []
        self.values_y = []
        self.values_z = []

# 创建滤波器实例
accel_filter = MovingAverageFilter(size=5)
# size=5: 使用最近5个读数的平均值
# 可以根据实际效果调整（3-10之间）

# ==================== 游戏状态定义 ====================

# Game states
STATE_BOOT_ANIMATION = -1  # Boot animation state
STATE_SPLASH = 0
STATE_DIFFICULTY_SELECT = 1
STATE_GAME_PLAY = 2
STATE_GAME_RESULT = 3

current_state = STATE_BOOT_ANIMATION
selected_difficulty = 0
difficulties = ["EASY", "NORMAL", "HARD"]

# Game variables
current_level = 1
total_levels = 10
score = 0
time_remaining = 0
game_start_time = 0
current_action = ""
actions = ["ROTATE", "BUTTON", "TAP", "SHAKE"]
action_completed = False
level_passed = False

# Result screen debounce
result_screen_start_time = 0

# Encoder variables
encoder_position = 0
last_encoder_position = 0
last_encoder_time = 0
encoder_debounce_ms = 80

# Shake detection variables
shake_threshold = 30
shake_duration = 0.2
shake_start_time = None
is_shaking = False

# Button state
button_pressed = False
last_button_value = button.value
button_clicked = False

# Color definitions
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 150, 0)
PURPLE = (180, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
PINK = (255, 20, 147)
OFF = (0, 0, 0)

def draw_hollow_triangle(group, palette, x_center, y_top, size):
    """Draw hollow triangle"""
    # Three edges
    # Left edge
    for i in range(size):
        y = y_top + i
        x = x_center - i // 2
        point = vectorio.Circle(pixel_shader=palette, radius=1, x=x, y=y)
        group.append(point)
    # Right edge
    for i in range(size):
        y = y_top + i
        x = x_center + i // 2
        point = vectorio.Circle(pixel_shader=palette, radius=1, x=x, y=y)
        group.append(point)
    # Bottom edge
    bottom_y = y_top + size - 1
    for x in range(x_center - size // 2, x_center + size // 2 + 1):
        point = vectorio.Circle(pixel_shader=palette, radius=1, x=x, y=bottom_y)
        group.append(point)

def draw_hollow_circle(group, palette, x_center, y_center, radius):
    """Draw hollow circle"""
    import math
    # Use parametric equation to draw circle perimeter
    for angle in range(0, 360, 3):  # Draw a point every 3 degrees
        rad = angle * math.pi / 180
        x = int(x_center + radius * math.cos(rad))
        y = int(y_center + radius * math.sin(rad))
        point = vectorio.Circle(pixel_shader=palette, radius=1, x=x, y=y)
        group.append(point)

def draw_hollow_square(group, palette, x_left, y_top, size):
    """Draw hollow square"""
    # Top edge
    for x in range(x_left, x_left + size):
        point = vectorio.Circle(pixel_shader=palette, radius=1, x=x, y=y_top)
        group.append(point)
    # Bottom edge
    for x in range(x_left, x_left + size):
        point = vectorio.Circle(pixel_shader=palette, radius=1, x=x, y=y_top + size - 1)
        group.append(point)
    # Left edge
    for y in range(y_top, y_top + size):
        point = vectorio.Circle(pixel_shader=palette, radius=1, x=x_left, y=y)
        group.append(point)
    # Right edge
    for y in range(y_top, y_top + size):
        point = vectorio.Circle(pixel_shader=palette, radius=1, x=x_left + size - 1, y=y)
        group.append(point)

def show_squid_game_title_zoom():
    """Display SQUID GAME text with zoom-in animation"""
    # Pink lighting
    pixels.fill(PINK)
    pixels.show()
    
    # Zoom animation: gradually scale from 1 to 3
    # Use more steps with shorter display time to make changes more noticeable
    for scale in range(1, 4):  # 1, 2, 3
        group = displayio.Group()
        
        # Adjust position based on scale to keep centered
        if scale == 1:
            x1, y1 = 42, 25
            x2, y2 = 46, 40
        elif scale == 2:
            x1, y1 = 28, 20
            x2, y2 = 34, 44
        else:  # scale == 3
            x1, y1 = 14, 15
            x2, y2 = 22, 45
        
        # First line: SQUID
        title1 = label.Label(terminalio.FONT, text="SQUID", x=x1, y=y1, scale=scale)
        group.append(title1)
        
        # Second line: GAME
        title2 = label.Label(terminalio.FONT, text="GAME", x=x2, y=y2, scale=scale)
        group.append(title2)
        
        display.root_group = group
        time.sleep(0.3)  # Display each size longer to make changes more noticeable
    
    # Keep large text displayed for a moment
    time.sleep(0.4)

def play_boot_animation():
    """Play Squid Game-style boot animation"""
    # Phase 1: Pink light flashing
    for _ in range(3):
        pixels.fill(PINK)
        pixels.show()
        time.sleep(0.2)
        pixels.fill(OFF)
        pixels.show()
        time.sleep(0.2)
    
    # Phase 2: Display SQUID GAME zoom animation
    show_squid_game_title_zoom()
    
    # Phase 3: Display triangle, circle, square guard symbols in sequence (using pixel-drawn hollow shapes)
    
    symbols_data = [
        # Triangle
        {
            "type": "triangle",
            "color": PINK
        },
        # Circle
        {
            "type": "circle",
            "color": CYAN
        },
        # Square
        {
            "type": "square",
            "color": YELLOW
        }
    ]
    
    for symbol_data in symbols_data:
        group = displayio.Group()
        
        # Create palette (white foreground)
        palette = displayio.Palette(1)
        palette[0] = 0xFFFFFF  # White
        
        if symbol_data["type"] == "triangle":
            # Draw hollow triangle
            draw_hollow_triangle(group, palette, 64, 15, 35)
            
        elif symbol_data["type"] == "circle":
            # Draw hollow circle
            draw_hollow_circle(group, palette, 64, 32, 18)
            
        elif symbol_data["type"] == "square":
            # Draw hollow square
            draw_hollow_square(group, palette, 46, 14, 36)
        
        display.root_group = group
        
        # Corresponding color light effect
        pixels.fill(symbol_data["color"])
        pixels.show()
        time.sleep(0.6)
    
    
    # Phase 4: Display number and countdown
    for countdown in range(3, 0, -1):
        group = displayio.Group()
        
        # Number 456 (protagonist's number)
        number_label = label.Label(terminalio.FONT, text="No.456", x=42, y=15, scale=1)
        group.append(number_label)
        
        # Countdown
        count_label = label.Label(terminalio.FONT, text=str(countdown), x=58, y=40, scale=2)
        group.append(count_label)
        
        display.root_group = group
        
        # Countdown lighting: all pink
        pixels.fill(PINK)
        pixels.show()
        
        time.sleep(0.6)
    
    # Phase 5: START flashing
    for _ in range(2):
        group = displayio.Group()
        start_label = label.Label(terminalio.FONT, text="START!", x=45, y=32, scale=1)
        group.append(start_label)
        display.root_group = group
        
        pixels.fill(PINK)
        pixels.show()
        time.sleep(0.3)
        
        pixels.fill(OFF)
        pixels.show()
        time.sleep(0.3)

def calculate_angles(x, y, z):
    """Calculate X-axis and Y-axis angles"""
    angle_x = math.atan2(x, math.sqrt(y*y + z*z)) * 180 / math.pi
    angle_y = math.atan2(y, math.sqrt(x*x + z*z)) * 180 / math.pi
    return angle_x, angle_y

def check_shake(angle_x, angle_y, current_time):
    """Detect shake - angle > 45 degrees, sustained for 0.3 seconds"""
    global shake_start_time, is_shaking
    
    # Check if either angle exceeds 45-degree threshold
    angle_exceeded = abs(angle_x) > shake_threshold or abs(angle_y) > shake_threshold
    
    if angle_exceeded:
        if shake_start_time is None:
            # First time exceeding 45 degrees, record start time
            shake_start_time = current_time
        elif current_time - shake_start_time >= shake_duration:
            # Exceeds 45 degrees and duration reaches 0.3 seconds, shake detected
            if not is_shaking:
                is_shaking = True
                return True
    else:
        # Angle returns below 45 degrees, reset state
        shake_start_time = None
        is_shaking = False
    
    return False

def get_time_limit(difficulty, level):
    """Get time limit based on difficulty and level"""
    base_times = {"EASY": 8, "NORMAL": 6, "HARD": 4}
    level_penalty = (level - 1) * 0.3  # Decrease 0.3 seconds per level
    return max(base_times[difficulty] - level_penalty, 1.5)  # Minimum 1.5 seconds

def create_splash_screen():
    """Create splash screen - Squid Game theme"""
    group = displayio.Group()
    
    # Game title
    title_label = label.Label(terminalio.FONT, text="SQUID GAME", x=32, y=10, scale=1)
    group.append(title_label)
    
    # Subtitle
    subtitle_label = label.Label(terminalio.FONT, text="ACTION RUSH", x=28, y=25, scale=1)
    group.append(subtitle_label)
    
    # Prize pool
    prize_label = label.Label(terminalio.FONT, text="$1 MILLION", x=32, y=40, scale=1)
    group.append(prize_label)
    
    # Hint
    hint_label = label.Label(terminalio.FONT, text="Press to Start", x=23, y=55, scale=1)
    group.append(hint_label)
    
    return group

def create_difficulty_screen():
    """Create difficulty selection screen with icons"""
    group = displayio.Group()
    
    # Title
    title_label = label.Label(terminalio.FONT, text="SELECT MODE", x=30, y=8, scale=1)
    group.append(title_label)
    
    # Define difficulty icons and positions
    difficulty_icons = [
        {"symbol": "△", "name": "EASY", "x": 64, "y": 28},    # Triangle
        {"symbol": "○", "name": "NORMAL", "x": 64, "y": 40},  # Circle
        {"symbol": "□", "name": "HARD", "x": 64, "y": 52}     # Square
    ]
    
    # Draw each difficulty option
    for i, diff in enumerate(difficulty_icons):
        if i == selected_difficulty:
            # Selected: show icon, name, and pointer
            pointer_label = label.Label(terminalio.FONT, text=">", x=20, y=diff["y"], scale=2)
            group.append(pointer_label)
            
            icon_label = label.Label(terminalio.FONT, text=diff["symbol"], x=35, y=diff["y"], scale=2)
            group.append(icon_label)
            
            name_label = label.Label(terminalio.FONT, text=diff["name"], x=55, y=diff["y"], scale=1)
            group.append(name_label)
        else:
            # Unselected: show only small icon and name
            icon_label = label.Label(terminalio.FONT, text=diff["symbol"], x=35, y=diff["y"], scale=1)
            group.append(icon_label)
            
            name_label = label.Label(terminalio.FONT, text=diff["name"], x=48, y=diff["y"], scale=1)
            group.append(name_label)
    
    return group

def create_game_screen():
    """Create game screen"""
    group = displayio.Group()
    
    # Difficulty and level info
    level_text = f"LEVEL: {current_level}/{total_levels}"
    level_label = label.Label(terminalio.FONT, text=level_text, x=10, y=10, scale=1)
    group.append(level_label)
    
    # Action prompt
    action_label = label.Label(terminalio.FONT, text=f"DO: {current_action}", x=10, y=25, scale=1)
    group.append(action_label)
    
    # Time display
    time_text = f"TIME: {time_remaining:.1f}s"
    time_label = label.Label(terminalio.FONT, text=time_text, x=10, y=40, scale=1)
    group.append(time_label)
    
    # Score display
    score_label = label.Label(terminalio.FONT, text=f"SCORE: {score}", x=10, y=55, scale=1)
    group.append(score_label)
    
    return group

def create_result_screen(success):
    """Create result screen"""
    group = displayio.Group()
    
    if success:
        result_label = label.Label(terminalio.FONT, text="YOU WIN!", x=40, y=15, scale=1)
        score_text = f"Prize:{score}pts"
    else:
        result_label = label.Label(terminalio.FONT, text="ELIMINATED", x=30, y=15, scale=1)
        score_text = f"Score:{score}pts"
    
    group.append(result_label)
    
    score_label = label.Label(terminalio.FONT, text=score_text, x=30, y=35, scale=1)
    group.append(score_label)
    
    hint_label = label.Label(terminalio.FONT, text="BTN:RETRY ROT:MENU", x=10, y=50, scale=1)
    group.append(hint_label)
    
    return group

def start_level():
    """Start new level"""
    global current_action, time_remaining, game_start_time, action_completed, level_passed
    current_action = choice(actions)  # Randomly select an action
    time_remaining = get_time_limit(difficulties[selected_difficulty], current_level)
    game_start_time = time.monotonic()
    action_completed = False
    level_passed = False
    
    # Reset shake detection state
    global shake_start_time, is_shaking
    shake_start_time = None
    is_shaking = False
    
    # ==================== 修改点1：重置滤波器 ====================
    # 每次开始新关卡时重置滤波器，避免上一关的数据影响
    accel_filter.reset()
    
    # Set LED color hint based on action
    pixels.fill(OFF)
    if current_action == "ROTATE":
        pixels.fill(BLUE)
    elif current_action == "BUTTON":
        pixels.fill(GREEN)
    elif current_action == "TAP":
        pixels.fill(YELLOW)
    elif current_action == "SHAKE":
        pixels.fill(PURPLE)
    pixels.show()
    
    print(f"Level {current_level}: {current_action}, Time limit: {time_remaining:.1f}s")

def check_action():
    """Check if player completed the current action"""
    global action_completed
    
    if current_action == "ROTATE" and encoder_position != last_encoder_position:
        action_completed = True
        pixels.fill(CYAN)
        pixels.show()
        print("Rotation detected!")
        return True
        
    elif current_action == "BUTTON" and button_clicked:
        action_completed = True
        pixels.fill(GREEN)
        pixels.show()
        print("Button press detected!")
        return True
        
    elif current_action == "TAP" and accelerometer.events["tap"]:
        action_completed = True
        pixels.fill(YELLOW)
        pixels.show()
        print("Tap detected!")
        return True
        
    elif current_action == "SHAKE":
        # ==================== 修改点2：使用滤波器 ====================
        # 1. 读取原始加速度数据
        x, y, z = accelerometer.acceleration
        
        # 2. 通过滤波器处理数据（关键改进！）
        x_filtered, y_filtered, z_filtered = accel_filter.filter(x, y, z)
        
        # 3. 使用滤波后的数据计算角度
        angle_x, angle_y = calculate_angles(x_filtered, y_filtered, z_filtered)
        
        # 4. 检测摇晃
        if check_shake(angle_x, angle_y, time.monotonic()):
            action_completed = True
            pixels.fill(PURPLE)
            pixels.show()
            print("Shake detected!")
            return True
    
    return False

# Play boot animation
print("=== SQUID GAME: ACTION RUSH ===")
print("Booting...")
print("Accelerometer filter: Moving Average (window size=5)")  # 新增：显示滤波器信息
play_boot_animation()

# Display splash after animation
display.root_group = create_splash_screen()
pixels.fill(PINK)  # Pink lighting
pixels.show()
current_state = STATE_SPLASH

print("Game Ready!")
print("10 levels, 10 points each level")
print(f"Shake detection: >{shake_threshold}° for {shake_duration}s")

while True:
    current_time = time.monotonic()
    current_time_ms = current_time * 1000
    
    # Encoder handling
    encoder_changed = encoder.update()
    if encoder_changed and current_time_ms - last_encoder_time > encoder_debounce_ms:
        encoder_position = encoder.position
        last_encoder_time = current_time_ms
    
    # Button handling
    current_button_value = button.value
    if last_button_value and not current_button_value:
        button_pressed = True
        button_clicked = True
    else:
        button_clicked = False
    last_button_value = current_button_value
    
    # State machine processing
    if current_state == STATE_SPLASH:
        if button_pressed:
            current_state = STATE_DIFFICULTY_SELECT
            encoder_position = 0
            last_encoder_position = 0
            display.root_group = create_difficulty_screen()
            print("State changed: SPLASH -> DIFFICULTY_SELECT")
            button_pressed = False
    
    elif current_state == STATE_DIFFICULTY_SELECT:
        if encoder_position != last_encoder_position:
            selected_difficulty = (selected_difficulty + 1) % len(difficulties)
            display.root_group = create_difficulty_screen()
            print(f"Difficulty selected: {difficulties[selected_difficulty]}")
            last_encoder_position = encoder_position
        
        if button_pressed:
            current_state = STATE_GAME_PLAY
            current_level = 1
            score = 0
            start_level()
            display.root_group = create_game_screen()
            print(f"Game started: {difficulties[selected_difficulty]}")
            button_pressed = False
    
    elif current_state == STATE_GAME_PLAY:
        # Update time
        elapsed = current_time - game_start_time
        time_remaining = max(get_time_limit(difficulties[selected_difficulty], current_level) - elapsed, 0)
        
        # Check action completion
        if not action_completed and check_action():
            level_passed = True
            score += 10  # Fixed 10 points per level
            print(f"Level {current_level} passed! Score: {score}")
        
        # Update display
        display.root_group = create_game_screen()
        
        # Check level end conditions
        if time_remaining <= 0:
            # Time's up, failed
            pixels.fill(RED)
            pixels.show()
            time.sleep(1)
            current_state = STATE_GAME_RESULT
            display.root_group = create_result_screen(False)
            button_pressed = False
            result_screen_start_time = time.monotonic()  # Record result screen entry time
            print("Level failed - timeout")
            
        elif level_passed:
            # Action completed, proceed to next level
            time.sleep(1)
            if current_level < total_levels:
                current_level += 1
                start_level()
                display.root_group = create_game_screen()
                print(f"Starting level {current_level}")
            else:
                # All levels completed
                pixels.fill(GREEN)  # Success lighting
                pixels.show()
                time.sleep(2)  # Celebration time
                current_state = STATE_GAME_RESULT
                display.root_group = create_result_screen(True)
                button_pressed = False  # Reset button state
                result_screen_start_time = time.monotonic()  # Record result screen entry time
                # Wait for button to be fully released
                time.sleep(0.5)
                print(f"All levels completed! Final score: {score}/100")
    
    elif current_state == STATE_GAME_RESULT:
        # Prevent immediate trigger - must stay on result screen for at least 1 second
        if time.monotonic() - result_screen_start_time < 1.0:
            button_pressed = False  # Ignore button presses during this time
            last_encoder_position = encoder_position  # Ignore rotation
            continue
        
        if button_pressed:
            # Button: restart
            current_state = STATE_GAME_PLAY
            current_level = 1
            score = 0
            start_level()
            display.root_group = create_game_screen()
            print("Game restarted")
            button_pressed = False
        
        # Encoder rotation: return to menu
        if encoder_position != last_encoder_position:
            current_state = STATE_SPLASH
            display.root_group = create_splash_screen()
            pixels.fill(PINK)  # Pink lighting
            pixels.show()
            print("Returned to menu")
            last_encoder_position = encoder_position
    
    time.sleep(0.01)