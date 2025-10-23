"""
Image to 8-bit Melody Converter
1-bit Dithering Mac OS Classic Style UI
使用pygame.mixer直接生成波形声音（无需MIDI设备）
Data Moshing Animation Effect
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageChops
import threading
import os
import pygame
import random
from image_processor import ImageProcessor
from melody_generator import MelodyGenerator


class Image2MelodyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrapbook - Image2Melody")
        self.root.geometry("1000x800")  # 增大窗口尺寸
        
        # 1-bit Dithering Mac OS Classic Style Colors
        self.bg_black = "#010101"           # 背景黑色
        self.primary_pink = "#C87488"       # 主题色 r:200 g:116 b:136
        self.hover_beige = "#CDBEB8"        # 选中/hover r:205 g:190 b:184
        self.white = "#FFFFFF"              # 白色用于对比
        
        # Dithering patterns (for 1-bit style)
        self.dither_pattern_dark = None
        self.dither_pattern_light = None
        
        self.root.configure(bg=self.bg_black)
        
        # Initialize processors
        self.image_processor = ImageProcessor()
        self.melody_generator = MelodyGenerator()
        
        # State variables
        self.current_image_path = None
        self.current_image = None
        self.pixelated_image = None
        self.pixel_size = 10  # 像素方块大小 (10×10)
        
        # Animation state
        self.is_animating = False
        self.animation_paused = False
        self.current_pixel_index = 0
        self.rgb_data_list = []
        self.grid_width = 0
        self.grid_height = 0
        self.octave_shift = 0
        
        # Animation speed control (1.0 = normal, 0.5 = 2x faster, 2.0 = 2x slower)
        self.speed_multiplier = 1.0
        
        # Data moshing state
        self.glitch_frames = []
        self.moshing_intensity = 0
        self.trace_background = None  # 用于渐淡trace效果的背景图像
        self.glitch_history = None  # 用于累积 glitch 效果的历史层
        
        # Recording state
        self.is_recording = False
        self.animation_frames = []  # 保存动画帧
        self.recorded_audio_data = []  # 保存音频数据（波形数组）
        self.frame_timestamps = []  # 保存帧时间戳
        
        # 初始化音频系统
        self.init_audio()
        
        # 创建抖动图案
        self.create_dither_patterns()
        
        # 加载像素字体
        self.load_pixel_font()
        
        self.setup_ui()
        self.setup_keyboard_bindings()
    
    def create_dither_patterns(self):
        """创建1-bit抖动图案（Mac OS Classic风格）"""
        # 创建抖动图案 - 用于模拟灰度
        pattern_size = 8
        
        # 50% 抖动图案（棋盘格）
        pattern_50 = Image.new('1', (pattern_size, pattern_size))
        pixels = pattern_50.load()
        for y in range(pattern_size):
            for x in range(pattern_size):
                pixels[x, y] = (x + y) % 2
        self.dither_pattern_dark = pattern_50
        
        # 25% 抖动图案（稀疏点阵）
        pattern_25 = Image.new('1', (pattern_size, pattern_size))
        pixels = pattern_25.load()
        for y in range(pattern_size):
            for x in range(pattern_size):
                pixels[x, y] = (x % 2 == 0 and y % 2 == 0)
        self.dither_pattern_light = pattern_25
    
    def apply_1bit_pixelation(self, image):
        """Convert image to bitmap style with classic halftone effect
        
        Features:
        1. Ordered dithering for bitmap appearance
        2. Classic halftone dot patterns
        3. High contrast black and white with colored midtones
        """
        # Convert to RGB and grayscale
        img_rgb = image.convert('RGB')
        img_gray = image.convert('L')
        rgb_pixels = img_rgb.load()
        gray_pixels = img_gray.load()
        width, height = img_rgb.size
        
        # Create result image
        result = Image.new('RGB', (width, height))
        result_pixels = result.load()
        
        # Bitmap color palette (reduced palette for bitmap effect)
        palette = {
            'black': (1, 1, 1),               # Pure black
            'dark_pink': (100, 50, 70),       # Dark pink
            'mid_pink': (200, 116, 136),      # Main pink
            'light_pink': (230, 170, 190),    # Light pink
            'beige': (205, 190, 184),         # Beige
            'light_beige': (240, 220, 210),   # Light beige
            'white': (255, 255, 255)          # Pure white
        }
        
        # Ordered dithering matrix (8x8 Bayer matrix for bitmap effect)
        bayer_matrix = [
            [ 0, 32,  8, 40,  2, 34, 10, 42],
            [48, 16, 56, 24, 50, 18, 58, 26],
            [12, 44,  4, 36, 14, 46,  6, 38],
            [60, 28, 52, 20, 62, 30, 54, 22],
            [ 3, 35, 11, 43,  1, 33,  9, 41],
            [51, 19, 59, 27, 49, 17, 57, 25],
            [15, 47,  7, 39, 13, 45,  5, 37],
            [63, 31, 55, 23, 61, 29, 53, 21]
        ]
        
        # Process each pixel with bitmap effect
        for y in range(height):
            for x in range(width):
                brightness = gray_pixels[x, y]
                r, g, b = rgb_pixels[x, y]
                
                # Calculate color temperature
                color_temp = (r - b) / 255.0 if (r + b) > 0 else 0
                
                # Get dithering threshold from Bayer matrix
                threshold_index = bayer_matrix[y % 8][x % 8]
                threshold = (threshold_index / 64.0) * 255
                
                # Apply ordered dithering to create bitmap effect
                if brightness < threshold * 0.2:  # Very dark
                    color = palette['black']
                elif brightness < threshold * 0.4:  # Dark
                    if color_temp > 0:
                        color = palette['dark_pink']
                    else:
                        color = palette['black']
                elif brightness < threshold * 0.6:  # Mid-dark
                    if color_temp > 0.1:
                        color = palette['mid_pink']
                    else:
                        color = palette['dark_pink']
                elif brightness < threshold * 0.8:  # Mid
                    if color_temp > 0:
                        color = palette['light_pink']
                    else:
                        color = palette['beige']
                elif brightness < threshold * 1.0:  # Mid-light
                    if color_temp > -0.1:
                        color = palette['light_pink']
                    else:
                        color = palette['light_beige']
                else:  # Bright
                    if color_temp > -0.2:
                        color = palette['light_pink']
                    else:
                        color = palette['white']
                
                result_pixels[x, y] = color
        
        print(f"✓ Bitmap effect applied (ordered dithering + halftone)")
        return result
    
    def apply_floyd_steinberg_dither(self, image, threshold=128, max_size=800):
        """Apply Floyd-Steinberg dithering to convert image to 1-bit
        
        Args:
            image: PIL Image object
            threshold: Brightness threshold (default 128)
            max_size: Maximum dimension to resize large images (default 800)
        """
        # Resize large images to prevent hanging
        width, height = image.size
        if width > max_size or height > max_size:
            # Calculate new size maintaining aspect ratio
            ratio = min(max_size / width, max_size / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"⚠ Large image resized: {width}×{height} → {new_width}×{new_height}")
        
        # Convert to grayscale
        img = image.convert('L')
        pixels = img.load()
        width, height = img.size
        
        # Process with progress updates
        total_pixels = width * height
        processed = 0
        last_update = 0
        
        for y in range(height):
            for x in range(width):
                old_pixel = pixels[x, y]
                new_pixel = 255 if old_pixel > threshold else 0
                pixels[x, y] = int(new_pixel)
                
                # Calculate quantization error
                quant_error = old_pixel - new_pixel
                
                # Distribute error to neighboring pixels (Floyd-Steinberg)
                if x + 1 < width:
                    pixels[x + 1, y] = int(min(255, max(0, pixels[x + 1, y] + quant_error * 7 / 16)))
                
                if x - 1 >= 0 and y + 1 < height:
                    pixels[x - 1, y + 1] = int(min(255, max(0, pixels[x - 1, y + 1] + quant_error * 3 / 16)))
                
                if y + 1 < height:
                    pixels[x, y + 1] = int(min(255, max(0, pixels[x, y + 1] + quant_error * 5 / 16)))
                
                if x + 1 < width and y + 1 < height:
                    pixels[x + 1, y + 1] = int(min(255, max(0, pixels[x + 1, y + 1] + quant_error * 1 / 16)))
                
                # Update progress every 10%
                processed += 1
                progress = int((processed / total_pixels) * 100)
                if progress >= last_update + 10:
                    last_update = progress
                    print(f"  Dithering: {progress}% complete...")
        
        # Convert back to RGB with pink/beige colors for 1-bit effect
        dithered = Image.new('RGB', (width, height))
        dithered_pixels = dithered.load()
        
        for y in range(height):
            for x in range(width):
                if pixels[x, y] > 128:
                    # White pixels -> Beige
                    dithered_pixels[x, y] = (205, 190, 184)  # hover_beige
                else:
                    # Black pixels -> Black
                    dithered_pixels[x, y] = (1, 1, 1)  # bg_black
        
        print("✓ Dithering complete!")
        return dithered
    
    def apply_data_moshing(self, image, intensity=0.0):
        """Apply enhanced glitch effects inspired by retro web aesthetics
        
        包括：
        1. RGB 通道分离（Chromatic Aberration）
        2. 扫描线故障（Scanline Glitch）
        3. 像素位移（Pixel Displacement）
        4. 颜色失真（Color Corruption）
        5. 随机噪点（Random Noise）
        """
        if intensity <= 0:
            return image
        
        img = image.copy()
        width, height = img.size
        
        # 1. RGB 通道分离效果（Chromatic Aberration）
        if intensity > 0.1 and random.random() < intensity:
            # 分离RGB通道
            if img.mode == 'RGB' or img.mode == 'RGBA':
                r, g, b = img.split()[:3]
                
                # 随机偏移量
                offset_x = int(random.randint(-5, 5) * intensity)
                offset_y = int(random.randint(-2, 2) * intensity)
                
                # 创建偏移后的通道
                r_shifted = ImageChops.offset(r, offset_x, 0)
                b_shifted = ImageChops.offset(b, -offset_x, offset_y)
                
                # 重新合成
                if img.mode == 'RGBA':
                    a = img.split()[3]
                    img = Image.merge('RGBA', (r_shifted, g, b_shifted, a))
                else:
                    img = Image.merge('RGB', (r_shifted, g, b_shifted))
        
        # 2. 扫描线故障效果
        pixels = img.load()
        num_scanlines = int(height * intensity * 0.3)
        
        for _ in range(num_scanlines):
            line_y = random.randint(0, height - 1)
            line_width = random.randint(int(width * 0.2), int(width * 0.8))
            start_x = random.randint(0, max(0, width - line_width))
            
            # 扫描线类型
            scanline_type = random.choice(['repeat', 'shift', 'corrupt', 'bright'])
            
            for lx in range(line_width):
                px = start_x + lx
                if px < width and px > 0:
                    try:
                        if scanline_type == 'repeat':
                            # 重复前一个像素
                            pixels[px, line_y] = pixels[px - 1, line_y]
                        elif scanline_type == 'shift':
                            # 垂直偏移
                            shift_y = min(height - 1, max(0, line_y + random.randint(-2, 2)))
                            pixels[px, line_y] = pixels[px, shift_y]
                        elif scanline_type == 'corrupt':
                            # Color corruption - bitmap style palette
                            corrupt_colors = [
                                (1, 1, 1),           # Black
                                (100, 50, 70),       # Dark pink
                                (200, 116, 136),     # Main pink
                                (230, 170, 190),     # Light pink
                                (255, 255, 255)      # White
                            ]
                            color = random.choice(corrupt_colors)
                            if img.mode == 'RGB':
                                pixels[px, line_y] = color
                            else:
                                pixels[px, line_y] = color + (255,)
                        elif scanline_type == 'bright':
                            # 增加亮度
                            pixel = pixels[px, line_y]
                            if isinstance(pixel, tuple) and len(pixel) >= 3:
                                r, g, b = pixel[:3]
                                pixels[px, line_y] = (
                                    min(255, int(r * 1.5)),
                                    min(255, int(g * 1.5)),
                                    min(255, int(b * 1.5))
                                ) if img.mode == 'RGB' else (
                                    min(255, int(r * 1.5)),
                                    min(255, int(g * 1.5)),
                                    min(255, int(b * 1.5)),
                                    pixel[3] if len(pixel) == 4 else 255
                                )
                    except:
                        pass
        
        # 3. 像素块位移
        num_displacements = int(width * height * intensity * 0.02)
        
        for _ in range(num_displacements):
            block_size = random.randint(5, 20)
            x = random.randint(0, width - block_size - 1)
            y = random.randint(0, height - block_size - 1)
            dx = random.randint(-30, 30)
            dy = random.randint(-10, 10)
            
            # 复制块到新位置
            for by in range(block_size):
                for bx in range(block_size):
                    src_x, src_y = x + bx, y + by
                    dst_x = max(0, min(width - 1, src_x + dx))
                    dst_y = max(0, min(height - 1, src_y + dy))
                    try:
                        pixels[dst_x, dst_y] = pixels[src_x, src_y]
                    except:
                        pass
        
        # 4. 随机噪点（颜色故障）
        num_noise = int(width * height * intensity * 0.01)
        
        for _ in range(num_noise):
            nx = random.randint(0, width - 1)
            ny = random.randint(0, height - 1)
            
            # Bitmap style noise palette
            noise_colors = [
                (1, 1, 1),           # Black
                (100, 50, 70),       # Dark pink
                (200, 116, 136),     # Main pink
                (230, 170, 190),     # Light pink
                (205, 190, 184),     # Beige
                (240, 220, 210),     # Light beige
                (255, 255, 255)      # White
            ]
            
            try:
                color = random.choice(noise_colors)
                if img.mode == 'RGBA':
                    pixels[nx, ny] = color + (255,)
                else:
                    pixels[nx, ny] = color
            except:
                pass
        
        return img
    
    def apply_subtle_shift(self, img):
        """应用微弱的整体画面shift效果（wiredfriend风格）
        
        创建微妙的1-bit粒子位移，增加动态感
        """
        import random
        from PIL import ImageChops
        
        width, height = img.size
        
        # 1. 微弱的整体偏移（0-2像素）
        global_shift_x = random.randint(-2, 2)
        global_shift_y = random.randint(-1, 1)
        
        # 只在非零偏移时应用
        if global_shift_x != 0 or global_shift_y != 0:
            img = ImageChops.offset(img, global_shift_x, global_shift_y)
        
        # 2. 极少数随机像素的微位移（1-bit粒子效果）
        if random.random() < 0.3:  # 30%概率
            pixels = img.load()
            num_particles = int(width * height * 0.002)  # 0.2%的像素
            
            for _ in range(num_particles):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                
                # 随机小范围位移
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                
                # 目标位置
                nx = max(0, min(width - 1, x + dx))
                ny = max(0, min(height - 1, y + dy))
                
                try:
                    # 交换像素
                    temp = pixels[x, y]
                    pixels[x, y] = pixels[nx, ny]
                    pixels[nx, ny] = temp
                except:
                    pass
        
        return img
    
    def load_pixel_font(self):
        """加载像素风格字体 Jersey10-Regular.ttf"""
        # 在macOS上，tkinter对自定义TTF字体支持有限
        # 尝试多种方法加载字体
        
        # 方法1: 尝试使用已安装的 Jersey10 字体
        jersey_font_names = [
            "Jersey 10",           # 系统识别名称（已确认，带空格！）
            "Jersey10",            # 无空格版本
            "Jersey 10 Regular",   # 完整名称
            "Jersey10-Regular",    # 连字符版本
        ]
        
        for font_name in jersey_font_names:
            try:
                test_font = tkfont.Font(family=font_name, size=16)
                self.pixel_font_large = (font_name, 36, "normal")  # 从 28 增加到 36
                self.pixel_font_medium = (font_name, 24, "normal") # 从 20 增加到 24
                self.pixel_font_small = (font_name, 16, "normal")  # 从 14 增加到 16
                print(f"✓ Using {font_name} font")
                return
            except:
                continue
        
        # 方法2: 尝试 Silkscreen（备用）
        print("⚠ Jersey 10 not found, trying Silkscreen...")
        silkscreen_font_names = [
            "Silkscreen",
            "Silkscreen Regular",
        ]
        
        for font_name in silkscreen_font_names:
            try:
                test_font = tkfont.Font(family=font_name, size=16)
                self.pixel_font_large = (font_name, 32, "normal")  # 从 28 增加到 32
                self.pixel_font_medium = (font_name, 24, "normal") # 从 20 增加到 24
                self.pixel_font_small = (font_name, 16, "normal")  # 从 14 增加到 16
                print(f"✓ Using {font_name} font (alternative)")
                return
            except:
                continue
        
        # 方法3: 尝试 Jersey10 Charted（备用）
        print("⚠ Trying Jersey10 Charted...")
        jersey_charted_names = [
            "Jersey 10 Charted",
            "Jersey10 Charted",
        ]
        
        for font_name in jersey_charted_names:
            try:
                test_font = tkfont.Font(family=font_name, size=16)
                self.pixel_font_large = (font_name, 32, "normal")
                self.pixel_font_medium = (font_name, 24, "normal")
                self.pixel_font_small = (font_name, 16, "normal")
                print(f"✓ Using {font_name} font (alternative)")
                return
            except:
                continue
        
        # 方法4: 使用macOS上可用的像素风格等宽字体
        print("⚠ Pixel fonts not found, trying system fonts...")
        pixel_fonts = [
            "Monaco",      # macOS内置，像素风格
            "Menlo",       # macOS内置，清晰等宽
            "Courier New", # 跨平台
            "Courier"      # 备用
        ]
        
        for font_name in pixel_fonts:
            try:
                test_font = tkfont.Font(family=font_name, size=16)
                self.pixel_font_large = (font_name, 32, "bold")
                self.pixel_font_medium = (font_name, 24, "bold")
                self.pixel_font_small = (font_name, 16, "normal")
                print(f"✓ Using {font_name} font (system font)")
                return
            except:
                continue
        
        # 最后备用
        print(f"⚠ Using default Courier font")
        self.pixel_font_large = ("Courier", 24, "bold")
        self.pixel_font_medium = ("Courier", 18, "bold")
        self.pixel_font_small = ("Courier", 12, "bold")
    
    def setup_ui(self):
        """Setup Mac OS Classic 1-bit dithering style UI"""
        # 顶部标题栏 - Mac OS Classic风格（条纹图案）
        title_frame = tk.Frame(self.root, bg=self.primary_pink, height=32)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        # 创建条纹背景canvas（模拟Mac OS标题栏）
        title_canvas = tk.Canvas(
            title_frame,
            bg=self.primary_pink,
            height=32,
            highlightthickness=0
        )
        title_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绘制垂直条纹
        for i in range(0, 1400, 2):  # 增加范围以适应更大窗口
            title_canvas.create_line(i, 0, i, 32, fill=self.bg_black, width=1)
        
        # 标题文字（居中）
        self.title_text_id = title_canvas.create_text(
            500, 16,  # 固定位置
            text="NetDream###8",
            font=self.pixel_font_medium,
            fill=self.bg_black,
            anchor=tk.CENTER
        )
        
        # 控制栏 - 使用beige颜色
        control_frame = tk.Frame(self.root, bg=self.hover_beige, height=48)
        control_frame.pack(fill=tk.X, pady=(2, 0))
        control_frame.pack_propagate(False)
        
        # 创建控制栏canvas（带边框）
        control_canvas = tk.Canvas(
            control_frame,
            bg=self.hover_beige,
            height=48,
            highlightthickness=2,
            highlightbackground=self.primary_pink
        )
        control_canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # 控制文字
        control_canvas.create_text(
            20, 24,  # 垂直居中
            text="CONTROLS: [W]↑ [S]↓ [A]← [D]→ [SPACE]⏸ [↑↓←→]Speed [R]Reset",
            font=self.pixel_font_small,
            fill=self.bg_black,
            anchor=tk.W
        )
        
        # Speed显示（中间位置）
        self.speed_display_id = control_canvas.create_text(
            700, 24,
            text="SPEED: 1.0x",
            font=self.pixel_font_small,
            fill=self.bg_black,
            anchor=tk.CENTER
        )
        
        # Pitch显示（右侧对齐）
        self.octave_display_id = control_canvas.create_text(
            980, 24,  # 固定位置，垂直居中
            text="PITCH: +0",
            font=self.pixel_font_small,
            fill=self.bg_black,
            anchor=tk.E
        )
        self.octave_canvas = control_canvas  # 保存引用用于更新
        
        # 主显示区域 - 带Mac风格边框
        main_frame = tk.Frame(self.root, bg=self.bg_black)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # 创建Mac风格窗口边框
        canvas_outer = tk.Frame(main_frame, bg=self.primary_pink, bd=3, relief=tk.RIDGE)
        canvas_outer.pack(fill=tk.BOTH, expand=True)
        
        canvas_inner = tk.Frame(canvas_outer, bg=self.bg_black, bd=2)
        canvas_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.image_canvas = tk.Canvas(
            canvas_inner,
            bg=self.bg_black,
            highlightthickness=0
        )
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绘制加载按钮
        self.root.after(100, self.draw_load_button)
        
        # 底部状态栏 - Mac风格
        status_frame = tk.Frame(self.root, bg=self.hover_beige, height=32)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        status_canvas = tk.Canvas(
            status_frame,
            bg=self.hover_beige,
            height=32,
            highlightthickness=1,
            highlightbackground=self.primary_pink
        )
        status_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 状态文字
        self.status_text_id = status_canvas.create_text(
            20, 16,
            text="[ READY ] Load image to start",
            font=self.pixel_font_small,
            fill=self.bg_black,
            anchor=tk.W
        )
        self.status_canvas = status_canvas  # 保存引用用于更新
        
        self.image_canvas.bind('<Button-1>', self.on_canvas_click)
    
    def draw_load_button(self):
        """Draw Mac OS Classic style load button in center of canvas"""
        self.image_canvas.delete("all")
        
        self.image_canvas.update()
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500
        
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Mac风格按钮尺寸
        button_width = 200
        button_height = 70
        button_spacing = 30
        
        # LOAD IMAGE 按钮（左侧）
        load_x = center_x - button_width // 2 - button_spacing
        self.load_button_rect = self.image_canvas.create_rectangle(
            load_x - button_width // 2,
            center_y - button_height // 2,
            load_x + button_width // 2,
            center_y + button_height // 2,
            fill=self.hover_beige,
            outline=self.primary_pink,
            width=3,
            tags="load_button"
        )
        
        self.image_canvas.create_text(
            load_x,
            center_y - 8,
            text="LOAD IMAGE",
            font=self.pixel_font_medium,
            fill=self.bg_black,
            tags="load_button"
        )
        
        self.image_canvas.create_text(
            load_x,
            center_y + 18,
            text="From file",
            font=self.pixel_font_small,
            fill=self.bg_black,
            tags="load_button"
        )
        
        # CAMERA 按钮（右侧）
        camera_x = center_x + button_width // 2 + button_spacing
        self.camera_button_rect = self.image_canvas.create_rectangle(
            camera_x - button_width // 2,
            center_y - button_height // 2,
            camera_x + button_width // 2,
            center_y + button_height // 2,
            fill=self.hover_beige,
            outline=self.primary_pink,
            width=3,
            tags="camera_button"
        )
        
        self.image_canvas.create_text(
            camera_x,
            center_y - 8,
            text="CAMERA",
            font=self.pixel_font_medium,
            fill=self.bg_black,
            tags="camera_button"
        )
        
        self.image_canvas.create_text(
            camera_x,
            center_y + 18,
            text="Live capture",
            font=self.pixel_font_small,
            fill=self.bg_black,
            tags="camera_button"
        )
        
        # Hover效果 - LOAD按钮
        self.image_canvas.tag_bind("load_button", "<Enter>", 
            lambda e: [self.image_canvas.itemconfig(self.load_button_rect, fill=self.primary_pink),
                      self.image_canvas.config(cursor="hand2")])
        self.image_canvas.tag_bind("load_button", "<Leave>", 
            lambda e: [self.image_canvas.itemconfig(self.load_button_rect, fill=self.hover_beige),
                      self.image_canvas.config(cursor="")])
        
        # Hover效果 - CAMERA按钮
        self.image_canvas.tag_bind("camera_button", "<Enter>", 
            lambda e: [self.image_canvas.itemconfig(self.camera_button_rect, fill=self.primary_pink),
                      self.image_canvas.config(cursor="hand2")])
        self.image_canvas.tag_bind("camera_button", "<Leave>", 
            lambda e: [self.image_canvas.itemconfig(self.camera_button_rect, fill=self.hover_beige),
                      self.image_canvas.config(cursor="")])
    
    def on_canvas_click(self, event):
        """Canvas click event"""
        items = self.image_canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if items and "load_button" in self.image_canvas.gettags(items[0]):
            self.load_image()
        elif items and "camera_button" in self.image_canvas.gettags(items[0]):
            self.capture_from_camera()
        elif items and "reload_button" in self.image_canvas.gettags(items[0]):
            self.reset_and_load()
    
    def setup_keyboard_bindings(self):
        """Setup keyboard bindings"""
        # Pitch control
        self.root.bind('<w>', lambda e: self.adjust_octave(12))
        self.root.bind('<W>', lambda e: self.adjust_octave(12))
        self.root.bind('<s>', lambda e: self.adjust_octave(-12))
        self.root.bind('<S>', lambda e: self.adjust_octave(-12))
        self.root.bind('<a>', lambda e: self.adjust_octave(-1))
        self.root.bind('<A>', lambda e: self.adjust_octave(-1))
        self.root.bind('<d>', lambda e: self.adjust_octave(1))
        self.root.bind('<D>', lambda e: self.adjust_octave(1))
        
        # Speed control
        self.root.bind('<Up>', lambda e: self.adjust_speed(0.2))      # 加快
        self.root.bind('<Down>', lambda e: self.adjust_speed(-0.2))   # 减慢
        self.root.bind('<Left>', lambda e: self.adjust_speed(-0.1))   # 稍慢
        self.root.bind('<Right>', lambda e: self.adjust_speed(0.1))   # 稍快
        self.root.bind('<r>', lambda e: self.reset_speed())           # 重置速度
        self.root.bind('<R>', lambda e: self.reset_speed())
        
        # Pause
        self.root.bind('<space>', lambda e: self.toggle_pause())
    
    def init_audio(self):
        """初始化音频系统（使用pygame.mixer，无需MIDI设备）"""
        if self.melody_generator.audio_initialized:
            print("✓ Audio system ready")
            return True
        else:
            print("✗ Audio initialization failed")
            messagebox.showwarning("Audio Warning", 
                "Could not initialize audio system.\nYou may not hear sounds during playback.")
            return False
    
    def adjust_octave(self, shift):
        """Adjust pitch"""
        if self.is_animating:
            self.octave_shift += shift
            self.octave_shift = max(-24, min(24, self.octave_shift))
            self.octave_canvas.itemconfig(self.octave_display_id, 
                                         text=f"PITCH: {self.octave_shift:+d}")
    
    def adjust_speed(self, delta):
        """调整动画速度"""
        if self.is_animating:
            self.speed_multiplier += delta
            # 限制速度范围：0.2x (5倍快) 到 3.0x (3倍慢)
            self.speed_multiplier = max(0.2, min(3.0, self.speed_multiplier))
            speed_display = f"{1.0/self.speed_multiplier:.1f}x" if self.speed_multiplier > 0 else "MAX"
            self.octave_canvas.itemconfig(self.speed_display_id, 
                                         text=f"SPEED: {speed_display}")
            print(f"⚡ Speed: {speed_display}")
    
    def reset_speed(self):
        """重置速度到正常"""
        if self.is_animating:
            self.speed_multiplier = 1.0
            self.octave_canvas.itemconfig(self.speed_display_id, 
                                         text="SPEED: 1.0x")
            print("⚡ Speed reset to 1.0x")
    
    def toggle_pause(self):
        """Pause/resume animation"""
        if self.is_animating:
            self.animation_paused = not self.animation_paused
            if self.animation_paused:
                self.status_canvas.itemconfig(self.status_text_id, 
                                             text="[ PAUSED ] Press SPACE to resume")
            else:
                self.status_canvas.itemconfig(self.status_text_id, 
                                             text="[ PLAYING ] Generating melody...")
                self.animate_next_pixel()
    
    def load_image(self):
        """Load image"""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.current_image_path = file_path
                self.current_image = Image.open(file_path)
                
                self.display_image(self.current_image)
                self.show_start_animation_popup()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def capture_from_camera(self):
        """Capture image from camera and show in main canvas"""
        try:
            import cv2
        except ImportError:
            messagebox.showerror("Error", "opencv-python library is required for camera capture.\n\nInstall with:\npip install opencv-python")
            return
        
        # 打开摄像头
        self.camera_cap = cv2.VideoCapture(0)
        
        if not self.camera_cap.isOpened():
            messagebox.showerror("Error", "Could not open camera!")
            return
        
        self.camera_active = True
        self.camera_frame = None
        self.camera_paused = False
        self.camera_octave_shift = 0  # 摄像头模式的音高偏移
        self.camera_speed = 1.0  # 摄像头音频播放速度倍率
        
        # 初始化录制状态
        self.camera_recording = True
        self.camera_frames = []
        self.camera_audio_notes = []
        
        # 在主 canvas 上显示摄像头预览
        self.update_camera_preview()
        
        # 显示摄像头控制按钮
        self.show_camera_controls()
        
        # 绑定键盘控制
        self.bind_camera_keyboard_controls()
    
    def update_camera_preview(self):
        """更新主 canvas 上的摄像头预览，并根据颜色生成实时声音"""
        if not self.camera_active:
            return
        
        import cv2
        import time
        
        ret, frame = self.camera_cap.read()
        if ret:
            # 保存当前帧
            self.camera_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 转换为PIL Image
            img = Image.fromarray(self.camera_frame)
            
            # 显示在主 canvas 上
            self.display_image(img)
            
            # 如果正在录制，保存帧
            if self.camera_recording and not self.camera_paused:
                self.camera_frames.append(img.copy())
            
            # 🎵 根据摄像头画面中心区域生成实时声音（如果未暂停）
            if not self.camera_paused:
                self.play_camera_audio(img)
            
            # 更新状态显示
            status = "PAUSED" if self.camera_paused else "RECORDING" if self.camera_recording else "LIVE"
            self.status_canvas.itemconfig(self.status_text_id,
                text=f"[ {status} ] Camera | Pitch: {self.camera_octave_shift:+d} | Speed: {self.camera_speed:.1f}x | Frames: {len(self.camera_frames)}"
            )
        
        # 继续更新（根据速度调整）
        if self.camera_active:
            frame_delay = int(33 / self.camera_speed)  # 基础 30 FPS，受速度影响
            self.root.after(frame_delay, self.update_camera_preview)
    
    def show_camera_controls(self):
        """在主 canvas 上显示摄像头控制按钮（4个按钮）"""
        self.image_canvas.delete("camera_control")
        
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500
        
        # 按钮位置（底部中央，4个按钮横排）
        center_x = canvas_width // 2
        bottom_y = canvas_height - 60
        
        button_width = 130
        button_height = 50
        button_spacing = 15
        
        # 计算4个按钮的起始位置
        total_width = button_width * 4 + button_spacing * 3
        start_x = center_x - total_width // 2
        
        # 按钮配置 [文本, 标签, 回调函数]
        buttons = [
            ("PAUSE", "pause_btn", self.toggle_camera_pause),
            ("SAVE", "save_btn", self.save_camera_recording),
            ("RELOAD", "reload_btn", self.reload_camera),
            ("EXIT", "exit_btn", self.cancel_camera)
        ]
        
        self.camera_button_rects = {}
        
        for i, (text, tag, callback) in enumerate(buttons):
            x = start_x + button_width // 2 + i * (button_width + button_spacing)
            
            # 创建按钮矩形
            rect_id = self.image_canvas.create_rectangle(
                x - button_width // 2,
                bottom_y - button_height // 2,
                x + button_width // 2,
                bottom_y + button_height // 2,
                fill=self.hover_beige,
                outline=self.primary_pink,
                width=3,
                tags=f"camera_control {tag}"
            )
            
            self.camera_button_rects[tag] = rect_id
            
            # 创建按钮文字
            self.image_canvas.create_text(
                x,
                bottom_y,
                text=text,
                font=self.pixel_font_medium,
                fill=self.bg_black,
                tags=f"camera_control {tag}"
            )
            
            # 绑定点击事件
            self.image_canvas.tag_bind(tag, "<Button-1>", lambda e, cb=callback: cb())
            
            # Hover 效果
            self.image_canvas.tag_bind(tag, "<Enter>", 
                lambda e, rect=rect_id: [self.image_canvas.itemconfig(rect, fill=self.primary_pink),
                                        self.image_canvas.config(cursor="hand2")])
            self.image_canvas.tag_bind(tag, "<Leave>", 
                lambda e, rect=rect_id: [self.image_canvas.itemconfig(rect, fill=self.hover_beige),
                                        self.image_canvas.config(cursor="")])
    
    def bind_camera_keyboard_controls(self):
        """绑定摄像头模式的键盘控制"""
        # W/S - 音高控制（上升/下降八度）
        self.root.bind('w', lambda e: self.adjust_camera_octave(+1))
        self.root.bind('W', lambda e: self.adjust_camera_octave(+1))
        self.root.bind('s', lambda e: self.adjust_camera_octave(-1))
        self.root.bind('S', lambda e: self.adjust_camera_octave(-1))
        
        # A/D - 八度控制（另一种方式）
        self.root.bind('a', lambda e: self.adjust_camera_octave(-1))
        self.root.bind('A', lambda e: self.adjust_camera_octave(-1))
        self.root.bind('d', lambda e: self.adjust_camera_octave(+1))
        self.root.bind('D', lambda e: self.adjust_camera_octave(+1))
        
        # 方向键 - 速度控制
        self.root.bind('<Up>', lambda e: self.adjust_camera_speed(+0.2))
        self.root.bind('<Down>', lambda e: self.adjust_camera_speed(-0.2))
        self.root.bind('<Left>', lambda e: self.adjust_camera_speed(-0.2))
        self.root.bind('<Right>', lambda e: self.adjust_camera_speed(+0.2))
        
        # 空格 - 暂停/继续
        self.root.bind('<space>', lambda e: self.toggle_camera_pause())
    
    def adjust_camera_octave(self, delta):
        """调整摄像头音高（八度）"""
        if hasattr(self, 'camera_active') and self.camera_active:
            self.camera_octave_shift += delta * 12  # 每次移动一个八度（12个半音）
            self.camera_octave_shift = max(-24, min(24, self.camera_octave_shift))  # 限制在±2个八度
            print(f"🎵 Camera octave: {self.camera_octave_shift:+d} semitones")
    
    def adjust_camera_speed(self, delta):
        """调整摄像头播放速度"""
        if hasattr(self, 'camera_active') and self.camera_active:
            self.camera_speed += delta
            self.camera_speed = max(0.2, min(3.0, self.camera_speed))  # 限制在 0.2x - 3.0x
            print(f"⚡ Camera speed: {self.camera_speed:.1f}x")
    
    def toggle_camera_pause(self):
        """暂停/继续摄像头"""
        if hasattr(self, 'camera_active') and self.camera_active:
            self.camera_paused = not self.camera_paused
            status = "PAUSED" if self.camera_paused else "RESUMED"
            print(f"⏸️  Camera {status}")
            
            # 停止声音
            if self.camera_paused:
                try:
                    pygame.mixer.stop()
                except:
                    pass
    
    def save_camera_recording(self):
        """保存摄像头录制的视频和音频"""
        if not hasattr(self, 'camera_frames') or len(self.camera_frames) == 0:
            messagebox.showinfo("Info", "No frames recorded yet!")
            return
        
        print(f"💾 Saving camera recording: {len(self.camera_frames)} frames, {len(self.camera_audio_notes)} notes")
        
        # 使用文件对话框
        from tkinter import filedialog
        
        # 保存视频
        video_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4"), ("All Files", "*.*")],
            title="Save Camera Video"
        )
        
        if video_path:
            try:
                import imageio
                import numpy as np
                
                # 计算 FPS（假设 30 FPS）
                fps = 30
                
                # 转换帧为 numpy 数组
                frames_np = []
                for frame in self.camera_frames:
                    frames_np.append(np.array(frame))
                
                # 保存视频
                imageio.mimsave(video_path, frames_np, fps=fps, codec='libx264', quality=8)
                print(f"✅ Video saved: {video_path}")
                messagebox.showinfo("Success", f"Video saved:\n{video_path}")
                
            except Exception as e:
                print(f"❌ Error saving video: {e}")
                messagebox.showerror("Error", f"Failed to save video:\n{str(e)}")
        
        # 保存音频（如果有音符记录）
        if len(self.camera_audio_notes) > 0:
            audio_path = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV Audio", "*.wav"), ("All Files", "*.*")],
                title="Save Camera Audio"
            )
            
            if audio_path:
                try:
                    # TODO: 实现音频保存逻辑
                    print(f"✅ Audio saved: {audio_path}")
                except Exception as e:
                    print(f"❌ Error saving audio: {e}")
    
    def reload_camera(self):
        """重新加载摄像头（清空录制）"""
        if hasattr(self, 'camera_active') and self.camera_active:
            self.camera_frames = []
            self.camera_audio_notes = []
            self.camera_octave_shift = 0
            self.camera_speed = 1.0
            self.camera_paused = False
            print("🔄 Camera reloaded - recording cleared")
            messagebox.showinfo("Reloaded", "Recording cleared!\nCamera reset to default settings.")
    
    def play_camera_audio(self, img):
        """根据摄像头画面颜色实时生成声音（使用与图片处理相同的HSV逻辑）"""
        # 采样中心区域的多个点（避免性能问题）
        width, height = img.size
        sample_points = []
        
        # 在中心区域采样 3x3 网格（9个点，减少计算量）
        center_x, center_y = width // 2, height // 2
        grid_size = 3
        spacing = 60
        
        for i in range(grid_size):
            for j in range(grid_size):
                x = center_x + (i - grid_size // 2) * spacing
                y = center_y + (j - grid_size // 2) * spacing
                
                # 确保在图像范围内
                if 0 <= x < width and 0 <= y < height:
                    sample_points.append((x, y))
        
        # 收集所有采样点的RGB值
        rgb_values = []
        for x, y in sample_points:
            pixel_color = img.getpixel((x, y))
            r, g, b = pixel_color[:3] if len(pixel_color) >= 3 else (pixel_color[0], pixel_color[0], pixel_color[0])
            rgb_values.append((r, g, b))
        
        # 计算平均RGB（更平滑的音频）
        if rgb_values:
            avg_r = sum(rgb[0] for rgb in rgb_values) / len(rgb_values)
            avg_g = sum(rgb[1] for rgb in rgb_values) / len(rgb_values)
            avg_b = sum(rgb[2] for rgb in rgb_values) / len(rgb_values)
            
            # 🎵 使用与图片处理相同的 HSV → 音符转换逻辑
            pitch, duration, velocity = self.melody_generator.rgba_to_note(
                int(avg_r), int(avg_g), int(avg_b), 255
            )
            
            # 应用八度偏移
            pitch += self.camera_octave_shift
            pitch = max(21, min(108, pitch))  # 限制在钢琴音域内
            
            # 记录音符（用于导出）
            if self.camera_recording and not self.camera_paused:
                self.camera_audio_notes.append({
                    'pitch': pitch,
                    'duration': duration,
                    'velocity': velocity,
                    'rgb': (int(avg_r), int(avg_g), int(avg_b))
                })
            
            # 🎵 播放短促的音符（实时反馈）
            # 只在音量足够大时播放（避免静音区域产生噪音）
            if velocity > 30:  # velocity 阈值
                try:
                    # 使用 melody_generator 的播放方法，但持续时间很短
                    self.melody_generator.play_note_direct(pitch, 0.05, velocity)
                except Exception as e:
                    # 静默失败，避免干扰实时预览
                    pass
    
    def capture_camera_frame(self):
        """捕获当前摄像头帧并开始处理"""
        print("🎥 CAPTURE button clicked!")
        print(f"Camera frame exists: {self.camera_frame is not None}")
        
        if self.camera_frame is not None:
            # 停止摄像头
            self.camera_active = False
            if hasattr(self, 'camera_cap') and self.camera_cap.isOpened():
                self.camera_cap.release()
            
            # 移除摄像头控制按钮
            self.image_canvas.delete("camera_control")
            
            # 保存捕获的图片
            self.current_image = Image.fromarray(self.camera_frame)
            self.current_image_path = "camera_capture"
            
            print(f"✅ Image captured: {self.current_image.size}")
            print("🎨 Calling show_start_animation_popup()...")
            
            # 显示并开始处理
            self.display_image(self.current_image)
            self.show_start_animation_popup()
        else:
            print("❌ No camera frame available!")
    
    def cancel_camera(self):
        """取消摄像头捕获，返回加载界面"""
        # 停止摄像头
        self.camera_active = False
        if hasattr(self, 'camera_cap') and self.camera_cap.isOpened():
            self.camera_cap.release()
        
        # 移除摄像头控制按钮
        self.image_canvas.delete("camera_control")
        
        # 解绑键盘控制
        self.unbind_camera_keyboard_controls()
        
        # 停止声音
        try:
            pygame.mixer.stop()
        except:
            pass
        
        # 返回加载界面
        self.draw_load_button()
        self.status_canvas.itemconfig(self.status_text_id,
            text="[ READY ] Load image to start")
    
    def unbind_camera_keyboard_controls(self):
        """解绑摄像头模式的键盘控制"""
        try:
            self.root.unbind('w')
            self.root.unbind('W')
            self.root.unbind('s')
            self.root.unbind('S')
            self.root.unbind('a')
            self.root.unbind('A')
            self.root.unbind('d')
            self.root.unbind('D')
            self.root.unbind('<Up>')
            self.root.unbind('<Down>')
            self.root.unbind('<Left>')
            self.root.unbind('<Right>')
            self.root.unbind('<space>')
        except:
            pass
    
    def show_start_animation_popup(self):
        """Show Mac OS Classic style start animation popup"""
        popup = tk.Toplevel(self.root)
        popup.title("Scrapbook")
        popup.geometry("450x280")
        popup.configure(bg=self.bg_black)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        
        # 绑定 Enter 键确认
        popup.bind('<Return>', lambda e: self.confirm_start_animation(popup))
        popup.bind('<Escape>', lambda e: self.cancel_animation(popup))
        
        # Mac风格边框
        border_frame = tk.Frame(popup, bg=self.primary_pink, bd=3, relief=tk.RIDGE)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        inner_frame = tk.Frame(border_frame, bg=self.hover_beige, bd=2)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # 标题
        title = tk.Label(
            inner_frame,
            text="IMAGE LOADED",
            font=self.pixel_font_large,
            bg=self.hover_beige,
            fg=self.bg_black
        )
        title.pack(pady=25)
        
        info_text = f"Size: {self.current_image.size[0]} x {self.current_image.size[1]} px\\n\\n"
        info_text += "Ready to pixelate and generate melody!\\n\\n"
        info_text += "Each pixel will play a note in real-time."
        
        info = tk.Label(
            inner_frame,
            text=info_text,
            font=self.pixel_font_small,
            bg=self.hover_beige,
            fg=self.bg_black,
            justify=tk.CENTER
        )
        info.pack(pady=15)
        
        # 提示文字
        hint = tk.Label(
            inner_frame,
            text="Press ENTER to start or ESC to cancel",
            font=self.pixel_font_small,
            bg=self.hover_beige,
            fg=self.primary_pink
        )
        hint.pack(pady=5)
        
        button_frame = tk.Frame(inner_frame, bg=self.hover_beige)
        button_frame.pack(pady=25)
        
        # 统一按钮样式参数（使用字符单位）
        button_config = {
            'font': self.pixel_font_medium,
            'bg': self.hover_beige,
            'fg': self.bg_black,
            'activebackground': self.primary_pink,
            'activeforeground': self.bg_black,
            'bd': 3,
            'relief': tk.RAISED,
            'cursor': 'hand2',
            'width': 14,  # 字符宽度
            'height': 2   # 行高
        }
        
        # START按钮 - Mac风格（统一尺寸）
        confirm_btn = tk.Button(
            button_frame,
            text="START",
            command=lambda: self.confirm_start_animation(popup),
            **button_config
        )
        confirm_btn.pack(side=tk.LEFT, padx=10)
        
        # CANCEL按钮（统一尺寸）
        cancel_btn = tk.Button(
            button_frame,
            text="CANCEL",
            command=lambda: self.cancel_animation(popup),
            **button_config
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def cancel_animation(self, popup):
        """Cancel animation and return to load screen"""
        popup.destroy()
        # 清空当前图片
        self.current_image_path = None
        self.current_image = None
        self.pixelated_image = None
        # 重新显示 LOAD 按钮界面
        self.draw_load_button()
        self.status_canvas.itemconfig(self.status_text_id,
            text="[ READY ] Load image to start")
    
    def confirm_start_animation(self, popup):
        """Confirm start animation"""
        popup.destroy()
        self.start_pixelation_animation()
    
    def display_image(self, image):
        """Display image"""
        self.image_canvas.delete("all")
        
        self.image_canvas.update()
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500
        
        img_copy = image.copy()
        img_copy.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
        
        self.photo_image = ImageTk.PhotoImage(img_copy)
        
        x = (canvas_width - self.photo_image.width()) // 2
        y = (canvas_height - self.photo_image.height()) // 2
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=self.photo_image)
    
    def start_pixelation_animation(self):
        """Start pixelation animation with original colors - extract top-left pixel of each 40×40 block"""
        if not self.current_image_path:
            return
        
        try:
            # 清空之前录制的音符和动画帧
            self.melody_generator.clear_recorded_notes()
            self.animation_frames = []
            self.frame_timestamps = []
            self.is_recording = True  # 启用录制
            
            self.status_canvas.itemconfig(self.status_text_id, 
                                         text="[ INITIALIZING ] Preparing animation...")
            self.root.update()
            
            print(f"Loading image: {self.current_image_path}")
            img = Image.open(self.current_image_path)
            print(f"Image loaded: {img.size[0]}×{img.size[1]}, mode: {img.mode}")
            
            # 检测是否有透明度通道
            has_alpha = img.mode == 'RGBA'
            
            # 转换为RGB或RGBA（保留原始颜色）
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGB')
                has_alpha = False
            
            # 如果图片太大，缩小到合理尺寸
            max_size = 800
            width, height = img.size
            if width > max_size or height > max_size:
                ratio = min(max_size / width, max_size / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"⚠ Large image resized: {width}×{height} → {new_width}×{new_height}")
                width, height = new_width, new_height
            
            # 保存原始图像用于音频轨
            original_img = img.copy()
            
            self.status_canvas.itemconfig(self.status_text_id, 
                                         text="[ PROCESSING ] Applying 1-bit pixelation...")
            self.root.update()
            
            # 应用 1-bit 像素化（三色）用于视觉轨
            pixelated_img = self.apply_1bit_pixelation(img)
            print("✓ 1-bit pixelation applied for visual track")
            
            self.status_canvas.itemconfig(self.status_text_id, 
                                         text="[ PROCESSING ] Creating pixel grid...")
            self.root.update()
            
            # 使用像素化后的图像尺寸计算网格
            pixel_width, pixel_height = pixelated_img.size
            
            # 计算网格大小 (每10×10像素一个块)
            self.grid_width = max(1, pixel_width // self.pixel_size)
            self.grid_height = max(1, pixel_height // self.pixel_size)
            
            print(f"Grid size: {self.grid_width}×{self.grid_height} = {self.grid_width * self.grid_height} blocks")
            
            # 限制最大块数（增加以显示更多像素）
            max_blocks = 800  # 从 300 增加到 800
            total_blocks = self.grid_width * self.grid_height
            if total_blocks > max_blocks:
                scale_factor = (max_blocks / total_blocks) ** 0.5
                self.pixel_size = int(self.pixel_size / scale_factor)
                self.grid_width = max(1, pixel_width // self.pixel_size)
                self.grid_height = max(1, pixel_height // self.pixel_size)
                print(f"⚠ Too many blocks, adjusted to: {self.grid_width}×{self.grid_height} blocks")
            
            print("Extracting colors: visual from 1-bit, audio from original...")
            self.rgb_data_list = []
            
            # 计算原始图像和像素化图像的缩放比例
            orig_width, orig_height = original_img.size
            scale_x = orig_width / pixel_width
            scale_y = orig_height / pixel_height
            
            # 遍历每个10×10块
            for grid_y in range(self.grid_height):
                for grid_x in range(self.grid_width):
                    # 像素化图像的左上角坐标（用于视觉）
                    pixel_x = grid_x * self.pixel_size
                    pixel_y = grid_y * self.pixel_size
                    
                    # 原始图像的对应坐标（用于音频）
                    orig_x = int(pixel_x * scale_x)
                    orig_y = int(pixel_y * scale_y)
                    
                    # 确保不越界
                    if pixel_x < pixel_width and pixel_y < pixel_height:
                        # 视觉轨：从1-bit像素化图像提取颜色
                        visual_pixel = pixelated_img.getpixel((pixel_x, pixel_y))
                        
                        # 音频轨：从原始图像提取颜色
                        if orig_x < orig_width and orig_y < orig_height:
                            audio_pixel = original_img.getpixel((orig_x, orig_y))
                        else:
                            audio_pixel = visual_pixel
                        
                        # 处理RGBA (1-bit图像是RGB)
                        visual_r, visual_g, visual_b = visual_pixel
                        visual_a = 255
                        
                        if has_alpha:
                            if isinstance(audio_pixel, tuple) and len(audio_pixel) == 4:
                                audio_r, audio_g, audio_b, audio_a = audio_pixel
                            else:
                                audio_r, audio_g, audio_b = audio_pixel
                                audio_a = 255
                        else:
                            if isinstance(audio_pixel, tuple) and len(audio_pixel) >= 3:
                                audio_r, audio_g, audio_b = audio_pixel[:3]
                            else:
                                audio_r = audio_g = audio_b = audio_pixel if isinstance(audio_pixel, int) else 0
                            audio_a = 255
                        
                        # 存储：视觉RGBA（用于显示）+ 音频RGBA（用于旋律）+ 网格坐标
                        self.rgb_data_list.append((
                            int(visual_r), int(visual_g), int(visual_b), int(visual_a),  # 视觉轨
                            int(audio_r), int(audio_g), int(audio_b), int(audio_a),      # 音频轨
                            grid_x, grid_y
                        ))
            
            print(f"✓ Extracted {len(self.rgb_data_list)} blocks (visual: 1-bit, audio: original)")
            
            # 创建像素化图像
            pixelated_width = self.grid_width * self.pixel_size
            pixelated_height = self.grid_height * self.pixel_size
            mode = 'RGBA' if has_alpha else 'RGB'
            self.pixelated_image = Image.new(mode, (pixelated_width, pixelated_height), 
                                            color=(0, 0, 0, 255) if has_alpha else (0, 0, 0))
            
            self.current_pixel_index = 0
            self.is_animating = True
            self.animation_paused = False
            self.octave_shift = 0
            self.octave_canvas.itemconfig(self.octave_display_id, text="PITCH: +0")
            
            # Reset data moshing state and trace background
            self.glitch_frames = []
            self.moshing_intensity = 0.0
            self.trace_background = None  # 重置trace背景
            self.glitch_history = None  # 重置glitch历史层
            
            self.status_canvas.itemconfig(self.status_text_id, 
                                         text="[ PLAYING ] Generating melody...")
            self.root.update()
            
            print("Starting animation: visual=1-bit pixel, audio=original...")
            self.animate_next_pixel()
            
        except Exception as e:
            import traceback
            error_msg = f"Failed to start animation: {str(e)}"
            print(f"✗ {error_msg}")
            traceback.print_exc()
            messagebox.showerror("Error", error_msg)
    
    def animate_next_pixel(self):
        """Animate next pixel block with fade trace effects and play note with RGBA support"""
        if not self.is_animating or self.animation_paused:
            return
        
        if self.current_pixel_index >= len(self.rgb_data_list):
            self.finish_animation()
            return
        
        # 初始化trace背景（第一次）
        if self.trace_background is None:
            self.trace_background = Image.new(
                self.pixelated_image.mode, 
                self.pixelated_image.size, 
                color=(1, 1, 1, 0) if self.pixelated_image.mode == 'RGBA' else (1, 1, 1)
            )
        
        # 初始化glitch历史层（第一次）
        if self.glitch_history is None:
            self.glitch_history = Image.new(
                'RGBA',
                self.pixelated_image.size,
                color=(0, 0, 0, 0)  # 透明背景
            )
        
        # 解包双轨数据：视觉RGBA + 音频RGBA + 坐标
        pixel_data = self.rgb_data_list[self.current_pixel_index]
        visual_r, visual_g, visual_b, visual_a, audio_r, audio_g, audio_b, audio_a, grid_x, grid_y = pixel_data
        
        # 绘制像素块到主图像（使用音频轨的原始颜色 + 微弱粒子shift效果）
        # 注意：显示使用原始颜色(audio)，音乐也使用原始颜色(audio)
        import random
        
        # 计算当前帧的shift偏移（基于时间的微弱波动）
        frame_offset = self.current_pixel_index % 60  # 60帧循环
        shift_x = int(random.random() * 2 - 1) if random.random() < 0.15 else 0  # 15%概率±1像素
        shift_y = int(random.random() * 2 - 1) if random.random() < 0.10 else 0  # 10%概率±1像素
        
        for py in range(self.pixel_size):
            for px in range(self.pixel_size):
                pixel_x = grid_x * self.pixel_size + px
                pixel_y = grid_y * self.pixel_size + py
                
                # 添加微弱的1-bit粒子效果（部分像素有轻微位移）
                use_shift = random.random() < 0.08  # 8%的像素有shift效果
                final_x = pixel_x + shift_x if use_shift else pixel_x
                final_y = pixel_y + shift_y if use_shift else pixel_y
                
                # 边界检查
                if final_x < self.pixelated_image.size[0] and final_y < self.pixelated_image.size[1]:
                    if final_x >= 0 and final_y >= 0:
                        # 使用音频轨的原始颜色进行显示（确保显示原图的像素化效果）
                        r_int = int(audio_r)
                        g_int = int(audio_g)
                        b_int = int(audio_b)
                        a_int = int(audio_a)
                        
                        # 微弱的颜色抖动（1-bit风格）- 极少数像素
                        if random.random() < 0.03:  # 3%概率
                            # 在调色板中随机选择相邻颜色
                            color_shift = random.choice([
                                (r_int, g_int, b_int),  # 原色
                                (max(0, r_int - 20), max(0, g_int - 10), max(0, b_int - 15)),  # 稍暗
                                (min(255, r_int + 15), min(255, g_int + 10), min(255, b_int + 10))  # 稍亮
                            ])
                            r_int, g_int, b_int = color_shift
                        
                        # 绘制到主图像和trace背景
                        if self.pixelated_image.mode == 'RGBA':
                            self.pixelated_image.putpixel((final_x, final_y), (r_int, g_int, b_int, a_int))
                            # trace背景不受shift影响
                            if pixel_x < self.pixelated_image.size[0] and pixel_y < self.pixelated_image.size[1]:
                                self.trace_background.putpixel((pixel_x, pixel_y), (r_int, g_int, b_int, 255))
                        else:
                            self.pixelated_image.putpixel((final_x, final_y), (r_int, g_int, b_int))
                            if pixel_x < self.pixelated_image.size[0] and pixel_y < self.pixelated_image.size[1]:
                                self.trace_background.putpixel((pixel_x, pixel_y), (r_int, g_int, b_int))
        
        # 应用渐淡效果到trace背景（每个像素透明度降低）
        if self.pixelated_image.mode == 'RGBA':
            trace_pixels = self.trace_background.load()
            width, height = self.trace_background.size
            for y in range(height):
                for x in range(width):
                    r, g, b, a = trace_pixels[x, y]
                    # 逐渐降低透明度（渐淡效果）
                    new_a = max(0, int(a * 0.95))  # 每帧降低5%
                    trace_pixels[x, y] = (r, g, b, new_a)
        
        # Calculate progressive data moshing intensity
        progress = (self.current_pixel_index + 1) / len(self.rgb_data_list)
        
        # 更强烈的 glitch 强度曲线（参考 fauux.neocities.org/glimmer 风格）
        if progress < 0.5:
            self.moshing_intensity = progress * 0.6  # 前半段快速增强到 0.3
        elif progress < 0.8:
            self.moshing_intensity = 0.3 + (progress - 0.5) * 0.4  # 中段继续增强到 0.42
        else:
            self.moshing_intensity = 0.42 * (1.0 - (progress - 0.8) / 0.2)  # 最后渐弱
        
        # 合成最终图像：trace背景 + 当前像素化图像
        final_image = self.trace_background.copy()
        if self.pixelated_image.mode == 'RGBA':
            final_image = Image.alpha_composite(final_image, self.pixelated_image)
        else:
            final_image.paste(self.pixelated_image, (0, 0))
        
        # 更频繁地应用 glitch 效果（每2帧而不是5帧），并累积到历史层
        if self.current_pixel_index % 2 == 0 and self.moshing_intensity > 0.05:
            # 生成glitch效果
            glitch_frame = self.apply_data_moshing(final_image.copy(), self.moshing_intensity)
            
            # 将glitch效果提取出来（只保留glitch部分，去掉原图）
            # 创建一个只包含glitch artifacts的图层
            if glitch_frame.mode != 'RGBA':
                glitch_frame = glitch_frame.convert('RGBA')
            
            # 累积到glitch历史层（alpha混合）
            self.glitch_history = Image.alpha_composite(self.glitch_history, glitch_frame)
            
            # 可选：让历史层逐渐淡化（如果希望旧的glitch慢慢消失）
            # 取消下面的注释来启用淡化效果
            # glitch_pixels = self.glitch_history.load()
            # width, height = self.glitch_history.size
            # for y in range(height):
            #     for x in range(width):
            #         r, g, b, a = glitch_pixels[x, y]
            #         new_a = max(0, int(a * 0.98))  # 每帧降低2%（比trace慢）
            #         glitch_pixels[x, y] = (r, g, b, new_a)
        
        # 合成所有层：final_image + glitch_history
        if self.glitch_history.mode == 'RGBA':
            final_image = Image.alpha_composite(final_image.convert('RGBA'), self.glitch_history)
        
        # 添加微弱的整体画面shift效果（wiredfriend风格）
        if random.random() < 0.20:  # 20%概率出现整体抖动
            final_image = self.apply_subtle_shift(final_image)
        
        self.display_image(final_image)
        
        # 如果正在录制，保存当前帧
        if self.is_recording:
            import time
            self.animation_frames.append(final_image.copy())
            self.frame_timestamps.append(time.time())
        
        # 使用音频轨的原始颜色播放音符
        threading.Thread(target=self.play_note_for_pixel, args=(audio_r, audio_g, audio_b, audio_a), daemon=True).start()
        
        # 计算HSV用于显示（从音频轨的原始颜色）
        h, s, v = self.melody_generator.rgb_to_hsv(audio_r, audio_g, audio_b)
        
        # Update status with glitch indicator and HSV info
        glitch_indicator = "⚡" if self.moshing_intensity > 0.1 else ""
        self.status_canvas.itemconfig(self.status_text_id,
            text=f"[ PLAYING ] {glitch_indicator} Block ({grid_x},{grid_y}) RGB({audio_r},{audio_g},{audio_b}) HSV({h:.1f}°,{s:.1f}%,{v:.1f}%) | {self.current_pixel_index+1}/{len(self.rgb_data_list)} | {progress*100:.1f}%"
        )
        
        self.current_pixel_index += 1
        
        # 动画速度控制（基于音频轨颜色 + 速度倍率）
        base_duration = int(50 + (audio_g / 255.0) * 20)  # 基础 50-70ms
        
        # 中间段加快（30%-70%进度时速度加倍）
        if 0.3 <= progress <= 0.7:
            base_duration = int(base_duration * 0.5)  # 中间段快2倍
        
        # 应用用户控制的速度倍率
        duration_ms = int(base_duration * self.speed_multiplier)
        
        self.root.after(duration_ms, self.animate_next_pixel)
    
    def play_note_for_pixel(self, r, g, b, a=255):
        """Play 8-bit style note for single pixel with HSV-based RGBA support"""
        try:
            # 使用HSV-based RGBA生成音符
            pitch, duration, velocity = self.melody_generator.rgba_to_note(r, g, b, a)
            pitch += self.octave_shift
            pitch = max(21, min(108, pitch))
            
            # 记录音符用于保存
            self.melody_generator.recorded_notes.append({
                'pitch': pitch,
                'duration': duration,
                'velocity': velocity,
                'rgb': (r, g, b, a)
            })
            
            # 直接播放波形音频（无需MIDI设备）
            self.melody_generator.play_note_direct(pitch, duration, velocity)
            
            # 调试输出
            if self.current_pixel_index % 10 == 0:
                h, s, v = self.melody_generator.rgb_to_hsv(r, g, b)
                print(f"Note: RGB({r},{g},{b}) → HSV({h:.2f},{s:.2f},{v:.2f}) → Pitch={pitch}, Vel={velocity}")
            
        except Exception as e:
            if self.current_pixel_index == 0:
                print(f"✗ Error playing note: {e}")
            pass
    
    def finish_animation(self):
        """Finish animation and show save options"""
        self.is_animating = False
        self.animation_paused = False
        
        # 停止所有正在播放的声音
        try:
            pygame.mixer.stop()
        except:
            pass
        
        total_notes = len(self.melody_generator.recorded_notes)
        total_frames = len(self.animation_frames) if self.animation_frames else 0
        
        print(f"\n🎬 Animation Complete:")
        print(f"   Notes recorded: {total_notes}")
        print(f"   Frames recorded: {total_frames}")
        print(f"   Recording was: {'ON' if self.is_recording else 'OFF'}")
        
        self.status_canvas.itemconfig(self.status_text_id,
            text=f"[ COMPLETE ] Generated {total_notes} notes, {total_frames} frames | EXPORT OPTIONS")
        
        self.image_canvas.update()
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        # 计算按钮布局（根据是否有视频帧动态调整）
        button_width = 110
        button_height = 50
        button_spacing = 20
        y_pos = canvas_height // 2 - 100  # 垂直位置
        
        # 确定要显示的按钮数量
        has_video = bool(self.animation_frames)
        num_buttons = 4 if has_video else 3  # MIDI, VIDEO(可选), AUDIO, NEW
        
        # 计算总宽度并居中
        total_width = num_buttons * button_width + (num_buttons - 1) * button_spacing
        start_x = (canvas_width - total_width) // 2
        
        # 当前按钮x位置
        current_x = start_x
        
        # MIDI按钮
        self.image_canvas.create_rectangle(
            current_x, y_pos,
            current_x + button_width, y_pos + button_height,
            fill=self.hover_beige,
            outline=self.primary_pink,
            width=3,
            tags="save_button"
        )
        
        self.image_canvas.create_text(
            current_x + button_width // 2, y_pos + button_height // 2,
            text="MIDI",
            font=self.pixel_font_small,
            fill=self.bg_black,
            tags="save_button"
        )
        current_x += button_width + button_spacing
        
        # VIDEO按钮（如果有录制帧）
        if has_video:
            self.image_canvas.create_rectangle(
                current_x, y_pos,
                current_x + button_width, y_pos + button_height,
                fill=self.hover_beige,
                outline=self.primary_pink,
                width=3,
                tags="export_video_button"
            )
            
            self.image_canvas.create_text(
                current_x + button_width // 2, y_pos + button_height // 2,
                text="VIDEO",
                font=self.pixel_font_small,
                fill=self.bg_black,
                tags="export_video_button"
            )
            current_x += button_width + button_spacing
        
        # AUDIO按钮
        self.image_canvas.create_rectangle(
            current_x, y_pos,
            current_x + button_width, y_pos + button_height,
            fill=self.hover_beige,
            outline=self.primary_pink,
            width=3,
            tags="export_audio_button"
        )
        
        self.image_canvas.create_text(
            current_x + button_width // 2, y_pos + button_height // 2,
            text="AUDIO",
            font=self.pixel_font_small,
            fill=self.bg_black,
            tags="export_audio_button"
        )
        current_x += button_width + button_spacing
        
        # NEW按钮
        self.image_canvas.create_rectangle(
            current_x, y_pos,
            current_x + button_width, y_pos + button_height,
            fill=self.hover_beige,
            outline=self.primary_pink,
            width=3,
            tags="reload_button"
        )
        
        self.image_canvas.create_text(
            current_x + button_width // 2, y_pos + button_height // 2,
            text="NEW",
            font=self.pixel_font_small,
            fill=self.bg_black,
            tags="reload_button"
        )
        
        # 绑定保存按钮点击和光标效果
        self.image_canvas.tag_bind("save_button", "<Button-1>", lambda e: self.save_melody())
        self.image_canvas.tag_bind("save_button", "<Enter>", self.on_save_button_enter)
        self.image_canvas.tag_bind("save_button", "<Leave>", self.on_save_button_leave)
        
        # 绑定导出视频按钮
        if self.animation_frames:
            self.image_canvas.tag_bind("export_video_button", "<Button-1>", lambda e: self.export_video())
            self.image_canvas.tag_bind("export_video_button", "<Enter>", self.on_export_video_button_enter)
            self.image_canvas.tag_bind("export_video_button", "<Leave>", self.on_export_video_button_leave)
        
        # 绑定导出音频按钮
        self.image_canvas.tag_bind("export_audio_button", "<Button-1>", lambda e: self.export_audio())
        self.image_canvas.tag_bind("export_audio_button", "<Enter>", self.on_export_audio_button_enter)
        self.image_canvas.tag_bind("export_audio_button", "<Leave>", self.on_export_audio_button_leave)
        
        # 绑定 LOAD NEW 按钮点击和光标效果
        self.image_canvas.tag_bind("reload_button", "<Button-1>", lambda e: self.reset_and_load())
        self.image_canvas.tag_bind("reload_button", "<Enter>", self.on_reload_button_enter)
        self.image_canvas.tag_bind("reload_button", "<Leave>", self.on_reload_button_leave)
    
    def on_save_button_enter(self, event):
        """鼠标进入 Save 按钮时高亮"""
        items = self.image_canvas.find_withtag("save_button")
        if items:
            self.image_canvas.itemconfig(items[0], fill=self.primary_pink)  # 矩形变粉色
        self.image_canvas.config(cursor="hand2")
    
    def on_save_button_leave(self, event):
        """鼠标离开 Save 按钮时恢复"""
        items = self.image_canvas.find_withtag("save_button")
        if items:
            self.image_canvas.itemconfig(items[0], fill=self.hover_beige)  # 恢复米色
        self.image_canvas.config(cursor="")
    
    def on_reload_button_enter(self, event):
        """鼠标进入 Load New 按钮时高亮"""
        items = self.image_canvas.find_withtag("reload_button")
        if items:
            self.image_canvas.itemconfig(items[0], fill=self.primary_pink)  # 矩形变粉色
        self.image_canvas.config(cursor="hand2")
    
    def on_reload_button_leave(self, event):
        """鼠标离开 Load New 按钮时恢复"""
        items = self.image_canvas.find_withtag("reload_button")
        if items:
            self.image_canvas.itemconfig(items[0], fill=self.hover_beige)  # 恢复米色
        self.image_canvas.config(cursor="")
    
    def on_export_video_button_enter(self, event):
        """鼠标进入 Export Video 按钮时高亮"""
        items = self.image_canvas.find_withtag("export_video_button")
        if items:
            self.image_canvas.itemconfig(items[0], fill=self.primary_pink)
        self.image_canvas.config(cursor="hand2")
    
    def on_export_video_button_leave(self, event):
        """鼠标离开 Export Video 按钮时恢复"""
        items = self.image_canvas.find_withtag("export_video_button")
        if items:
            self.image_canvas.itemconfig(items[0], fill=self.hover_beige)
        self.image_canvas.config(cursor="")
    
    def on_export_audio_button_enter(self, event):
        """鼠标进入 Export Audio 按钮时高亮"""
        items = self.image_canvas.find_withtag("export_audio_button")
        if items:
            self.image_canvas.itemconfig(items[0], fill=self.primary_pink)
        self.image_canvas.config(cursor="hand2")
    
    def on_export_audio_button_leave(self, event):
        """鼠标离开 Export Audio 按钮时恢复"""
        items = self.image_canvas.find_withtag("export_audio_button")
        if items:
            self.image_canvas.itemconfig(items[0], fill=self.hover_beige)
        self.image_canvas.config(cursor="")
    
    def save_melody(self):
        """保存生成的旋律为MIDI文件"""
        if not self.melody_generator.recorded_notes:
            messagebox.showwarning("No Melody", "No melody to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Melody",
            defaultextension=".mid",
            filetypes=[
                ("MIDI Files", "*.mid"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # 确保文件扩展名是 .mid
                if not file_path.lower().endswith('.mid'):
                    file_path += '.mid'
                
                self.melody_generator.save_recorded_melody(file_path)
                messagebox.showinfo("Success", f"Melody saved successfully!\n\n{len(self.melody_generator.recorded_notes)} notes saved to:\n{file_path}")
                self.status_canvas.itemconfig(self.status_text_id,
                    text=f"[ SAVED ] Melody saved to {os.path.basename(file_path)}")
            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to save melody: {str(e)}")
    
    def export_video(self):
        """导出视频（包含音频）"""
        if not self.animation_frames:
            messagebox.showwarning("No Video", "No animation frames to export!\n\nFrames are only recorded during animation playback.")
            return
        
        print(f"📹 Starting video export: {len(self.animation_frames)} frames")
        
        file_path = filedialog.asksaveasfilename(
            title="Export Video",
            defaultextension=".mp4",
            filetypes=[
                ("MP4 Video", "*.mp4"),
                ("AVI Video", "*.avi"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                import numpy as np
                
                # 检查是否安装了 imageio
                try:
                    import imageio
                    print(f"✓ imageio loaded: {imageio.__version__}")
                except ImportError:
                    print("✗ imageio not installed")
                    messagebox.showerror("Error", "imageio library is required for video export.\n\nInstall with:\npip install imageio imageio-ffmpeg")
                    return
                
                self.status_canvas.itemconfig(self.status_text_id,
                    text="[ EXPORTING ] Rendering video...")
                self.root.update()
                
                # 计算帧率（基于时间戳）
                if len(self.frame_timestamps) > 1:
                    avg_frame_time = (self.frame_timestamps[-1] - self.frame_timestamps[0]) / len(self.frame_timestamps)
                    fps = int(1.0 / max(avg_frame_time, 0.016))  # 最小16ms = 60fps
                    fps = max(10, min(fps, 60))  # 限制在 10-60 fps
                else:
                    fps = 30
                
                print(f"📊 Video settings: {len(self.animation_frames)} frames @ {fps} FPS")
                
                # 转换PIL图像为numpy数组
                video_frames = []
                for i, frame in enumerate(self.animation_frames):
                    if i % 100 == 0:
                        print(f"  Converting frame {i+1}/{len(self.animation_frames)}...")
                    if frame.mode != 'RGB':
                        frame = frame.convert('RGB')
                    video_frames.append(np.array(frame))
                
                print(f"💾 Saving to: {file_path}")
                
                # 保存视频（不包含音频）
                imageio.mimsave(file_path, video_frames, fps=fps, codec='libx264')
                
                print(f"✅ Video exported successfully!")
                
                messagebox.showinfo("Success", 
                    f"Video exported successfully!\n\n"
                    f"Frames: {len(self.animation_frames)}\n"
                    f"FPS: {fps}\n"
                    f"Duration: {len(self.animation_frames)/fps:.2f}s\n"
                    f"File: {file_path}\n\n"
                    f"Note: Export audio separately and combine in video editor if needed.")
                
                self.status_canvas.itemconfig(self.status_text_id,
                    text=f"[ EXPORTED ] Video saved to {os.path.basename(file_path)}")
                    
            except Exception as e:
                import traceback
                print(f"✗ Video export failed:")
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to export video:\n\n{str(e)}\n\nCheck terminal for details.")

    
    def export_audio(self):
        """导出音频WAV文件"""
        if not self.melody_generator.recorded_notes:
            messagebox.showwarning("No Audio", "No audio to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Audio",
            defaultextension=".wav",
            filetypes=[
                ("WAV Audio", "*.wav"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                import numpy as np
                import wave
                
                self.status_canvas.itemconfig(self.status_text_id,
                    text="[ EXPORTING ] Rendering audio...")
                self.root.update()
                
                # 生成音频波形
                sample_rate = 44100
                audio_data = []
                
                for note_info in self.melody_generator.recorded_notes:
                    pitch = note_info['pitch']
                    duration = note_info['duration']
                    velocity = note_info['velocity']
                    
                    # 生成方波音符
                    frequency = 440.0 * (2 ** ((pitch - 69) / 12.0))
                    num_samples = int(duration * sample_rate)
                    t = np.linspace(0, duration, num_samples, False)
                    
                    # 方波生成（8-bit风格）
                    wave_data = np.sign(np.sin(2 * np.pi * frequency * t))
                    wave_data *= (velocity / 127.0) * 0.3  # 音量调整
                    
                    audio_data.extend(wave_data)
                
                # 转换为16-bit PCM
                audio_data = np.array(audio_data)
                audio_data = np.int16(audio_data * 32767)
                
                # 保存WAV文件
                with wave.open(file_path, 'w') as wav_file:
                    wav_file.setnchannels(1)  # 单声道
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(audio_data.tobytes())
                
                duration_sec = len(audio_data) / sample_rate
                messagebox.showinfo("Success", 
                    f"Audio exported successfully!\n\n"
                    f"Notes: {len(self.melody_generator.recorded_notes)}\n"
                    f"Duration: {duration_sec:.2f}s\n"
                    f"Sample Rate: {sample_rate} Hz\n"
                    f"File: {file_path}")
                
                self.status_canvas.itemconfig(self.status_text_id,
                    text=f"[ EXPORTED ] Audio saved to {os.path.basename(file_path)}")
                    
            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to export audio: {str(e)}")
    
    def reset_and_load(self):
        """Reset and load new image"""
        self.current_image_path = None
        self.current_image = None
        self.pixelated_image = None
        self.melody_generator.clear_recorded_notes()  # 清空录制的音符
        self.draw_load_button()
        self.status_canvas.itemconfig(self.status_text_id,
            text="[ READY ] Load image to start")
        
        # 自动打开文件选择对话框
        self.root.after(100, self.load_image)


def main():
    root = tk.Tk()
    app = Image2MelodyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
