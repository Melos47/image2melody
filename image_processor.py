"""
Image Processor Module
处理图像并提取RGB数据
"""
from PIL import Image
import numpy as np


class ImageProcessor:
    def __init__(self, sample_rate=100, pixel_size=70):
        """
        初始化图像处理器
        sample_rate: 采样率，从图像中提取多少个点
        pixel_size: 像素化的像素块大小，默认8x8
        """
        self.sample_rate = sample_rate
        self.pixel_size = pixel_size
        self.pixelated_image = None
    
    def pixelate_image(self, image_path, pixel_size=None):
        """
        将图像像素化为8x8像素块（或自定义大小）
        返回像素化后的PIL Image对象
        支持RGBA（透明度）
        """
        if pixel_size is None:
            pixel_size = self.pixel_size
        
        # 打开图像
        img = Image.open(image_path)
        
        # 保留原始模式（RGB或RGBA）
        original_mode = img.mode
        
        # 如果不是RGB或RGBA，转换为RGB
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGB')
        
        # 获取原始尺寸
        original_width, original_height = img.size
        
        # 计算缩小后的尺寸（每个像素块变成1个像素）
        small_width = max(1, original_width // pixel_size)
        small_height = max(1, original_height // pixel_size)
        
        # 先缩小图像（使用NEAREST插值以保持清晰边缘）
        img_small = img.resize((small_width, small_height), Image.Resampling.NEAREST)
        
        # 再放大回接近原始尺寸（使用NEAREST插值创建像素化效果）
        pixelated_width = small_width * pixel_size
        pixelated_height = small_height * pixel_size
        img_pixelated = img_small.resize((pixelated_width, pixelated_height), Image.Resampling.NEAREST)
        
        # 保存像素化图像
        self.pixelated_image = img_pixelated
        
        return img_pixelated, (small_width, small_height)
    
    def extract_rgb_from_pixelated(self, image_path, pixel_size=None):
        """
        从像素化图像中提取RGB/RGBA数据
        每个像素块提取一个颜色值（支持透明度）
        """
        if pixel_size is None:
            pixel_size = self.pixel_size
        
        # 像素化图像
        pixelated_img, (grid_width, grid_height) = self.pixelate_image(image_path, pixel_size)
        
        # 从缩小的网格中提取每个像素的RGB/RGBA值
        img = Image.open(image_path)
        
        # 保留原始模式
        has_alpha = img.mode == 'RGBA'
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGB')
            has_alpha = False
        
        # 缩小到网格大小
        img_small = img.resize((grid_width, grid_height), Image.Resampling.NEAREST)
        
        rgb_data = []
        
        # 遍历每个像素块（从左到右，从上到下）
        for y in range(grid_height):
            for x in range(grid_width):
                pixel = img_small.getpixel((x, y))
                if has_alpha:
                    # RGBA模式
                    r, g, b, a = pixel
                    rgb_data.append((r, g, b, a))
                else:
                    # RGB模式
                    r, g, b = pixel
                    rgb_data.append((r, g, b, 255))  # 默认alpha=255（不透明）
        
        return rgb_data, pixelated_img
    
    def extract_rgb_data(self, image_path):
        """
        从图像中提取RGB数据
        使用网格采样方法从图像中提取代表性的RGB值
        """
        # 打开图像
        img = Image.open(image_path)
        
        # 转换为RGB模式（如果不是的话）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 获取图像尺寸
        width, height = img.size
        
        # 计算采样网格
        grid_size = int(np.sqrt(self.sample_rate))
        step_x = max(1, width // grid_size)
        step_y = max(1, height // grid_size)
        
        rgb_data = []
        
        # 网格采样
        for y in range(0, height, step_y):
            for x in range(0, width, step_x):
                if len(rgb_data) >= self.sample_rate:
                    break
                
                # 获取像素的RGB值
                r, g, b = img.getpixel((x, y))
                rgb_data.append((r, g, b))
            
            if len(rgb_data) >= self.sample_rate:
                break
        
        return rgb_data
    
    def extract_rgb_data_advanced(self, image_path, method='grid'):
        """
        高级RGB提取方法
        method: 'grid' - 网格采样, 'random' - 随机采样, 'edge' - 边缘采样
        """
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        width, height = img.size
        rgb_data = []
        
        if method == 'grid':
            # 网格采样（默认方法）
            return self.extract_rgb_data(image_path)
        
        elif method == 'random':
            # 随机采样
            np.random.seed(42)  # 为了可重复性
            for _ in range(self.sample_rate):
                x = np.random.randint(0, width)
                y = np.random.randint(0, height)
                r, g, b = img.getpixel((x, y))
                rgb_data.append((r, g, b))
        
        elif method == 'edge':
            # 边缘优先采样（从图像边缘采样更多）
            img_array = np.array(img)
            
            # 简单的边缘检测
            from PIL import ImageFilter
            edges = img.filter(ImageFilter.FIND_EDGES)
            edge_array = np.array(edges.convert('L'))
            
            # 找到边缘像素位置
            edge_positions = np.argwhere(edge_array > 50)
            
            if len(edge_positions) > self.sample_rate:
                # 随机选择边缘位置
                indices = np.random.choice(len(edge_positions), self.sample_rate, replace=False)
                selected_positions = edge_positions[indices]
            else:
                selected_positions = edge_positions
            
            for y, x in selected_positions:
                r, g, b = img.getpixel((x, y))
                rgb_data.append((r, g, b))
        
        return rgb_data
    
    def get_image_statistics(self, image_path):
        """
        获取图像的统计信息
        """
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        
        stats = {
            'size': img.size,
            'mode': img.mode,
            'mean_r': np.mean(img_array[:, :, 0]),
            'mean_g': np.mean(img_array[:, :, 1]),
            'mean_b': np.mean(img_array[:, :, 2]),
            'std_r': np.std(img_array[:, :, 0]),
            'std_g': np.std(img_array[:, :, 1]),
            'std_b': np.std(img_array[:, :, 2]),
        }
        
        return stats
    
    def visualize_sampling(self, image_path, save_path=None):
        """
        可视化采样点在图像上的位置
        """
        from PIL import ImageDraw
        
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        width, height = img.size
        
        # 创建副本用于绘制
        img_with_points = img.copy()
        draw = ImageDraw.Draw(img_with_points)
        
        # 计算采样点位置
        grid_size = int(np.sqrt(self.sample_rate))
        step_x = max(1, width // grid_size)
        step_y = max(1, height // grid_size)
        
        count = 0
        for y in range(0, height, step_y):
            for x in range(0, width, step_x):
                if count >= self.sample_rate:
                    break
                
                # 绘制采样点
                draw.ellipse([x-3, y-3, x+3, y+3], fill='red', outline='yellow')
                count += 1
            
            if count >= self.sample_rate:
                break
        
        if save_path:
            img_with_points.save(save_path)
        
        return img_with_points

    def extract_rgb_by_columns(self, image_path, pixel_size=None):
        """
        按列（Y轴）读取图片，生成和弦数据
        每一列的所有像素生成一个和弦
        从左到右生成旋律
        
        返回: list of list of (r, g, b, a)
        每个子列表代表一列的所有像素颜色
        """
        if pixel_size is None:
            pixel_size = self.pixel_size
        
        # 像素化图像
        pixelated_img, (grid_width, grid_height) = self.pixelate_image(image_path, pixel_size)
        
        # 从缩小的网格中提取每列的所有像素
        img = Image.open(image_path)
        
        # 保留原始模式
        has_alpha = img.mode == 'RGBA'
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGB')
            has_alpha = False
        
        # 缩小到网格大小
        img_small = img.resize((grid_width, grid_height), Image.Resampling.NEAREST)
        
        columns_data = []
        
        # 遍历每一列（从左到右）
        for x in range(grid_width):
            column_pixels = []
            # 遍历该列的所有行（从上到下）
            for y in range(grid_height):
                pixel = img_small.getpixel((x, y))
                if has_alpha:
                    r, g, b, a = pixel
                    column_pixels.append((r, g, b, a))
                else:
                    r, g, b = pixel
                    column_pixels.append((r, g, b, 255))
            
            columns_data.append(column_pixels)
        
        return columns_data, pixelated_img, (grid_width, grid_height)
