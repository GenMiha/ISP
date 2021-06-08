from main import message_react

def test_bot_starts(message):
    message.text = '/start'
    print(message)
    handler = process_message(message)
    assert handler == message_react.handle_message


def get_message_handler(message):
    for handler in message_react.message_handlers:
        if message_react._test_message_handler(handler, message):
            return handler
    return None


def process_message(message):
    handler = get_message_handler(message)
    try:
        handler['function'](message)
    except ValueError:
        pass
    return handler['function']