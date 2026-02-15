from ai_concierge.database.db import SessionLocal
from ai_concierge.database.models import Event, Expense, CartItem
from ai_concierge.brain.llm_client import LLMClient
from datetime import datetime

class QueryModule:
    def __init__(self, llm_client):
        self.llm = llm_client

    async def handle_async(self, intent_data: dict, user_id: int):
        domain = intent_data.get("domain", "general")
        session = SessionLocal()
        context_data = ""
        
        try:
            if domain == "calendar":
                events = session.query(Event).filter(Event.user_id == user_id).order_by(Event.start_time).limit(10).all()
                if not events:
                    context_data = "No upcoming events found."
                else:
                    context_data = "Upcoming Events:\n" + "\n".join(
                        [f"- {e.title} at {e.start_time}" for e in events]
                    )
                    
            elif domain == "budget":
                expenses = session.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.date.desc()).limit(10).all()
                if not expenses:
                    context_data = "No recent expenses found."
                else:
                    context_data = "Recent Expenses:\n" + "\n".join(
                        [f"- ${e.amount} on {e.category} ({e.description})" for e in expenses]
                    )
            
            elif domain == "cart":
                items = session.query(CartItem).filter(CartItem.user_id == user_id, CartItem.is_bought == 0).all()
                if not items:
                    context_data = "Cart is empty."
                else:
                    context_data = "Shopping List:\n" + "\n".join([f"- {i.item_name}" for i in items])
                    
            else:
                 context_data = "No specific data requested."

        except Exception as e:
            context_data = f"Error fetching data: {e}"
        finally:
            session.close()

        prompt = f"""
        The user asked a question about their {domain}.
        
        Here is the DATABASE DATA:
        {context_data}
        
        Please answer the user's implicit question specifically based on this data.
        If the data is empty, say so.
        """
        
        response = await self.llm.generate_response(prompt)
        return response

    def handle(self, intent_data: dict, user_id: int):
        return "⚠️ Async handler required"
