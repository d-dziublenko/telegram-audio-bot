# YouTube to Audio Telegram Bot

A production-ready Telegram bot that converts YouTube videos to audio files. Simply send a YouTube URL to the bot, and it will download and send back the audio track. This project features robust error handling, automated testing, Docker support, and comprehensive documentation to help you get started quickly.

## Features

- 🎵 Extracts high-quality audio from YouTube videos
- 📱 Simple Telegram interface with intuitive commands
- 🚀 Fast conversion and delivery with progress notifications
- 🛡️ URL validation to ensure only valid links are processed
- 📊 Comprehensive logging for monitoring and debugging
- 🔒 Secure environment variable configuration
- 🧹 Automatic cleanup of temporary files
- ⚡ Progress notifications during processing
- 📏 File size validation (50MB Telegram limit)
- 🐳 Docker support for easy deployment
- ✅ Automated testing with GitHub Actions
- 🤝 Clear contribution guidelines for open source collaboration

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.7 or higher (the bot is tested on versions 3.7 through 3.11)
- pip (Python package installer)
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Docker and Docker Compose (optional, for containerized deployment)

## Quick Start

### Option 1: Traditional Python Setup

The traditional setup is perfect if you want to run the bot directly on your system and have full control over the Python environment.

```bash
# Clone the repository
git clone https://github.com/d-dziublenko/telegram-audio-bot.git
cd telegram-audio-bot

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env with your bot token

# Create required directories
mkdir -p audios stickers

# Run the bot
python bot.py
```

### Option 2: Docker Setup (Recommended for Production)

Docker provides a consistent environment across different systems and makes deployment much simpler. This approach is ideal for production use or when you want to avoid Python version conflicts.

```bash
# Clone the repository
git clone https://github.com/d-dziublenko/telegram-audio-bot.git
cd telegram-audio-bot

# Set up configuration
cp .env.example .env
# Edit .env with your bot token

# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

## Detailed Setup

For comprehensive setup instructions including creating your Telegram bot, various deployment options, and advanced configuration, please refer to our [SETUP_GUIDE.md](SETUP_GUIDE.md). This guide covers everything from creating your bot on Telegram to deploying on cloud platforms.

## Usage

Once your bot is running, interacting with it is straightforward:

1. **Start the bot**: Send `/start` to receive a welcome message and instructions
2. **Get help**: Send `/help` for detailed usage information
3. **Convert videos**: Send any YouTube URL to receive the audio file

The bot accepts various YouTube URL formats:

- Standard: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short: `https://youtu.be/VIDEO_ID`
- Mobile: `https://m.youtube.com/watch?v=VIDEO_ID`

## Project Structure

```
telegram-audio-bot/
│
├── .github/
│   └── workflows/
│       └── test.yml        # GitHub Actions for automated testing
│
├── bot.py                  # Main bot application with enhanced error handling
├── tests.py                # Comprehensive test suite
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container definition
├── docker-compose.yml      # Docker Compose configuration
│
├── .gitignore             # Git ignore rules
├── .env.example           # Environment variable template
├── .env                   # Your configuration (not in version control)
│
├── README.md              # This file
├── SETUP_GUIDE.md         # Comprehensive setup and deployment guide
├── CONTRIBUTING.md        # Guidelines for contributors
├── LICENSE                # AGPL-3.0 license
│
├── audios/                # Temporary audio storage (auto-cleaned)
│   └── .gitkeep          # Keeps directory in git
└── stickers/              # Bot stickers
    └── welcome.webp       # Welcome sticker (optional)
```

## How It Works

The bot operates through a carefully designed workflow that ensures reliability and user satisfaction:

1. **URL Reception**: When a user sends a message, the bot first validates it as a properly formatted URL
2. **YouTube Validation**: The bot checks if the URL points to YouTube, ensuring it can process the request
3. **Progress Notification**: A "processing" message keeps the user informed that their request is being handled
4. **Audio Extraction**: Using pytube, the bot downloads the highest quality audio stream available
5. **File Processing**: Filenames are sanitized to remove problematic characters, and file size is checked against Telegram's limits
6. **Delivery**: The audio file is sent to the user with a success message
7. **Cleanup**: Temporary files are automatically deleted to prevent disk space issues

## Testing

This project includes a comprehensive test suite to ensure reliability. The tests cover filename sanitization, message handlers, error handling, and more. Running tests helps catch bugs before they affect users.

### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests.py -v

# Run with coverage report
pytest tests.py --cov=bot --cov-report=html
```

### Automated Testing

The repository includes GitHub Actions configuration that automatically runs tests when you push changes or create pull requests. This continuous integration setup tests the bot across multiple Python versions (3.7 through 3.11) to ensure broad compatibility.

## Docker Deployment

Docker simplifies deployment by packaging the bot with all its dependencies. The included Dockerfile and docker-compose.yml provide a complete containerized solution with health checks, resource limits, and automatic restart capabilities.

### Building the Docker Image

```bash
# Build the image
docker build -t youtube-audio-bot .

# Run with environment variables
docker run -e TELEGRAM_BOT_TOKEN=your_token_here youtube-audio-bot
```

### Using Docker Compose

Docker Compose provides additional benefits like easy environment variable management and service orchestration:

```bash
# Start the service
docker-compose up -d

# View real-time logs
docker-compose logs -f telegram-bot

# Restart the service
docker-compose restart

# Stop and remove containers
docker-compose down
```

## Configuration Options

The bot supports several configuration options through environment variables, allowing you to customize its behavior without modifying code:

| Variable             | Description                                     | Default | Required |
| -------------------- | ----------------------------------------------- | ------- | -------- |
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather                   | None    | Yes      |
| `LOG_LEVEL`          | Logging verbosity (DEBUG, INFO, WARNING, ERROR) | INFO    | No       |
| `MAX_FILE_SIZE_MB`   | Maximum file size in megabytes                  | 50      | No       |

## Contributing

We welcome contributions from the community! This project follows clear guidelines to ensure code quality and maintainability. Before contributing, please read our [CONTRIBUTING.md](CONTRIBUTING.md) file which covers:

- Code of conduct and community standards
- Development setup instructions
- Code style guidelines and standards
- Commit message conventions
- Pull request process and review criteria
- How to report bugs effectively
- How to suggest enhancements

### Quick Contribution Guide

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest tests.py`)
5. Commit your changes using conventional commits (`feat: add amazing feature`)
6. Push to your branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request with a clear description

## Error Handling

The bot includes sophisticated error handling to provide a smooth user experience even when things go wrong:

- **Invalid URLs**: Provides clear feedback about proper URL format with examples
- **Non-YouTube URLs**: Specifically requests YouTube links to set proper expectations
- **Connection errors**: Handles network issues gracefully with user-friendly messages
- **Large files**: Proactively notifies users when files exceed Telegram's 50MB limit
- **Download failures**: Manages restricted or unavailable videos with helpful error messages
- **Cleanup on errors**: Ensures temporary files are removed even if processing fails

## Security Considerations

This project implements several security best practices to protect both the bot and its users:

- **Token Security**: Bot tokens are stored in environment variables, never committed to version control
- **Input Validation**: All URLs are thoroughly validated before processing
- **File System Safety**: Filenames are sanitized to prevent directory traversal attacks
- **Resource Limits**: File size limits and timeouts prevent abuse
- **Error Information**: Error messages are designed to be helpful without exposing sensitive system information
- **Container Security**: Docker setup runs as non-root user for additional isolation

For production deployments, consider the additional security measures outlined in [SETUP_GUIDE.md](SETUP_GUIDE.md).

## Troubleshooting

### Common Issues and Solutions

**Bot not responding:**
First, verify your bot token is correctly set in the `.env` file. Then check that the bot is actually running by looking for log output. Finally, ensure you're messaging the correct bot in Telegram.

**Module import errors:**
Make sure your virtual environment is activated before installing dependencies. Run `pip install -r requirements.txt` again to ensure all packages are installed. Verify you're using Python 3.7 or higher with `python --version`.

**YouTube download failures:**
YouTube frequently updates their platform, which can break download functionality. Update pytube to the latest version with `pip install --upgrade pytube`. Also check if the video is public and available in your region, as some videos have geographic or age restrictions.

**Docker issues:**
If the Docker container exits immediately, check the logs with `docker-compose logs`. Ensure your `.env` file exists and contains a valid bot token. Verify Docker has enough resources allocated, especially if running on Docker Desktop.

For more detailed troubleshooting information, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

## Monitoring and Maintenance

### Viewing Logs

Logs are essential for understanding what your bot is doing and diagnosing issues:

```bash
# For direct Python execution
python bot.py  # Logs appear in console

# For Docker deployment
docker-compose logs -f telegram-bot

# To save logs to a file
python bot.py > bot.log 2>&1
```

### Health Monitoring

The Docker setup includes health checks that automatically restart the bot if it becomes unresponsive. For additional monitoring, consider implementing a status command or integrating with monitoring services.

### Regular Maintenance

To keep your bot running smoothly:

- Update dependencies regularly, especially pytube: `pip install --upgrade -r requirements.txt`
- Monitor disk usage in the `audios/` directory
- Review logs for recurring errors or unusual patterns
- Keep your bot token secure and rotate it periodically

## Limitations

While powerful, the bot has some inherent limitations to be aware of:

- **File Size**: Maximum 50MB due to Telegram Bot API restrictions
- **Processing Time**: Larger videos take longer to download and convert
- **Availability**: Some videos may be geo-restricted, age-gated, or private
- **Format**: Currently outputs in the original audio format (usually .mp4 audio container)
- **Concurrent Users**: Default setup handles one request at a time

## License

This project is licensed under the AGPL-3.0 license - see the [LICENSE](LICENSE) file for details. This permissive license allows you to use, modify, and distribute this software for personal purposes, with attribution.

## Acknowledgments

This project stands on the shoulders of excellent open-source libraries:

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - Elegant Telegram bot framework
- [pytube](https://github.com/pytube/pytube) - Lightweight YouTube video downloading
- [Django Validators](https://docs.djangoproject.com/en/stable/ref/validators/) - Robust URL validation

Special thanks to all contributors who help improve this project!

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Read through [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed information
3. Search existing [GitHub Issues](https://github.com/d-dziublenko/telegram-audio-bot/issues)
4. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Error messages and logs
   - Your environment details (OS, Python version, etc.)

## Disclaimer

This bot is designed for personal use and educational purposes. Users are responsible for complying with YouTube's Terms of Service and respecting copyright laws in their jurisdiction. The bot should only be used to download content you have permission to access and download.

Remember that content creators rely on ad revenue and views. Consider supporting creators directly through YouTube Premium, Patreon, or other means if you frequently consume their content.

---

**Made with ❤️ by Dmytro Dziublenko**

If you find this bot helpful, consider giving it a ⭐ on GitHub!
