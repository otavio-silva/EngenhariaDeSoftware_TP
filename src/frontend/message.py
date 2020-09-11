
def formatToDisplayV2(message, max_chars=25):
    split = message.split()
    count = 0
    line = ""
    for word in split:
        count += len(word)
        line += " " + word
        if count > max_chars :
            line += "\n"
            count=0
    return line