from enum import Enum
class MessageOrigin(Enum):
    SENT = 1
    RECEIVED = 2

class Message :

    def __init__(self, message, origin : MessageOrigin):
        self.message = message
        self.origin = origin


    def getFormattedText(self, max_chars=25):
        count = 0
        formatted_msg = ""
        for word in message.split():
            count += len(word)
            formatted_msg += " " + word
            if count > max_chars :
                formatted_msg += "\n"
                count=0
        return formatted_msg