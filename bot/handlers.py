from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from ai_concierge.brain.intent_parser import IntentParser
from ai_concierge.modules.calendar import CalendarModule
from ai_concierge.modules.budget import BudgetModule
from ai_concierge.modules.query import QueryModule
from ai_concierge.modules.delete import DeleteModule
from ai_concierge.modules.sheets import SheetsModule
from ai_concierge.database.models import User
from ai_concierge.database.db import SessionLocal
from ai_concierge.brain.llm_client import LLMClient

router = Router()

llm_client = LLMClient()
sheets_module = SheetsModule()

intent_parser = IntentParser()
calendar_module = CalendarModule(sheets_module)
budget_module = BudgetModule(sheets_module)
query_module = QueryModule(llm_client)
delete_module = DeleteModule(llm_client)

@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    session = SessionLocal()
    
    db_user = session.query(User).filter(User.telegram_id == user.id).first()
    if not db_user:
        db_user = User(telegram_id=user.id, username=user.username, full_name=user.full_name)
        session.add(db_user)
        session.commit()
    session.close()

    await message.answer(f"Hello {user.first_name}! I am your AI Concierge. I can help with:\n- Calendar & Budget Tracking\n- Syncing data to Google Sheets\n- Querying and Deleting your data")

@router.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    try:
        parsed_data = await intent_parser.parse(user_text)
        intent = parsed_data.get("intent")
        print(f"User: {user_text} -> Intent: {intent}")
    except Exception as e:
        await message.answer(f"⚠️ Brain error: {e}")
        return

    response_text = ""
    
    if intent == "schedule_event":
        response_text = await calendar_module.handle_async(parsed_data, user_id)
    elif intent == "log_expense":
        response_text = await budget_module.handle_async(parsed_data, user_id)
    elif intent == "delete_data":
        await message.answer("🤔 Identifying item to delete...")
        response_text = await delete_module.handle_async(parsed_data, user_id)
    elif intent == "query_data":
        await message.answer("🔍 Checking your data...")
        response_text = await query_module.handle_async(parsed_data, user_id)
    elif intent == "chat":
        response_text = parsed_data.get("response", "I'm not sure what to say.")
    else:
        response_text = "🤷‍♂️ I didn't understand that intent."
    await message.answer(response_text)
