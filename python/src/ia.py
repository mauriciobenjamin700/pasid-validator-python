from decouple import config
from groq import Groq

GROQ_API_KEY = config("GROQ_API_KEY", default=None)

class IAService:
    
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        
    
    def ask(self, prompt: str) -> str:
        """
        Ask a question to the IA model and get the response.
        
        Args:
            prompt (str): The question to ask.
        
        Returns:
            str: The response from the IA model.
        """
        chat = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        return chat.choices[0].message.content.strip().replace('*', '')