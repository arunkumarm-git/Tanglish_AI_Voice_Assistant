# tts_player.py
# --- MODIFIED to support dynamic Tanglish voice selection ---

import asyncio
import edge_tts
import os
import pygame
import tempfile

# --- Configuration for Edge TTS ---
# These are no longer hardcoded globals.
# VOICE = "en-IN-NeerjaNeural"
# STYLE = "expressive"

async def _generate_speech(text: str, output_file: str, voice: str, style: str):
    """
    Internal async function to generate and save the speech MP3.
    """
    print(f"TTS: Synthesizing '{text}' with voice {voice} ({style})...")
    try:
        communicate = edge_tts.Communicate(text, voice, rate="+0%", pitch="+0Hz")
        await communicate.save(output_file)
    except Exception as e:
        print(f"TTS Warning: Error during synthesis: {e}")
        # Fallback without style if needed
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

def speak(text: str, **kwargs):
    """
    Synthesizes speech using edge-tts and plays it with pygame.
    
    Args:
        text: The text to speak
        **kwargs: Now supports lang="ta-IN" and gender="MALE"
    """
    if not text or not text.strip():
        print("TTS Warning: Received empty text. Nothing to speak.")
        return
    
    # --- Dynamic Voice Selection ---
    lang = kwargs.get("lang", "en-IN")
    gender = kwargs.get("gender", "FEMALE").upper()
    
    # Voice map for your project
    VOICE_MAP = {
        ("ta-IN", "MALE"): "ta-IN-ValluvarNeural",
        ("ta-IN", "FEMALE"): "ta-IN-PallaviNeural",
        ("en-IN", "FEMALE"): "en-IN-NeerjaNeural",
        ("en-IN", "MALE"): "en-IN-PrabhatNeural",
    }
    
    # Default to Neerja if no match
    VOICE = VOICE_MAP.get((lang, gender), "en-IN-NeerjaNeural")
    STYLE = "expressive" if "en-" in lang else "default"
    # -------------------------------
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_path = temp_file.name
    temp_file.close()
    
    try:
        # 1. Generate the speech file with the correct voice
        asyncio.run(_generate_speech(text, temp_path, VOICE, STYLE))
        
        if not os.path.exists(temp_path):
            print("TTS Error: File generation failed.")
            return
        
        # 2. Initialize pygame mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # 3. Load and play the audio
        print(f"TTS: Playing audio with {VOICE}...")
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        # 4. Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        print("TTS: Playback complete.")
        
    except Exception as e:
        print(f"CRITICAL TTS ERROR: {e}")
        print("Make sure pygame is installed: pip install pygame")
    
    finally:
        # 5. Clean up
        pygame.mixer.music.unload() if pygame.mixer.get_init() else None
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

if __name__ == "__main__":
    # --- Test commands ---
    print("Testing Edge TTS with ta-IN-ValluvarNeural (Tanglish Male)...")
    speak("Vanakkam sir, system online. Ready for your command.", lang="ta-IN", gender="MALE")
    
    print("\nTesting Creator Info...")
    speak("Enna create pannadhu Arun Kumar M.", lang="ta-IN", gender="MALE")
    
    print("\nTesting English (Female)...")
    speak("Hello! I am your voice assistant.", lang="en-IN", gender="FEMALE")