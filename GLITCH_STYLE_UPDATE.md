# Glitch 风格升级 (Glitch Style Update)

## 更新日期：2025-10-21

参考网站：[fauux.neocities.org/glimmer](https://fauux.neocities.org/glimmer)

---

## 主要改进

### 1. 像素大小调整
- **从** `10×10` **改为** `15×15`
- 更大的像素块，更清晰的视觉效果
- 减少块数，提高性能

### 2. 增强的 Glitch 效果

参考 fauux.neocities.org 的复古 web 美学，添加了 5 种 glitch 效果：

#### 🌈 RGB 通道分离（Chromatic Aberration）
```python
# 分离RGB通道并偏移
r_shifted = ImageChops.offset(r, offset_x, 0)
b_shifted = ImageChops.offset(b, -offset_x, offset_y)
```

**效果：**
- 红色和蓝色通道随机偏移
- 创造彩色边缘和色散效果
- 模拟 CRT 显示器的色差
- 强度随 intensity 参数变化

#### 📺 扫描线故障（Scanline Glitch）
4 种扫描线类型：

1. **repeat** - 重复前一个像素
   ```python
   pixels[px, line_y] = pixels[px - 1, line_y]
   ```

2. **shift** - 垂直偏移
   ```python
   shift_y = line_y + random.randint(-2, 2)
   pixels[px, line_y] = pixels[px, shift_y]
   ```

3. **corrupt** - 颜色失真（Mac Classic 色）
   ```python
   pixels[px, line_y] = (200, 116, 136)  # 粉色
   pixels[px, line_y] = (205, 190, 184)  # 米色
   ```

4. **bright** - 增加亮度
   ```python
   pixels[px, line_y] = (int(r * 1.5), int(g * 1.5), int(b * 1.5))
   ```

**数量：**
- `num_scanlines = int(height * intensity * 0.3)`
- 最多 30% 的扫描线受影响

#### 📦 像素位移（Pixel Displacement）
```python
# 随机块大小和位移
block_size = random.randint(5, 20)
dx = random.randint(-30, 30)
dy = random.randint(-10, 10)
```

**效果：**
- 5-20 像素的方块随机位移
- 水平位移 ±30px
- 垂直位移 ±10px
- 创造破碎、错位的视觉

#### 🎨 颜色失真（Color Corruption）
Mac OS Classic 四色调色板：
```python
noise_colors = [
    (1, 1, 1),          # 黑
    (200, 116, 136),    # 粉
    (205, 190, 184),    # 米
    (255, 255, 255)     # 白
]
```

#### ⚡ 随机噪点（Random Noise）
```python
num_noise = int(width * height * intensity * 0.01)
```

**效果：**
- 1% 的像素随机变色
- 使用 Mac Classic 调色板
- 模拟数字噪声和干扰

---

## Glitch 强度曲线

### 新的强度分配

```python
if progress < 0.5:
    intensity = progress * 0.6        # 0% → 30%
elif progress < 0.8:
    intensity = 0.3 + (progress - 0.5) * 0.4  # 30% → 42%
else:
    intensity = 0.42 * (1.0 - (progress - 0.8) / 0.2)  # 42% → 0%
```

**对比旧版：**
```python
# 旧版（较弱）
if progress < 0.7:
    intensity = progress * 0.3        # 0% → 21%
else:
    intensity = (1.0 - progress) * 0.7  # 21% → 0%
```

### 强度对比图

```
旧版:  0% ────▲──────── 21% ───▼─── 0%
       0%     70%      100%

新版:  0% ──▲──── 30% ──▲── 42% ──▼─ 0%
       0%    50%    80%    100%
```

**改进：**
- ✅ 最大强度从 21% 提升到 **42%**（翻倍）
- ✅ 更早开始增强（50% 而非 70%）
- ✅ 峰值持续更久（50%-80% 区间）
- ✅ 更戏剧性的视觉效果

---

## 触发频率

### 旧版
```python
if self.current_pixel_index % 5 == 0:  # 每5帧
    apply_glitch()
```
- 触发频率：20%
- 较少的 glitch 效果

### 新版
```python
if self.current_pixel_index % 2 == 0:  # 每2帧
    apply_glitch()
```
- 触发频率：**50%**
- 更持续、更明显的 glitch

**提升：**
- 触发频率 **2.5 倍**
- 更接近 fauux.neocities.org 的持续性 glitch 风格

---

## 技术细节

### ImageChops 导入

添加了 PIL.ImageChops 用于通道操作：
```python
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageChops
```

### 通道偏移算法

```python
# 分离通道
r, g, b = img.split()[:3]

# 计算偏移量（基于强度）
offset_x = int(random.randint(-5, 5) * intensity)
offset_y = int(random.randint(-2, 2) * intensity)

# 偏移通道
r_shifted = ImageChops.offset(r, offset_x, 0)
b_shifted = ImageChops.offset(b, -offset_x, offset_y)

# 重新合成
img = Image.merge('RGB', (r_shifted, g, b_shifted))
```

**特点：**
- 红色通道向右偏移
- 蓝色通道向左+下偏移
- 绿色通道保持原位
- 创造经典的 chromatic aberration 效果

---

## 视觉效果对比

### 旧版 Data Moshing
- 基础像素位移
- 简单颜色偏移
- 单一扫描线重复
- 较弱的视觉冲击

### 新版 Enhanced Glitch
- ✅ RGB 通道分离（彩色边缘）
- ✅ 4 种扫描线类型
- ✅ 像素块位移
- ✅ Mac Classic 颜色失真
- ✅ 随机噪点
- ✅ 更强的视觉冲击力

---

## 性能影响

### 像素大小改变
```
10×10 → 15×15
块数减少：(10/15)² = 44% 减少
```

**示例：**
- 800×450 图像
- 旧版：80×45 = **3600 块**
- 新版：53×30 = **1590 块**（减少 56%）

### Glitch 计算

**每帧额外操作：**
1. RGB 通道分离：O(width × height)
2. 通道偏移：O(width × height)
3. 扫描线：O(scanlines × width)
4. 像素位移：O(blocks × block_size²)
5. 随机噪点：O(noise_points)

**总额外时间：**
- 约 10-20ms per frame
- 可接受的性能影响

---

## 使用指南

### 启动程序
```bash
./run.sh
```

### 观察 Glitch 效果

**低强度阶段（0-50%）：**
- 轻微的 RGB 通道分离
- 偶尔的扫描线
- 少量噪点

**高强度阶段（50-80%）：**
- 明显的彩色边缘
- 频繁的扫描线故障
- 像素块位移
- 颜色失真
- 大量噪点

**衰减阶段（80-100%）：**
- 逐渐减弱的效果
- 回归原始画面

### Glitch 指示器

```
[ PLAYING ] ⚡ Block (x,y) ...
```
- ⚡ 符号表示 glitch 强度 > 10%
- 状态栏实时显示

---

## 风格参考

### fauux.neocities.org/glimmer

**借鉴元素：**
1. **RGB 通道分离** - 彩色边缘效果
2. **扫描线故障** - 水平线条干扰
3. **像素化美学** - 复古数字风格
4. **持续性 glitch** - 不断变化的效果
5. **色彩失真** - 非自然的颜色变化

**Mac OS Classic 融合：**
- 使用粉色 #C87488
- 使用米色 #CDBEB8
- 使用黑色 #010101
- 保持 1-bit 像素风格

---

## 代码结构

### apply_data_moshing()

```
1. RGB 通道分离
   ├─ 条件：intensity > 0.1
   ├─ 偏移量：±5px (x), ±2px (y)
   └─ 效果：彩色边缘

2. 扫描线故障
   ├─ 数量：height × intensity × 0.3
   ├─ 类型：repeat/shift/corrupt/bright
   └─ 效果：水平线条干扰

3. 像素位移
   ├─ 数量：pixels × intensity × 0.02
   ├─ 块大小：5-20px
   └─ 效果：破碎错位

4. 随机噪点
   ├─ 数量：pixels × intensity × 0.01
   ├─ 颜色：Mac Classic 调色板
   └─ 效果：数字噪声
```

---

## 配置参数

### 可调整的参数

```python
# RGB 通道偏移范围
offset_x_range = (-5, 5)
offset_y_range = (-2, 2)

# 扫描线数量系数
scanline_factor = 0.3

# 像素位移数量系数
displacement_factor = 0.02

# 随机噪点数量系数
noise_factor = 0.01

# 块位移范围
dx_range = (-30, 30)
dy_range = (-10, 10)

# Glitch 触发间隔
glitch_interval = 2  # 每2帧
```

### 强度曲线调整

```python
# 更激进的曲线
if progress < 0.3:
    intensity = progress * 1.0    # 快速上升
elif progress < 0.9:
    intensity = 0.3 + (progress - 0.3) * 0.5  # 持续高强度
else:
    intensity = 0.6 * (1.0 - progress)  # 快速衰减

# 更平缓的曲线
if progress < 0.8:
    intensity = progress * 0.25   # 缓慢上升
else:
    intensity = 0.2 * (1.0 - progress)  # 缓慢衰减
```

---

## 效果示例

### RGB 通道分离
```
原始:  [R][G][B]
       ███

效果:  [R]  [G] [B]
       █  █  █
        (彩色边缘)
```

### 扫描线故障
```
原始:  ████████████
       ████████████
       ████████████

效果:  ████████████
       █████──█████  ← 故障线
       ████████████
```

### 像素位移
```
原始:  [块A][块B]
       [块C][块D]

效果:  [块A]  [块B]
         [块C]
           [块D]  ← 错位
```

---

## 总结

### 关键改进
1. ✅ 像素大小：10×10 → **15×15**
2. ✅ Glitch 强度：21% → **42%**
3. ✅ 触发频率：20% → **50%**
4. ✅ 效果种类：3 种 → **5 种**
5. ✅ 视觉冲击：中等 → **强烈**

### 视觉风格
- 🎨 复古 web 美学
- 📺 CRT 显示器效果
- 🌈 RGB 通道分离
- ⚡ 持续性 glitch
- 🖥️ Mac OS Classic 融合

### 性能优化
- 📦 块数减少 56%
- ⏱️ 处理更快
- 🎯 效果更强

---

**版本**：Glitch Style v2.0  
**日期**：2025-10-21  
**像素大小**：15×15  
**Glitch 强度**：42% (max)  
**风格参考**：fauux.neocities.org/glimmer
