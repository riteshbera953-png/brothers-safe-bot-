# BROTHERS SAFE TELEGRAM BOT

A basic Telegram bot project with configurable Force Join checks and a small HTTP health-check endpoint for hosting platforms such as Render.

## Files

- `safe_bot-1.py` — Main bot entry point.
- `force_join.py` — Reusable Force Join helper functions.
- `requirements.txt` — Python dependencies.
- `README.md` — Setup and deployment instructions.

## Requirements

- Python 3.10 or newer
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- The bot added as an administrator in each required channel so Telegram membership checks can work

## Configure

1. In your hosting provider, add an environment variable named `BOT_TOKEN`.
2. Set its value to your bot's token. Do not commit your token to GitHub.
3. Check the channel IDs and links in `force_join.py` and make sure they match your channels.
4. Make the bot an administrator in each required channel.

## Install and Run Locally

```bash
pip install -r requirements.txt
python safe_bot-1.py
```

## Deploy on Render

1. Upload the project files to a GitHub repository.
2. Create a **Web Service** in Render and connect the repository.
3. Set the Build Command to:

   ```bash
   pip install -r requirements.txt
   ```

4. Set the Start Command to:

   ```bash
   python safe_bot-1.py
   ```

5. Add `BOT_TOKEN` under the service's Environment Variables.
6. Deploy the service and review the logs for startup errors.

The health-check endpoint responds at `/` and `/health`. This endpoint does not confirm that Telegram polling is functioning; check the Render logs as well.

## Notes

- The main bot and `force_join.py` must be connected through imports and calls for Force Join to run in the main bot.
- The bot needs administrator access to the required channels for membership checks.
- Keep bot tokens and other secrets out of source control.
