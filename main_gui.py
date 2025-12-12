import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QTextEdit, QLabel, QFrame, QComboBox, QGroupBox
)
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool, Slot, Qt
from PySide6.QtGui import QIcon, QFont

import audio_recorder
import main as processing_logic
import tts_player
import os

# --- Worker Signals ---
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    status_update = Signal(str)
    conversation_update = Signal(str, str)

# --- 1. Audio Recorder Worker ---
class AudioWorker(QRunnable):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals

    @Slot()
    def run(self):
        try:
            self.signals.status_update.emit("🎤 Listening... (Speak now)")
            audio_recorder.record_with_immediate_stop()
            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit((e, "Audio recording failed"))

# --- 2. Command Processor Worker ---
class CommandWorker(QRunnable):
    def __init__(self, audio_path, signals, voice_config):
        super().__init__()
        self.signals = signals
        self.audio_path = audio_path
        self.voice_config = voice_config

    @Slot()
    def run(self):
        try:
            if not os.path.exists(self.audio_path):
                self.signals.status_update.emit(f"❌ Error: {self.audio_path} not found.")
                return

            self.signals.status_update.emit("🧠 Thinking... (Transcribing & processing)")
            
            final_response, user_transcription = processing_logic.process_command(self.audio_path)
            
            if not user_transcription.strip():
                user_transcription = "(No speech detected)"
                
            self.signals.conversation_update.emit(user_transcription, final_response)
            self.signals.status_update.emit("🗣️ Speaking...")
            
            # Use selected voice configuration
            tts_player.speak(final_response, **self.voice_config)
            
            self.signals.finished.emit()

        except Exception as e:
            self.signals.error.emit((e, "Command processing failed"))
            print(f"Error in CommandWorker: {e}")

# --- 3. Main GUI Window ---
class AssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(r"media\logo.png"))
        self.setWindowTitle("JARVIS - AI Voice Assistant")
        self.setGeometry(100, 100, 900, 700)
        
        self.thread_pool = QThreadPool()
        print(f"Multithreading with max {self.thread_pool.maxThreadCount()} threads.")
        
        # Default voice configuration
        self.voice_config = {"lang": "en-IN", "gender": "FEMALE"}
        
        self.init_ui()
        self.apply_stylesheet()
        self.greet_user()

    def init_ui(self):
        # --- Main Container ---
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Header Section ---
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout()
        
        title_label = QLabel("JARVIS")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("AI Voice Assistant • Tanglish Enabled")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_frame.setLayout(header_layout)
        
        # --- Status Display ---
        self.status_label = QLabel("🟢 System Online - Ready for commands")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        # --- Voice Settings Panel ---
        voice_group = QGroupBox("Voice Settings")
        voice_group.setObjectName("voiceGroup")
        voice_layout = QHBoxLayout()
        
        # Language Selection
        lang_label = QLabel("Language:")
        lang_label.setObjectName("settingLabel")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English (India)", "Tamil (India)"])
        self.lang_combo.setObjectName("comboBox")
        self.lang_combo.currentTextChanged.connect(self.update_voice_config)
        
        # Gender Selection
        gender_label = QLabel("Voice:")
        gender_label.setObjectName("settingLabel")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Female", "Male"])
        self.gender_combo.setObjectName("comboBox")
        self.gender_combo.currentTextChanged.connect(self.update_voice_config)
        
        # Voice Info Label
        self.voice_info_label = QLabel("🎵 en-IN-NeerjaNeural (Expressive)")
        self.voice_info_label.setObjectName("voiceInfoLabel")
        
        voice_layout.addWidget(lang_label)
        voice_layout.addWidget(self.lang_combo)
        voice_layout.addWidget(gender_label)
        voice_layout.addWidget(self.gender_combo)
        voice_layout.addStretch()
        voice_layout.addWidget(self.voice_info_label)
        voice_group.setLayout(voice_layout)
        
        # --- Listen Button ---
        self.listen_button = QPushButton("🎤 LISTEN")
        self.listen_button.setObjectName("listenButton")
        self.listen_button.setCursor(Qt.PointingHandCursor)
        self.listen_button.clicked.connect(self.start_listening)
        
        # --- Conversation Log ---
        conv_label = QLabel("Conversation History")
        conv_label.setObjectName("sectionLabel")
        
        self.conversation_log = QTextEdit()
        self.conversation_log.setReadOnly(True)
        self.conversation_log.setObjectName("conversationLog")
        
        # --- Assembly ---
        main_layout.addWidget(header_frame)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(voice_group)
        main_layout.addWidget(self.listen_button)
        main_layout.addWidget(conv_label)
        main_layout.addWidget(self.conversation_log, stretch=1)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0c29, stop:0.5 #302b63, stop:1 #24243e);
            }
            
            #headerFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            #titleLabel {
                font-size: 48px;
                font-weight: bold;
                color: #00d4ff;
                font-family: 'Consolas', 'Courier New', monospace;
                letter-spacing: 8px;
                text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            }
            
            #subtitleLabel {
                font-size: 16px;
                color: #a8dadc;
                margin-top: 5px;
                font-style: italic;
            }
            
            #statusLabel {
                font-size: 16px;
                padding: 15px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                color: #4ecca3;
                border: 1px solid rgba(78, 204, 163, 0.3);
                font-weight: bold;
            }
            
            #voiceGroup {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 10px;
                font-size: 14px;
                color: #ffffff;
            }
            
            #voiceGroup::title {
                color: #00d4ff;
                font-weight: bold;
                font-size: 14px;
            }
            
            #settingLabel {
                color: #ffffff;
                font-size: 13px;
                font-weight: bold;
                padding-right: 5px;
            }
            
            #comboBox {
                background: rgba(0, 0, 0, 0.4);
                border: 1px solid rgba(0, 212, 255, 0.3);
                border-radius: 5px;
                padding: 8px;
                color: #ffffff;
                font-size: 13px;
                min-width: 150px;
            }
            
            #comboBox:hover {
                border: 1px solid #00d4ff;
                background: rgba(0, 0, 0, 0.5);
            }
            
            #comboBox::drop-down {
                border: none;
                background: rgba(0, 212, 255, 0.2);
                border-radius: 3px;
            }
            
            #comboBox QAbstractItemView {
                background: #1a1a2e;
                color: #ffffff;
                selection-background-color: #00d4ff;
                border: 1px solid #00d4ff;
            }
            
            #voiceInfoLabel {
                color: #ffd700;
                font-size: 12px;
                font-style: italic;
                padding: 5px 10px;
                background: rgba(255, 215, 0, 0.1);
                border-radius: 5px;
            }
            
            #listenButton {
                font-size: 22px;
                font-weight: bold;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099cc);
                color: white;
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.2);
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            #listenButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00e5ff, stop:1 #00aadd);
                border: 2px solid rgba(255, 255, 255, 0.4);
                transform: scale(1.02);
            }
            
            #listenButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0099cc, stop:1 #007799);
            }
            
            #listenButton:disabled {
                background: rgba(100, 100, 100, 0.3);
                color: rgba(255, 255, 255, 0.3);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            #sectionLabel {
                font-size: 14px;
                font-weight: bold;
                color: #00d4ff;
                padding: 5px;
            }
            
            #conversationLog {
                background: rgba(0, 0, 0, 0.4);
                border: 1px solid rgba(0, 212, 255, 0.3);
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                line-height: 1.6;
                color: #ffffff;
            }
            
            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.2);
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(0, 212, 255, 0.5);
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 212, 255, 0.7);
            }
        """)

    def update_voice_config(self):
        """Update voice configuration based on user selection"""
        lang_map = {
            "English (India)": "en-IN",
            "Tamil (India)": "ta-IN"
        }
        
        gender_map = {
            "Female": "FEMALE",
            "Male": "MALE"
        }
        
        lang = lang_map[self.lang_combo.currentText()]
        gender = gender_map[self.gender_combo.currentText()]
        
        self.voice_config = {"lang": lang, "gender": gender}
        
        # Update voice info display
        voice_names = {
            ("en-IN", "FEMALE"): "🎵 en-IN-NeerjaNeural (Expressive)",
            ("en-IN", "MALE"): "🎵 en-IN-PrabhatNeural",
            ("ta-IN", "FEMALE"): "🎵 ta-IN-PallaviNeural",
            ("ta-IN", "MALE"): "🎵 ta-IN-ValluvarNeural"
        }
        
        self.voice_info_label.setText(voice_names.get((lang, gender), "🎵 Voice Selected"))

    def greet_user(self):
        greeting = "Vanakkam sir, system online. Ready for your command."
        self.update_conversation_log("", greeting)
        
        # Play greeting with default voice
        def greet():
            tts_player.speak(greeting, **self.voice_config)
        
        greeting_worker = QRunnable.create(greet)
        self.thread_pool.start(greeting_worker)

    def start_listening(self):
        self.listen_button.setEnabled(False)
        self.listen_button.setText("⏺️ LISTENING...")
        
        audio_signals = WorkerSignals()
        audio_signals.status_update.connect(self.update_status)
        audio_signals.finished.connect(self.start_processing)
        audio_signals.error.connect(self.on_error)
        
        audio_worker = AudioWorker(audio_signals)
        self.thread_pool.start(audio_worker)

    def start_processing(self):
        self.listen_button.setText("🧠 PROCESSING...")
        self.update_status("🧠 Processing audio...")

        command_signals = WorkerSignals()
        command_signals.status_update.connect(self.update_status)
        command_signals.conversation_update.connect(self.update_conversation_log)
        command_signals.finished.connect(self.reset_button)
        command_signals.error.connect(self.on_error)
        
        command_worker = CommandWorker("recorded_audio.wav", command_signals, self.voice_config)
        self.thread_pool.start(command_worker)

    def update_status(self, message):
        status_colors = {
            "🟢": "#4ecca3",
            "🎤": "#00d4ff",
            "🧠": "#a78bfa",
            "🗣️": "#fbbf24",
            "❌": "#ef4444"
        }
        
        color = "#4ecca3"
        for emoji, emoji_color in status_colors.items():
            if emoji in message:
                color = emoji_color
                break
        
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"""
            font-size: 16px;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            color: {color};
            border: 1px solid {color}55;
            font-weight: bold;
        """)

    def update_conversation_log(self, user_text, ai_text):
        if user_text:
            self.conversation_log.append(
                f"<div style='margin: 10px 0;'>"
                f"<span style='color: #00d4ff; font-weight: bold;'>👤 You:</span> "
                f"<span style='color: #e0e0e0;'>{user_text}</span>"
                f"</div>"
            )
        if ai_text:
            self.conversation_log.append(
                f"<div style='margin: 10px 0;'>"
                f"<span style='color: #4ecca3; font-weight: bold;'>🤖 JARVIS:</span> "
                f"<span style='color: #c8e6c9;'>{ai_text}</span>"
                f"</div>"
            )
        
        scrollbar = self.conversation_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def reset_button(self):
        self.listen_button.setEnabled(True)
        self.listen_button.setText("🎤 LISTEN")
        self.update_status("🟢 System Online - Ready for commands")
        
    def on_error(self, error_tuple):
        e, message = error_tuple
        print(f"ERROR: {message}\n{e}")
        self.update_status(f"❌ Error: {message}")
        self.update_conversation_log("", f"Sorry sir, an error occurred: {message}")
        self.reset_button()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.path.exists(r"whisper_medium/model"):
        print("CRITICAL: Whisper model not found at 'whisper_medium/model'.")
        print("Please ensure the model, tokenizer, and feature_extractor are in this folder.")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AssistantWindow()
    window.show()
    sys.exit(app.exec())