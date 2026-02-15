from ai_concierge.database.db import SessionLocal
from ai_concierge.database.models import Event, Expense
from ai_concierge.brain.llm_client import LLMClient
import json
import re

class DeleteModule:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    async def handle_async(self, intent_data: dict, user_id: int):
        domain = intent_data.get("domain")
        target = intent_data.get("target", "").lower()
        
        session = SessionLocal()
        response = ""
        
        try:
            if domain == "calendar":
                if target == "all":
                    count = session.query(Event).filter(Event.user_id == user_id).delete()
                    session.commit()
                    return f"🗑️ Deleted ALL events ({count} removed)."
                
                candidates = session.query(Event).filter(Event.user_id == user_id).limit(20).all()
                if not candidates:
                    return "⚠️ No events found to delete."
                
                items_text = "\n".join([f"ID {e.id}: '{e.title}' at {e.start_time}" for e in candidates])
                
            elif domain == "budget":
                if target == "all":
                    count = session.query(Expense).filter(Expense.user_id == user_id).delete()
                    session.commit()
                    return f"🗑️ Deleted ALL expenses ({count} removed)."
                
                candidates = session.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.id.desc()).limit(20).all()
                if not candidates:
                    return "⚠️ No expenses found to delete."
                    
                items_text = "\n".join([f"ID {e.id}: ${e.amount} for '{e.category}' ({e.description}) on {e.date}" for e in candidates])
            
            else:
                 return "❓ I can only delete from 'calendar' or 'budget' right now."

            prompt = f"""
            The user wants to delete an item described as: "{target}"
            
            Here are the available items in the database:
            {items_text}
            
            Determine which ID matches the user's description best.
            - If "delete event at 3rd of feb", look for date/time match.
            - If "delete food", look for category/description match.
            - If multiple match, pick the most likely or the precise one.
            - If NONE match, return ID: 0.
            
            Return ONLY a valid JSON object: {{ "id": <number> }}
            """

            llm_response = await self.llm.generate_response(prompt)
            cleaned = re.sub(r'```json\s*|\s*```', '', llm_response).strip()
            decision = json.loads(cleaned)
            target_id = decision.get("id")
            
            if target_id and target_id > 0:
                if domain == "calendar":
                    item = session.query(Event).get(target_id)
                    title = item.title if item else "Unknown"
                else:
                    item = session.query(Expense).get(target_id)
                    title = f"${item.amount} ({item.category})" if item else "Unknown"

                if item:
                    session.delete(item)
                    session.commit()
                    response = f"🗑️ Deleted: **{title}**"
                else:
                    response = "⚠️ Item ID found by Brain but not in DB (weird)."
            else:
                response = f"🤷‍♂️ I couldn't find an item matching '{target}' to delete."

        except Exception as e:
            session.rollback()
            response = f"❌ Error deleting data: {e}"
        finally:
            session.close()
            
        return response

    def handle(self, intent_data: dict, user_id: int):
         return "⚠️ Async handler required"
