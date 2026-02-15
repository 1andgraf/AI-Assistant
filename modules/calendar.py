from ai_concierge.database.db import SessionLocal
from ai_concierge.database.models import Event
from datetime import datetime
import asyncio

class CalendarModule:
    def __init__(self, sheets_module=None):
        self.sheets = sheets_module

    async def handle_async(self, intent_data: dict, user_id: int):
        title = intent_data.get("title", "Untitled Event")
        time_str = intent_data.get("datetime", "Unknown time")
        
        event_date = datetime.utcnow()
        
        session = SessionLocal()
        try:
            new_event = Event(
                user_id=user_id,
                title=f"{title} ({time_str})", 
                start_time=event_date
            )
            session.add(new_event)
            session.commit()
            
            if self.sheets:
                data = {
                    "title": new_event.title,
                    "start_time": time_str,
                    "user_id": user_id
                }
                loop = asyncio.get_running_loop()
                loop.run_in_executor(None, self.sheets.append_event, data)

            return f"✅ Scheduled: **{title}** for {time_str}."
        except Exception as e:
            session.rollback()
            return f"❌ Failed to schedule event: {e}"
        finally:
            session.close()

    def handle(self, intent_data: dict, user_id: int):
        return "⚠️ Async required"
