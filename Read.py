import string

def getUser(line):
        if ":" in line and "!" in line:
        	separate = line.split(":", 2)
        	user = separate[1].split("!", 1)[0]
        	return user
        return ""

def getMessage(line):
        if ":" in line:
                separate = line.split(":", 2)
                if len(separate) > 2:
                        message = separate[2]
                        return message
        return ""
