# 🎨 CoralPixels 字体使用说明

## ✅ 字体已切换到 CoralPixels！

### 当前字体配置
- **主要字体**: CoralPixels-Regular.ttf ✨
- **备用字体1**: Jersey 10 Charted
- **备用字体2**: Monaco (系统内置)
- **最终备用**: Courier

---

## 🔤 字体对比

### CoralPixels vs Jersey10 Charted

**CoralPixels** (当前使用):
- 更圆润的像素风格
- 更可爱、友好的外观
- 适合休闲游戏风格
- 字母间距更宽

**Jersey10 Charted** (备用):
- 更棱角分明
- 复古街机游戏风格
- 更紧凑的排列

---

## 📦 字体安装状态

### 已安装的字体

```bash
~/Library/Fonts/
├── CoralPixels-Regular.ttf      ✅ 已安装
└── Jersey10Charted-Regular.ttf  ✅ 已安装
```

### 系统识别名称

- **文件名**: `CoralPixels-Regular.ttf`
- **系统识别**: `Coral Pixels`
- **tkinter名称**: `"Coral Pixels"`

---

## 🎮 程序字体配置

### 当前设置

```python
self.pixel_font_large = ("Coral Pixels", 32, "normal")   # 标题
self.pixel_font_medium = ("Coral Pixels", 24, "normal")  # 按钮
self.pixel_font_small = ("Coral Pixels", 16, "normal")   # 状态栏
```

### 降级顺序

程序会按以下顺序尝试字体：

1. **Coral Pixels** ⭐ (首选)
   - `"Coral Pixels"`
   - `"CoralPixels"`
   - `"Coral-Pixels"`
   - `"CoralPixels-Regular"`

2. **Jersey 10 Charted** (备用)
   - `"Jersey 10 Charted"`
   - `"Jersey10 Charted"`

3. **系统字体** (降级)
   - `"Monaco"` - macOS 像素风格
   - `"Menlo"` - macOS 等宽字体
   - `"Courier New"` - 跨平台
   - `"Courier"` - 最终备用

---

## 🔄 切换字体

### 切换到 Jersey10 Charted

编辑 `main.py` 第 71-78 行：

```python
# 将这些行移到前面
jersey_font_names = [
    "Jersey 10 Charted",
    "Jersey10 Charted",
]

for font_name in jersey_font_names:
    # ... (保持原有代码)
```

### 切换到系统字体 (Monaco)

```python
# 直接使用 Monaco
self.pixel_font_large = ("Monaco", 32, "normal")
self.pixel_font_medium = ("Monaco", 24, "normal")
self.pixel_font_small = ("Monaco", 16, "normal")
```

---

## ✨ 视觉效果

### CoralPixels 字体特点

```
IMAGE TO 8BIT MELODY
𝙸𝙼𝙰𝙶𝙴 𝚃𝙾 𝟾𝙱𝙸𝚃 𝙼𝙴𝙻𝙾𝙳𝚈

[ PIXEL AUDIO CONVERTER v2.0 ]
[ 𝙿𝙸𝚇𝙴𝙻 𝙰𝚄𝙳𝙸𝙾 𝙲𝙾𝙽𝚅𝙴𝚁𝚃𝙴𝚁 𝚟𝟸.𝟶 ]

[ LOAD IMAGE ]
[ 𝙻𝙾𝙰𝙳 𝙸𝙼𝙰𝙶𝙴 ]
```

**特点**:
- ✅ 圆润可爱
- ✅ 8-bit 游戏风格
- ✅ 易于阅读
- ✅ 字母间距舒适

---

## 🔍 验证安装

### 检查字体是否加载

运行程序时查看控制台输出：

```bash
source venv/bin/activate
python main.py
```

**期待看到**:
```
✓ Audio initialized successfully
✓ Audio system ready
✓ Using Coral Pixels font  ← 成功！
```

### 如果看到其他字体

```
✓ Using Jersey 10 Charted font (alternative)
```
说明 CoralPixels 未正确安装，自动使用了备用字体。

```
✓ Using Monaco font (system font)
```
说明两个像素字体都未安装，使用系统字体。

---

## 🛠️ 重新安装字体

### 方法1: 使用安装脚本

```bash
./install_font.sh
```

脚本会安装：
- ✅ CoralPixels-Regular.ttf
- ✅ Jersey10Charted-Regular.ttf

### 方法2: 手动安装

```bash
# 安装 CoralPixels
cp Coral_Pixels/CoralPixels-Regular.ttf ~/Library/Fonts/

# 安装 Jersey10
cp Coral_Pixels/Jersey10Charted-Regular.ttf ~/Library/Fonts/
```

### 方法3: 使用 Font Book

```bash
# 打开字体文件
open Coral_Pixels/CoralPixels-Regular.ttf

# 在 Font Book 中点击 "Install Font"
```

---

## 📊 字体信息

### CoralPixels-Regular.ttf

| 属性 | 值 |
|------|-----|
| 字体名称 | Coral Pixels |
| 文件名 | CoralPixels-Regular.ttf |
| 风格 | Regular |
| 类型 | 像素字体 |
| 适合尺寸 | 12px - 48px |
| 最佳用途 | 游戏UI、标题、按钮 |

### 推荐尺寸

- **大标题**: 32-40px ✅ 当前 32px
- **中等文字**: 20-28px ✅ 当前 24px
- **小文字**: 14-18px ✅ 当前 16px
- **最小可读**: 12px

---

## 🎨 自定义字体大小

如果觉得字体太大或太小，可以调整：

### 编辑 main.py

```python
# 在 load_pixel_font() 方法中
self.pixel_font_large = ("Coral Pixels", 32, "normal")   # 改为你想要的大小
self.pixel_font_medium = ("Coral Pixels", 24, "normal")  # 例如: 28
self.pixel_font_small = ("Coral Pixels", 16, "normal")   # 例如: 18
```

### 推荐组合

**更大（适合大屏幕）**:
```python
self.pixel_font_large = ("Coral Pixels", 40, "normal")
self.pixel_font_medium = ("Coral Pixels", 28, "normal")
self.pixel_font_small = ("Coral Pixels", 18, "normal")
```

**更小（适合小屏幕）**:
```python
self.pixel_font_large = ("Coral Pixels", 28, "normal")
self.pixel_font_medium = ("Coral Pixels", 20, "normal")
self.pixel_font_small = ("Coral Pixels", 14, "normal")
```

---

## 🎉 总结

### 当前状态

- ✅ CoralPixels 字体已安装
- ✅ 程序正在使用 CoralPixels
- ✅ 备用字体已配置
- ✅ 自动降级机制工作正常

### 视觉效果

程序界面现在使用：
- 🎮 CoralPixels 圆润像素字体
- 👆 手型光标反馈
- 🎨 完整的 8-bit 游戏风格
- 🎵 实时音频播放

### 控制台确认

启动程序时显示：
```
✓ Audio initialized successfully
✓ Audio system ready
✓ Using Coral Pixels font
```

享受更可爱的像素风格界面！🎮✨
