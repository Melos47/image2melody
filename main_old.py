"""
Image to 8-bit Melody Converter
主程序 - 使用Tkinter创建双框架GUI界面
"""
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import threading
from image_processor import ImageProcessor
from melody_generator import MelodyGenerator


class Image2MelodyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to 8-bit Melody Converter")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2b2b2b")
        
        self.image_processor = ImageProcessor()
        self.melody_generator = MelodyGenerator()
        self.current_image_path = None
        self.current_image = None
        self.pixelated_image = None
        self.pixel_size = 30  # 默认8x8像素块
        
        # 动画和演奏状态
        self.is_animating = False
        self.animation_paused = False
        self.current_pixel_index = 0
        self.rgb_data_list = []
        self.grid_width = 0
        self.grid_height = 0
        self.octave_shift = 0  # WASD控制的音高偏移
        
        self.setup_ui()
        self.setup_keyboard_bindings()
    
    def setup_ui(self):
        """设置用户界面"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="🎵 Image to 8-bit Melody Converter 🎵",
            font=("Arial", 24, "bold"),
            bg="#2b2b2b",
            fg="#00ff00"
        )
        title_label.pack(pady=20)
        
        # 按钮框架
        button_frame = tk.Frame(self.root, bg="#2b2b2b")
        button_frame.pack(pady=10)
        
        self.load_btn = tk.Button(
            button_frame,
            text="📁 Load Image",
            command=self.load_image,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.load_btn.grid(row=0, column=0, padx=10)
        
        self.start_animation_btn = tk.Button(
            button_frame,
            text="� Start Animation",
            command=self.start_pixelation_animation,
            font=("Arial", 12, "bold"),
            bg="#E91E63",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.start_animation_btn.grid(row=0, column=1, padx=10)
        
        self.pause_btn = tk.Button(
            button_frame,
            text="⏸️ Pause",
            command=self.toggle_pause,
            font=("Arial", 12, "bold"),
            bg="#FF5722",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.pause_btn.grid(row=0, column=2, padx=10)
        
        self.generate_btn = tk.Button(
            button_frame,
            text="🎼 Generate Melody",
            command=self.generate_melody,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.generate_btn.grid(row=0, column=3, padx=10)
        
        self.generate_btn.grid(row=0, column=3, padx=10)
        
        self.play_btn = tk.Button(
            button_frame,
            text="▶️ Play Melody",
            command=self.play_melody,
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.play_btn.grid(row=0, column=4, padx=10)
        
        self.play_btn.grid(row=0, column=3, padx=10)
        
        self.play_btn.grid(row=0, column=4, padx=10)
        
        self.save_btn = tk.Button(
            button_frame,
            text="💾 Save MIDI",
            command=self.save_midi,
            font=("Arial", 12, "bold"),
            bg="#9C27B0",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.save_btn.grid(row=0, column=5, padx=10)
        
        # 键盘控制说明
        control_frame = tk.Frame(self.root, bg="#2b2b2b")
        control_frame.pack(pady=5)
        
        control_label = tk.Label(
            control_frame,
            text="🎹 Keyboard Controls: W=Up Octave | S=Down Octave | A=Down Semitone | D=Up Semitone | Space=Pause/Resume",
            font=("Arial", 10),
            bg="#2b2b2b",
            fg="#FFD700"
        )
        control_label.pack()
        
        # 音高显示
        self.octave_label = tk.Label(
            control_frame,
            text="♪ Octave Shift: 0",
            font=("Arial", 10, "bold"),
            bg="#2b2b2b",
            fg="#00ff00"
        )
        self.octave_label.pack(pady=5)
        
        # 主内容框架（包含两个并排的框架）
        content_frame = tk.Frame(self.root, bg="#2b2b2b")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 左侧框架 - 图像显示
        left_frame = tk.LabelFrame(
            content_frame,
            text="📸 Image Display",
            font=("Arial", 14, "bold"),
            bg="#3b3b3b",
            fg="#00ff00",
            relief=tk.RIDGE,
            borderwidth=3
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.image_canvas = tk.Canvas(
            left_frame,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.image_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 右侧框架 - 文字信息显示
        right_frame = tk.LabelFrame(
            content_frame,
            text="📝 Information & Analysis",
            font=("Arial", 14, "bold"),
            bg="#3b3b3b",
            fg="#00ff00",
            relief=tk.RIDGE,
            borderwidth=3
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # 文字显示区域（带滚动条）
        text_scroll = tk.Scrollbar(right_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.info_text = tk.Text(
            right_frame,
            font=("Courier", 11),
            bg="#1e1e1e",
            fg="#00ff00",
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
            padx=10,
            pady=10
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        text_scroll.config(command=self.info_text.yview)
        
        # 状态栏
        self.status_bar = tk.Label(
            self.root,
            text="Ready to convert images to melodies! 🎵",
            font=("Arial", 10),
            bg="#1e1e1e",
            fg="#00ff00",
            anchor=tk.W,
            padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 初始化信息文本
        self.update_info_text("Welcome to Image to 8-bit Melody Converter!\n\n"
                             "How it works:\n"
                             "1. Load an image using the 'Load Image' button\n"
                             "2. Click 'Start Animation' to begin pixelation & live performance\n"
                             "3. Watch as pixels animate from left to right, top to bottom\n"
                             "4. Each pixel block plays a note in real-time!\n"
                             "5. Use WASD keys to control the melody during animation:\n"
                             "   • W: Raise octave (+12 semitones)\n"
                             "   • S: Lower octave (-12 semitones)\n"
                             "   • A: Lower by 1 semitone\n"
                             "   • D: Raise by 1 semitone\n"
                             "   • Space: Pause/Resume animation\n\n"
                             "The converter maps RGB values to musical parameters:\n"
                             "- Red (R): Pitch/Note frequency\n"
                             "- Green (G): Note duration\n"
                             "- Blue (B): Velocity/Volume\n\n"
                             "Live performance mode creates an interactive 8-bit experience!\n\n"
                             "Ready to begin! 🎵")
    
    def setup_keyboard_bindings(self):
        """设置键盘绑定"""
        self.root.bind('<w>', lambda e: self.adjust_octave(12))
        self.root.bind('<W>', lambda e: self.adjust_octave(12))
        self.root.bind('<s>', lambda e: self.adjust_octave(-12))
        self.root.bind('<S>', lambda e: self.adjust_octave(-12))
        self.root.bind('<a>', lambda e: self.adjust_octave(-1))
        self.root.bind('<A>', lambda e: self.adjust_octave(-1))
        self.root.bind('<d>', lambda e: self.adjust_octave(1))
        self.root.bind('<D>', lambda e: self.adjust_octave(1))
        self.root.bind('<space>', lambda e: self.toggle_pause())
    
    def adjust_octave(self, shift):
        """调整音高"""
        if self.is_animating:
            self.octave_shift += shift
            # 限制范围 -24 到 +24 (两个八度)
            self.octave_shift = max(-24, min(24, self.octave_shift))
            self.octave_label.config(text=f"♪ Octave Shift: {self.octave_shift:+d} semitones")
            self.status_bar.config(text=f"Pitch adjusted: {self.octave_shift:+d} semitones")
    
    def toggle_pause(self):
        """暂停/恢复动画"""
        if self.is_animating:
            self.animation_paused = not self.animation_paused
            if self.animation_paused:
                self.pause_btn.config(text="▶️ Resume")
                self.status_bar.config(text="Animation paused - Press Space or click Resume to continue")
            else:
                self.pause_btn.config(text="⏸️ Pause")
                self.status_bar.config(text="Animation resumed - Creating melody...")
                self.animate_next_pixel()
    
    def load_image(self):
        """加载图像文件"""
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
                
                # 在canvas中显示图像
                self.display_image(self.current_image)
                
                # 处理图像并显示信息
                rgb_data = self.image_processor.extract_rgb_data(file_path)
                self.display_image_info(file_path, rgb_data)
                
                # 启用动画按钮
                self.start_animation_btn.config(state=tk.NORMAL)
                self.generate_btn.config(state=tk.DISABLED)
                self.pixelated_image = None  # 重置像素化图像
                self.status_bar.config(text=f"Loaded: {file_path} - Click 'Start Animation' to begin!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def start_pixelation_animation(self):
        """开始像素化动画和实时演奏"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        try:
            self.status_bar.config(text="Starting live performance animation...")
            
            # 准备数据
            img = Image.open(self.current_image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            original_width, original_height = img.size
            
            # 计算网格尺寸
            self.grid_width = max(1, original_width // self.pixel_size)
            self.grid_height = max(1, original_height // self.pixel_size)
            
            # 缩小到网格大小
            img_small = img.resize((self.grid_width, self.grid_height), Image.Resampling.NEAREST)
            
            # 提取所有像素块的RGB数据
            self.rgb_data_list = []
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    r, g, b = img_small.getpixel((x, y))
                    self.rgb_data_list.append((r, g, b, x, y))
            
            # 创建空白画布用于动画
            pixelated_width = self.grid_width * self.pixel_size
            pixelated_height = self.grid_height * self.pixel_size
            self.pixelated_image = Image.new('RGB', (pixelated_width, pixelated_height), color='black')
            
            # 重置状态
            self.current_pixel_index = 0
            self.is_animating = True
            self.animation_paused = False
            self.octave_shift = 0
            self.octave_label.config(text="♪ Octave Shift: 0")
            
            # 禁用开始按钮，启用暂停按钮
            self.start_animation_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            
            # 显示初始信息
            info = "🎬 Live Performance Started!\n"
            info += f"{'=' * 50}\n\n"
            info += f"Original Size: {original_width} x {original_height} pixels\n"
            info += f"Grid Size: {self.grid_width} x {self.grid_height}\n"
            info += f"Total Blocks: {len(self.rgb_data_list)}\n"
            info += f"Pixel Block Size: {self.pixel_size}x{self.pixel_size}\n\n"
            info += "🎹 Use WASD to control pitch during performance!\n"
            info += "  W = Up octave (+12)\n"
            info += "  S = Down octave (-12)\n"
            info += "  A = Down semitone (-1)\n"
            info += "  D = Up semitone (+1)\n"
            info += "  Space = Pause/Resume\n\n"
            info += "Each pixel block will play a note as it appears...\n"
            self.update_info_text(info)
            
            # 开始动画
            self.animate_next_pixel()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start animation: {str(e)}")
    
    def animate_next_pixel(self):
        """动画下一个像素块并播放音符"""
        if not self.is_animating or self.animation_paused:
            return
        
        if self.current_pixel_index >= len(self.rgb_data_list):
            # 动画完成
            self.finish_animation()
            return
        
        # 获取当前像素块数据
        r, g, b, grid_x, grid_y = self.rgb_data_list[self.current_pixel_index]
        
        # 在像素化图像上填充这个8x8块
        for py in range(self.pixel_size):
            for px in range(self.pixel_size):
                pixel_x = grid_x * self.pixel_size + px
                pixel_y = grid_y * self.pixel_size + py
                if pixel_x < self.pixelated_image.size[0] and pixel_y < self.pixelated_image.size[1]:
                    self.pixelated_image.putpixel((pixel_x, pixel_y), (r, g, b))
        
        # 更新显示
        self.display_image(self.pixelated_image)
        
        # 播放这个像素块对应的音符（在后台线程）
        threading.Thread(target=self.play_note_for_pixel, args=(r, g, b), daemon=True).start()
        
        # 更新信息
        progress = (self.current_pixel_index + 1) / len(self.rgb_data_list) * 100
        self.status_bar.config(text=f"Playing... Block ({grid_x},{grid_y}) [{self.current_pixel_index+1}/{len(self.rgb_data_list)}] {progress:.1f}%")
        
        # 移动到下一个像素
        self.current_pixel_index += 1
        
        # 计算延迟时间（基于绿色值，但要合理）
        duration_ms = int(50 + (g / 255.0) * 150)  # 50-200ms之间
        
        # 继续动画
        self.root.after(duration_ms, self.animate_next_pixel)
    
    def play_note_for_pixel(self, r, g, b):
        """为单个像素块播放音符"""
        try:
            # 使用melody_generator的映射方法
            pitch, duration, velocity = self.melody_generator.rgb_to_note(r, g, b)
            
            # 应用八度偏移
            pitch += self.octave_shift
            
            # 限制音高范围
            pitch = max(21, min(108, pitch))
            
            # 使用pygame播放单个音符
            import pygame.midi
            
            if not pygame.midi.get_init():
                pygame.midi.init()
            
            # 打开MIDI输出
            if not hasattr(self, 'midi_out') or self.midi_out is None:
                try:
                    self.midi_out = pygame.midi.Output(0)
                    self.midi_out.set_instrument(80)  # Square wave
                except:
                    return
            
            # 播放音符
            self.midi_out.note_on(pitch, velocity, 0)
            import time
            time.sleep(min(duration * 0.5, 0.2))  # 限制最大持续时间
            self.midi_out.note_off(pitch, velocity, 0)
            
        except Exception as e:
            pass  # 静默失败，不影响动画
    
    def finish_animation(self):
        """完成动画"""
        self.is_animating = False
        self.animation_paused = False
        
        # 关闭MIDI输出
        if hasattr(self, 'midi_out') and self.midi_out:
            try:
                self.midi_out.close()
                self.midi_out = None
            except:
                pass
        
        # 更新按钮状态
        self.start_animation_btn.config(state=tk.NORMAL, text="🔄 Replay Animation")
        self.pause_btn.config(state=tk.DISABLED)
        self.generate_btn.config(state=tk.NORMAL)
        
        # 显示完成信息
        info = "🎉 Performance Complete!\n"
        info += f"{'=' * 50}\n\n"
        info += f"Total blocks played: {len(self.rgb_data_list)}\n"
        info += f"Final octave shift: {self.octave_shift:+d} semitones\n\n"
        info += "You can:\n"
        info += "• Click 'Replay Animation' to perform again\n"
        info += "• Click 'Generate Melody' to create a full MIDI file\n"
        info += "• Load a new image to start over\n"
        self.update_info_text(info)
        
        self.status_bar.config(text="✅ Animation complete! The pixelated image is ready.")
    
    def pixelate_image(self):
        """像素化图像（旧方法，保留作为备用）"""
        """像素化图像"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        try:
            self.status_bar.config(text="Pixelating image...")
            
            # 像素化图像并提取RGB数据
            rgb_data, pixelated_img = self.image_processor.extract_rgb_from_pixelated(
                self.current_image_path, 
                self.pixel_size
            )
            
            self.pixelated_image = pixelated_img
            
            # 显示像素化后的图像
            self.display_image(pixelated_img)
            
            # 显示像素化信息
            self.display_pixelated_info(rgb_data, pixelated_img.size)
            
            # 启用生成按钮
            self.generate_btn.config(state=tk.NORMAL)
            self.status_bar.config(text="Image pixelated! Ready to generate melody.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to pixelate image: {str(e)}")
    
    def display_pixelated_info(self, rgb_data, pixelated_size):
        """显示像素化信息"""
        info = f"🎨 Image Pixelated Successfully!\n"
        info += f"{'=' * 50}\n\n"
        info += f"Original Image: {self.current_image.size[0]} x {self.current_image.size[1]} pixels\n"
        info += f"Pixelated Size: {pixelated_size[0]} x {pixelated_size[1]} pixels\n"
        info += f"Pixel Block Size: {self.pixel_size} x {self.pixel_size} pixels\n"
        info += f"Total Pixel Blocks: {len(rgb_data)}\n"
        info += f"Grid Dimensions: {pixelated_size[0] // self.pixel_size} x {pixelated_size[1] // self.pixel_size}\n\n"
        
        info += f"RGB Data from Pixelated Blocks (first 20):\n"
        info += f"{'-' * 50}\n"
        
        grid_width = pixelated_size[0] // self.pixel_size
        
        for i, rgb in enumerate(rgb_data[:20], 1):
            row = (i - 1) // grid_width
            col = (i - 1) % grid_width
            info += f"Block ({row},{col}): R={rgb[0]:3d}, G={rgb[1]:3d}, B={rgb[2]:3d}\n"
        
        if len(rgb_data) > 20:
            info += f"... and {len(rgb_data) - 20} more blocks\n"
        
        info += f"\n{'=' * 50}\n"
        info += "Each pixel block will become a musical note!\n"
        info += "Ready to generate melody! Click 'Generate Melody' button."
        
        self.update_info_text(info)
    
    def display_image(self, image):
        """在canvas中显示图像"""
        # 获取canvas尺寸
        self.image_canvas.update()
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        # 调整图像大小以适应canvas
        img_copy = image.copy()
        img_copy.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
        
        # 转换为PhotoImage并显示
        self.photo_image = ImageTk.PhotoImage(img_copy)
        self.image_canvas.delete("all")
        
        # 居中显示
        x = (canvas_width - self.photo_image.width()) // 2
        y = (canvas_height - self.photo_image.height()) // 2
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=self.photo_image)
    
    def display_image_info(self, file_path, rgb_data):
        """显示图像信息"""
        info = f"📁 Image Loaded Successfully!\n"
        info += f"{'=' * 50}\n\n"
        info += f"File Path: {file_path}\n"
        info += f"Image Size: {self.current_image.size[0]} x {self.current_image.size[1]} pixels\n"
        info += f"Image Mode: {self.current_image.mode}\n"
        info += f"Sample Points Extracted: {len(rgb_data)}\n\n"
        
        info += f"RGB Data Sample (first 10 points):\n"
        info += f"{'-' * 50}\n"
        for i, rgb in enumerate(rgb_data[:10], 1):
            info += f"Point {i}: R={rgb[0]:3d}, G={rgb[1]:3d}, B={rgb[2]:3d}\n"
        
        if len(rgb_data) > 10:
            info += f"... and {len(rgb_data) - 10} more points\n"
        
        info += f"\n{'=' * 50}\n"
        info += "Ready to generate melody! Click 'Generate Melody' button."
        
        self.update_info_text(info)
    
    def generate_melody(self):
        """生成旋律"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        self.status_bar.config(text="Generating melody...")
        self.generate_btn.config(state=tk.DISABLED)
        
        def generate_thread():
            try:
                # 如果已经像素化，使用像素化的RGB数据
                if self.pixelated_image:
                    rgb_data, _ = self.image_processor.extract_rgb_from_pixelated(
                        self.current_image_path, 
                        self.pixel_size
                    )
                    source = "pixelated image"
                else:
                    # 否则使用原始图像数据
                    rgb_data = self.image_processor.extract_rgb_data(self.current_image_path)
                    source = "original image"
                
                # 生成旋律
                notes, melody_info = self.melody_generator.generate_melody(rgb_data)
                
                # 在主线程中更新UI
                self.root.after(0, lambda: self.on_melody_generated(notes, melody_info, source))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate melody: {str(e)}"))
                self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL))
        
        # 在后台线程中生成
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def on_melody_generated(self, notes, melody_info, source="image"):
        """旋律生成完成后的回调"""
        info = "🎵 Melody Generated Successfully!\n"
        info += f"{'=' * 50}\n\n"
        info += f"Source: {source}\n\n"
        info += melody_info
        
        self.update_info_text(info)
        
        # 启用播放和保存按钮
        self.play_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.generate_btn.config(state=tk.NORMAL)
        self.status_bar.config(text="Melody generated! Ready to play or save.")
    
    def play_melody(self):
        """播放旋律"""
        try:
            self.status_bar.config(text="Playing melody...")
            self.melody_generator.play_melody()
            self.status_bar.config(text="Playback complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play melody: {str(e)}")
    
    def save_midi(self):
        """保存MIDI文件"""
        file_path = filedialog.asksaveasfilename(
            title="Save MIDI File",
            defaultextension=".mid",
            filetypes=[("MIDI Files", "*.mid"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                self.melody_generator.save_midi(file_path)
                messagebox.showinfo("Success", f"MIDI file saved to:\n{file_path}")
                self.status_bar.config(text=f"Saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save MIDI: {str(e)}")
    
    def update_info_text(self, text):
        """更新信息文本框"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)


def main():
    root = tk.Tk()
    app = Image2MelodyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
