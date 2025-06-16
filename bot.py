#!/usr/bin/env python3
"""
YouTube to Audio Telegram Bot
A bot that converts YouTube videos to audio files and sends them via Telegram.
"""

import os
import logging
from time import sleep
from pathlib import Path

try:
    import telebot
    from pytube import YouTube
    from django.core.validators import URLValidator
    from requests.exceptions import ConnectionError
    from django.core.exceptions import ValidationError
except ImportError as e:
    print(f"Some modules are missing: {e}")
    print("Please run: pip install -r requirements.txt")
    exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')  # Replace with your token
if TOKEN == 'YOUR_BOT_TOKEN_HERE':
    logger.error("Please set your bot token in the TELEGRAM_BOT_TOKEN environment variable or in the code")
    exit(1)

# Directories setup
AUDIO_DIR = Path('audios')
STICKER_DIR = Path('stickers')

# Create directories if they don't exist
AUDIO_DIR.mkdir(exist_ok=True)
STICKER_DIR.mkdir(exist_ok=True)

# Initialize bot and validator
bot = telebot.TeleBot(TOKEN)
validator = URLValidator()

# Constants
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB - Telegram bot file size limit
WELCOME_STICKER_PATH = STICKER_DIR / 'welcome.webp'


@bot.message_handler(commands=['start'])
def welcome(message):
    """Send welcome message and sticker to new users."""
    welcome_text = (
        f"Welcome, {message.from_user.first_name}! 🎵\n\n"
        f"I'm <b>{bot.get_me().first_name}</b> - your YouTube audio converter.\n\n"
        "Just send me a YouTube URL and I'll extract the audio for you!\n\n"
        "Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    
    # Send welcome message
    bot.send_message(message.chat.id, welcome_text, parse_mode='html')
    
    # Send welcome sticker if it exists
    if WELCOME_STICKER_PATH.exists():
        try:
            with open(WELCOME_STICKER_PATH, 'rb') as sticker:
                bot.send_sticker(message.chat.id, sticker)
        except Exception as e:
            logger.warning(f"Could not send welcome sticker: {e}")


@bot.message_handler(commands=['help'])
def help_command(message):
    """Send help information to the user."""
    help_text = (
        "📖 <b>How to use this bot:</b>\n\n"
        "1. Send me any YouTube video URL\n"
        "2. I'll download and convert it to audio\n"
        "3. You'll receive the audio file directly in chat\n\n"
        "⚠️ <b>Note:</b> Large videos may take some time to process.\n"
        "Maximum file size is 50MB due to Telegram limitations."
    )
    bot.send_message(message.chat.id, help_text, parse_mode='html')


@bot.message_handler(content_types=['text'])
def send_audio(message):
    """Process YouTube URLs and send audio files."""
    try:
        # Validate URL
        validator(message.text)
        
        # Check if it's a YouTube URL
        if 'youtube.com' not in message.text and 'youtu.be' not in message.text:
            bot.send_message(
                message.chat.id, 
                "Please send a <b>YouTube</b> URL! 🎥",
                parse_mode='html'
            )
            return
        
        # Send processing message
        processing_msg = bot.send_message(
            message.chat.id, 
            "⏳ Processing your video...\nThis may take a moment.",
            parse_mode='html'
        )
        
        # Download and send audio
        logger.info(f"Processing URL: {message.text} for user {message.from_user.id}")
        audio_path = download_audio(message.text, AUDIO_DIR)
        
        # Check file size
        file_size = audio_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            bot.delete_message(message.chat.id, processing_msg.message_id)
            bot.send_message(
                message.chat.id,
                f"❌ Sorry, the audio file is too large ({file_size / 1024 / 1024:.1f}MB).\n"
                f"Maximum allowed size is 50MB.",
                parse_mode='html'
            )
            audio_path.unlink()  # Delete the file
            return
        
        # Send audio file
        with open(audio_path, 'rb') as audio:
            bot.send_audio(
                message.chat.id, 
                audio,
                caption="🎵 Here's your audio file!",
                timeout=60  # Increase timeout for large files
            )
        
        # Delete processing message
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
        # Clean up
        audio_path.unlink()
        logger.info(f"Successfully sent audio to user {message.from_user.id}")
        
    except ValidationError:
        bot.send_message(
            message.chat.id, 
            "❌ That doesn't look like a valid URL!\n"
            "Please send a YouTube link like:\n"
            "https://www.youtube.com/watch?v=...",
            parse_mode='html'
        )
    except ConnectionError:
        bot.send_message(
            message.chat.id, 
            "🌐 Connection error!\n"
            "Please check if the video is available and try again.",
            parse_mode='html'
        )
    except Exception as e:
        logger.error(f"Error processing URL for user {message.from_user.id}: {e}")
        bot.send_message(
            message.chat.id,
            "❌ An error occurred while processing your video.\n"
            "Please try again or try a different video.",
            parse_mode='html'
        )
        # Attempt to clean up any partial downloads
        try:
            if 'audio_path' in locals() and audio_path.exists():
                audio_path.unlink()
        except:
            pass


def download_audio(url: str, output_dir: Path) -> Path:
    """
    Download audio from YouTube video.
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save the audio file
        
    Returns:
        Path to the downloaded audio file
    """
    # Create YouTube object
    yt = YouTube(url)
    
    # Clean the title for filename
    clean_title = sanitize_filename(yt.title)
    
    # Get audio stream (highest quality audio-only stream)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    
    if not audio_stream:
        raise Exception("No audio stream available for this video")
    
    # Download the audio
    logger.info(f"Downloading: {clean_title}")
    output_path = audio_stream.download(
        output_path=str(output_dir),
        filename=f"{clean_title}.mp4"
    )
    
    return Path(output_path)


def sanitize_filename(filename: str) -> str:
    """
    Remove invalid characters from filename.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for filesystem
    """
    # Characters not allowed in filenames
    invalid_chars = ['\\', '/', '*', '?', '"', '<', '>', '|', '#', ':']
    
    # Replace invalid characters with spaces
    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, ' ')
    
    # Remove multiple spaces and trim
    sanitized = ' '.join(sanitized.split())
    
    # Limit length to avoid filesystem issues
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    # Ensure filename is not empty
    if not sanitized:
        sanitized = "audio"
    
    return sanitized


@bot.message_handler(func=lambda message: True)
def handle_other_content(message):
    """Handle non-text messages."""
    bot.send_message(
        message.chat.id,
        "🤔 Please send me a YouTube URL as text.\n"
        "I can only process text messages with YouTube links.",
        parse_mode='html'
    )


def main():
    """Main function to run the bot."""
    logger.info("Starting YouTube Audio Bot...")
    
    # Check if welcome sticker exists
    if not WELCOME_STICKER_PATH.exists():
        logger.warning(
            f"Welcome sticker not found at {WELCOME_STICKER_PATH}. "
            "Users won't receive a welcome sticker."
        )
    
    try:
        logger.info("Bot is polling for messages...")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed with error: {e}")
        sleep(5)  # Wait before potential restart


if __name__ == '__main__':
    main()