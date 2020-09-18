from enum import Enum

class MessageOrigin(Enum):
    SENT = 1
    RECEIVED = 2

    def from_value(self,value):
        if value == 1 : 
            return self.SENT
        else: 
            return self.RECEIVED

class Message :

    def __init__(self, text, origin : MessageOrigin):
        self.text = text
        self.origin = origin
        self.persisted = False

    def format_to_display(self, max_chars=25):
        count = 0
        formatted_msg = ""
        for word in self.text.split():
            count += len(word)
            formatted_msg += " " + word
            if count > max_chars :
                formatted_msg += "\n"
                count=0
        return formatted_msg

    def set_as_persisted(self):
        self.persisted = True

    def to_csv_line(self) :
        return str(self.origin.value) + "," + self.text

    def from_csv_line(self,line):
        s=line.split(",")
        return Message(s[1],self.origin.from_value(s[0]))