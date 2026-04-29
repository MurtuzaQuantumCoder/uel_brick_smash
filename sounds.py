# Sound generation using Pygame's sndarray
# Generates chiptune-like sound effects programmatically

import pygame
import numpy as np
import math

class SoundGenerator:
    """Generates chiptune sound effects using sine waves and numpy."""

    def __init__(self):
        self.sounds = {}
        self.sample_rate = 22050  # Low sample rate for retro feel
        self._generate_all_sounds()

    def _generate_tone(self, frequency, duration, volume=0.5, fade_out=True):
        """Generate a simple sine wave tone."""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        wave = np.sin(2 * math.pi * frequency * t)

        if fade_out and samples > 100:
            fade_samples = min(int(samples * 0.3), samples // 4)
            fade = np.linspace(1, 0, fade_samples)
            wave[-fade_samples:] *= fade

        wave *= volume
        wave = np.int16(wave * 32767)
        wave = wave.reshape(-1, 1)
        sound = pygame.sndarray.make_sound(wave)
        return sound

    def _generate_noise(self, duration, volume=0.3):
        """Generate white noise for explosion/break effects."""
        samples = int(duration * self.sample_rate)
        noise = np.random.uniform(-1, 1, samples)
        wave = np.int16(noise * volume * 32767)
        wave = wave.reshape(-1, 1)
        sound = pygame.sndarray.make_sound(wave)
        return sound

    def _generate_arpeggio(self, freqs, duration, volume=0.5):
        """Generate an arpeggio (rapid note sequence)."""
        sound = pygame.mixer.Sound(buffer=np.zeros((0, 2), dtype=np.int16))
        note_duration = duration / len(freqs)
        for freq in freqs:
            note = self._generate_tone(freq, note_duration, volume, fade_out=False)
            sound = pygame.sndarray.use_arraytype('numpy')
            pygame.mixer.Sound.play(sound)
        return sound

    def _generate_all_sounds(self):
        """Generate all game sound effects."""
        # Wall bounce - high short beep
        self.sounds['wall'] = self._generate_tone(440, 0.1, 0.4)

        # Paddle hit - medium tone
        self.sounds['paddle'] = self._generate_tone(330, 0.15, 0.5)

        # Brick break - descending tones
        self.sounds['brick'] = self._generate_noise(0.2, 0.4)

        # Power-up collected - ascending happy tone
        self.sounds['powerup'] = self._generate_tone(660, 0.3, 0.6)

        # Life lost - descending sad tone
        self.sounds['life_lost'] = self._generate_tone(220, 0.5, 0.6)

        # Victory - triumphant arpeggio-like
        self.sounds['victory'] = self._generate_tone(880, 0.8, 0.7)

        # Game over - low ominous tone
        self.sounds['game_over'] = self._generate_tone(150, 1.0, 0.7)

        # Countdown beep
        self.sounds['beep'] = self._generate_tone(523, 0.2, 0.5)  # C5

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
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
    sound_manager = SoundGenerator()
    return sound_manager
