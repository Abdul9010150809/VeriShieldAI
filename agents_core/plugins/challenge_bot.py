import random

class ChallengeBot:
    def __init__(self):
        print("🗣️ CHALLENGE BOT: Active Defense Layer Initialized.")
        self.challenges = [
            "Turn head LEFT",
            "Turn head RIGHT",
            "Blink THREE times",
            "Smile",
            "Look UP"
        ]

    def generate_challenge(self):
        """
        Selects a random action for the user to perform.
        """
        selected_challenge = random.choice(self.challenges)
        print(f"   [Challenge] ISSUED COMMAND: '{selected_challenge}'")
        return selected_challenge

    def verify_response(self, challenge, user_action):
        """
        Compares what the user did vs. what was asked.
        In a real app, 'user_action' comes from the Vision AI detecting movement.
        """
        print(f"   [Challenge] Analyzing User Movement: '{user_action}'...")
        
        if challenge == user_action:
            return True
        else:
            return False