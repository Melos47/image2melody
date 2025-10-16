# 🎵 Image to 8-bit Melody Converter

将图像转换为8-bit风格旋律的Python应用程序。该程序分析图片中的RGB值，并生成相应的MIDI音乐。

## 📸 功能特点

- **双框架UI设计**：
  - 左侧框架显示加载的图片
  - 右侧框架显示分析信息和旋律数据
  
- **RGB到音乐映射**：
  - **红色 (R)**：决定音高/音符频率
  - **绿色 (G)**：决定音符时长
  - **蓝色 (B)**：决定音符力度/音量
  
- **音乐生成**：
  - 生成8-bit风格的旋律
  - 支持实时播放
  - 导出MIDI文件格式

## 🚀 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/Melos47/image2melody.git
cd image2melody
```

### 2. 安装tkinter支持（macOS用户）

在macOS上，需要先安装支持tkinter的Python：

```bash
/opt/homebrew/bin/brew install python-tk@3.12
```

### 3. 创建虚拟环境

```bash
/opt/homebrew/bin/python3.12 -m venv venv
```

### 4. 激活虚拟环境并安装依赖

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 依赖包说明

- `Pillow`: 图像处理
- `numpy`: 数值计算
- `MIDIUtil`: MIDI文件生成
- `pygame`: 音频播放
- `tkinter`: GUI界面（需要单独安装python-tk）

## 💻 使用方法

### 启动应用

**方法1：使用启动脚本（推荐）**
```bash
./run.sh
```

**方法2：手动激活环境**
```bash
source venv/bin/activate
python main.py
```

### 操作步骤

1. **加载图片** 📁
   - 点击"Load Image"按钮
   - 选择一张图片（支持PNG, JPG, JPEG, BMP, GIF）
   - 图片将显示在左侧框架中

2. **生成旋律** 🎼
   - 点击"Generate Melody"按钮
   - 程序会分析图片的RGB值
   - 右侧框架会显示详细的音符信息

3. **播放旋律** ▶️
   - 点击"Play Melody"按钮
   - 欣赏由图片生成的8-bit旋律

4. **保存MIDI** 💾
   - 点击"Save MIDI"按钮
   - 选择保存位置
   - 生成的MIDI文件可以在任何MIDI播放器中使用

## 🎨 工作原理

### RGB到音乐的转换算法

```python
音高 (Pitch) = f(Red值)
  - 红色值映射到音阶中的音符
  - 支持C大调音阶
  - 可自动调整八度

时长 (Duration) = f(Green值)
  - 绿色值映射到节拍长度
  - 范围：0.25 - 2.0 拍

力度 (Velocity) = f(Blue值)
  - 蓝色值映射到MIDI velocity
  - 范围：60 - 127
```

### 采样策略

程序使用网格采样方法从图像中提取具有代表性的RGB值：
- 默认采样32个点
- 均匀分布在整个图像上
- 可配置采样率以调整旋律长度

## 📂 项目结构

```
image2melody/
│
├── main.py                 # 主程序，GUI界面
├── melody_generator.py     # 旋律生成模块
├── image_processor.py      # 图像处理模块
├── requirements.txt        # 依赖包列表
└── README.md              # 项目说明文档
```

## 🎯 模块说明

### main.py
- 实现Tkinter GUI界面
- 管理用户交互
- 协调图像处理和音乐生成

### image_processor.py
- 加载和处理图像
- 提取RGB数据
- 支持多种采样方法（网格、随机、边缘）

### melody_generator.py
- RGB到音符的转换
- MIDI文件生成
- 音乐播放功能

## 🎼 示例

### 输入
任意图片文件（如：风景照、肖像、抽象画等）

### 输出
- 实时显示的图片
- 详细的RGB分析数据
- 可播放的8-bit旋律
- 可导出的MIDI文件

## ⚙️ 配置选项

可以在代码中修改以下参数：

```python
# image_processor.py
sample_rate = 32  # 采样点数量（影响旋律长度）

# melody_generator.py
tempo = 120       # 速度（BPM）
scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # 音阶定义
```

## 🔧 系统要求

- **操作系统**: Windows, macOS, Linux
- **Python版本**: 3.8+
- **内存**: 最少512MB
- **显示器**: 最低分辨率1200x700

## 🐛 故障排除

### 常见问题

1. **pygame音频播放问题**
   ```bash
   # 重新安装pygame
   pip uninstall pygame
   pip install pygame
   ```

2. **图片无法加载**
   - 确保图片格式受支持
   - 检查文件路径是否包含特殊字符

3. **MIDI播放无声音**
   - 确保系统音量已开启
   - 检查是否安装了MIDI音效库

## 🎨 自定义扩展

### 添加新的音阶

编辑 `melody_generator.py` 中的 `scale_notes` 列表：

```python
# 例如：小调音阶
self.scale_notes = [60, 62, 63, 65, 67, 68, 70, 72]  # C minor
```

### 更改采样方法

在 `image_processor.py` 中使用不同的采样方法：

```python
# 使用随机采样
rgb_data = image_processor.extract_rgb_data_advanced(image_path, method='random')

# 使用边缘采样
rgb_data = image_processor.extract_rgb_data_advanced(image_path, method='edge')
```

## 📝 许可证

此项目仅供学习和研究使用。

## 👨‍💻 作者

Melos47

## 🙏 致谢

- Tkinter - Python GUI框架
- Pillow - Python图像处理库
- MIDIUtil - MIDI文件生成库
- pygame - 多媒体库

## 📮 联系方式

如有问题或建议，请在GitHub仓库中创建Issue。

---

**享受将视觉艺术转换为听觉艺术的乐趣！** 🎨 → 🎵
