import json
import os

# Path to the global logs configuration file.
LOGS_CONFIG_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "logs_config.json")
)

def load_logs_config():
    # Load the log channel config from disk, handling invalid file contents.
    if os.path.exists(LOGS_CONFIG_FILE):
        try:
            with open(LOGS_CONFIG_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_logs_config(config):
    # Persist the log channel configuration to disk.
    os.makedirs(os.path.dirname(LOGS_CONFIG_FILE), exist_ok=True)
    with open(LOGS_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_log_channel_id(guild_id):
    # Return the configured log channel ID for the given guild.
    config = load_logs_config()
    value = config.get(str(guild_id))
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def set_log_channel_id(guild_id, channel_id):
    # Save the log channel ID for a guild.
    config = load_logs_config()
    config[str(guild_id)] = int(channel_id)
    save_logs_config(config)

def remove_log_channel(guild_id):
    # Remove a guild's log channel entry from configuration.
    config = load_logs_config()
    if str(guild_id) in config:
        del config[str(guild_id)]
        save_logs_config(config)
