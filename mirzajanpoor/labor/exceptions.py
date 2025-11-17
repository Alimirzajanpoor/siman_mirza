# labor/exceptions.py
from rest_framework.exceptions import APIException


class InsufficientBalanceError(APIException):
    status_code = 400
    default_detail = "Insufficient wallet balance."
    default_code = "insufficient_balance"


class InvalidTransactionError(APIException):
    status_code = 400
    default_detail = "Invalid transaction type or amount."
    default_code = "invalid_transaction"


class WalletAlreadyExistsError(APIException):
    status_code = 400
    default_detail = "Wallet already exists for this labor"
    default_code = "Wallet already exists"



# Optional: Generic domain error
class DomainError(APIException):
    status_code = 400
    default_detail = "A domain error occurred."
    default_code = "domain_error"
