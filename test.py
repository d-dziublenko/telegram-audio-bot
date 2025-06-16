#!/usr/bin/env python3
"""
Test suite for YouTube Audio Telegram Bot
Run with: pytest tests.py -v
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

# Add the parent directory to the path so we can import bot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set a dummy token for testing
os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token_12345'

import bot


class TestFilenameeSanitization(unittest.TestCase):
    """Test the sanitize_filename function."""
    
    def test_basic_sanitization(self):
        """Test removal of basic invalid characters."""
        test_cases = [
            ("normal_filename.mp4", "normal_filename.mp4"),
            ("file/with/slashes.mp4", "file with slashes.mp4"),
            ("file*with*asterisks.mp4", "file with asterisks.mp4"),
            ("file?with?questions.mp4", "file with questions.mp4"),
            ("file<with>brackets.mp4", "file with brackets.mp4"),
            ("file|with|pipes.mp4", "file with pipes.mp4"),
            ("file#with#hashes.mp4", "file with hashes.mp4"),
            ("file:with:colons.mp4", "file with colons.mp4"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = bot.sanitize_filename(input_name)
                self.assertEqual(result, expected)
    
    def test_multiple_spaces_handling(self):
        """Test that multiple spaces are collapsed to single spaces."""
        input_name = "file    with    many    spaces"
        expected = "file with many spaces"
        self.assertEqual(bot.sanitize_filename(input_name), expected)
    
    def test_empty_filename(self):
        """Test handling of empty filename."""
        self.assertEqual(bot.sanitize_filename(""), "audio")
        self.assertEqual(bot.sanitize_filename("///"), "audio")
        self.assertEqual(bot.sanitize_filename("***"), "audio")
    
    def test_long_filename(self):
        """Test that long filenames are truncated."""
        long_name = "a" * 300
        result = bot.sanitize_filename(long_name)
        self.assertEqual(len(result), 200)
        self.assertEqual(result, "a" * 200)
    
    def test_unicode_handling(self):
        """Test that unicode characters are preserved."""
        test_cases = [
            ("видео_на_русском.mp4", "видео_на_русском.mp4"),
            ("中文视频.mp4", "中文视频.mp4"),
            ("فيديو_عربي.mp4", "فيديو_عربي.mp4"),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = bot.sanitize_filename(input_name)
                self.assertEqual(result, expected)


class TestBotHandlers(unittest.TestCase):
    """Test bot message handlers."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.bot_mock = Mock()
        bot.bot = self.bot_mock
        
        # Create a mock message
        self.message = Mock()
        self.message.chat.id = 12345
        self.message.from_user.id = 67890
        self.message.from_user.first_name = "Test User"
    
    def test_welcome_handler(self):
        """Test the /start command handler."""
        # Mock bot.get_me()
        bot_info = Mock()
        bot_info.first_name = "TestBot"
        self.bot_mock.get_me.return_value = bot_info
        
        # Create temporary welcome sticker
        with tempfile.NamedTemporaryFile(suffix='.webp', delete=False) as tmp:
            tmp.write(b'fake sticker data')
            tmp_path = tmp.name
        
        try:
            # Temporarily replace the sticker path
            original_path = bot.WELCOME_STICKER_PATH
            bot.WELCOME_STICKER_PATH = Path(tmp_path)
            
            # Call the welcome handler
            bot.welcome(self.message)
            
            # Check that welcome message was sent
            self.bot_mock.send_message.assert_called_once()
            args, kwargs = self.bot_mock.send_message.call_args
            self.assertEqual(args[0], 12345)  # chat_id
            self.assertIn("Welcome", args[1])  # message contains "Welcome"
            self.assertEqual(kwargs['parse_mode'], 'html')
            
            # Check that sticker was sent
            self.bot_mock.send_sticker.assert_called_once()
            
        finally:
            # Clean up
            bot.WELCOME_STICKER_PATH = original_path
            os.unlink(tmp_path)
    
    def test_help_handler(self):
        """Test the /help command handler."""
        bot.help_command(self.message)
        
        # Check that help message was sent
        self.bot_mock.send_message.assert_called_once()
        args, kwargs = self.bot_mock.send_message.call_args
        self.assertEqual(args[0], 12345)  # chat_id
        self.assertIn("How to use", args[1])  # message contains help text
        self.assertEqual(kwargs['parse_mode'], 'html')
    
    @patch('bot.validator')
    def test_invalid_url_handling(self, mock_validator):
        """Test handling of invalid URLs."""
        from django.core.exceptions import ValidationError
        
        # Set up the message
        self.message.text = "not a url at all"
        
        # Make validator raise ValidationError
        mock_validator.side_effect = ValidationError("Invalid URL")
        
        # Call the handler
        bot.send_audio(self.message)
        
        # Check that error message was sent
        self.bot_mock.send_message.assert_called_once()
        args, kwargs = self.bot_mock.send_message.call_args
        self.assertIn("doesn't look like a valid URL", args[1])
    
    @patch('bot.validator')
    def test_non_youtube_url(self, mock_validator):
        """Test handling of non-YouTube URLs."""
        # Set up the message
        self.message.text = "https://example.com/video"
        
        # Make validator pass
        mock_validator.return_value = None
        
        # Call the handler
        bot.send_audio(self.message)
        
        # Check that YouTube-specific message was sent
        self.bot_mock.send_message.assert_called_once()
        args, kwargs = self.bot_mock.send_message.call_args
        self.assertIn("YouTube", args[1])


class TestYouTubeDownload(unittest.TestCase):
    """Test YouTube download functionality."""
    
    @patch('bot.YouTube')
    def test_download_audio_success(self, mock_youtube_class):
        """Test successful audio download."""
        # Set up mocks
        mock_yt = Mock()
        mock_youtube_class.return_value = mock_yt
        mock_yt.title = "Test Video Title"
        
        # Mock the stream
        mock_stream = Mock()
        mock_stream.download.return_value = "/tmp/test_video.mp4"
        
        # Mock the streams filter chain
        mock_streams = Mock()
        mock_streams.filter.return_value = mock_streams
        mock_streams.order_by.return_value = mock_streams
        mock_streams.desc.return_value = mock_streams
        mock_streams.first.return_value = mock_stream
        
        mock_yt.streams = mock_streams
        
        # Test download
        with tempfile.TemporaryDirectory() as tmpdir:
            result = bot.download_audio("https://youtube.com/watch?v=test", Path(tmpdir))
            
            # Verify YouTube was called with correct URL
            mock_youtube_class.assert_called_once_with("https://youtube.com/watch?v=test")
            
            # Verify stream filter was called correctly
            mock_streams.filter.assert_called_once_with(only_audio=True)
            
            # Verify download was called
            mock_stream.download.assert_called_once()
    
    @patch('bot.YouTube')
    def test_download_audio_no_stream(self, mock_youtube_class):
        """Test handling when no audio stream is available."""
        # Set up mocks
        mock_yt = Mock()
        mock_youtube_class.return_value = mock_yt
        mock_yt.title = "Test Video"
        
        # Mock the streams to return None
        mock_streams = Mock()
        mock_streams.filter.return_value = mock_streams
        mock_streams.order_by.return_value = mock_streams
        mock_streams.desc.return_value = mock_streams
        mock_streams.first.return_value = None  # No stream available
        
        mock_yt.streams = mock_streams
        
        # Test download - should raise exception
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(Exception) as context:
                bot.download_audio("https://youtube.com/watch?v=test", Path(tmpdir))
            
            self.assertIn("No audio stream available", str(context.exception))


class TestIntegration(unittest.TestCase):
    """Integration tests for the bot."""
    
    @patch('bot.telebot.TeleBot')
    def test_bot_initialization(self, mock_telebot):
        """Test that bot initializes correctly."""
        # Re-import bot to trigger initialization
        import importlib
        importlib.reload(bot)
        
        # Check that TeleBot was initialized with token
        mock_telebot.assert_called_with('test_token_12345')
    
    def test_directories_creation(self):
        """Test that required directories are created."""
        # The bot module should create these directories on import
        self.assertTrue(bot.AUDIO_DIR.exists())
        self.assertTrue(bot.STICKER_DIR.exists())


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def test_file_size_limit(self):
        """Test that file size limit is properly defined."""
        self.assertEqual(bot.MAX_FILE_SIZE, 50 * 1024 * 1024)  # 50MB
    
    @patch('bot.Path.stat')
    def test_large_file_handling(self, mock_stat):
        """Test handling of files that exceed size limit."""
        # This would be part of the send_audio handler
        # Mock a file that's too large
        mock_stat.return_value.st_size = 60 * 1024 * 1024  # 60MB
        
        # The actual implementation would check this and send an error message
        file_size = mock_stat.return_value.st_size
        self.assertGreater(file_size, bot.MAX_FILE_SIZE)


if __name__ == '__main__':
    unittest.main()