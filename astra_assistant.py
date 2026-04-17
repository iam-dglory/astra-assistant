import os
import tkinter as tk
import subprocess
import threading
import math
import urllib.request
import xml.etree.ElementTree as ET
import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from openai import OpenAI

# The OpenAI API key provided by the user
OPENAI_API_KEY = "sk-abcdef1234567890abcdef1234567890abcdef12"

class AstraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Transparent borderless UI
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.config(bg='black')
        try:
            self.attributes('-alpha', 0.85)
        except: pass

        width, height = 300, 300
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        self.label = tk.Label(self, text="A S T R A", fg="#00ffff", bg="black", font=("Arial", 16, "bold"))
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.angle = 0
        self.state = "SPEAKING" # SPEAKING(cyan), LISTENING(orange), THINKING(purple)
        self.is_running = True
        
        self.animate()
        
        threading.Thread(target=self.run_astra_workflow, daemon=True).start()

    def set_state(self, new_state, label_text=None):
        self.state = new_state
        if label_text:
            self.label.config(text=label_text)
            
        if self.state == "SPEAKING":
            self.label.config(fg="#00ffff")
        elif self.state == "LISTENING":
            self.label.config(fg="#ff8800")
        elif self.state == "THINKING":
            self.label.config(fg="#a020f0")

    def animate(self):
        if not self.is_running:
            return
            
        self.canvas.delete("dynamic")
        cx, cy = 150, 150
        r_base = 100
        
        if self.state == "SPEAKING":
            color1, color2 = "#00ffff", "#00bfff"
            r = r_base + 10 * math.sin(self.angle * 2)
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color1, width=2, tags="dynamic")
            r2 = r_base - 20 + 5 * math.cos(self.angle * 3)
            self.canvas.create_oval(cx - r2, cy - r2, cx + r2, cy + r2, outline=color2, width=1, dash=(4, 4), tags="dynamic")
            
        elif self.state == "LISTENING":
            color1, color2 = "#ff8800", "#ff4500"
            r = r_base + 15 + 5 * math.sin(self.angle * 4) # faster jitter indicates listening logic
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color1, width=3, tags="dynamic")
            for i in range(3):
                offset = i * (math.pi / 1.5)
                r_inner = r_base - 10 + 10 * math.sin(self.angle * 5 + offset)
                self.canvas.create_oval(cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner, outline=color2, width=1, tags="dynamic")
                
        elif self.state == "THINKING":
            color1, color2 = "#a020f0", "#9400d3"
            r = r_base + 5
            # Draw rotating arcs to symbolize processing
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=math.degrees(self.angle*2), extent=120, outline=color1, width=3, style=tk.ARC, tags="dynamic")
            self.canvas.create_arc(cx - r+15, cy - r+15, cx + r-15, cy + r-15, start=math.degrees(-self.angle*3), extent=90, outline=color2, width=2, style=tk.ARC, tags="dynamic")
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill=color1, outline="", tags="dynamic") # core
            
        self.angle += 0.1
        self.after(50, self.animate)

    def speak(self, text):
        try:
            subprocess.run(['say', '-v', 'Samantha', '-r', '150', text])
        except: pass

    def fetch_news(self):
        text = "Here are today's tech and AI updates. "
        url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                count = 0
                for item in root.findall('./channel/item'):
                    title = item.find('title').text.replace("&apos;", "'").replace("&amp;", "and")
                    text += f"Update {count + 1}. {title}. "
                    count += 1
                    if count == 3: break
        except Exception:
            text += "I wasn't able to fetch the daily news right now. "
        return text

    def run_astra_workflow(self):
        # 1. Greeting & News
        self.set_state("SPEAKING", "A S T R A")
        intro = "Hey Gopika, This is Astra, your personal jarvis. "
        news = self.fetch_news()
        self.speak(intro + news)
        
        # 2. Ask about day
        self.speak("That's the news. Now, tell me, how was your day?")
        
        # 3. Listen
        self.set_state("LISTENING", "L I S T E N I N G")
        fs = 44100
        seconds = 5 # Listen for 5 seconds
        try:
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait() # Blocking record
            wav.write('temp.wav', fs, recording)
            
            recognizer = sr.Recognizer()
            with sr.AudioFile('temp.wav') as source:
                audio_data = recognizer.record(source)
                user_text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            user_text = None
        except Exception as e:
            user_text = None
            
        # Cleanup temp audio
        try: os.remove('temp.wav')
        except: pass
        
        # 4. Thinking & processing
        self.set_state("THINKING", "T H I N K I N G")
        time.sleep(1) # Visual padding
        
        if not user_text:
            reply = "I didn't quite catch that. But I hope the rest of your day goes wonderfully."
        else:
            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Astra, a helpful, polite, and brief Jarvis-like AI voice assistant. Respond in 1 to 2 short sentences max."},
                        {"role": "user", "content": f"How was your day? I replied: {user_text}"}
                    ],
                    max_tokens=60
                )
                reply = response.choices[0].message.content
            except Exception as e:
                # Catch invalid API key cleanly
                reply = f"I heard you say: {user_text}. However, my neural connection failed due to an invalid API key, so I can't generate a deep response. But it's great to hear from you."
        
        # 5. Reply
        self.set_state("SPEAKING", "A S T R A")
        self.speak(reply)
        
        # 6. Close cleanly
        self.is_running = False
        self.after(0, self.destroy)

if __name__ == "__main__":
    app = AstraApp()
    app.mainloop()
