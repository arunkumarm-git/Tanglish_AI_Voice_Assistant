# audio_recorder.py
# --- MODIFIED to be GUI-friendly ---

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import threading
import sys

SAMPLE_RATE = 16000
FILENAME = "recorded_audio.wav"
SILENCE_THRESHOLD = 0.005
MAX_SILENCE_DURATION = 1.0
CALIBRATION_TIME = 0.5
CHUNK_SIZE = 512

def record_with_immediate_stop():
    print("🎤 Quick calibration (0.5s)... Stay quiet!")
    
    recording = []
    noise_samples = []
    recording_started = False
    calibration_done = False
    silence_start = None
    background_noise_level = 0
    start_time = time.time()
    processing_complete = threading.Event()
    
    def save_and_exit_thread():
        """Save file in background thread"""
        # This function NO LONGER EXITS THE PROGRAM.
        # It just saves the file and sets an event.
        try:
            if recording:
                print(f"🔄 Saving {len(recording)} chunks...")
                audio_data = np.concatenate(recording, axis=0)
                audio_data_int16 = np.clip(audio_data * 32767, -32767, 32767).astype(np.int16)
                write(FILENAME, SAMPLE_RATE, audio_data_int16)
                duration = len(audio_data) / SAMPLE_RATE
                print(f"✅ Saved {FILENAME} ({duration:.2f}s)")
            else:
                print("❌ No audio recorded")
        except Exception as e:
            print(f"❌ Save error: {e}")
        finally:
            processing_complete.set()
            # CRITICAL: os._exit(0) has been REMOVED.

    def callback(indata, frames, time_info, status):
        nonlocal recording_started, calibration_done, silence_start, background_noise_level
        
        volume_norm = np.sqrt(np.mean(np.square(indata)))
        current_time = time.time()
        
        if not calibration_done:
            noise_samples.append(volume_norm)
            if current_time - start_time > CALIBRATION_TIME:
                background_noise_level = np.mean(noise_samples) * 2.0
                calibration_done = True
                print(f"📊 Noise level: {background_noise_level:.6f}")
                print("🎤 Speak now...")
            return
        
        current_threshold = max(SILENCE_THRESHOLD, background_noise_level)
        
        if volume_norm > current_threshold:
            if not recording_started:
                recording_started = True
                print("🔴 Recording...")
            silence_start = None
            recording.append(indata.copy())
        elif recording_started:
            if silence_start is None:
                silence_start = current_time
                print("⏸️  Silence...")
            elif current_time - silence_start > MAX_SILENCE_DURATION:
                print("⏹️  Stopping...")
                save_thread = threading.Thread(target=save_and_exit_thread, daemon=False)
                save_thread.start()
                raise sd.CallbackStop()

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE, 
            channels=1, 
            callback=callback, 
            dtype='float32',
            blocksize=CHUNK_SIZE
        ):
            sd.sleep(30000)
            
    except sd.CallbackStop:
        print("CallbackStop received. Waiting for save...")
        processing_complete.wait(timeout=2.0)
        # CRITICAL: sys.exit(0) has been REMOVED.
        print("Recording function finished.")
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
        save_thread = threading.Thread(target=save_and_exit_thread, daemon=False)
        save_thread.start()
        processing_complete.wait(timeout=2.0)
        # CRITICAL: sys.exit(0) has been REMOVED.
        print("Recording function finished (KeyboardInterrupt).")

if __name__ == "__main__":
    # This file should no longer be run directly.
    # Run main_gui.py instead.
    print("This file is a module. Run main_gui.py to start the assistant.")
    try:
        record_with_immediate_stop()
    except Exception as e:
        print(f"❌ Error: {e}")