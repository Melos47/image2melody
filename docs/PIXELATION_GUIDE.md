# 像素化功能说明

## 🎨 新功能：像素化处理 (更新: 80×80大像素块)

### 功能概述

像素化功能将上传的图片转换为经典的像素块风格，真实还原8-bit游戏时代的视觉效果，并基于这些像素块生成音乐。

**最新更新** (2025-10-20):
- ✅ **像素块大小**: 从 50×50 升级到 **80×80**
- ✅ **动画速度**: 从 100-200ms 提升到 **50-100ms**（**2倍速**）

---

## 📐 像素化原理

### 矩阵处理流程

```
原始图片 (例如: 640x480)
    ↓
缩小到网格 (8x6, 每80个像素变成1个)
    ↓
放大回像素块尺寸 (640x480, 使用NEAREST插值)
    ↓
像素化图片 (80×80像素块组成)
```

### 技术实现

1. **缩小阶段**
   - 原始尺寸 ÷ 80 = 网格尺寸
   - 使用NEAREST插值保持清晰边缘
   - 例如：640x480 → 8x6网格 (48个像素块)

2. **放大阶段**
   - 网格尺寸 × 8 = 像素化尺寸
   - 每个网格点变成8x8像素块
   - 例如：80x60 → 640x480像素块图

3. **RGB提取**
   - 遍历网格（从左到右，从上到下）
   - 每个网格点提取一个RGB值
   - 按顺序形成RGB数据数组

---

## 🎵 从像素到音符

### 映射关系

每个8x8像素块 → 一个音符

```python
像素块位置: (x, y) in 网格
像素块颜色: (R, G, B)
    ↓
音符参数:
- Pitch (音高) = f(R)     # 红色值决定音高
- Duration (时长) = f(G)  # 绿色值决定节拍
- Velocity (力度) = f(B)  # 蓝色值决定音量
```

### 音乐生成顺序

像素块按照矩阵顺序扫描：
```
[Block(0,0)] → [Block(1,0)] → [Block(2,0)] → ...
     ↓
[Block(0,1)] → [Block(1,1)] → [Block(2,1)] → ...
     ↓
    ...
```

每个块依次生成一个音符，形成完整的旋律序列。

---

## 🖥️ UI操作流程

### 按钮功能

1. **📁 Load Image**
   - 加载原始图片
   - 显示在左侧框架
   - 启用"Pixelate"按钮

2. **🎨 Pixelate (8x8)**
   - 将图片像素化为8x8块
   - 更新左侧显示为像素化效果
   - 右侧显示像素块信息
   - 启用"Generate Melody"按钮

3. **🎼 Generate Melody**
   - 基于像素化的RGB数据生成音乐
   - 显示音符详细信息
   - 启用播放和保存功能

4. **▶️ Play Melody**
   - 播放生成的8-bit旋律

5. **💾 Save MIDI**
   - 保存为MIDI文件

---

## 📊 信息显示

### 像素化后的信息面板

```
🎨 Image Pixelated Successfully!
==================================================

Original Image: 640 x 480 pixels
Pixelated Size: 640 x 480 pixels
Pixel Block Size: 8 x 8 pixels
Total Pixel Blocks: 4800
Grid Dimensions: 80 x 60

RGB Data from Pixelated Blocks (first 20):
--------------------------------------------------
Block (0,0): R=123, G= 45, B=200
Block (0,1): R= 98, G=156, B= 78
Block (0,2): R=210, G= 34, B=145
...
```

### 旋律生成后的信息

```
🎵 Melody Generated Successfully!
==================================================

Source: pixelated image

Total Notes: 4800
Tempo: 120 BPM
Total Duration: 2400.00 beats
Estimated Time: 1200.00 seconds

Note Mapping:
--------------------------------------------------
#     RGB              Pitch   Dur     Vel
--------------------------------------------------
1     (123, 45,200)    F#4     0.44    127
2     ( 98,156, 78)    E4      1.48     85
...
```

---

## 🎮 8-bit风格效果

### 视觉效果
- ✅ 马赛克像素块
- ✅ 清晰的边缘（无模糊）
- ✅ 复古游戏画面感
- ✅ 8x8网格可见

### 音频效果
- ✅ 基于像素块的序列化音符
- ✅ 每个块对应一个独特音符
- ✅ 方波音色（8-bit风格）
- ✅ 可保存为MIDI

---

## 🔧 自定义选项

### 修改像素块大小

在 `main.py` 中修改：
```python
self.pixel_size = 8  # 改为16可以得到16x16像素块
```

在 `image_processor.py` 中修改：
```python
def __init__(self, sample_rate=32, pixel_size=8):
    self.pixel_size = pixel_size  # 改为其他值
```

### 常用像素块尺寸
- 4x4: 更细腻，音符更多
- 8x8: 标准8-bit风格（推荐）
- 16x16: 更粗糙，音符较少
- 32x32: 极简风格

---

## 💡 使用技巧

1. **选择合适的图片**
   - 色彩丰富的图片生成更有变化的旋律
   - 简单图案生成更规律的节奏

2. **观察像素化效果**
   - 像素化后的颜色决定音乐特征
   - 可以尝试不同的图片获得不同风格

3. **调整像素块大小**
   - 更小的块 = 更多音符 = 更长的旋律
   - 更大的块 = 更少音符 = 更短的旋律

---

## 📝 代码示例

### 单独使用像素化功能

```python
from image_processor import ImageProcessor

# 创建处理器
processor = ImageProcessor(pixel_size=8)

# 像素化图像
rgb_data, pixelated_img = processor.extract_rgb_from_pixelated(
    "your_image.jpg", 
    pixel_size=8
)

# 保存像素化图像
pixelated_img.save("pixelated_output.png")

# 使用RGB数据生成音乐
# ... (参考 melody_generator.py)
```

---

**享受像素化图像到8-bit音乐的转换过程！** 🎨🎵
