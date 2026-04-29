# Sound generation using Pygame's sndarray
# Generates chiptune-like sound effects programmatically

import pygame
import numpy as np
import math

class SoundGenerator:
    """Generates chiptune sound effects using sine waves and numpy."""

    def __init__(self):
        self.sounds = {}
        self.sample_rate = 22050
        self._generate_all_sounds()

    def _generate_tone(self, frequency, duration, volume=0.5, fade_out=True):
        """Generate a simple sine wave tone."""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        wave = np.sin(2 * np.pi * frequency * t)

        if fade_out and samples > 100:
            fade_samples = min(int(samples * 0.3), samples // 4)
            fade = np.linspace(1, 0, fade_samples)
            wave[-fade_samples:] *= fade

        wave *= volume
        wave = np.int16(wave * 32767)
        wave = np.column_stack([wave, wave])
        sound = pygame.sndarray.make_sound(wave)
        return sound

    def _generate_soft_chime(self, base_freq, duration, volume=0.5):
        """Generate a sweet, soft bell-like chime with harmonics."""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        
        # Create a pleasant chime with harmonics
        wave = np.sin(2 * np.pi * base_freq * t) * 0.4
        wave += np.sin(2 * np.pi * base_freq * 2 * t) * 0.2
        wave += np.sin(2 * np.pi * base_freq * 3 * t) * 0.1
        wave += np.sin(2 * np.pi * base_freq * 5 * t) * 0.05
        
        # Gentle envelope
        envelope = np.exp(-t * 2) * (1 - np.exp(-t * 10))
        wave *= envelope
        
        wave *= volume
        wave = np.int16(wave * 32767)
        wave = np.column_stack([wave, wave])
        sound = pygame.sndarray.make_sound(wave)
        return sound

    def _generate_break_sound(self, volume=0.4):
        """Generate a sweet, soft sound for brick breaking."""
        samples = int(0.3 * self.sample_rate)
        t = np.linspace(0, 0.3, samples, False)
        
        # Ascending gentle arpeggio
        wave = np.zeros(samples)
        for i, freq in enumerate([523, 659, 784, 1047]):  # C5, E5, G5, C6
            freq_wave = np.sin(2 * np.pi * freq * t)
            # Stagger the start times
            freq_samples = samples // 4
            start_idx = i * freq_samples
            end_idx = start_idx + freq_samples
            wave[start_idx:end_idx] += freq_wave[start_idx:end_idx] * 0.25
        
        # Apply gentle envelope
        envelope = np.exp(-t * 4)
        wave *= envelope
        
        wave *= volume
        wave = np.int16(wave * 32767)
        wave = np.column_stack([wave, wave])
        sound = pygame.sndarray.make_sound(wave)
        return sound

    def _generate_victory_melody(self):
        """Generate a mesmerizing, triumphant victory melody."""
        duration = 2.5
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        wave = np.zeros(samples)
        
        # Beautiful arpeggio sequence (C major)
        notes = [
            (523, 0.15),    # C5
            (659, 0.15),    # E5
            (784, 0.15),    # G5
            (1047, 0.3),    # C6
            (784, 0.15),    # G5
            (1047, 0.15),   # C6
            (1319, 0.4),    # E6
        ]
        
        current_time = 0
        for freq, note_dur in notes:
            note_samples = int(note_dur * self.sample_rate)
            start_idx = int(current_time * self.sample_rate)
            end_idx = min(start_idx + note_samples, samples)
            
            available_samples = end_idx - start_idx
            if available_samples <= 0:
                current_time += note_dur
                continue
                
            note_t = np.linspace(0, note_dur, note_samples)
            note_wave = np.sin(2 * np.pi * freq * note_t)
            note_wave *= np.exp(-note_t * 3)  # Decay envelope
            
            wave[start_idx:end_idx] += note_wave[:available_samples]
            current_time += note_dur
        
        # Normalize and apply gentle fade out
        wave *= 0.3
        fade_samples = int(0.5 * self.sample_rate)
        fade = np.ones(samples)
        fade[-fade_samples:] = np.linspace(1, 0, fade_samples)
        wave *= fade
        
        wave = np.int16(wave * 32767)
        wave = np.column_stack([wave, wave])
        sound = pygame.sndarray.make_sound(wave)
        return sound

    def _generate_game_over_melody(self):
        """Generate a gentle, dreamy game over melody."""
        duration = 2.0
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        wave = np.zeros(samples)
        
        # Gentle descending minor melody
        notes = [
            (659, 0.4),     # E5
            (587, 0.3),     # D5
            (523, 0.4),     # C5
            (392, 0.5),     # G4
            (349, 0.5),     # F4
            (294, 0.8),     # D4
        ]
        
        current_time = 0
        for freq, note_dur in notes:
            note_samples = int(note_dur * self.sample_rate)
            start_idx = int(current_time * self.sample_rate)
            end_idx = min(start_idx + note_samples, samples)
            
            available_samples = end_idx - start_idx
            if available_samples <= 0:
                current_time += note_dur
                continue
                
            note_t = np.linspace(0, note_dur, note_samples)
            # Add slight vibrato for dreamy effect
            vibrato = np.sin(2 * np.pi * 5 * note_t) * 2
            note_wave = np.sin(2 * np.pi * (freq + vibrato) * note_t)
            note_wave *= np.exp(-note_t * 2)  # Gentle decay
            
            wave[start_idx:end_idx] += note_wave[:available_samples] * 0.3
            current_time += note_dur
        
        # Apply fade out
        fade_samples = int(0.5 * self.sample_rate)
        fade = np.ones(samples)
        fade[-fade_samples:] = np.linspace(1, 0, fade_samples)
        wave *= fade
        
        wave = np.int16(wave * 32767)
        wave = np.column_stack([wave, wave])
        sound = pygame.sndarray.make_sound(wave)
        return sound

    def _generate_all_sounds(self):
        """Generate all game sound effects."""
        # Wall bounce - high short beep
        self.sounds['wall'] = self._generate_tone(440, 0.1, 0.4)

        # Paddle hit - medium tone
        self.sounds['paddle'] = self._generate_tone(330, 0.15, 0.5)

        # Brick break - sweet chime (soft and pleasant)
        self.sounds['brick'] = self._generate_break_sound(0.4)

        # Power-up collected - ascending happy tone
        self.sounds['powerup'] = self._generate_tone(660, 0.3, 0.6)

        # Life lost - descending sad tone
        self.sounds['life_lost'] = self._generate_tone(220, 0.5, 0.6)

        # Victory - mesmerizing triumphant melody
        self.sounds['victory'] = self._generate_victory_melody()

        # Game over - gentle, dreamy melody
        self.sounds['game_over'] = self._generate_game_over_melody()

        # Countdown beep
        self.sounds['beep'] = self._generate_tone(523, 0.2, 0.5)

        # Menu navigation
        self.sounds['select'] = self._generate_tone(440, 0.1, 0.4)
        self.sounds['confirm'] = self._generate_tone(660, 0.2, 0.5)

    def play(self, sound_name):
        """Play a sound by name."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def set_volume(self, volume):
        """Set global sound volume (0.0 to 1.0)."""
        for sound in self.sounds.values():
            sound.set_volume(volume)

# Global sound manager instance
sound_manager = None

def init_sounds():
    """Initialize the sound system."""
    global sound_manager
    pygame.mixer.init(frequency=22050, size=-16, channels=2)
    sound_manager = SoundGenerator()
    return sound_manager