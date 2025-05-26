# Tadpole, a Rookie - Telegram bot

*A simple telegram bot that converts YouTube videos into mp3 files*

<br/>

## Requirements

- Python 3.9+ (CPython)
- FFmpeg
  - Tested with FFmpeg 7.1.1 "Péter"
  - [FFmpeg releases page](https://ffmpeg.org/download.html#releases)

<br/>

## Installation

1. **Setup virtual environment in project's root directory** <br/>
- For Linux:
```bash
python3 -m venv venv
```
- For Windows:
```cmd
python -m venv venv
```
<br/>

2. **Activate virtual environment** <br/>
- For Linux:
```bash
source venv/bin/activate
```
- For Windows:
```cmd
venv\scripts\activate
```
<br/>

3. **Install requirements in your venv** <br/>
```bash
pip install -r requirements.txt
```
<br/>

4. **Create .env file in project's root directory and configure API-token** <br/>
```.env
TOKEN=your_token
```

<br/>

## Running the bot

Run from root directory
- For Linux:
```bash
python3 bot.py
```
- For Windows:
```cmd
python bot.py
```

<br/><br/>

<p align="center">
    <img src="https://i.imgur.com/LxAQYdK.jpeg" width="400" alt="Bot preview">
</p>