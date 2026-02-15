from ai_concierge.database.db import SessionLocal
from ai_concierge.database.models import Expense
from datetime import datetime
import asyncio

class BudgetModule:
    def __init__(self, sheets_module=None):
        self.sheets = sheets_module

    async def handle_async(self, intent_data: dict, user_id: int):
        amount = intent_data.get("amount", 0)
        category = intent_data.get("category", "General")
        description = intent_data.get("description", "")
        
        session = SessionLocal()
        try:
            new_expense = Expense(
                user_id=user_id,
                amount=float(amount),
                category=category,
                description=description
            )
            session.add(new_expense)
            session.commit()

            if self.sheets:
                data = {
                    "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "amount": amount,
                    "category": category,
                    "description": description,
                    "user_id": user_id
                }
                loop = asyncio.get_running_loop()
                loop.run_in_executor(None, self.sheets.append_expense, data)

            return f"💸 Logged expense: **${amount}** for {category} ({description})."
        except Exception as e:
            session.rollback()
            return f"❌ Failed to log expense: {e}"
        finally:
            session.close()

    def handle(self, intent_data: dict, user_id: int):
        return "⚠️ Async required"
