from src.transaction import schema
from settings import settings
import hashlib


def validate(t: schema.Transaction):
    secret_key = settings.SECRET_KEY
    string_load = f"{t.account_id}{t.amount}{t.transaction_id}{t.user_id}{secret_key}"
    my_string_bits = string_load.encode("utf-8")
    secret_thing = hashlib.sha256(my_string_bits)
    signature = secret_thing.hexdigest()
    if signature == t.signature:
        return signature
