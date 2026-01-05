import asyncio
import os
import random
from dotenv import load_dotenv

# Import ALL three agents
# CHANGE THIS: Use the full path "agents_core.plugins..."
from agents_core.plugins.artifact_scanner import ArtifactScanner
from agents_core.plugins.finance_verifier import FinanceVerifier
from agents_core.plugins.challenge_bot import ChallengeBot

load_dotenv()

class DefenseOrchestrator:
    def __init__(self):
        print("\n🤖 SYSTEM INITIALIZING: VeriShield AI Agentic Core")
        
        self.vision_agent = ArtifactScanner()
        self.finance_agent = FinanceVerifier()
        self.challenge_agent = ChallengeBot()  # <--- NEW AGENT
        
        print("✅ Core Active: All Systems Online.")

    # UPDATE THIS METHOD
    async def analyze_transaction(self, user_id, amount, image_path=None):
        print(f"\n🔎 AGENT ACTIVE: Processing request for {user_id} (${amount})...")
        
        # 1. FINANCE CHECK
        finance_result = self.finance_agent.analyze_transaction(user_id, amount)
        if finance_result['status'] != "SAFE":
            return self.trigger_lockdown(finance_result['reason'])

        # 2. VISUAL CHECK (Now using the real image path)
        if image_path:
            # We pass the real file path to the scanner
            scan_result = self.vision_agent.scan_video_feed(image_path)
            
            if scan_result['status'] == "THREAT_DETECTED":
                return self.trigger_lockdown(scan_result['reason'])
        
        return "✅ APPROVED: Identity Verified & Human Confirmed."

    def trigger_lockdown(self, reason):
        print(f"🚨 SECURITY ALERT: {reason}")
        return "❌ BLOCKED: Transaction Terminated."

if __name__ == "__main__":
    brain = DefenseOrchestrator()
    
    # Run a test loop to see if it catches a "Fake" user who fails the challenge
    for i in range(1, 4):
        print(f"\n--- Attempt #{i} ---")
        asyncio.run(brain.analyze_transaction(f"User_{i}", 500))