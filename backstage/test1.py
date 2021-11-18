def is_sensitive_chat_security(wording_no):
    return wording_no >= 901000 and wording_no <= 901999


print(is_sensitive_chat_security(9020000))