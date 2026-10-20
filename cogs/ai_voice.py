from transformers import pipeline

class VoiceAssistant:
    def __init__(self, personality="friendly"):
        self.generator = pipeline("text-generation", model="gpt2", device=-1)  # Runs on CPU
        self.personalities = {
            "friendly": "You are a cheerful and optimistic assistant.",
            "sarcastic": "You are a witty and sarcastic assistant.",
            "formal": "You are a professional and polite assistant."
        }
        self.personality = self.personalities.get(personality, "You are a neutral assistant.")

    def formulate_response(self, command):
        prompt = f"{self.personality} Respond to: '{command}'"
        try:
            responses = self.generator(prompt, max_length=50, num_return_sequences=1, temperature=0.7)
            return responses[0]["generated_text"].strip()
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "I'm having trouble coming up with a response."

    def process_command(self, command):
        response = self.formulate_response(command)
        print(f"Echo: {response}")    
