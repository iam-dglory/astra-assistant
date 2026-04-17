# Astra Personal Jarvis

A conversational, dark-themed AI voice assistant tailored for macOS that not only gives you a brief rundown of the latest AI news every day at 11:00 AM, but also interactively asks you how your day was and speaks back!

## Features
- **Conversational Jarvis Brain:** Powered by OpenAI GPT-3.5 and Google Free STT, she listens to you via your microphone and relies dynamically.
- **Tri-State Visual UI:** A sleek, borderless UI that shifts its holographic animation and color depending on whether she is **SPEAKING** (cyan), **LISTENING** (orange), or **THINKING** (purple).
- **Background Orchestration:** Automatically scheduled to run daily at `11:00 AM` using macOS `launchd`.
- **Smart Briefing:** Automatically fetches the top 3 live Artificial Intelligence headlines directly from RSS feeds (TechCrunch).
- **Polite Delivery:** Uses Apple's native voice dictation ('Samantha', slowed to 150 WPM) to deliver a calm, composed, and methodical readout.

## Setup Instructions

1. **Install Requirements:** Make sure you have python3 installed on your Mac, and install the required modules:
   ```bash
   pip3 install openai scipy numpy sounddevice SpeechRecognition
   ```
2. **Set your API Key:** Open `astra_assistant.py` and replace `OPENAI_API_KEY` at the top with your real OpenAI API key.
3. **Setup Launch Agent for Daily Scheduling:**
   Open a terminal and run the following command from the root of this folder to orchestrate the background schedule.
   ```bash
   cp com.astra.daily.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.astra.daily.plist
   ```
4. **Trigger Manually:** To launch her instantly:
   ```bash
   python3 astra_assistant.py
   ```
