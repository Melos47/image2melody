# 🚀 快速启动指南

## ⚠️ 重要提示

**不要使用系统的 python3 命令！**

❌ 错误方式：
```bash
python3 main.py                                    # 会报错：ModuleNotFoundError: No module named '_tkinter'
/opt/homebrew/bin/python3 main.py                 # 会报错：ModuleNotFoundError: No module named '_tkinter'
```

✅ 正确方式：

### 方法1：使用启动脚本（最简单）
```bash
./run.sh
```

### 方法2：手动激活虚拟环境
```bash
source venv/bin/activate
python main.py
```

### 方法3：直接使用虚拟环境的Python
```bash
venv/bin/python main.py
```

---

## 📋 完整安装步骤（仅需一次）

如果这是第一次运行，请按以下步骤操作：

### 1. 安装Python 3.12（带tkinter支持）
```bash
/opt/homebrew/bin/brew install python-tk@3.12
```

### 2. 创建虚拟环境
```bash
/opt/homebrew/bin/python3.12 -m venv venv
```

### 3. 安装依赖
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 运行程序
```bash
./run.sh
```

---

## 🎨 使用说明

### 🎬 实时演奏模式（新功能！推荐）

1. **加载图片** 📁
   - 点击"Load Image"按钮
   - 选择任意图片（PNG、JPG等）

2. **开始动画** �
   - 点击"Start Animation"按钮
   - 观看像素从左到右、从上到下生成
   - 每个像素块自动播放音符！

3. **实时控制** �
   - **W**: 升高八度（+12半音）
   - **S**: 降低八度（-12半音）
   - **A**: 降低半音（-1）
   - **D**: 升高半音（+1）
   - **Space**: 暂停/继续

4. **享受创作** 🎵
   - 根据颜色和感觉调整音高
   - 创造独一无二的音乐
   - 完成后可重放或保存MIDI

### � 传统模式

1. **加载图片** → 2. **Generate Melody** → 3. **Play** → 4. **Save**

---

## 🐛 常见问题

### 问题：ModuleNotFoundError: No module named '_tkinter'
**解决方案**：使用虚拟环境运行，不要直接用 `python3` 命令

### 问题：No module named 'PIL' 或其他模块
**解决方案**：确保在虚拟环境中安装了依赖
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 问题：Permission denied: ./run.sh
**解决方案**：添加执行权限
```bash
chmod +x run.sh
```

---

## 💡 技术细节

### 为什么需要Python 3.12？
- macOS的Python 3.13（Homebrew版本）没有包含tkinter支持
- Python 3.12通过 `python-tk@3.12` 包提供完整的tkinter支持

### 虚拟环境的作用？
- 隔离项目依赖，避免污染系统Python
- 确保使用正确版本的Python和包

### RGB到音乐的映射
- **R (红色)** → 音高（Pitch）：0-255 → C4-C6
- **G (绿色)** → 时长（Duration）：0-255 → 0.25-2.0拍
- **B (蓝色)** → 力度（Velocity）：0-255 → 60-127

### 像素化处理
- 图像被转换为8x8像素块的网格
- 每个像素块代表一个音符
- 创造真实的8-bit游戏视觉和音频效果
- 像素块从左到右、从上到下扫描生成旋律序列

---

**祝您使用愉快！** 🎵✨
