# 🔤 Jersey10 Charted 字体安装指南

## ✅ 问题已解决！

### 问题
- ❌ tkinter 无法直接加载 TTF 字体文件
- ❌ pyglet 注册的字体 tkinter 无法识别
- ❌ macOS 对自定义字体支持有限

### 解决方案
将字体安装到 macOS 系统字体目录，让系统识别后 tkinter 就能使用！

---

## 📦 快速安装（已完成）

### 方法1: 使用安装脚本（推荐）

```bash
./install_font.sh
```

这个脚本会：
1. ✅ 检查字体文件是否存在
2. ✅ 复制到 `~/Library/Fonts/` 
3. ✅ 系统自动识别字体

### 方法2: 手动安装

```bash
# 复制字体文件到用户字体目录
cp Coral_Pixels/Jersey10Charted-Regular.ttf ~/Library/Fonts/

# 或者使用 Font Book 应用
open Coral_Pixels/Jersey10Charted-Regular.ttf
# 在 Font Book 中点击 "Install Font"
```

---

## 🎨 验证安装

### 检查字体是否可用

```bash
source venv/bin/activate
python -c "
import tkinter as tk
from tkinter import font as tkfont

root = tk.Tk()
root.withdraw()

# 检查字体
families = list(tkfont.families())
jersey_fonts = [f for f in families if 'Jersey' in f]

print('找到的 Jersey 字体:')
for f in jersey_fonts:
    print(f'  ✓ {f}')
"
```

**期待输出**:
```
找到的 Jersey 字体:
  ✓ Jersey 10 Charted
```

### 运行程序验证

```bash
source venv/bin/activate
python main.py
```

**控制台输出**:
```
✓ Audio initialized successfully
✓ Audio system ready
✓ Using Jersey 10 Charted font  ← 看到这个就成功了！
```

---

## 🔍 字体名称说明

### macOS 识别的字体名称

- **文件名**: `Jersey10Charted-Regular.ttf`
- **系统识别名**: `Jersey 10 Charted` ⚠️ **注意有空格！**

### 代码中的使用

```python
# 正确 ✅
font = ("Jersey 10 Charted", 24, "normal")

# 错误 ❌
font = ("Jersey10 Charted", 24, "normal")  # 缺少空格
font = ("Jersey10Charted", 24, "normal")   # 完全无空格
```

---

## 🎮 程序中的字体设置

### 当前配置

```python
self.pixel_font_large = ("Jersey 10 Charted", 32, "normal")   # 标题
self.pixel_font_medium = ("Jersey 10 Charted", 24, "normal")  # 按钮
self.pixel_font_small = ("Jersey 10 Charted", 16, "normal")   # 状态栏
```

### 自动降级机制

如果 Jersey 字体不可用，程序会自动使用备用字体：

1. **Jersey 10 Charted** ✅ (首选)
2. **Monaco** - macOS 内置像素风格字体
3. **Menlo** - macOS 内置等宽字体
4. **Courier New** - 跨平台字体
5. **Courier** - 最后备用

---

## 🛠️ 故障排除

### 问题1: 字体安装后仍显示 "Using Monaco font"

**解决**:
```bash
# 1. 验证字体文件是否存在
ls -la ~/Library/Fonts/Jersey10Charted-Regular.ttf

# 2. 打开 Font Book 验证
open -a "Font Book"
# 搜索 "Jersey" 确认字体已安装

# 3. 重启程序
source venv/bin/activate
python main.py
```

### 问题2: Font Book 中看不到字体

**解决**:
```bash
# 重新安装字体
./install_font.sh

# 或手动安装
open Coral_Pixels/Jersey10Charted-Regular.ttf
```

### 问题3: 程序报错 "Font family not found"

**解决**:
检查字体名称是否正确（注意空格）：
```python
# 正确
("Jersey 10 Charted", 24, "normal")

# 查看系统中所有字体
python -c "
import tkinter as tk
from tkinter import font as tkfont
root = tk.Tk()
for f in sorted(tkfont.families()):
    if 'Jersey' in f:
        print(f)
"
```

---

## 📸 视觉效果对比

### 之前 (Courier)
```
IMAGE TO 8BIT MELODY
[ PIXEL AUDIO CONVERTER v2.0 ]
[ LOAD IMAGE ]
```

### 现在 (Jersey 10 Charted)
```
𝙸𝙼𝙰𝙶𝙴 𝚃𝙾 𝟾𝙱𝙸𝚃 𝙼𝙴𝙻𝙾𝙳𝚈
[ 𝙿𝙸𝚇𝙴𝙻 𝙰𝚄𝙳𝙸𝙾 𝙲𝙾𝙽𝚅𝙴𝚁𝚃𝙴𝚁 𝚟𝟸.𝟶 ]
[ 𝙻𝙾𝙰𝙳 𝙸𝙼𝙰𝙶𝙴 ]
```

更有复古8-bit游戏的感觉！🎮

---

## 🗑️ 卸载字体（可选）

如果需要移除字体：

```bash
# 删除字体文件
rm ~/Library/Fonts/Jersey10Charted-Regular.ttf

# 或使用 Font Book
# 1. 打开 Font Book
# 2. 搜索 "Jersey"
# 3. 右键 → Remove "Jersey 10 Charted"
```

---

## 📝 文件清单

### 字体相关文件

```
image2melody/
├── Coral_Pixels/
│   ├── Jersey10Charted-Regular.ttf  ← 字体文件
│   ├── CoralPixels-Regular.ttf      ← 备用字体
│   └── OFL.txt                      ← 许可证
├── install_font.sh                  ← 安装脚本
└── main.py                          ← 程序主文件
```

### 系统字体目录

```
~/Library/Fonts/
└── Jersey10Charted-Regular.ttf  ← 安装后的位置
```

---

## 🎉 总结

### 成功标志

运行程序时看到：
```
✓ Audio initialized successfully
✓ Audio system ready
✓ Using Jersey 10 Charted font  ← 这里！
```

### 视觉检查

启动程序后：
- 标题文字应该是像素风格
- 按钮文字更有游戏感
- 整体更复古8-bit风格

### 现在可以

- ✅ 使用 Jersey 10 Charted 像素字体
- ✅ 完整的8-bit复古视觉体验
- ✅ 自动降级到备用字体（如果需要）
- ✅ 鼠标光标反馈
- ✅ 所有按钮正常工作

享受完整的像素风格图片音乐转换器！🎮🎵
