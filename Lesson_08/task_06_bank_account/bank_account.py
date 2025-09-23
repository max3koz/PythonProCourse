class BankAccount:
    """
    Class for modeling a bank account.
    """

    def __init__(self):
        self._balance = 0.0

    def deposit(self, amount: float) -> None:
        """Replenishes the account with the specified amount."""
        if amount < 0:
            raise ValueError("The amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraws funds if there is sufficient balance."""
        if amount < 0:
            raise ValueError("The amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def get_balance(self) -> float:
        """Returns the current balance."""
        return self._balance
