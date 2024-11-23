import discord
import asyncio
import os
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


FILE_TO_MONITOR = 'location/of/textfile.txt'
CHANNEL_ID = 1000089000000000081  # Channel to post to
CHECK_INTERVAL = 1  # Seconds to recheck txt file
DISCORD_API_KEY = 'KEY_HERE'

class FileMonitor:
    def __init__(self, filename):
        self.filename = filename
        self.last_position = 0
        self.first_run = True
        
    async def check_for_changes(self):
        try:
            if not os.path.exists(self.filename):
                print(f"File not found: {self.filename}")
                return None
                
            # Get the current file size
            current_size = os.path.getsize(self.filename)
            
            # If it's the first run, just store the file size and return
            if self.first_run:
                self.last_position = current_size
                self.first_run = False
                return None
            
            # If file hasn't grown, no new content
            if current_size <= self.last_position:
                return None
                
            with open(self.filename, 'r', encoding='utf-8') as file:
                # Go to where we last read
                file.seek(self.last_position)
                
                # Read new content
                new_content = file.read()
                
                # Update our position
                self.last_position = current_size
                
                # Split into lines and filter out empty ones
                return [line.strip() for line in new_content.split('\n') if line.strip()]
                
        except Exception as e:
            print(f"Error checking file: {e}")
            return None

monitor = FileMonitor(FILE_TO_MONITOR)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    print(f"Starting file monitor for: {os.path.abspath(FILE_TO_MONITOR)}")
    client.loop.create_task(check_file_loop())

async def check_file_loop():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    
    if not channel:
        print("Error: Could not find channel")
        return
    
    while not client.is_closed():
        try:
            new_lines = await monitor.check_for_changes()
            
            if new_lines:
                print(f"Found {len(new_lines)} new lines")
                for line in new_lines:
                    await channel.send(line)
                    await asyncio.sleep(0.5)  # Small delay between messages
            
            await asyncio.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            print(f"Error in check_file_loop: {e}")
            await asyncio.sleep(CHECK_INTERVAL)

client.run(DISCORD_API_KEY)
