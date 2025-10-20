"""
测试直接音频播放（无需MIDI设备）
播放一段简单的8-bit风格旋律
"""
import pygame
import numpy as np
import time

def generate_square_wave(frequency, duration, volume=0.5):
    """生成8-bit风格的方波音频"""
    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    
    # 生成方波（8-bit经典声音）
    t = np.linspace(0, duration, num_samples, False)
    wave = np.sign(np.sin(2 * np.pi * frequency * t))
    
    # 应用音量和添加淡出效果（防止爆音）
    fade_length = int(sample_rate * 0.01)  # 10ms淡出
    fade_out = np.ones(num_samples)
    if fade_length < num_samples:
        fade_out[-fade_length:] = np.linspace(1, 0, fade_length)
    wave = wave * fade_out * volume
    
    # 转换为16位整数
    wave = (wave * 32767).astype(np.int16)
    
    # 创建立体声
    stereo_wave = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo_wave)

def midi_note_to_frequency(midi_note):
    """将MIDI音符号转换为频率（Hz）"""
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def main():
    print("=" * 60)
    print("8-BIT AUDIO TEST - 直接播放测试（无需MIDI设备）")
    print("=" * 60)
    
    # 初始化pygame mixer
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("✓ Audio initialized successfully")
    except Exception as e:
        print(f"✗ Audio initialization failed: {e}")
        return
    
    # 播放C大调五声音阶: C, D, E, G, A
    pentatonic_scale = [60, 62, 64, 67, 69]  # C4, D4, E4, G4, A4
    note_names = ['C4', 'D4', 'E4', 'G4', 'A4']
    
    print("\n播放8-bit五声音阶...")
    print("-" * 60)
    
    for midi_note, name in zip(pentatonic_scale, note_names):
        frequency = midi_note_to_frequency(midi_note)
        print(f"Playing {name} ({midi_note}) - {frequency:.2f} Hz")
        
        sound = generate_square_wave(frequency, 0.3, volume=0.3)
        sound.play()
        time.sleep(0.35)  # 稍微长一点以听清音符
    
    print("\n播放简单的8-bit旋律...")
    print("-" * 60)
    
    # 简单的旋律: C-E-G-E-C
    melody = [60, 64, 67, 64, 60]
    durations = [0.2, 0.2, 0.4, 0.2, 0.4]
    
    for midi_note, duration in zip(melody, durations):
        frequency = midi_note_to_frequency(midi_note)
        print(f"♪ {midi_note} - {frequency:.2f} Hz - {duration}s")
        
        sound = generate_square_wave(frequency, duration, volume=0.3)
        sound.play()
        time.sleep(duration + 0.05)
    
    print("\n" + "=" * 60)
    print("✓ 测试完成！你应该听到了8-bit风格的声音")
    print("如果听不到，请检查:")
    print("  1. 系统音量是否打开")
    print("  2. 扬声器/耳机是否连接")
    print("=" * 60)

if __name__ == "__main__":
    main()
