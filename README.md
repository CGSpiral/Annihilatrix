
# Annihilatrix Bot

Annihilatrix is a fun and experimental Discord bot designed for creating and spamming channels in a server. It was created to explore the possibilities of automation and channel management in Discord, but it is **NOT INTENDED** to be used for harm or disruption of any community or server. Please use this bot responsibly and only in servers where you have full permission.

## Features

- **Mass Channel Creation and Spamming**: Create up to 100 text channels and spam a message in them.
- **Channel Deletion**: Delete all text and category channels in the server.
- **Mass Banning**: Ban all members who don't have specific permissions (for fun or as part of moderation).
- **Permission Management**: The bot can disable the "COMMUNITY" feature for the server.

---

## Disclaimer

This bot is intended for **educational purposes** and **fun use only**. It is not designed to harm servers, communities, or violate Discord's Terms of Service. Use responsibly.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- The following Python packages:
  - `discord.py`
  - `asyncio`

## How to Create and Set Up the Bot

### Steps

### Step 1: Create a Discord Bot Account

- Go to the [Discord Developer Portal](https://discord.com/developers/applications).
- Click on the **"New Application"** button.
- Name your application (e.g., "Annihilatrix").
- Under the **"Bot"** tab, click **"Add Bot"**.
- Click on **"Copy"** under the **TOKEN** section to get your bot's token. You will need this token to authenticate your bot with Discord.
- (Optional) Customize your bot’s username, avatar, and description as you like.

### Step 2: Clone the repository or download the bot code to your machine.
   - Clone this repository to your local machine:
  ```bash
   git clone https://github.com/CGSpiral/Annihilatrix
   ```
### Step 3: Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Set up your bot's token:

   **Option 1**: Use PowerShell command to temporarily set the token:
   Windows PowerShell:
   ```powershell
   $env:ANNIHILATRIX="your-bot-token"
   ```

   **Option 2**: Manually create or edit a `.env` file in the bot's directory and add the following line:
   ```env
   ANNIHILATRIX=your-bot-token
   ```
   Save the file and ensure it is in the same directory as the bot's main script.
### Step 5: Create an `.inv` file with the authorized user IDs, one per line:

   ```plaintext
   123456789012345678
   987654321098765432
   ```

### Step 6: Run the bot:

   ```bash
   python Annihilatrix.py
   ```
##Make sure to add your custom ban reason on line 148 in the code
---

## Usage

### Commands

- `#spam <message>`: Spams the message in the server if left blank default message will be spammed.
- `#stop`: Stops any ongoing spam operations.
- `#wipe`: Bans all server members.

---

## Support

For issues, open a GitHub issue.

---

## Disclaimer (Repeated)

This bot is a **fun/educational project** and should not be used maliciously. Misuse may lead to consequences on Discord.

## License

```plaintext
MIT License

Copyright (c) 2024 CGSpiral

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
