import g4f
import asyncio
from g4f.client import Client, AsyncClient

class LLMClient:
    def __init__(self):
        # We let g4f auto-select the best working provider by not specifying one
        self.client = AsyncClient()

    async def generate_response(self, prompt: str) -> str:
        """
        Generates a response from the LLM based on the prompt.
        """
        try:
            # Using GPT-4 model identifier, g4f will find a provider that supports it
            response = await self.client.chat.completions.create(
                model="gpt-4", 
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return str(e)

if __name__ == "__main__":
    # Simple test
    async def test():
        llm = LLMClient()
        print("Testing LLM Client (Auto-Provider)...")
        response = await llm.generate_response("Hello, are you working? Reply with 'Yes'.")
        print(f"Response: {response}")

    asyncio.run(test())
