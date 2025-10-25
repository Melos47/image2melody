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
        
        # 确保文件扩展名是 .mid
        if not file_path.lower().endswith('.mid'):
            file_path += '.mid'
        
        # 创建新的MIDI文件
        midi_file = MIDIFile(1)  # 1个轨道
        track = 0
        channel = 0
        time = 0
        
        # 设置音轨名称
        midi_file.addTrackName(track, time, "Image2Melody")
        midi_file.addTempo(track, time, self.tempo)
        midi_file.addProgramChange(track, channel, time, 80)  # Square wave (8-bit音效)
        
        current_time = 0
        note_count = 0
        
        for note in self.recorded_notes:
            pitch = int(note['pitch'])
            duration = float(note['duration'])
            velocity = int(note['velocity'])
            
            # 确保参数在有效范围内
            pitch = max(0, min(127, pitch))
            velocity = max(0, min(127, velocity))
            duration = max(0.1, duration)  # 最小持续时间
            
            midi_file.addNote(track, channel, pitch, current_time, duration, velocity)
            current_time += duration
            note_count += 1
        
        # 保存文件（二进制模式）
        try:
            with open(file_path, "wb") as output_file:
                midi_file.writeFile(output_file)
            
            print(f"✓ Saved {note_count} notes to {file_path}")
            print(f"✓ File size: {os.path.getsize(file_path)} bytes")
            return file_path
        except Exception as e:
            print(f"✗ Error saving MIDI file: {e}")
            raise
    
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
    
    def generate_chord_from_column(self, column_pixels, octave_shift=0):
        """
        从一列像素生成和弦
        column_pixels: list of (r, g, b, a) 元组
        octave_shift: 音高偏移（半音）
        
        返回: list of (pitch, velocity, duration) 元组
        """
        chord_notes = []
        
        for r, g, b, a in column_pixels:
            # 使用HSV转换获取音符
            pitch, velocity, duration = self.rgba_to_note_hsv(r, g, b, a)
            
            # 应用音高偏移
            adjusted_pitch = max(0, min(127, pitch + octave_shift))
            
            chord_notes.append((adjusted_pitch, velocity, duration))
        
        return chord_notes
    
    def play_chord_direct(self, chord_notes, max_duration):
        """
        直接播放和弦（同时播放多个音符）
        chord_notes: list of (pitch, velocity, duration) 元组
        max_duration: 和弦的最大持续时间（秒）
        """
        if not self.audio_initialized:
            return
        
        sounds = []
        
        try:
            # 为和弦中的每个音符生成声音
            for pitch, velocity, duration in chord_notes:
                frequency = self.midi_note_to_frequency(pitch)
                volume = velocity / 127.0 * 0.2  # 降低音量避免和弦过响
                note_duration = min(duration / 4.0, max_duration)  # 使用较短的时长
                
                sound = self.generate_square_wave(frequency, note_duration, volume)
                sounds.append(sound)
            
            # 同时播放所有音符
            for sound in sounds:
                sound.play()
                
        except Exception as e:
            print(f"播放和弦失败: {e}")
    
    def generate_melody_from_columns(self, columns_data, octave_shift=0):
        """
        从列数据生成旋律
        columns_data: list of list of (r, g, b, a)
        每个子列表代表一列的所有像素
        
        返回: MIDI文件和音符信息
        """
        # 创建MIDI文件
        self.midi_file = MIDIFile(1)  # 1个轨道
        track = 0
        channel = 0
        time = 0
        self.midi_file.addTempo(track, time, self.tempo)
        
        self.notes = []
        current_time = 0
        
        # 遍历每一列（从左到右）
        for col_index, column_pixels in enumerate(columns_data):
            # 为这一列生成和弦
            chord_notes = self.generate_chord_from_column(column_pixels, octave_shift)
            
            # 计算和弦持续时间（使用列中所有音符的平均时长）
            avg_duration = sum(d for _, _, d in chord_notes) / len(chord_notes) if chord_notes else 0.5
            chord_duration = min(1.0, max(0.25, avg_duration))
            
            # 将和弦中的所有音符添加到MIDI文件（同一时间开始）
            for pitch, velocity, duration in chord_notes:
                self.midi_file.addNote(track, channel, pitch, current_time, chord_duration, velocity)
                
                # 记录音符信息
                self.notes.append({
                    'index': len(self.notes),
                    'column': col_index,
                    'pitch': pitch,
                    'velocity': velocity,
                    'duration': chord_duration,
                    'time': current_time,
                    'rgb': column_pixels[0][:3] if column_pixels else (0, 0, 0)  # 使用列的第一个像素颜色作为代表
                })
            
            # 移动到下一列的时间
            current_time += chord_duration
        
        # 生成信息文本
        melody_info = self.generate_chord_melody_info(columns_data)
        
        return self.notes, melody_info
    
    def generate_chord_melody_info(self, columns_data):
        """生成和弦旋律信息文本"""
        if not self.notes:
            return "No chord melody generated yet."
        
        num_columns = len(columns_data)
        num_notes = len(self.notes)
        
        info = f"Chord Melody Generated\n"
        info += f"{'=' * 50}\n"
        info += f"Total Columns: {num_columns}\n"
        info += f"Total Notes: {num_notes}\n"
        info += f"Average notes per column: {num_notes / num_columns:.1f}\n"
        info += f"Tempo: {self.tempo} BPM\n"
        
        if self.notes:
            total_duration = self.notes[-1]['time'] + self.notes[-1]['duration']
            info += f"Total Duration: {total_duration:.2f} beats\n"
            info += f"Estimated Time: {(total_duration / self.tempo * 60):.2f} seconds\n\n"
        
        info += "First 5 Chords:\n"
        info += f"{'-' * 50}\n"
        
        # 按列分组显示前5个和弦
        current_column = -1
        chord_count = 0
        
        for note in self.notes:
            if note['column'] != current_column:
                current_column = note['column']
                chord_count += 1
                if chord_count > 5:
                    break
                info += f"\nColumn {current_column + 1}:\n"
            
            pitch_name = self.midi_note_to_name(note['pitch'])
            info += f"  {pitch_name:<5} (vel: {note['velocity']:<3}, dur: {note['duration']:.2f})\n"
        
        info += f"\n... and {num_columns - 5} more columns\n" if num_columns > 5 else "\n"
        
        return info
