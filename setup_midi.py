#!/usr/bin/env python3
"""
MIDI设备设置向导
帮助用户配置MIDI输出设备
"""
import subprocess
import os
import sys

def print_header(text):
    print("\n" + "=" * 60)
    print(text.center(60))
    print("=" * 60 + "\n")

def print_step(number, text):
    print(f"\n📍 步骤 {number}: {text}")
    print("-" * 60)

def check_midi_devices():
    """检查MIDI设备"""
    try:
        import pygame.midi
        pygame.midi.init()
        count = pygame.midi.get_count()
        
        if count > 0:
            print(f"✅ 找到 {count} 个MIDI设备:")
            for i in range(count):
                info = pygame.midi.get_device_info(i)
                name = info[1].decode()
                is_output = info[3]
                if is_output:
                    print(f"   ✓ {name}")
            pygame.midi.quit()
            return True
        else:
            print("❌ 没有找到MIDI设备")
            pygame.midi.quit()
            return False
    except Exception as e:
        print(f"❌ 检查MIDI设备时出错: {e}")
        return False

def open_audio_midi_setup():
    """打开Audio MIDI Setup"""
    try:
        subprocess.run(["open", "-a", "Audio MIDI Setup"], check=True)
        return True
    except:
        return False

def main():
    print_header("🎵 Image2Melody MIDI设置向导")
    
    print("这个向导将帮助您配置MIDI输出设备，以便听到8-bit音乐。\n")
    
    # 检查当前状态
    print_step(1, "检查当前MIDI设备状态")
    has_midi = check_midi_devices()
    
    if has_midi:
        print("\n✨ 太好了！您已经配置好MIDI设备了！")
        print("\n您可以直接运行程序：")
        print("   python main.py")
        return
    
    # 需要配置
    print("\n需要配置MIDI设备才能听到声音。\n")
    print("有两个选项：")
    print("  1. 启用IAC Driver（macOS内置，免费）")
    print("  2. 安装SimpleSynth（下载安装，简单直接）")
    
    while True:
        choice = input("\n请选择 (1 或 2, q退出): ").strip()
        
        if choice.lower() == 'q':
            print("\n再见！👋")
            return
        
        if choice == '1':
            setup_iac_driver()
            break
        elif choice == '2':
            setup_simplesynth()
            break
        else:
            print("❌ 无效选择，请输入 1 或 2")
    
    # 重新检查
    print_step(3, "验证配置")
    print("等待3秒后检查...")
    import time
    time.sleep(3)
    
    if check_midi_devices():
        print("\n🎉 成功！MIDI设备已配置！")
        print("\n现在可以运行程序了：")
        print("   python main.py")
    else:
        print("\n⚠️ 还没有检测到MIDI设备。")
        print("请按照提示完成配置，然后重新运行此向导。")

def setup_iac_driver():
    """设置IAC Driver"""
    print_step(2, "启用IAC Driver")
    
    print("正在打开 Audio MIDI Setup...")
    if open_audio_midi_setup():
        print("✓ Audio MIDI Setup 已打开\n")
    else:
        print("❌ 无法自动打开，请手动打开：")
        print("   Applications → Utilities → Audio MIDI Setup\n")
    
    print("请按照以下步骤操作：")
    print()
    print("1️⃣  在Audio MIDI Setup窗口中")
    print("   点击菜单：Window → Show MIDI Studio")
    print("   (或按快捷键 ⌘ + 2)")
    print()
    print("2️⃣  在MIDI Studio窗口中")
    print("   找到并双击 'IAC Driver' 图标")
    print()
    print("3️⃣  在弹出的窗口中")
    print("   勾选 ✅ 'Device is online'")
    print("   点击 'Apply' 按钮")
    print()
    print("4️⃣  关闭所有窗口")
    print()
    
    input("完成后按回车键继续...")
    
    print("\n⚠️ 注意：IAC Driver需要配合GarageBand或Logic Pro才能听到声音")
    print("   或者您可以安装SimpleSynth来直接播放声音")

def setup_simplesynth():
    """设置SimpleSynth"""
    print_step(2, "安装SimpleSynth")
    
    print("SimpleSynth是一个免费的MIDI合成器。\n")
    print("下载链接：https://notahat.com/simplesynth/")
    print()
    print("请按照以下步骤操作：")
    print()
    print("1️⃣  在浏览器中访问上述网址")
    print("   点击 'Download SimpleSynth'")
    print()
    print("2️⃣  下载完成后")
    print("   打开 .dmg 文件")
    print("   将SimpleSynth拖到Applications文件夹")
    print()
    print("3️⃣  启动SimpleSynth")
    print("   从Applications文件夹双击SimpleSynth")
    print("   或在终端运行: open -a SimpleSynth")
    print()
    print("4️⃣  确认SimpleSynth窗口显示")
    print("   'CoreMIDI ON' (绿色)")
    print("   如果是红色OFF，点击它切换到ON")
    print()
    
    print("是否已经完成SimpleSynth安装？")
    installed = input("输入 y 继续，n 稍后再说: ").strip().lower()
    
    if installed == 'y':
        print("\n尝试启动SimpleSynth...")
        try:
            subprocess.run(["open", "-a", "SimpleSynth"])
            print("✓ SimpleSynth已启动")
            print("请保持SimpleSynth在后台运行")
        except:
            print("❌ 无法自动启动，请手动启动SimpleSynth")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断。再见！👋")
        sys.exit(0)
