# Discord_Bot
A simple Discord bot that monitors a text file for changes and automatically posts new lines to a specified Discord channel. The bot efficiently tracks file modifications by monitoring the file position, making it ideal for log files or any text file that grows by appending new lines.
## Features
- Real-time monitoring of text file changes
- Posts new lines to a specified Discord channel
- Efficiently handles large files by only reading new content
- Configurable check interval
- Error handling and status reporting
## Configuration
Edit the following variables in the script:
```
FILE_TO_MONITOR = 'location/of/textfile.txt'  # Path to your text file
CHANNEL_ID = 1000089000000000081              # Discord channel ID
CHECK_INTERVAL = 1                            # How often to check for changes (in seconds)
DISCORD_API_KEY = 'YOUR_BOT_TOKEN'            # Your Discord bot token
```
