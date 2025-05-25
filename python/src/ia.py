from ollama import ChatResponse, Client

class IAService:
    
    def __init__(self):
        self.models = {
            "llama3.2": "llama3.2",
            "deep-seek": "DeepSeek-R1"
        }
        self.model = self.models["llama3.2"]  # Default model
        self.client = Client(
            host="http://ollama:11434"
        )
        
    
    def ask(self, prompt: str) -> str:
        """
        Ask a question to the IA model and get the response.
        
        Args:
            prompt (str): The question to ask.
        
        Returns:
            str: The response from the IA model.
        """
        ia_response:ChatResponse = self.client.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        
        return ia_response.message.content