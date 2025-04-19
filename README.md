
Built by https://www.blackbox.ai

---

```markdown
# MentionBot

## Project Overview
MentionBot is a Telegram bot designed to respond to direct mentions within group chats. It allows the admin to customize the bot's reply message whenever it is mentioned, enhancing the interaction experience in Telegram groups. The bot notifies the admin of all mentions, ensuring swift acknowledgment and response.

## Installation
To run MentionBot, please follow these steps:

1. **Clone the repository** to your local machine:
   ```bash
   git clone <repository-url>
   cd MentionBot
   ```

2. **Install the required packages** using `pip`. Make sure you have Python 3.7 or higher installed:
   ```bash
   pip install python-telegram-bot
   ```

3. **Set your Bot Token and Admin ID** in `bot.py`. Replace the placeholder values in the constants `BOT_TOKEN` and `ADMIN_ID` with your own.

## Usage
Once the bot is set up and running, you can interact with it in the following ways:

- Start the bot:
  - Send the `/start` command to the bot in your Telegram group to receive a welcome message.

- Set a custom reply message (only available to the admin):
  - Use the command `/setmessage Your custom message here` to update the bot's reply message. The admin ID is hardcoded into the bot, and only the admin can set the message.

- Mention the bot in a group chat:
  - When someone mentions the bot (e.g., @MentionBot), it will respond with the custom message set by the admin and notify the admin about the mention.

## Features
- The bot responds to direct mentions in group chats.
- The admin can customize the bot's reply message through a dedicated command.
- It notifies the admin privately whenever the bot is mentioned, maintaining awareness of group interactions.

## Dependencies
This project depends on the `python-telegram-bot` library. You can install it using pip as noted in the installation section.

### Dependencies List
- `python-telegram-bot >= 20.0` (make sure to check compatibility with your Python version)

## Project Structure
```
MentionBot/
│
├── bot.py                # Main bot implementation file
└── requirements.txt      # (If introduced) File with dependencies (optional)
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```

Make sure to replace `<repository-url>` in the installation section with your actual repository URL.