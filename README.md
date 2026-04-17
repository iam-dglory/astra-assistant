# Astra Personal Jarvis

A minimalist, dark-themed AI voice assistant tailored for macOS that automatically gives you a brief rundown of the latest AI and Tech news every day at 11:00 AM. 

## Features
- **Jarvis-like Interface:** A borderless, translucent dark-mode UI with a pulsing holographic orb.
- **Background Orchestration:** Automatically scheduled to run daily at `11:00 AM` using macOS `launchd`.
- **Smart Briefing:** Automatically fetches the top 3 live Artificial Intelligence headlines directly from RSS feeds (TechCrunch).
- **Polite Delivery:** Uses Apple's native voice dictation ('Samantha', slowed to 150 WPM) to deliver a calm, composed, and methodical readout.

## Setup Instructions

1. **Install Requirements:** Make sure you have python3 installed on your Mac.
2. **Setup Launch Agent for Daily Scheduling:**
   Open a terminal and run the following command from the root of this folder to copy the scheduler over and load it.
   ```bash
   cp com.astra.daily.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.astra.daily.plist
   ```
3. **Trigger Manually:** If you want to trigger Astra right away, simply run:
   ```bash
   python3 astra_assistant.py
   ```
