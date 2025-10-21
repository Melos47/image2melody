# 🎨 Image2Melody - 图像到旋律转换器# Image to 8-bit Melody Converter



将图片转换为 8-bit 风格的音乐旋律！基于 HSV 色彩空间，结合 Mac OS Classic 1-bit 美学和 glitch art 动画效果。将图片转换为8-bit风格的音乐旋律！基于HSV色彩空间生成独特的音符。



<div align="center">## ✨ 最新更新 (v3.0 - Dithering & Moshing Edition)



[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)- 🎨 **1-Bit Floyd-Steinberg Dithering**: 使用经典误差扩散算法将图片转换为黑白点阵

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)- 🌈 **Mac OS Classic 主题**: 复古Mac风格界面，粉色边框和米色按钮

[![macOS](https://img.shields.io/badge/macOS-Compatible-silver.svg)](https://www.apple.com/macos/)- ⚡ **Data Moshing 效果**: 渐进式数据损坏动画，创造glitch art美学

- 🎭 **Progressive Glitch Curve**: 动画从清晰到混沌再到清晰的视觉叙事

</div>- 💫 **三种Glitch类型**: 像素位移、色彩通道偏移、扫描线损坏



---### v2.0 功能

- 🎨 **HSV色彩模型**: 基于色相、饱和度、明度生成音符

## ✨ 核心特性- 💾 **保存功能**: 将生成的旋律保存为MIDI文件

- 🎵 **实时播放**: 动画过程中实时播放音符

### 🎨 视觉效果- 🎹 **键盘控制**: WASD调整音高，空格暂停

- **Mac OS Classic 风格界面** - 复古粉色边框和米色按钮- 📊 **调试输出**: 查看每个像素的HSV和音符信息

- **1-bit 像素化** - 10×10 像素块，带抖动图案纹理

- **Glitch Art 动画** - RGB 通道分离、扫描线故障、像素位移## 功能特点

- **微弱粒子 Shift** - wiredfriend 风格的 1-bit 动态效果

- **渐淡轨迹效果** - 透明度逐渐降低的视觉轨迹### 🎨 视觉效果 (v3.0 新功能!)



### 🎵 音乐生成- **1-Bit Floyd-Steinberg Dithering**：

- **双轨系统** - 视觉轨（1-bit 风格）+ 音频轨（原始 HSV）  - 经典误差扩散算法，将彩色图片转换为黑白点阵

- **HSV 到音符映射**:  - Mac OS Classic 配色：黑色 (#010101) 和 米色 (#CDBEB8)

  - 色相 (Hue) → 音高 (Pitch)  - 保留图片细节的同时创造复古点阵美学

  - 饱和度 (Saturation) → 力度 (Velocity)  - 自动在动画开始前应用抖动处理

  - 明度 (Value) → 时长 (Duration) + 八度  

- **实时播放** - pygame 方波合成，8-bit 音效- **Progressive Data Moshing**：

- **MIDI 导出** - 标准 .mid 格式，可在任何 DAW 中打开  - 渐进式glitch效果，随动画进度变化

  - 三种损坏类型：

### ⌨️ 交互控制    - 像素块位移 (Displacement)

- **音高控制**: `W`/`S` (±12半音), `A`/`D` (±1半音)    - 色彩通道偏移 (Color Shift)

- **速度控制**: `↑↓←→` 调整速度, `R` 重置    - 扫描线损坏 (Scanline Corruption)

- **播放控制**: `Space` 暂停/继续  - 强度曲线：0% → 21% → 0% (渐入渐出)

- **实时显示**: 当前速度和音高  - 状态栏 ⚡ 图标指示glitch活跃状态

  

---- **Mac OS Classic 界面**：

  - 条纹标题栏（粉色 #C87488）

## 🚀 快速开始  - 米色按钮和选中状态 (#CDBEB8)

  - 粉色边框和黑色背景 (#010101)

### 安装  - Jersey 10 像素字体

  - 复古弹窗设计

```bash

# 1. 克隆仓库### 🎬 实时演奏模式

git clone https://github.com/Melos47/image2melody.git

cd image2melody- **动画像素化**：

  - 从(0,0)开始逐个生成像素块

# 2. 安装 Python 和 tkinter（macOS）  - 80×80像素块，50-100ms动画速度

brew install python-tk@3.12  - 实时音符播放：每个像素块立即播放对应音符

  - 键盘控制：WASD实时调整音高

# 3. 创建虚拟环境并安装依赖  - 互动体验：暂停、继续、重放

/opt/homebrew/bin/python3.12 -m venv venv  

source venv/bin/activate- **🎹 键盘交互**：

pip install -r requirements.txt  - W: 升高八度 (+12半音)

```  - S: 降低八度 (-12半音)

  - A: 降低半音 (-1半音)

### 运行  - D: 升高半音 (+1半音)

  - Space: 暂停/继续动画

```bash  

# 使用启动脚本（推荐）- **HSV到音乐映射**：

./run.sh  - **色相 (H)**：决定音符（五声音阶）

  - **饱和度 (S)**：决定音符力度/音量

# 或手动运行  - **明度 (V)**：决定音符时长

source venv/bin/activate  

python main.py- **音乐生成**：

```  - 生成8-bit风格的旋律

  - 支持实时播放（方波合成）

---  - 导出MIDI文件格式



## 🎮 使用方法## 🚀 安装步骤



### 基本流程### 1. 克隆仓库



1. **加载图片** - 点击 `LOAD IMAGE` 按钮```bash

2. **开始动画** - 点击 `START ANIMATION`git clone https://github.com/Melos47/image2melody.git

3. **实时控制** - 使用键盘调整音高和速度cd image2melody

4. **保存作品** - 点击 `SAVE MIDI` 导出```



### 键盘控制### 2. 安装tkinter支持（macOS用户）



| 按键 | 功能 | 说明 |在macOS上，需要先安装支持tkinter的Python：

|------|------|------|

| `W` | 升高八度 | +12 半音 |```bash

| `S` | 降低八度 | -12 半音 |/opt/homebrew/bin/brew install python-tk@3.12

| `A` | 降低半音 | -1 半音 |```

| `D` | 升高半音 | +1 半音 |

| `↑` | 加快速度 | +0.2x 倍率 |### 3. 创建虚拟环境

| `↓` | 减慢速度 | -0.2x 倍率 |

| `←` | 微调减慢 | -0.1x 倍率 |```bash

| `→` | 微调加快 | +0.1x 倍率 |/opt/homebrew/bin/python3.12 -m venv venv

| `R` | 重置速度 | 1.0x |```

| `Space` | 暂停/继续 | - |

### 4. 激活虚拟环境并安装依赖

### 速度特性

```bash

- **自动加速**: 30%-70% 进度时速度自动快 2 倍source venv/bin/activate

- **手动控制**: 可调范围 0.2x (最快) 到 3.0x (最慢)pip install -r requirements.txt

- **实时显示**: 顶部控制栏显示当前速度```



---### 依赖包说明



## 🎨 技术原理- `Pillow`: 图像处理

- `numpy`: 数值计算

### 像素化处理- `MIDIUtil`: MIDI文件生成

```- `pygame`: 音频播放

原始图像 → 缩小到网格 → 提取代表色 → 1-bit 处理 → 10×10 像素块- `tkinter`: GUI界面（需要单独安装python-tk）

```

## 💻 使用方法

### HSV 到音乐映射

```python### 启动应用

音高 = f(色相)    # 0-360° → C4-B5 五声音阶

力度 = f(饱和度)  # 0-100% → 60-127 (MIDI velocity)**方法1：使用启动脚本（推荐）**

时长 = f(明度)    # 0-100% → 0.25-2.0 拍```bash

八度 = f(明度)    # 暗→低八度, 亮→高八度./run.sh

``````



### 双轨系统**方法2：手动激活环境**

- **视觉轨**: 1-bit 像素化 + glitch 效果（显示用）```bash

- **音频轨**: 原始 HSV 数据（音乐生成用）source venv/bin/activate

python main.py

---```



## 📂 项目结构### 操作步骤



```#### 🎬 实时演奏模式（推荐！）

image2melody/

├── main.py                    # 主程序 - GUI 和动画控制1. **加载图片** 📁

├── melody_generator.py        # 旋律生成 - HSV 到 MIDI   - 点击"Load Image"按钮

├── image_processor.py         # 图像处理 - 像素化和采样   - 选择一张图片（支持PNG, JPG, JPEG, BMP, GIF）

├── requirements.txt           # Python 依赖   - 图片将显示在左侧框架中

├── run.sh                     # 启动脚本

├── README.md                  # 项目说明2. **开始动画演奏** �

├── QUICKSTART.md             # 快速开始指南   - 点击"Start Animation"按钮

├── COMPLETE_GUIDE.md         # 完整使用指南   - 像素化从(0,0)开始，逐块生成

├── UI_AND_VISUAL_IMPROVEMENTS.md  # UI 改进文档   - 每个像素块自动播放对应音符

├── Jersey10-Regular.ttf      # 像素字体   - 使用WASD键实时控制音高：

├── Silkscreen-Regular.ttf    # 备用字体     - **W**: 升高八度（更明亮）

└── docs/                      # 技术文档     - **S**: 降低八度（更低沉）

    ├── 8BIT_MELODY_GUIDE.md     - **A**: 降低半音（微调）

    ├── HSV_MELODY_GUIDE.md     - **D**: 升高半音（微调）

    ├── MAC_OS_CLASSIC_STYLE.md     - **Space**: 暂停/继续

    ├── DUAL_TRACK_SYSTEM.md

    ├── DITHERING_AND_MOSHING_GUIDE.md3. **观察和互动** 🎮

    ├── VISUAL_FLOW_DIAGRAM.md   - 左侧：观看像素块逐个填充

    ├── LIVE_PERFORMANCE_GUIDE.md   - 右侧：查看实时进度和控制提示

    ├── REAL_TIME_AUDIO_GUIDE.md   - 状态栏：显示当前播放位置和进度

    ├── TESTING_GUIDE.md

    └── archive/               # 过时文档归档4. **完成后操作** ✨

```   - 点击"Replay Animation"重新演奏

   - 点击"Generate Melody"生成完整MIDI

---   - 点击"Save MIDI"保存音乐文件



## 🎯 核心依赖#### 📝 传统模式



| 库 | 版本 | 用途 |1. **加载图片** → 2. **Generate Melody** → 3. **Play** → 4. **Save**

|---|---|---|

| `Pillow` | 10.4.0 | 图像处理和像素化 |## 🎨 工作原理

| `numpy` | 1.26.4 | 数值计算和波形生成 |

| `pygame` | 2.6.1 | 实时音频播放 |### 像素化处理

| `MIDIUtil` | 1.2.1 | MIDI 文件生成 |

| `tkinter` | - | GUI 界面（需单独安装） |程序使用矩阵处理将图像转换为8x8像素块：



---```python

1. 将原始图像缩小：原始宽度 ÷ 8 = 网格宽度

## 🎨 视觉效果详解2. 使用NEAREST插值保持清晰边缘

3. 放大到像素块尺寸（每个像素块 = 8x8 pixels）

### 1-bit 风格4. 每个像素块提取一个代表性RGB值

- **调色板**: 黑色、深粉、浅粉、米色等 10 种颜色```

- **抖动图案**: 4×4 Bayer 矩阵，模拟经典 1-bit 纹理

- **色温感知**: 暖色→粉色系，冷色→米色系### RGB到音乐的转换算法



### Glitch 效果```python

- **RGB 通道分离**: 随机偏移红蓝通道音高 (Pitch) = f(Red值)

- **扫描线故障**: 4 种类型（重复、偏移、失真、增亮）  - 红色值映射到音阶中的音符

- **像素位移**: 随机块状位移  - 支持C大调音阶

- **粒子 Shift**: 微弱的像素交换和抖动  - 可自动调整八度



---时长 (Duration) = f(Green值)

  - 绿色值映射到节拍长度

## 🔧 自定义配置  - 范围：0.25 - 2.0 拍



### 修改像素大小力度 (Velocity) = f(Blue值)

```python  - 蓝色值映射到MIDI velocity

# main.py, line 45  - 范围：60 - 127

self.pixel_size = 10  # 改为 15 或 20```

```

### 采样策略

### 修改最大像素块数

```python程序提供两种处理模式：

# main.py, line ~1050

max_blocks = 800  # 增加到 1200 显示更多细节**1. 像素化模式（推荐，8-bit风格）**

```- 将图像转换为8x8像素块

- 每个像素块 = 一个音符

### 修改音阶- 网格状采样，从左到右、从上到下

```python- 适合生成复古8-bit游戏音乐

# melody_generator.py, line ~48

self.scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C 大调五声音阶**2. 原始采样模式**

```- 网格采样方法从图像中提取具有代表性的RGB值

- 默认采样32个点

---- 均匀分布在整个图像上

- 可配置采样率以调整旋律长度

## 🐛 常见问题

## 📂 项目结构

### 1. 无法播放声音

```bash```

# 重装 pygameimage2melody/

pip uninstall pygame│

pip install pygame==2.6.1├── main.py                 # 主程序，GUI界面

```├── melody_generator.py     # 旋律生成模块

├── image_processor.py      # 图像处理模块

### 2. tkinter 无法导入├── requirements.txt        # 依赖包列表

```bash└── README.md              # 项目说明文档

# macOS```

brew install python-tk@3.12

## 🎯 模块说明

# Ubuntu/Debian

sudo apt-get install python3-tk### main.py

```- 实现Tkinter GUI界面

- 管理用户交互

### 3. MIDI 文件无法打开- 协调图像处理和音乐生成

- 确保文件扩展名是 `.mid`（程序会自动添加）

- 使用 GarageBand、Logic Pro 或 Ableton Live 打开### image_processor.py

- 检查文件大小（应 > 100 bytes）- 加载和处理图像

- 提取RGB数据

### 4. 动画太慢/太快- 支持多种采样方法（网格、随机、边缘）

- 使用 `↑↓←→` 键实时调整速度

- 按 `R` 键重置到默认速度 1.0x### melody_generator.py

- RGB到音符的转换

---- MIDI文件生成

- 音乐播放功能

## 📚 详细文档

## 🎼 示例

- **[QUICKSTART.md](QUICKSTART.md)** - 新手快速入门

- **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** - 完整功能指南### 输入

- **[docs/HSV_MELODY_GUIDE.md](docs/HSV_MELODY_GUIDE.md)** - HSV 音乐映射原理任意图片文件（如：风景照、肖像、抽象画等）

- **[docs/MAC_OS_CLASSIC_STYLE.md](docs/MAC_OS_CLASSIC_STYLE.md)** - 界面设计说明

- **[docs/DUAL_TRACK_SYSTEM.md](docs/DUAL_TRACK_SYSTEM.md)** - 双轨系统架构### 输出

- **[docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - 测试和调试- 实时显示的图片

- 详细的RGB分析数据

---- 可播放的8-bit旋律

- 可导出的MIDI文件

## 🎬 示例效果

## ⚙️ 配置选项

### 输入

- 任意图片（PNG、JPG、JPEG、BMP、GIF）可以在代码中修改以下参数：

- 推荐尺寸：500×500 到 2000×2000

```python

### 输出# image_processor.py

- **视觉**: Mac OS Classic 1-bit 风格动画sample_rate = 32  # 采样点数量（影响旋律长度）

- **音频**: 8-bit 方波音效

- **文件**: 标准 MIDI 文件（.mid）# melody_generator.py

tempo = 120       # 速度（BPM）

### 动画流程scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # 音阶定义

``````

加载图片 → 像素化处理 → 逐块动画 → Glitch 效果 → 轨迹渐淡 → 完成

   ↓           ↓            ↓           ↓            ↓          ↓## 🔧 系统要求

 原图    1-bit处理    逐步显示    故障特效    视觉轨迹    保存 MIDI

```- **操作系统**: Windows, macOS, Linux

- **Python版本**: 3.8+

---- **内存**: 最少512MB

- **显示器**: 最低分辨率1200x700

## 🎓 技术亮点

## 🐛 故障排除

1. **双轨架构** - 视觉和音频分离，互不干扰

2. **实时合成** - pygame 方波生成，无需 MIDI 设备### 常见问题

3. **HSV 色彩空间** - 更符合人类感知的音乐映射

4. **Progressive Glitch** - 随进度变化的动态故障效果1. **pygame音频播放问题**

5. **1-bit 美学** - 经典 Mac OS 抖动算法   ```bash

6. **键盘实时控制** - 音高和速度动态调整   # 重新安装pygame

   pip uninstall pygame

---   pip install pygame

   ```

## 🤝 贡献

2. **图片无法加载**

欢迎提交 Issue 和 Pull Request！   - 确保图片格式受支持

   - 检查文件路径是否包含特殊字符

### 开发建议

- Fork 本仓库3. **MIDI播放无声音**

- 创建功能分支 (`git checkout -b feature/AmazingFeature`)   - 确保系统音量已开启

- 提交更改 (`git commit -m 'Add some AmazingFeature'`)   - 检查是否安装了MIDI音效库

- 推送到分支 (`git push origin feature/AmazingFeature`)

- 开启 Pull Request## 🎨 自定义扩展



---### 添加新的音阶



## 📝 更新日志编辑 `melody_generator.py` 中的 `scale_notes` 列表：



### v4.0 (Current)```python

- ✨ 添加键盘速度控制（↑↓←→ + R）# 例如：小调音阶

- ✨ 自动中间段加速（30%-70% 快 2 倍）self.scale_notes = [60, 62, 63, 65, 67, 68, 70, 72]  # C minor

- ✨ 微弱粒子 Shift 效果（wiredfriend 风格）```

- 🐛 修复 MIDI 文件保存格式问题

- 🐛 修复动画显示原始颜色问题### 更改采样方法

- 💄 Save/Load 按钮粉色高亮效果

在 `image_processor.py` 中使用不同的采样方法：

### v3.0

- ✨ Mac OS Classic 1-bit 风格```python

- ✨ Glitch Art 动画效果# 使用随机采样

- ✨ 渐淡轨迹系统rgb_data = image_processor.extract_rgb_data_advanced(image_path, method='random')

- ✨ 双轨架构（视觉/音频分离）

# 使用边缘采样

### v2.0rgb_data = image_processor.extract_rgb_data_advanced(image_path, method='edge')

- ✨ HSV 色彩空间```

- ✨ 实时播放和键盘控制

- ✨ MIDI 导出功能## � 详细文档



---### v3.0 新文档

- **[DITHERING_AND_MOSHING_GUIDE.md](DITHERING_AND_MOSHING_GUIDE.md)** - Floyd-Steinberg抖动和数据损坏详细技术文档

## 📄 许可证- **[MAC_OS_CLASSIC_STYLE.md](MAC_OS_CLASSIC_STYLE.md)** - Mac OS Classic界面设计指南

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - 快速测试指南

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件- **[VISUAL_FLOW_DIAGRAM.md](VISUAL_FLOW_DIAGRAM.md)** - 可视化流程图和示例

- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - 完整实现总结

---

### 其他指南

## 👨‍💻 作者- **[HSV_MELODY_GUIDE.md](HSV_MELODY_GUIDE.md)** - HSV色彩到音乐映射详解

- **[SOUND_TROUBLESHOOTING.md](SOUND_TROUBLESHOOTING.md)** - 音频问题排查

**Melos47**- **[QUICKSTART.md](QUICKSTART.md)** - 快速开始指南

- GitHub: [@Melos47](https://github.com/Melos47)

- Project: [image2melody](https://github.com/Melos47/image2melody)## �📝 许可证



---此项目仅供学习和研究使用。



## 🙏 致谢## 👨‍💻 作者



- **Python** - 编程语言Melos47

- **tkinter** - GUI 框架

- **Pillow** - 图像处理库## 🙏 致谢

- **pygame** - 多媒体库

- **MIDIUtil** - MIDI 生成库- Tkinter - Python GUI框架

- **Jersey 10** - 像素字体- Pillow - Python图像处理库

- **fauux.neocities.org** - Glitch art 灵感来源- MIDIUtil - MIDI文件生成库

- pygame - 多媒体库

---- Jersey 10 字体 - 复古像素字体



<div align="center">## 📮 联系方式



**🎨 将视觉艺术转换为听觉艺术的魔法 🎵**如有问题或建议，请在GitHub仓库中创建Issue。



Made with ❤️ by Melos47---



</div>**享受将视觉艺术转换为听觉艺术的乐趣！** 🎨 → 🎵 → ⚡

