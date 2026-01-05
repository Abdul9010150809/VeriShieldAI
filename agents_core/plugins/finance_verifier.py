class FinanceVerifier:
    def __init__(self):
        print("💰 FINANCE AUDIT: Banking Patterns Loaded.")
        # In a real app, this would connect to a Bank API or SQL Database
        self.risk_threshold = 10000  # Any transaction over $10k is suspicious

    def analyze_transaction(self, user_id, amount):
        print(f"   [Finance] Auditing transaction for ${amount}...")
        
        # Rule 1: Limit Check
        if amount > self.risk_threshold:
            return {
                "status": "HIGH_RISK",
                "reason": f"Amount ${amount} exceeds safety limit of ${self.risk_threshold}."
            }
        
        # Rule 2: Anomaly Check (Simulated)
        # We assume amounts ending in '999' are suspicious bots
        if str(amount).endswith("999"):
            return {
                "status": "SUSPICIOUS",
                "reason": "Bot-like transfer pattern detected."
            }

        return {
            "status": "SAFE",
            "reason": "Transaction is within normal limits."
        }