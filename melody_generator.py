"""
Melody Generator Module
将RGB值转换为8-bit风格的音乐旋律
基于HSV（色相、饱和度、明度）生成音符
使用pygame.mixer直接生成波形声音（无需MIDI设备）
"""
from midiutil import MIDIFile
import pygame
import numpy as np
import tempfile
import os
import colorsys


class MelodyGenerator:
    def __init__(self):
        self.midi_file = None
        self.notes = []
        self.tempo = 160  # BPM - 8-bit风格通常更快
        self.temp_midi_path = None
        self.recorded_notes = []  # 记录所有播放的音符
        
        # 初始化pygame mixer用于直接播放波形音频（无需MIDI）
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.audio_initialized = True
            print("✓ Audio initialized successfully")
        except Exception as e:
            self.audio_initialized = False
            print(f"✗ Audio initialization failed: {e}")
        
        # 音阶定义 - 8-bit游戏风格的五声音阶
        # 使用C大调五声音阶: C, D, E, G, A
        self.pentatonic_scale = [60, 62, 64, 67, 69, 72, 74, 76]  # C4, D4, E4, G4, A4, C5, D5, E5
        
        # 完整音阶用于更复杂的旋律
        self.full_scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C, D, E, F, G, A, B, C (MIDI note numbers)
    
    def generate_square_wave(self, frequency, duration, volume=0.5):
        """
        生成8-bit风格的方波音频（无需MIDI设备）
        frequency: 频率（Hz）
        duration: 持续时间（秒）
        volume: 音量（0.0-1.0）
        """
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
    
    def midi_note_to_frequency(self, midi_note):
        """将MIDI音符号转换为频率（Hz）"""
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
    
    def play_note_direct(self, pitch, duration, velocity):
        """
        直接播放音符（使用波形生成，无需MIDI设备）
        pitch: MIDI音符号（60=C4）
        duration: 持续时间（秒）
        velocity: 音量（0-127）
        """
        if not self.audio_initialized:
            return
        
        try:
            frequency = self.midi_note_to_frequency(pitch)
            volume = velocity / 127.0 * 0.3  # 限制最大音量为0.3避免过响
            
            sound = self.generate_square_wave(frequency, duration, volume)
            sound.play()
            
        except Exception as e:
            print(f"播放音符失败: {e}")
        
    def rgb_to_hsv(self, r, g, b):
        """将RGB转换为HSV（色相、饱和度、明度）"""
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        return h, s, v
    
    def rgba_to_note_hsv(self, r, g, b, a=255):
        """
        基于HSV色彩空间生成8-bit风格音符
        H (Hue/色相): 决定音高 (0-1 -> 12个半音，循环色轮)
        S (Saturation/饱和度): 决定音量/力度 (0-1 -> 高饱和度=强音量)
        V (Value/明度): 决定时长 (0-1 -> 亮度高=长音符)
        A (Alpha/透明度): 额外的音量调节
        """
        # 转换到HSV色彩空间
        h, s, v = self.rgb_to_hsv(r, g, b)
        
        # 色相 (Hue) → 音高
        # 色相是0-1的循环值，映射到五声音阶
        scale_len = len(self.pentatonic_scale)
        pitch_index = int(h * scale_len) % scale_len
        base_pitch = self.pentatonic_scale[pitch_index]
        
        # 明度 (Value) → 八度偏移
        # 亮的颜色高音，暗的颜色低音
        if v > 0.7:
            octave_shift = 12  # 高一个八度
        elif v > 0.4:
            octave_shift = 0   # 标准八度
        else:
            octave_shift = -12 # 低一个八度
        
        pitch = base_pitch + octave_shift
        pitch = max(36, min(96, pitch))  # C2到C7
        
        # 明度 (Value) → 时长
        # 亮色=长音符，暗色=短音符
        if v > 0.7:
            duration = 0.25  # 1/4拍
        elif v > 0.4:
            duration = 0.125  # 1/8拍
        else:
            duration = 0.0625  # 1/16拍（非常短）
        
        # 饱和度 (Saturation) + Alpha → 力度
        # 高饱和度=鲜艳颜色=强音量
        # 低饱和度=灰色=弱音量
        saturation_velocity = int(50 + s * 60)  # 50-110
        alpha_factor = a / 255.0
        velocity = int(saturation_velocity * alpha_factor)
        velocity = max(40, min(127, velocity))
        
        return pitch, duration, velocity
    
    def rgba_to_note(self, r, g, b, a=255):
        """
        将RGBA值转换为8-bit风格的音符参数（使用HSV）
        """
        return self.rgba_to_note_hsv(r, g, b, a)
    
    def rgb_to_note(self, r, g, b):
        """
        将RGB值转换为音符参数（向后兼容）
        调用rgba_to_note，默认alpha=255
        """
        return self.rgba_to_note(r, g, b, 255)
    
    def generate_melody(self, rgb_data, max_notes=64):
        """
        从RGB数据生成旋律
        """
        # 限制音符数量以避免过长
        sample_size = min(len(rgb_data), max_notes)
        
        # 采样RGB数据
        if len(rgb_data) > max_notes:
            # 均匀采样
            indices = np.linspace(0, len(rgb_data) - 1, max_notes, dtype=int)
            sampled_rgb = [rgb_data[i] for i in indices]
        else:
            sampled_rgb = rgb_data
        
        # 创建MIDI文件
        self.midi_file = MIDIFile(1)  # 1个音轨
        track = 0
        channel = 0
        time = 0
        
        self.midi_file.addTempo(track, time, self.tempo)
        
        # 添加程序改变以获得8-bit音效 (Square wave)
        self.midi_file.addProgramChange(track, channel, time, 80)  # Lead 1 (square)
        
        self.notes = []
        current_time = 0
        
        # 生成音符
        for i, (r, g, b) in enumerate(sampled_rgb):
            pitch, duration, velocity = self.rgb_to_note(r, g, b)
            
            self.midi_file.addNote(track, channel, pitch, current_time, duration, velocity)
            
            self.notes.append({
                'index': i + 1,
                'rgb': (r, g, b),
                'pitch': pitch,
                'duration': duration,
                'velocity': velocity,
                'time': current_time
            })
            
            current_time += duration
        
        # 生成信息文本
        melody_info = self.generate_melody_info()
        
        return self.notes, melody_info
    
    def generate_melody_info(self):
        """生成旋律信息文本"""
        if not self.notes:
            return "No melody generated yet."
        
        info = f"Total Notes: {len(self.notes)}\n"
        info += f"Tempo: {self.tempo} BPM\n"
        info += f"Total Duration: {self.notes[-1]['time'] + self.notes[-1]['duration']:.2f} beats\n"
        info += f"Estimated Time: {((self.notes[-1]['time'] + self.notes[-1]['duration']) / self.tempo * 60):.2f} seconds\n\n"
        
        info += "Note Mapping:\n"
        info += f"{'-' * 50}\n"
        info += f"{'#':<5} {'RGB':<18} {'Pitch':<7} {'Dur':<7} {'Vel':<5}\n"
        info += f"{'-' * 50}\n"
        
        # 显示前20个音符
        for note in self.notes[:20]:
            rgb_str = f"({note['rgb'][0]:3d},{note['rgb'][1]:3d},{note['rgb'][2]:3d})"
            pitch_name = self.midi_note_to_name(note['pitch'])
            info += f"{note['index']:<5} {rgb_str:<18} {pitch_name:<7} {note['duration']:<7.2f} {note['velocity']:<5}\n"
        
        if len(self.notes) > 20:
            info += f"... and {len(self.notes) - 20} more notes\n"
        
        info += f"\n{'=' * 50}\n"
        info += "Legend:\n"
        info += "- Pitch: Musical note (C4, D4, E4, etc.)\n"
        info += "- Dur: Note duration in beats\n"
        info += "- Vel: Note velocity (volume, 0-127)\n"
        
        return info
    
    def midi_note_to_name(self, midi_number):
        """将MIDI音符号转换为音符名称"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi_number // 12) - 1
        note = notes[midi_number % 12]
        return f"{note}{octave}"
    
    def save_midi(self, file_path):
        """保存MIDI文件"""
        if not self.midi_file:
            raise ValueError("No melody generated yet!")
        
        with open(file_path, "wb") as output_file:
            self.midi_file.writeFile(output_file)
        
        return file_path
    
    def play_melody(self):
        """播放生成的旋律"""
        if not self.midi_file:
            raise ValueError("No melody generated yet!")
        
        # 创建临时MIDI文件
        if self.temp_midi_path and os.path.exists(self.temp_midi_path):
            os.remove(self.temp_midi_path)
        
        # 使用临时文件
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.mid', delete=False) as temp_file:
            self.temp_midi_path = temp_file.name
            self.midi_file.writeFile(temp_file)
        
        # 播放MIDI文件
        try:
            pygame.mixer.music.load(self.temp_midi_path)
            pygame.mixer.music.play()
            
            # 等待播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        finally:
            # 清理临时文件
            if self.temp_midi_path and os.path.exists(self.temp_midi_path):
                try:
                    pygame.mixer.music.unload()
                    os.remove(self.temp_midi_path)
                except:
                    pass
    
    def save_recorded_melody(self, file_path):
        """
        保存录制的旋律为MIDI文件
        使用recorded_notes列表中的所有音符
        """
        if not self.recorded_notes:
            raise ValueError("No notes recorded yet!")
        
        # 创建新的MIDI文件
        midi_file = MIDIFile(1)
        track = 0
        channel = 0
        time = 0
        
        midi_file.addTempo(track, time, self.tempo)
        midi_file.addProgramChange(track, channel, time, 80)  # Square wave
        
        current_time = 0
        for note in self.recorded_notes:
            pitch = note['pitch']
            duration = note['duration']
            velocity = note['velocity']
            
            midi_file.addNote(track, channel, pitch, current_time, duration, velocity)
            current_time += duration
        
        # 保存文件
        with open(file_path, "wb") as output_file:
            midi_file.writeFile(output_file)
        
        print(f"✓ Saved {len(self.recorded_notes)} notes to {file_path}")
        return file_path
    
    def clear_recorded_notes(self):
        """清空录制的音符"""
        self.recorded_notes = []
    
    def __del__(self):
        """清理资源"""
        if self.temp_midi_path and os.path.exists(self.temp_midi_path):
            try:
                os.remove(self.temp_midi_path)
            except:
                pass
