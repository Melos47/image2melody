"""
Melody Generator Module
将RGB值转换为8-bit风格的音乐旋律
"""
from midiutil import MIDIFile
import pygame
import numpy as np
import tempfile
import os


class MelodyGenerator:
    def __init__(self):
        self.midi_file = None
        self.notes = []
        self.tempo = 120  # BPM
        self.temp_midi_path = None
        
        # 初始化pygame mixer用于播放
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # 音阶定义 (C大调的音符)
        self.scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C, D, E, F, G, A, B, C (MIDI note numbers)
        
    def rgb_to_note(self, r, g, b):
        """
        将RGB值转换为音符参数
        R: 决定音高 (0-255 -> 音阶中的音符)
        G: 决定时长 (0-255 -> 0.25-2.0 拍)
        B: 决定力度 (0-255 -> 60-127 velocity)
        """
        # 音高: 映射R值到音阶
        pitch_index = int((r / 255.0) * (len(self.scale_notes) - 1))
        pitch = self.scale_notes[pitch_index]
        
        # 可选：添加八度变化以增加音域
        octave_shift = (r % 32) // 16  # 0, 1, 或 2 个八度
        pitch += octave_shift * 12
        
        # 时长: 映射G值到节拍长度
        duration = 0.25 + (g / 255.0) * 1.75  # 0.25到2.0拍
        
        # 力度: 映射B值到MIDI velocity
        velocity = 60 + int((b / 255.0) * 67)  # 60到127
        
        return pitch, duration, velocity
    
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
    
    def __del__(self):
        """清理资源"""
        if self.temp_midi_path and os.path.exists(self.temp_midi_path):
            try:
                os.remove(self.temp_midi_path)
            except:
                pass
