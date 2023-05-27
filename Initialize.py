import time


def joinRoom(s, expectedUser):
    readbuffer = ""
    start = time.time()
    while time.time() - start < 5:
        readbuffer = readbuffer + s.recv_timeout()
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()
        for line in temp:
            # print(line)
            if "Login authentication failed" in line:
                return 4

            if "Improperly formatted auth" in line:
                return 3

            if expectedUser.lower() not in line.lower():
                s.close()
                return 1

            if "failed" in line:
                return 99

            if ":End of /NAMES list" in line:
                # s.sendMessage("I'm here! I'm calu's bot :3")
                return 0
    return 2
