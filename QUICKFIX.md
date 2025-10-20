# 🚨 听不到声音？ 快速解决方案！

## 问题：没有MIDI设备

运行 `python test_midi.py` 显示：
```
❌ 没有找到MIDI设备!
```

**这就是为什么听不到声音！** macOS需要配置MIDI输出设备。

---

## 🎯 最快的解决方案（5分钟）

### 步骤1：启用IAC Driver

1. **打开Audio MIDI Setup**
   - 按 `⌘ + Space`
   - 输入 "Audio MIDI Setup"
   - 回车

2. **显示MIDI Studio**
   - 点击菜单：Window → Show MIDI Studio
   - 或按 `⌘ + 2`

3. **启用IAC Driver**
   - 双击 "IAC Driver" 图标
   - 勾选 ✅ "Device is online"
   - 点击 "Apply"

### 步骤2：选择音频输出方式

**方式A：使用GarageBand（推荐）**
```bash
# 打开GarageBand
open -a GarageBand

# 创建 → 空项目 → 软件乐器
# 保持GarageBand运行在后台
```

**方式B：下载SimpleSynth**
- 访问：https://notahat.com/simplesynth/
- 下载、安装、启动

### 步骤3：验证

```bash
cd /Users/siqi/Documents/PolyU/Sem1/SD5913/image2melody
source venv/bin/activate
python test_midi.py
```

应该看到：
```
✓ 设备 0: IAC Driver Bus 1
✓ 默认输出设备: 0
```

### 步骤4：运行程序

```bash
python main.py
```

启动时应该看到：
```
✓ pygame.midi initialized
✓ MIDI output initialized on device 0
```

现在加载图片，开始动画，就能听到声音了！🎵

---

## 🔍 检查清单

- [ ] IAC Driver已启用（Device is online ✅）
- [ ] GarageBand或SimpleSynth正在运行
- [ ] `test_midi.py` 显示有设备
- [ ] 系统音量已打开
- [ ] 图片饱和度高（不要用灰色图）

---

## 📞 快速帮助

### 设置向导
```bash
source venv/bin/activate
python setup_midi.py
```

### 测试MIDI
```bash
source venv/bin/activate
python test_midi.py
```

### 完整指南
查看 `WHY_NO_SOUND.md` 文件

---

**祝您早日听到美妙的8-bit音乐！** 🎮🎵✨
