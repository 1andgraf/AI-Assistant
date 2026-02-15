import json
import re
from ai_concierge.brain.llm_client import LLMClient

class IntentParser:
    def __init__(self):
        self.llm = LLMClient()

    async def parse(self, user_text: str) -> dict:
        """
        Analyzes user text and returns a JSON dictionary with the intent and parameters.
        """
        prompt = f"""
        You are the Brain of an AI Concierge.
        Your job is to classify the USER INPUT into a valid JSON object representing the user's intent.

        USER INPUT: "{user_text}"

        AVAILABLE INTENTS:
        1. schedule_event
           - title (string)
           - datetime (string)
        2. log_expense
           - amount (number)
           - category (string)
           - description (string)
        3. shopping_cart
           - action (string): "add", "list", "clear", "remove"
           - item (string): item name if adding or removing
        4. generate_plan
           - topic (string): "nutrition" or "training"
           - goal (string): user's stated goal
        5. get_route
           - origin (string, optional)
           - destination (string)
        6. practice_language
           - language (string): target language
           - text (string): the user's input text to correct/reply to
        7. query_data
           - domain (string): "calendar", "budget", "cart", or "general"
        8. delete_data
           - domain (string): "calendar", "budget"
           - target (string): description of what to delete or "all" to clear everything
        9. chat
           - response (string): generic response

        RULES:
        - Output ONLY valid JSON.
        - If the intent is unclear, default to "chat".
        
        EXAMPLE INPUT: "What do I have tomorrow?"
        EXAMPLE OUTPUT: {{ "intent": "query_data", "domain": "calendar" }}
        
        EXAMPLE INPUT: "Delete all expenses"
        EXAMPLE OUTPUT: {{ "intent": "delete_data", "domain": "budget", "target": "all" }}

        Now, generate the JSON for the USER INPUT.
        """

        raw_response = await self.llm.generate_response(prompt)
        print(f"Raw LLM Response: {raw_response}") # Debugging

        try:
            # Clean up potential markdown formatting
            cleaned_response = re.sub(r'```json\s*|\s*```', '', raw_response).strip()
            data = json.loads(cleaned_response)
            return data
        except json.JSONDecodeError:
             print("Failed to decode JSON from LLM.")
             return {"intent": "chat", "response": raw_response}

if __name__ == "__main__":
    import asyncio
    async def test():
        parser = IntentParser()
        print("Testing Intent Parser...")
        # res = await parser.parse("Buy milk for 5 dollars")
        # print(res)
        res = await parser.parse("Meeting with team next Friday at 10am")
        print(res)

    asyncio.run(test())
