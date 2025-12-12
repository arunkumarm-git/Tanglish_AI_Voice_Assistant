# main.py
# --- MODIFIED to be a 'logic' module for the GUI ---

import librosa
import command_and_response_giver
import numpy as np
from transformers import pipeline
from command_response_fetcher import parse_commands
from open_or_close_decision_maker import open_or_close
import tts_player # This is no longer used here, but in the GUI
import os
from dotenv import load_dotenv

# --- LOAD .ENV ---
# This is now handled by main_gui.py, but good to keep
load_dotenv()
# -----------------

# --- Models Loaded Once ---
print("Loading speech recognition model from local relative path...")
speech_to_text_pipe = pipeline(
    "automatic-speech-recognition",
    model=r"whisper_medium/model",
    tokenizer=r"whisper_medium/tokenizer",
    feature_extractor=r"whisper_medium/feature_extractor",
    generate_kwargs={"language": "en"}
)
print("Model loaded. Ready for your command!")


def load_audio_with_librosa(audio_path, target_sr=16000):
    try:
        audio, _ = librosa.load(audio_path, sr=target_sr)
        return audio
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None


def process_command(audio_path="recorded_audio.wav"):
    """
    Processes audio, determines command, and returns text.
    MODIFIED: Returns (final_response, user_transcription)
    """
    audio_array = load_audio_with_librosa(audio_path)
    if audio_array is None:
        return "Could not process the audio file.", "Error processing audio."

    print("\nTranscribing audio...")
    unstr_english_command = speech_to_text_pipe(audio_array.copy())['text']
    print(f"Heard: '{unstr_english_command}'")
    
    if not unstr_english_command or not unstr_english_command.strip():
        print("Empty transcription. Nothing to process.")
        final_response = command_and_response_giver.responser("Sorry, I didn't hear anything.")
        return final_response, "(Silence)"

    print("Getting structured command from LLM...")
    command_response_text = command_and_response_giver.get_command(unstr_english_command)
    print(f"LLM Output:\n{command_response_text}")
    
    tasks = parse_commands(command_response_text)
    
    if not tasks:
        print("Could not parse any valid commands from LLM response.")
        final_response = command_and_response_giver.responser("Sorry, I had trouble understanding that.")
        return final_response, unstr_english_command

    first_command = tasks[0].get("command")
    
    if first_command == "no_action":
        print("Detected conversational turn.")
        conversational_text = tasks[0].get("response", "I'm not sure how to respond.")
        print("Generating conversational response...")
        final_response = command_and_response_giver.responser(conversational_text)
        
        # RETURN both strings
        return final_response, unstr_english_command
    else:
        print("Detected action command(s). Executing sequence.")
        all_initial_responses = []
        final_execution_result = ""

        for task in tasks:
            command = task.get("command")
            args = task.get("args", [])
            response = task.get("response", "Working on it...")

            if command is None or command == "no_action":
                continue

            print(f"Executing Task: {command}, Arguments: {args}")
            all_initial_responses.append(response)
            execution_result = open_or_close(command, args)
            
            if execution_result:
                final_execution_result = str(execution_result)
            
            print(f"Task result: {execution_result}")

        combined_initial_response = " ".join(all_initial_responses)
        full_response = f"{combined_initial_response} {final_execution_result}".strip()
        
        print("Generating final Tanglish response...")
        final_response = command_and_response_giver.responser(full_response)
        
        # RETURN both strings
        return final_response, unstr_english_command


# The __main__ block is removed, as main_gui.py is the new entry point.
# if __name__ == "__main__":
#     ...