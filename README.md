# Echo.aic

Echo is a Windows-oriented voice assistant with speech recognition, spoken
responses, local music playback, and Spotify playback controls.

## Requirements

- Python 3.10 or newer
- A working microphone and audio output
- Spotify credentials for Spotify playback features

## Setup

1. Clone this repository and open a PowerShell terminal in its folder.
2. Create and activate a virtual environment, then install dependencies:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Use `.env.example` as a reference for configuration names. The application
   reads environment variables directly and does not load `.env` files. Set
   the values in PowerShell (or use your preferred secret manager) before
   starting the app. For example:

   ```powershell
   $env:SPOTIFY_CLIENT_ID = "your-client-id"
   $env:SPOTIFY_CLIENT_SECRET = "your-client-secret"
   $env:SPOTIFY_REDIRECT_URI = "http://localhost:2009/"
   ```

   Register the same redirect URI in your Spotify application's settings.
   Keep real credentials private; never commit them.

4. Put MP3 files that you own or are licensed to use in `local_music`.
5. Start Echo:

   ```powershell
   python main.py
   ```

Say “Hey echo” or “OK echo” to activate the command listener. Google speech
recognition is used to transcribe audio, so voice recognition requires an
internet connection. Spotify playback also requires an authenticated Spotify
account and an available playback device.

## Notes

- `data.env` and local media are intentionally excluded from Git.
- The optional experimental AI voice implementation in `cogs/ai_voice.py`
  has separate model dependencies and is not used by `main.py`.
