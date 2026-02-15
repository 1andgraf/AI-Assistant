# AI Concierge Telegram Bot

A personal assistant bot built with Python and Aiogram, featuring calendar management, budget tracking, and Google Sheets synchronization.

## Features

- **📅 Calendar Management**: Schedule and manage your events easily through natural language.
- **💸 Budget Tracking**: Log your expenses and categorize them on the go.
- **📊 Google Sheets Sync**: Automatically back up your events and expenses to a Google Sheet.
- **🔍 Data Query & Deletion**: Query your logged data or delete specific items using AI-powered natural language processing.
- **🧠 AI Powered**: Uses a Large Language Model (LLM) to parse intents and understand your requests.

## Prerequisites

- Python 3.9+
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Google Cloud Service Account credentials (for Google Sheets sync)

## Installation

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd ai-concierge
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file in the root directory:

   ```env
   BOT_TOKEN=your_telegram_bot_token
   GOOGLE_CREDENTIALS_FILE=google_credentials.json
   SHEET_URL=your_google_sheet_url
   LLM_API_KEY=your_llm_api_key
   ```

4. Place your Google Service Account JSON file in the root directory as `google_credentials.json`.

## Usage

Run the bot:

```bash
python main.py
```

## Repository Structure

- `main.py`: Entry point for the bot.
- `bot/`: Contains telegram handlers and keyboards.
- `modules/`: Core functionality modules (Calendar, Budget, Query, Delete, Sheets).
- `database/`: Database models and initialization (SQLite/SQLAlchemy).
- `brain/`: AI logic for intent parsing and LLM interaction.

## Contributing

Feel free to open issues or submit pull requests.

## License

MIT
