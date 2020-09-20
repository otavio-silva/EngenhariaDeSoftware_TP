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

    def __init__(self, text, origin : MessageOrigin, msg_id=None):
        self.text = text
        self.origin = origin
        self.persisted = False
        self.id = msg_id
    
    def set_message_id(self, msg_id):
        self.id = int(msg_id)

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
        return str(self.origin.value) + "," + self.text + "," + str(self.id)

    def from_csv_line(self,line):
        s=line.split(",")
        return Message(s[1],self.origin.from_value(int(s[0])),int(s[2]))