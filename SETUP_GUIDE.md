# Complete Setup and Deployment Guide

This guide walks you through setting up your Telegram YouTube Audio Bot from scratch, including creating the bot on Telegram, configuring the code, and deploying it.

## Table of Contents

1. [Creating Your Telegram Bot](#creating-your-telegram-bot)
2. [Local Development Setup](#local-development-setup)
3. [Testing Your Bot](#testing-your-bot)
4. [Deployment Options](#deployment-options)
5. [Maintenance and Monitoring](#maintenance-and-monitoring)

## Creating Your Telegram Bot

### Step 1: Talk to BotFather

1. Open Telegram and search for `@BotFather`
2. Start a conversation and send `/newbot`
3. Follow the prompts:
   - Choose a name for your bot (e.g., "YouTube Audio Converter")
   - Choose a username (must end in 'bot', e.g., `youtube_audio_converter_bot`)
4. BotFather will give you a token like: `5612345678:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`
5. **Save this token securely** - you'll need it to run your bot

### Step 2: Configure Your Bot (Optional)

While still chatting with BotFather, you can:

- `/setdescription` - Add a description for your bot
- `/setabouttext` - Set the about section
- `/setuserpic` - Upload a profile picture
- `/setcommands` - Set the command list:
  ```
  start - Start the bot and see welcome message
  help - Get help on how to use the bot
  ```

## Local Development Setup

### Prerequisites Check

First, verify you have Python installed:

```bash
python --version  # Should be 3.7 or higher
```

### Step 1: Clone and Navigate

```bash
git clone https://github.com/d-dziublenko/telegram-audio-bot.git
cd telegram-audio-bot
```

### Step 2: Virtual Environment Setup

Creating a virtual environment keeps your project dependencies isolated:

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter errors, try upgrading pip first:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Environment Configuration

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your favorite text editor:

   ```bash
   # On Windows
   notepad .env

   # On macOS/Linux
   nano .env
   ```

3. Replace `your_bot_token_here` with your actual bot token from BotFather

### Step 5: Create Required Directories

```bash
mkdir -p audios stickers
```

### Step 6: Add Welcome Sticker (Optional)

If you want a welcome sticker, create or download a `.webp` file and save it as `stickers/welcome.webp`

## Testing Your Bot

### Running the Bot

With your virtual environment activated and token configured:

```bash
python bot.py
```

You should see:

```
2024-01-01 12:00:00,000 - __main__ - INFO - Starting YouTube Audio Bot...
2024-01-01 12:00:00,100 - __main__ - INFO - Bot is polling for messages...
```

### Testing in Telegram

1. Open Telegram and search for your bot by its username
2. Send `/start` - You should receive a welcome message
3. Send a YouTube URL like `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
4. Wait for the bot to process and send you the audio file

### Common Issues During Testing

**Bot not responding:**

- Check that the bot is running (you should see log messages)
- Verify your token is correct
- Ensure you're messaging the right bot

**"Some modules are missing" error:**

- Make sure your virtual environment is activated
- Run `pip install -r requirements.txt` again

**YouTube download errors:**

- Try updating pytube: `pip install --upgrade pytube`
- Some videos may be restricted or age-gated
- Check if the URL is valid and publicly accessible

## Deployment Options

### Option 1: VPS Deployment (Recommended)

#### Using systemd (Linux)

1. Create a systemd service file:

   ```bash
   sudo nano /etc/systemd/system/telegram-bot.service
   ```

2. Add the following content:

   ```ini
   [Unit]
   Description=Telegram YouTube Audio Bot
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/home/your-username/telegram-audio-bot
   Environment="PATH=/home/your-username/telegram-audio-bot/venv/bin"
   ExecStart=/home/your-username/telegram-audio-bot/venv/bin/python bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Start and enable the service:
   ```bash
   sudo systemctl start telegram-bot
   sudo systemctl enable telegram-bot
   sudo systemctl status telegram-bot
   ```

### Option 2: Docker Deployment

1. Create a `Dockerfile`:

   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   RUN mkdir -p audios stickers

   CMD ["python", "bot.py"]
   ```

2. Create `docker-compose.yml`:

   ```yaml
   version: "3.8"
   services:
     bot:
       build: .
       environment:
         - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
       volumes:
         - ./stickers:/app/stickers
       restart: unless-stopped
   ```

3. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Option 3: Cloud Platform Deployment

#### Heroku (Free tier discontinued, but still an option)

1. Create `Procfile`:

   ```
   worker: python bot.py
   ```

2. Create `runtime.txt`:

   ```
   python-3.9.16
   ```

3. Deploy:
   ```bash
   heroku create your-bot-name
   heroku config:set TELEGRAM_BOT_TOKEN=your_token_here
   git push heroku main
   heroku ps:scale worker=1
   ```

#### Railway.app

1. Connect your GitHub repository to Railway
2. Add environment variable `TELEGRAM_BOT_TOKEN`
3. Deploy directly from the Railway dashboard

## Maintenance and Monitoring

### Logging

The bot logs important events. To save logs to a file, modify the logging configuration in `bot.py`:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

### Monitoring Bot Health

Create a simple health check:

```python
@bot.message_handler(commands=['status'])
def status(message):
    # Optional: Add admin check
    if message.from_user.id == YOUR_ADMIN_ID:
        uptime = time.time() - START_TIME
        bot.send_message(
            message.chat.id,
            f"🟢 Bot is running\nUptime: {uptime//3600:.0f}h {(uptime%3600)//60:.0f}m"
        )
```

### Regular Maintenance Tasks

1. **Check disk space** - Audio files are deleted after sending, but check for orphaned files
2. **Update dependencies** - Especially pytube for YouTube compatibility:
   ```bash
   pip install --upgrade pytube
   ```
3. **Monitor logs** - Look for repeated errors or unusual patterns
4. **Backup your configuration** - Keep your `.env` file backed up securely

### Scaling Considerations

If your bot becomes popular:

1. Implement rate limiting per user
2. Add a queue system for processing videos
3. Consider using webhook mode instead of polling
4. Add a database to track usage statistics
5. Implement caching for frequently requested videos

## Security Best Practices

1. **Never commit sensitive data**:

   - Always use environment variables for tokens
   - Keep `.env` in `.gitignore`

2. **Validate all inputs**:

   - The bot already validates URLs
   - Consider adding user whitelisting for private bots

3. **Set resource limits**:

   - Maximum file size (already implemented)
   - Timeout for downloads
   - Rate limiting per user

4. **Keep dependencies updated**:
   ```bash
   pip list --outdated
   pip install --upgrade [package-name]
   ```

## Troubleshooting Deployment

### Bot works locally but not in production:

- Check environment variables are set correctly
- Verify network connectivity
- Check firewall rules (Telegram bot API needs outbound HTTPS)
- Review logs for specific error messages

### High memory usage:

- Implement cleanup for interrupted downloads
- Add maximum concurrent downloads limit
- Monitor for memory leaks in long-running processes

### Slow performance:

- Consider using a CDN for frequently requested content
- Implement caching mechanisms
- Use async operations where possible

## Getting Help

If you encounter issues:

1. Check the logs first - they often contain helpful error messages
2. Search for the error message online
3. Check pytube GitHub issues for YouTube-related problems
4. Ask in the project's GitHub Issues section
5. Telegram bot development communities can be helpful

Remember to always respect YouTube's Terms of Service and copyright laws when using this bot.
