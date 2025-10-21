# 双轨系统 (Dual Track System)

## 概述

图像转旋律应用现在采用**双轨系统**：
- **视觉轨**：Floyd-Steinberg 抖动 + Data Moshing 效果
- **音频轨**：基于原始图像颜色生成 8-bit 旋律

## 技术架构

### 像素大小
- **20×20 像素块** (从 40×40 改为 20×20)
- 更细腻的像素化效果
- 更多的音符数量

### 视觉轨 (Visual Track)

```
原始图像 → Floyd-Steinberg Dithering → 20×20 像素化 → Data Moshing → 显示
```

**处理流程：**
1. 加载原始图像
2. 应用 Floyd-Steinberg 1-bit 抖动算法
3. 将抖动后的图像分割为 20×20 像素块
4. 提取每个块左上角的颜色（抖动后的颜色）
5. 填充整个 20×20 块为该颜色
6. 应用 Data Moshing 效果（位移、色彩偏移、扫描线）
7. 显示在 UI 上

**颜色特点：**
- 1-bit Floyd-Steinberg 抖动
- Mac OS Classic 风格：粉色 (#C87488)、米色 (#CDBEB8)、黑色 (#010101)
- 渐进式 Data Moshing (0% → 21% → 0%)

### 音频轨 (Audio Track)

```
原始图像 → 直接提取颜色 → RGBA → HSV → 8-bit 旋律
```

**处理流程：**
1. 在同样的 20×20 网格位置
2. 从**原始图像**（未抖动）提取左上角像素颜色
3. 获取完整的 RGBA 值
4. 转换为 HSV (色相、饱和度、亮度)
5. 基于 HSV 生成音符

**音符映射：**
- **色相 (Hue, 0-360°)** → 音符选择（五声音阶）
- **饱和度 (Saturation, 0-100%)** → 音量/力度
- **亮度 (Value, 0-100%)** → 持续时间
- **Alpha** → 音量微调

## 代码实现

### 数据结构

每个像素块存储 **10 个值**：

```python
(
    visual_r, visual_g, visual_b, visual_a,  # 视觉轨：抖动后的颜色
    audio_r, audio_g, audio_b, audio_a,      # 音频轨：原始颜色
    grid_x, grid_y                           # 网格坐标
)
```

### 关键函数

#### `start_pixelation_animation()`

```python
# 1. 保存原始图像副本
original_img = img.copy()

# 2. 应用 Floyd-Steinberg 抖动（视觉轨）
dithered_img = self.apply_floyd_steinberg_dither(img, max_size=800)

# 3. 提取双轨颜色
for grid_y in range(self.grid_height):
    for grid_x in range(self.grid_width):
        # 视觉轨：从抖动图像提取
        visual_pixel = dithered_img.getpixel((dither_x, dither_y))
        
        # 音频轨：从原始图像提取
        audio_pixel = original_img.getpixel((orig_x, orig_y))
        
        # 存储两组颜色
        self.rgb_data_list.append((
            visual_r, visual_g, visual_b, visual_a,
            audio_r, audio_g, audio_b, audio_a,
            grid_x, grid_y
        ))
```

#### `animate_next_pixel()`

```python
# 解包双轨数据
visual_r, visual_g, visual_b, visual_a, \
audio_r, audio_g, audio_b, audio_a, \
grid_x, grid_y = pixel_data

# 视觉：使用抖动颜色绘制
self.pixelated_image.putpixel((x, y), (visual_r, visual_g, visual_b, visual_a))

# 音频：使用原始颜色生成旋律
self.play_note_for_pixel(audio_r, audio_g, audio_b, audio_a)

# 显示：显示音频轨的HSV信息
h, s, v = self.melody_generator.rgb_to_hsv(audio_r, audio_g, audio_b)
```

## 视觉效果

### Floyd-Steinberg Dithering

**算法：**
- 误差扩散抖动
- 1-bit 输出（黑/白或粉色/米色/黑）
- 保持视觉密度的同时减少色彩

**误差分布：**
```
       X    7/16
  3/16 5/16 1/16
```

### Data Moshing

**3 种效果类型：**
1. **位移故障** (Displacement) - 像素块随机位移
2. **色彩偏移** (Color Shift) - RGB 通道分离
3. **扫描线** (Scanlines) - 水平线条故障

**强度曲线：**
- 0-70% 进度：强度从 0% 增加到 21%
- 70-100% 进度：强度从 21% 降低到 0%
- 强度 > 10% 时显示 ⚡ 指示器

## 音频生成

### HSV 转音符

```python
def rgba_to_note(r, g, b, a=255):
    # 转换为 HSV
    h, s, v = rgb_to_hsv(r, g, b)
    
    # 色相 → 五声音阶音符
    pentatonic_scale = [0, 2, 4, 7, 9]
    hue_index = int(h * 5) % 5
    note_offset = pentatonic_scale[hue_index]
    
    # 基础音高 + 色相偏移
    pitch = 60 + note_offset + int((h % 0.2) * 12)
    
    # 饱和度 → 力度 (60-127)
    velocity = int(60 + s * 67)
    
    # 亮度 → 持续时间 (0.1-0.3秒)
    duration = 0.1 + v * 0.2
    
    return pitch, duration, velocity
```

### 方波合成

- 使用 pygame.mixer
- 8-bit 风格方波
- 采样率：22050 Hz
- 音量：基于 velocity

## UI 显示

### 状态栏格式

```
[ PLAYING ] ⚡ Block (x,y) RGB(r,g,b) HSV(h°,s%,v%) | n/total | progress%
```

**示例：**
```
[ PLAYING ] ⚡ Block (5,3) RGB(180,75,120) HSV(330.5°,58.3%,70.6%) | 53/100 | 53.0%
```

**说明：**
- `⚡` - Data Moshing 强度 > 10% 时显示
- `RGB` - 音频轨的原始颜色（用于旋律生成）
- `HSV` - 色相/饱和度/亮度（音符映射的基础）

## 性能优化

### 图像大小限制

- **最大尺寸**：800px（用于抖动处理）
- **最大块数**：300 个
- 自动调整像素大小以满足限制

### 处理速度

- Floyd-Steinberg 抖动：~3 秒（800×450 图像）
- 像素化：瞬时
- 动画帧率：50-70ms/块

## 优势

### 视觉美学
✅ 保留 Floyd-Steinberg 1-bit 抖动的复古美学
✅ Mac OS Classic 风格
✅ 动态 Data Moshing 效果

### 音频准确性
✅ 基于原始图像颜色，不受抖动影响
✅ 完整的 HSV 色彩空间映射
✅ 更丰富的音符变化

### 用户体验
✅ 视觉和听觉分离，互不干扰
✅ 实时显示音频轨的 HSV 信息
✅ 透明的双轨处理流程

## 使用方法

1. **启动程序**：`./run.sh`
2. **上传图片**：点击 "UPLOAD IMAGE" 按钮
3. **开始播放**：点击 "START" 按钮
4. **观察效果**：
   - 视觉：抖动 + Data Moshing 效果
   - 音频：基于原始颜色的 8-bit 旋律
   - 状态栏：显示音频轨的 RGB 和 HSV 信息

## 技术细节

### 坐标映射

由于抖动后图像尺寸可能变化，需要坐标映射：

```python
# 计算缩放比例
scale_x = original_width / dithered_width
scale_y = original_height / dithered_height

# 从抖动图像坐标映射到原始图像坐标
orig_x = int(dither_x * scale_x)
orig_y = int(dither_y * scale_y)
```

### RGBA 兼容性

处理有/无 alpha 通道的图像：

```python
if has_alpha:
    visual_r, visual_g, visual_b, visual_a = visual_pixel
    audio_r, audio_g, audio_b, audio_a = audio_pixel
else:
    visual_r, visual_g, visual_b = visual_pixel
    visual_a = 255
    audio_r, audio_g, audio_b = audio_pixel
    audio_a = 255
```

## 文件结构

```
main.py
├── start_pixelation_animation()  # 双轨处理入口
│   ├── 保存原始图像副本
│   ├── 应用 Floyd-Steinberg 抖动
│   ├── 提取视觉轨颜色（抖动）
│   └── 提取音频轨颜色（原始）
│
├── animate_next_pixel()           # 播放单个像素块
│   ├── 使用视觉轨颜色绘制
│   ├── 应用 Data Moshing
│   ├── 使用音频轨颜色生成旋律
│   └── 显示音频轨 HSV 信息
│
└── apply_floyd_steinberg_dither() # Floyd-Steinberg 算法
    ├── 误差扩散
    ├── 1-bit 量化
    └── Mac OS Classic 色板

melody_generator.py
├── rgb_to_hsv()                   # RGB → HSV 转换
├── rgba_to_note()                 # HSV → 音符映射
└── play_note_direct()             # 方波合成播放
```

## 示例

### 输入图像
```
原始图像: colorful_sunset.jpg (1920×1080)
```

### 处理过程
```
1. 调整大小: 800×450
2. Floyd-Steinberg 抖动: 800×450 (1-bit)
3. 网格划分: 40×22 = 880 块 (20×20 每块)
4. 视觉轨: 880 个抖动颜色块
5. 音频轨: 880 个原始颜色块
6. 播放: 880 个音符 + Data Moshing 效果
```

### 输出
- **视觉**：1-bit 抖动像素艺术 + 渐进式故障效果
- **音频**：880 个基于原始 HSV 的 8-bit 音符
- **时长**：约 44-62 秒 (50-70ms/块)

---

**版本**：双轨系统 v1.0  
**日期**：2025-10-21  
**像素大小**：20×20  
**抖动算法**：Floyd-Steinberg 1-bit  
**音符映射**：HSV 五声音阶
