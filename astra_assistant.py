import tkinter as tk
import subprocess
import threading
import math
import urllib.request
import xml.etree.ElementTree as ET

def get_news_text():
    # Jarvis greeting
    text = "Hey Gopika, This is Astra, your personal jarvis, here are today's tech and ai updates. "
    
    # Fetch RSS
    url = "https://techcrunch.com/category/artificial-intelligence/feed/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            count = 0
            for item in root.findall('./channel/item'):
                title = item.find('title').text
                # Clean up known special characters if any
                title = title.replace("&apos;", "'").replace("&amp;", "and")
                text += f"Update {count + 1}. {title}. "
                count += 1
                if count == 3: break
    except Exception as e:
        text += "Actually, I wasn't able to fetch the daily news from the server. "
    
    text += "That's everything for today. Have a productive day."
    return text

class JarvisUI(tk.Tk):
    def __init__(self, text_to_speak):
        super().__init__()
        self.text_to_speak = text_to_speak
        
        # Transparent borderless UI
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.config(bg='black')
        
        # Add translucency (works on mac)
        try:
            self.attributes('-alpha', 0.85)
        except:
            pass

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
        self.is_speaking = True
        self.animate()

        # Start speaking in background thread to avoid blocking main UI loop
        threading.Thread(target=self.speak_and_close, daemon=True).start()

    def animate(self):
        if not self.is_speaking:
            return
            
        self.canvas.delete("dynamic")
        cx, cy = 150, 150
        r_base = 100
        
        # Simple dynamic visual
        r = r_base + 10 * math.sin(self.angle)
        
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#00ffff", width=2, tags="dynamic")
        
        r2 = r_base - 20 + 5 * math.cos(self.angle * 1.5)
        self.canvas.create_oval(cx - r2, cy - r2, cx + r2, cy + r2, outline="#00bfff", width=1, dash=(4, 4), tags="dynamic")
        
        self.angle += 0.2
        self.after(50, self.animate)

    def speak_and_close(self):
        # Speak with Apple 'say' using polite Samantha voice and slower rate (150 words per min)
        try:
            subprocess.run(['say', '-v', 'Samantha', '-r', '150', self.text_to_speak])
        except Exception as e:
            print(f"Speaking failed: {e}")
        
        # Finished speaking
        self.is_speaking = False
        
        # Safely shut down Tkinter window from thread
        self.after(0, self.destroy)

if __name__ == "__main__":
    news = get_news_text()
    app = JarvisUI(news)
    app.mainloop()
