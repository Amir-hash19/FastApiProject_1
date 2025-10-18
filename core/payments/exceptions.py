
class NotFoundErrorException(Exception):
    def __init__(self, payment_id: int):
        self.payment_id = payment_id
        self.message = f"payment with ID {self.payment_id} not found"
        super().__init__(self.message)
        