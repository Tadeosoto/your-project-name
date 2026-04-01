import math  # to generate sine waves
import os  # for audio fallback in WSL
import pygame  # pygame mixer for playback

# Added: tiny synthesized sounds so no external files are needed
_initialized = False  # ensure mixer is initialized once

def _ensure_init():  # initialize mixer, with fallback to dummy driver
    global _initialized
    if not _initialized:
        try:
            pygame.mixer.init()  # normal audio device
        except pygame.error:
            # Fallback for environments without audio (e.g., some WSL setups)
            os.environ.setdefault("SDL_AUDIODRIVER", "dummy")  # mute but avoid crash
            pygame.mixer.init()
        _initialized = True  # remember we are ready

def _tone(freq_hz: float, duration_s: float, volume: float = 0.2):  # synthesizes a sine tone
    _ensure_init()  # make sure mixer exists
    sample_rate = 44100  # CD-quality sample rate
    n_samples = int(duration_s * sample_rate)  # total frames to generate
    arr = bytearray()  # raw PCM data buffer
    for i in range(n_samples):
        # simple sine wave
        t = i / sample_rate  # current time in seconds
        sample = int(32767 * volume * math.sin(2 * math.pi * freq_hz * t))  # 16-bit amplitude
        # 16-bit little endian mono
        arr += int(sample & 0xFF).to_bytes(1, 'little', signed=False)  # low byte
        arr += int((sample >> 8) & 0xFF).to_bytes(1, 'little', signed=False)  # high byte
    snd = pygame.mixer.Sound(buffer=bytes(arr))  # create Sound from raw buffer
    return snd  # return reusable Sound

_shoot_sound = None  # cached Sound for shooting
_explosion_low = None  # cached low explosion layer
_explosion_high = None  # cached high explosion layer

def _load_sounds():  # lazily build and cache sounds
    global _shoot_sound, _explosion_low, _explosion_high
    if _shoot_sound is None:
        _shoot_sound = _tone(900, 0.05, 0.25)  # short high blip
    if _explosion_low is None or _explosion_high is None:
        # build two tones for a chunkier feel
        _explosion_low = _tone(120, 0.12, 0.3)  # boom layer
        _explosion_high = _tone(220, 0.10, 0.2)  # crack layer

def play_shoot():  # public API for shooting SFX
    _ensure_init()
    _load_sounds()
    _shoot_sound.play()  # play cached sound

def play_explosion():  # public API for explosion SFX
    _ensure_init()
    _load_sounds()
    # Play both layers together
    _explosion_low.play()  # start low boom
    _explosion_high.play()  # layer high crack

