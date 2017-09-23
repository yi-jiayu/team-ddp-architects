message_types = {"NEW", "PRICE", "QUANTITY", "CANCEL", "SOD", "EOD"}


def validate(message):
    if message['messageId'] < 0:
        return False

    message_type = message['messageType']
    if message_type not in message_types:
        return False

    if message_type == 'SOD':
        return validate_sod(message)
    elif message_type == 'NEW':
        return validate_new(message)
    elif message_type == 'QUANTITY':
        return validate_quantity(message)
    elif message_type == 'PRICE':
        return validate_price(message)
    elif message_type == 'CANCEL':
        return validate_cancel(message)


def validate_sod(message):
    
    pass


def validate_new(message):
    pass


def validate_quantity(message):
    pass


def validate_price(message):
    pass


def validate_cancel(message):
    pass
