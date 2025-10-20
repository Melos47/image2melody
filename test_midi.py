#!/usr/bin/env python3
"""
测试MIDI设备
"""
import pygame.midi

pygame.midi.init()

print("=" * 60)
print("MIDI设备信息")
print("=" * 60)

device_count = pygame.midi.get_count()
print(f"\n总共发现 {device_count} 个MIDI设备:\n")

if device_count == 0:
    print("❌ 没有找到MIDI设备!")
    print("\n解决方案:")
    print("1. 安装SimpleSynth (https://notahat.com/simplesynth/)")
    print("2. 或启用IAC Driver (Audio MIDI Setup)")
    print("3. 然后重新运行此脚本")
else:
    for i in range(device_count):
        info = pygame.midi.get_device_info(i)
        # info = (interf, name, input, output, opened)
        interf, name, is_input, is_output, opened = info
        
        device_type = []
        if is_input:
            device_type.append("输入")
        if is_output:
            device_type.append("输出")
        
        status = "✓" if is_output else "○"
        print(f"{status} 设备 {i}:")
        print(f"  名称: {name.decode()}")
        print(f"  接口: {interf.decode()}")
        print(f"  类型: {', '.join(device_type)}")
        print(f"  状态: {'已打开' if opened else '未打开'}")
        print()
    
    default_output = pygame.midi.get_default_output_id()
    if default_output == -1:
        print("❌ 没有找到默认输出设备")
    else:
        print(f"✓ 默认输出设备: {default_output}")
        info = pygame.midi.get_device_info(default_output)
        print(f"  名称: {info[1].decode()}")

pygame.midi.quit()

print("\n" + "=" * 60)
