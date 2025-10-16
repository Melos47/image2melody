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
        
        self.setup_ui()
    
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
        self.generate_btn.grid(row=0, column=1, padx=10)
        
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
        self.play_btn.grid(row=0, column=2, padx=10)
        
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
        self.save_btn.grid(row=0, column=3, padx=10)
        
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
                             "2. The program will analyze RGB values from the image\n"
                             "3. Click 'Generate Melody' to convert RGB to musical notes\n"
                             "4. Play the generated 8-bit style melody\n"
                             "5. Save the melody as a MIDI file\n\n"
                             "The converter maps RGB values to musical parameters:\n"
                             "- Red (R): Pitch/Note frequency\n"
                             "- Green (G): Note duration\n"
                             "- Blue (B): Velocity/Volume\n\n"
                             "Ready to begin! 🎵")
    
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
                
                # 启用生成按钮
                self.generate_btn.config(state=tk.NORMAL)
                self.status_bar.config(text=f"Loaded: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
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
                # 提取RGB数据
                rgb_data = self.image_processor.extract_rgb_data(self.current_image_path)
                
                # 生成旋律
                notes, melody_info = self.melody_generator.generate_melody(rgb_data)
                
                # 在主线程中更新UI
                self.root.after(0, lambda: self.on_melody_generated(notes, melody_info))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate melody: {str(e)}"))
                self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL))
        
        # 在后台线程中生成
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def on_melody_generated(self, notes, melody_info):
        """旋律生成完成后的回调"""
        info = "🎵 Melody Generated Successfully!\n"
        info += f"{'=' * 50}\n\n"
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
