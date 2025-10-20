# 🎵 声音设置快速指南

## 当前状态：❌ 没有MIDI设备

运行 `test_midi.py` 显示：
```
❌ 没有找到MIDI设备!
```

这意味着您需要在macOS上配置MIDI输出设备才能听到声音。

---

## ✅ 解决方案（2选1）

### 方案1：启用IAC Driver（推荐，免费）

这是macOS内置的虚拟MIDI设备，无需安装额外软件。

#### 步骤：

1. **打开Audio MIDI Setup**
   ```bash
   open -a "Audio MIDI Setup"
   ```
   或者从 Applications → Utilities → Audio MIDI Setup

2. **显示MIDI Studio**
   - 点击菜单 Window → Show MIDI Studio
   - 或按快捷键 `⌘ + 2`

3. **启用IAC Driver**
   - 在MIDI Studio窗口中找到"IAC Driver"图标
   - 双击"IAC Driver"图标
   - 勾选 "Device is online"
   - 点击"Apply"

4. **验证设置**
   ```bash
   source venv/bin/activate
   python test_midi.py
   ```
   
   应该看到：
   ```
   ✓ 设备 0:
     名称: IAC Driver Bus 1
     类型: 输出
   ```

5. **运行程序**
   ```bash
   python main.py
   ```

**注意**: IAC Driver只是一个虚拟MIDI端口，它会转发MIDI信号，但不会产生实际声音。要听到声音，您还需要：
- 在macOS设置中配置IAC Driver连接到内置合成器
- 或者使用方案2（SimpleSynth）

---

### 方案2：安装SimpleSynth（最简单）

SimpleSynth是一个免费的软件MIDI合成器，可以直接播放MIDI音符。

#### 下载安装：

1. **访问官网下载**
   - 网址: https://notahat.com/simplesynth/
   - 点击"Download SimpleSynth"
   - 下载.dmg文件

2. **安装**
   - 打开下载的.dmg文件
   - 将SimpleSynth拖到Applications文件夹

3. **启动SimpleSynth**
   ```bash
   open -a SimpleSynth
   ```
   
   或从Applications文件夹双击SimpleSynth图标

4. **配置SimpleSynth**
   - SimpleSynth启动后会显示一个小窗口
   - 确保窗口显示"CoreMIDI ON"
   - 保持SimpleSynth在后台运行

5. **验证设置**
   ```bash
   source venv/bin/activate
   python test_midi.py
   ```
   
   应该看到SimpleSynth设备

6. **运行程序**
   ```bash
   python main.py
   ```

---

## 🎹 验证声音

设置完成后，运行测试：

```bash
source venv/bin/activate
python test_midi.py
```

**成功的输出应该类似：**
```
✓ 设备 0:
  名称: IAC Driver Bus 1 (或 SimpleSynth virtual input)
  类型: 输出
✓ 默认输出设备: 0
```

**然后运行主程序：**
```bash
python main.py
```

启动时应该看到：
```
✓ pygame.midi initialized
✓ MIDI output initialized on device 0
```

---

## 🔍 故障排除

### 问题1: 设置后仍然没有设备

**解决：**
1. 重启Terminal
2. 确认IAC Driver或SimpleSynth正在运行
3. 重新运行test_midi.py

### 问题2: 有设备但听不到声音

**IAC Driver用户：**
- IAC Driver需要配置音频路由
- 建议改用SimpleSynth（更简单）

**SimpleSynth用户：**
- 确认SimpleSynth窗口显示"CoreMIDI ON"
- 检查macOS系统音量
- 检查SimpleSynth的音量滑块

### 问题3: 程序运行但声音很小

**解决：**
- 这是正常的，灰色/低饱和度的像素会产生弱音量
- 尝试使用鲜艳、饱和度高的图片
- 或在SimpleSynth中调高音量

---

## 📝 配置总结

| 方案 | 优点 | 缺点 |
|------|------|------|
| IAC Driver | 免费，系统内置 | 需要额外配置音频路由 |
| SimpleSynth | 简单，即装即用 | 需要下载安装 |

**推荐：SimpleSynth**（更简单，直接能听到声音）

---

## ✨ 设置完成后

1. **运行程序**
   ```bash
   source venv/bin/activate
   python main.py
   ```

2. **加载图片**
   - 建议使用鲜艳的像素艺术或纯色图案

3. **享受音乐**
   - 每个像素会播放对应的音符
   - 使用WASD调整音高
   - 完成后可以保存MIDI文件

---

**Good luck!** 🎵✨
