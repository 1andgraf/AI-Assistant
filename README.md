# AI Assistant Telegram Bot

My version of OpenClawd-like personal assistant bot built with Python. You can chat with it in Telegram.

---
<img width="536" height="402" alt="Screenshot 2026-02-15 at 16 11 16" src="https://github.com/user-attachments/assets/b41d14e6-203c-427d-987b-eb4b86d10fec" />  
<img width="883" height="306" alt="Screenshot 2026-02-15 at 16 07 47" src="https://github.com/user-attachments/assets/e7abb999-600b-42f5-aa18-472150f21b03" />  
<img width="648" height="283" alt="Screenshot 2026-02-15 at 16 09 23" src="https://github.com/user-attachments/assets/e54c10d6-8cf4-48e4-b21d-3ac4a32441de" />

## Features

- **Calendar**: Ask bot to schedule and manage your events.
- **Budget Tracking**: Ask bot to log your expenses and categorize them.
- **Google Sheets**: Bot saves your events and expences to Google Sheets.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/1andgraf/AI-Assistant.git
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

5. Run the bot:
   ```bash
   python main.py
   ```
