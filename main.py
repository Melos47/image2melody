"""
Image to 8-bit Melody Converter
Redesigned Pixel-style UI - Single Screen Mode
使用pygame.mixer直接生成波形声音（无需MIDI设备）
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os
import pygame
from image_processor import ImageProcessor
from melody_generator import MelodyGenerator


class Image2MelodyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image2Melody - 8bit Converter")
        self.root.geometry("900x700")
        
        # Pixel style colors
        self.bg_dark = "#1a1a1a"
        self.bg_medium = "#2d2d2d"
        self.bg_light = "#404040"
        self.accent_green = "#00ff41"
        self.accent_cyan = "#00ffff"
        self.text_color = "#c0c0c0"
        
        self.root.configure(bg=self.bg_dark)
        
        # Initialize processors
        self.image_processor = ImageProcessor()
        self.melody_generator = MelodyGenerator()
        
        # State variables
        self.current_image_path = None
        self.current_image = None
        self.pixelated_image = None
        self.pixel_size = 70  # 增大像素方块 (从50改为120)
        
        # Animation state
        self.is_animating = False
        self.animation_paused = False
        self.current_pixel_index = 0
        self.rgb_data_list = []
        self.grid_width = 0
        self.grid_height = 0
        self.octave_shift = 0
        
        # Recording state
        self.is_recording = False
        self.animation_frames = []  # 保存动画帧
        
        # 初始化音频系统
        self.init_audio()
        
        self.pixel_font_large = ("Courier", 24, "bold")
        self.pixel_font_medium = ("Courier", 18, "bold")
        self.pixel_font_small = ("Courier", 12, "bold")
        
        self.setup_ui()
        self.setup_keyboard_bindings()
    
    def setup_ui(self):
        """Setup pixel-style UI"""
        # Top title bar
        title_frame = tk.Frame(self.root, bg=self.bg_dark, height=80)
        title_frame.pack(fill=tk.X, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="IMAGE TO 8BIT MELODY",
            font=self.pixel_font_large,
            bg=self.bg_dark,
            fg=self.accent_green
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="[ PIXEL AUDIO CONVERTER v2.0 ]",
            font=self.pixel_font_small,
            bg=self.bg_dark,
            fg=self.accent_cyan
        )
        subtitle_label.pack()
        
        # Control hints
        control_frame = tk.Frame(self.root, bg=self.bg_medium, height=60)
        control_frame.pack(fill=tk.X, padx=20, pady=5)
        control_frame.pack_propagate(False)
        
        control_text = tk.Label(
            control_frame,
            text="CONTROLS: [W]UP [S]DOWN [A]LEFT [D]RIGHT [SPACE]PAUSE",
            font=self.pixel_font_small,
            bg=self.bg_medium,
            fg=self.text_color
        )
        control_text.pack(side=tk.LEFT, padx=10, expand=True)
        
        self.octave_label = tk.Label(
            control_frame,
            text="PITCH: +0",
            font=self.pixel_font_small,
            bg=self.bg_medium,
            fg=self.accent_green
        )
        self.octave_label.pack(side=tk.RIGHT, padx=10)
        
        # Main display area
        main_frame = tk.Frame(self.root, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        canvas_frame = tk.Frame(main_frame, bg=self.bg_light, bd=4, relief=tk.RIDGE)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.image_canvas = tk.Canvas(
            canvas_frame,
            bg=self.bg_dark,
            highlightthickness=0
        )
        self.image_canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # Draw load button
        self.root.after(100, self.draw_load_button)
        
        # Bottom status bar
        status_frame = tk.Frame(self.root, bg=self.bg_medium, height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_bar = tk.Label(
            status_frame,
            text="[ READY ] LOAD IMAGE TO START",
            font=self.pixel_font_small,
            bg=self.bg_medium,
            fg=self.accent_cyan,
            anchor=tk.W,
            padx=20
        )
        self.status_bar.pack(fill=tk.BOTH, expand=True)
        
        self.image_canvas.bind('<Button-1>', self.on_canvas_click)
    
    def draw_load_button(self):
        """Draw load button in center of canvas"""
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
        
        button_width = 300
        button_height = 100
        
        self.load_button_rect = self.image_canvas.create_rectangle(
            center_x - button_width // 2,
            center_y - button_height // 2,
            center_x + button_width // 2,
            center_y + button_height // 2,
            fill=self.bg_light,
            outline=self.accent_green,
            width=3,
            tags="load_button"
        )
        
        self.image_canvas.create_text(
            center_x,
            center_y - 10,
            text="[ LOAD IMAGE ]",
            font=self.pixel_font_medium,
            fill=self.accent_green,
            tags="load_button"
        )
        
        self.image_canvas.create_text(
            center_x,
            center_y + 20,
            text="CLICK TO SELECT",
            font=self.pixel_font_small,
            fill=self.text_color,
            tags="load_button"
        )
        
        self.image_canvas.tag_bind("load_button", "<Enter>", 
            lambda e: self.image_canvas.itemconfig(self.load_button_rect, fill=self.bg_medium))
        self.image_canvas.tag_bind("load_button", "<Leave>", 
            lambda e: self.image_canvas.itemconfig(self.load_button_rect, fill=self.bg_light))
    
    def on_canvas_click(self, event):
        """Canvas click event"""
        items = self.image_canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if items and "load_button" in self.image_canvas.gettags(items[0]):
            self.load_image()
        elif items and "reload_button" in self.image_canvas.gettags(items[0]):
            self.reset_and_load()
    
    def setup_keyboard_bindings(self):
        """Setup keyboard bindings"""
        self.root.bind('<w>', lambda e: self.adjust_octave(12))
        self.root.bind('<W>', lambda e: self.adjust_octave(12))
        self.root.bind('<s>', lambda e: self.adjust_octave(-12))
        self.root.bind('<S>', lambda e: self.adjust_octave(-12))
        self.root.bind('<a>', lambda e: self.adjust_octave(-1))
        self.root.bind('<A>', lambda e: self.adjust_octave(-1))
        self.root.bind('<d>', lambda e: self.adjust_octave(1))
        self.root.bind('<D>', lambda e: self.adjust_octave(1))
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
            self.octave_label.config(text=f"PITCH: {self.octave_shift:+d}")
    
    def toggle_pause(self):
        """Pause/resume animation"""
        if self.is_animating:
            self.animation_paused = not self.animation_paused
            if self.animation_paused:
                self.status_bar.config(text="[ PAUSED ] PRESS SPACE TO RESUME")
            else:
                self.status_bar.config(text="[ PLAYING ] GENERATING MELODY...")
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
    
    def show_start_animation_popup(self):
        """Show start animation popup"""
        popup = tk.Toplevel(self.root)
        popup.title("START ANIMATION")
        popup.geometry("500x300")
        popup.configure(bg=self.bg_dark)
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        
        title = tk.Label(
            popup,
            text="IMAGE LOADED",
            font=self.pixel_font_large,
            bg=self.bg_dark,
            fg=self.accent_green
        )
        title.pack(pady=30)
        
        info_text = f"Size: {self.current_image.size[0]} x {self.current_image.size[1]} px\\n\\n"
        info_text += "Ready to pixelate and generate melody!\\n\\n"
        info_text += "Each pixel will play a note in real-time."
        
        info = tk.Label(
            popup,
            text=info_text,
            font=self.pixel_font_small,
            bg=self.bg_dark,
            fg=self.text_color,
            justify=tk.CENTER
        )
        info.pack(pady=10)
        
        button_frame = tk.Frame(popup, bg=self.bg_dark)
        button_frame.pack(pady=30)
        
        confirm_btn = tk.Button(
            button_frame,
            text="[ START ANIMATION ]",
            font=self.pixel_font_medium,
            bg=self.bg_light,
            fg=self.accent_green,
            activebackground=self.bg_medium,
            activeforeground=self.accent_cyan,
            bd=3,
            relief=tk.RIDGE,
            padx=30,
            pady=15,
            cursor="hand2",
            command=lambda: self.confirm_start_animation(popup)
        )
        confirm_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(
            button_frame,
            text="[ CANCEL ]",
            font=self.pixel_font_small,
            bg=self.bg_light,
            fg=self.text_color,
            activebackground=self.bg_medium,
            bd=3,
            relief=tk.RIDGE,
            padx=20,
            pady=10,
            cursor="hand2",
            command=popup.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
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
        """Start pixelation animation and real-time playback with RGBA support"""
        if not self.current_image_path:
            return
        
        try:
            # 清空之前录制的音符
            self.melody_generator.clear_recorded_notes()
            
            self.status_bar.config(text="[ INITIALIZING ] PREPARING ANIMATION...")
            
            img = Image.open(self.current_image_path)
            
            # 检测是否有透明度通道
            has_alpha = img.mode == 'RGBA'
            
            # 转换为RGB或RGBA（保留透明度）
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGB')
                has_alpha = False
            
            original_width, original_height = img.size
            
            self.grid_width = max(1, original_width // self.pixel_size)
            self.grid_height = max(1, original_height // self.pixel_size)
            
            img_small = img.resize((self.grid_width, self.grid_height), Image.Resampling.NEAREST)
            
            self.rgb_data_list = []
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    pixel = img_small.getpixel((x, y))
                    if has_alpha:
                        r, g, b, a = pixel
                        self.rgb_data_list.append((r, g, b, a, x, y))
                    else:
                        r, g, b = pixel
                        self.rgb_data_list.append((r, g, b, 255, x, y))
            
            pixelated_width = self.grid_width * self.pixel_size
            pixelated_height = self.grid_height * self.pixel_size
            # 使用RGBA模式创建图像以支持透明度
            mode = 'RGBA' if has_alpha else 'RGB'
            self.pixelated_image = Image.new(mode, (pixelated_width, pixelated_height), color=(0, 0, 0, 255) if has_alpha else 'black')
            
            self.current_pixel_index = 0
            self.is_animating = True
            self.animation_paused = False
            self.octave_shift = 0
            self.octave_label.config(text="PITCH: +0")
            
            self.status_bar.config(text="[ PLAYING ] GENERATING MELODY...")
            
            self.animate_next_pixel()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start animation: {str(e)}")
    
    def animate_next_pixel(self):
        """Animate next pixel block and play note with RGBA support"""
        if not self.is_animating or self.animation_paused:
            return
        
        if self.current_pixel_index >= len(self.rgb_data_list):
            self.finish_animation()
            return
        
        # 解包RGBA数据
        pixel_data = self.rgb_data_list[self.current_pixel_index]
        r, g, b, a, grid_x, grid_y = pixel_data
        
        # 绘制像素块
        for py in range(self.pixel_size):
            for px in range(self.pixel_size):
                pixel_x = grid_x * self.pixel_size + px
                pixel_y = grid_y * self.pixel_size + py
                if pixel_x < self.pixelated_image.size[0] and pixel_y < self.pixelated_image.size[1]:
                    # 根据图像模式设置像素颜色
                    if self.pixelated_image.mode == 'RGBA':
                        self.pixelated_image.putpixel((pixel_x, pixel_y), (r, g, b, a))
                    else:
                        self.pixelated_image.putpixel((pixel_x, pixel_y), (r, g, b))
        
        self.display_image(self.pixelated_image)
        
        # 使用RGBA数据播放音符
        threading.Thread(target=self.play_note_for_pixel, args=(r, g, b, a), daemon=True).start()
        
        progress = (self.current_pixel_index + 1) / len(self.rgb_data_list) * 100
        self.status_bar.config(
            text=f"[ PLAYING ] BLOCK ({grid_x},{grid_y}) RGB({r},{g},{b}) A:{a} | {self.current_pixel_index+1}/{len(self.rgb_data_list)} | {progress:.1f}%"
        )
        
        self.current_pixel_index += 1
        # 加快动画速度：从100-200ms改为50-100ms
        duration_ms = int(50 + (g / 255.0) * 20)  # 50-100ms，更快节奏
        
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
        self.status_bar.config(text=f"[ COMPLETE ] Generated {total_notes} notes | SAVE MELODY?")
        
        self.image_canvas.update()
        canvas_width = self.image_canvas.winfo_width()
        
        # Save按钮
        self.image_canvas.create_rectangle(
            canvas_width // 2 - 220, 20,
            canvas_width // 2 - 20, 70,
            fill=self.bg_light,
            outline=self.accent_green,
            width=2,
            tags="save_button"
        )
        
        self.image_canvas.create_text(
            canvas_width // 2 - 120, 45,
            text="[ SAVE MIDI ]",
            font=self.pixel_font_small,
            fill=self.accent_green,
            tags="save_button"
        )
        
        # Load New按钮
        self.image_canvas.create_rectangle(
            canvas_width // 2 + 20, 20,
            canvas_width // 2 + 220, 70,
            fill=self.bg_light,
            outline=self.accent_cyan,
            width=2,
            tags="reload_button"
        )
        
        self.image_canvas.create_text(
            canvas_width // 2 + 120, 45,
            text="[ LOAD NEW ]",
            font=self.pixel_font_small,
            fill=self.accent_cyan,
            tags="reload_button"
        )
        
        # 绑定保存按钮
        self.image_canvas.tag_bind("save_button", "<Button-1>", lambda e: self.save_melody())
    
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
                self.melody_generator.save_recorded_melody(file_path)
                messagebox.showinfo("Success", f"Melody saved successfully!\n\n{len(self.melody_generator.recorded_notes)} notes saved to:\n{file_path}")
                self.status_bar.config(text=f"[ SAVED ] Melody saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save melody: {str(e)}")
    
    def reset_and_load(self):
        """Reset and load new image"""
        self.current_image_path = None
        self.current_image = None
        self.pixelated_image = None
        self.melody_generator.clear_recorded_notes()  # 清空录制的音符
        self.draw_load_button()
        self.status_bar.config(text="[ READY ] LOAD IMAGE TO START")


def main():
    root = tk.Tk()
    app = Image2MelodyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
