import logging
import re
import sys
import yaml
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Function to get all user messages
def get_all_user(users):
    return [{"message": user.message} for user in users]

# Function to start the Telegram client and listen for messages
def start(config):
    # Initialize the Telegram client
    client = TelegramClient(config["session_name"], config["api_id"], config["api_hash"])
    client.start()

    # Lists to hold the input and output channel entities
    input_channels_entities = []
    output_channel_entities = []
    
    # Fetch input and output channels from the user's dialogs
    for d in client.iter_dialogs():
        if d.name in config["input_channel_names"] or d.entity.id in config["input_channel_ids"]:
            input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
        if d.name in config["output_channel_names"] or d.entity.id in config["output_channel_ids"]:
            output_channel_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
            
    # Exit if no output channels are found
    if not output_channel_entities:
        logger.error("Could not find any output channels in the user's dialogs")
        sys.exit(1)

    # Exit if no input channels are found
    if not input_channels_entities:
        logger.error("Could not find any input channels in the user's dialogs")
        sys.exit(1)
        
    # Log the number of channels being listened to and forwarded
    logger.info(f"Listening on {len(input_channels_entities)} channels. Forwarding messages to {len(output_channel_entities)} channels.")
    
    # Event handler for new messages in input channels
    # This section is designed to modify the message handling behavior based on the messages
    # received from the Telegram channel, specifically tailored for Forex Robot Nation signal provider.
    # It should be adjusted if used with different message formats or signal providers.
    @client.on(events.NewMessage(chats=input_channels_entities))
    async def handler(event):
        # Forward messages to output channels
        for output_channel in output_channel_entities:
            message = getattr(event.message, 'message').lower()

            currency_pair_pattern = r"([A-Z]{3}/[A-Z]{3})"
            currency_pair_match = re.search(currency_pair_pattern, message)

            # Initialize the response message
            res = ""

            # Process messages containing 'closed' or 'cancelled'
            # and format the response accordingly
            if 'closed' in message or 'cancelled' in message:
                res = f"rfc close {currency_pair_match.group()}"
            
            # Process messages containing 'move sl'
            # and format the response accordingly
            if 'move sl' in message:
                res = f"rfc sl entry {currency_pair_match.group()}"
            
            # Process messages containing 'potential downward/upward movement'
            # Replace 'Target' with 'Take' in the response message
            if ('potential downward movement' in message or 'potential upward movement' in message) and 'trade safely' in message:
                res = message.replace('target', 'take')
                
            # Send the formatted response message to the output channel
            # Convert the message to uppercase before sending
            if res:
                await client.send_message(output_channel, message=res.upper())
                    
    # Run the client until disconnected
    client.run_until_disconnected()

# Entry point of the script
if __name__ == "__main__":
    # Ensure a configuration file is provided
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
        sys.exit(1)
    # Load the configuration file
    with open(sys.argv[1], 'rb') as f:
        config = yaml.safe_load(f)
    # Start the client with the loaded configuration
    start(config)