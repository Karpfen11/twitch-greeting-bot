import socket, ssl, json
#twitch greeting bot

#building a socket which can connect to the irc chat server from twitch with the modules: socket and ssl
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc = ssl.wrap_socket(socket)
ip, port = "irc.chat.twitch.tv", 6697
irc.connect((ip, port))

#define a chat_user list to check if users are not in the list and greet them.
chat_user = []

#load the json config file to get the username, oauth token and channel
file = r"C:\Users\PC\Desktop\fiverr\config.json"
with open(file, "r") as f:
    data = json.load(f)

#define vars. from the data of the config
name = data["username"]
channel = data["channel"]
token = data["token"]


class bot:
    #send method to send messages to the irc server not the chat
    def send(self, irc, message):
        irc.send(bytes(f"{message}\r\n", "utf8"))

    #this method is just for sending messages in the twitch chat
    def send_chat(self, irc, message):
        self.send(irc, f"PRIVMSG #{channel} :{message}")

    #method to handle the chat messages and to something
    def commands(self, irc, message):
        args = [str(message[i]) for i in range(len(message)) if i > 2] #list comp to get the args of the chat message
        args[0] = args[0].replace(":", "")

        user = message[0].split("!")[0].replace(":", "")
        if user not in chat_user:
            chat_user.append(user)
            self.send_chat(irc, f"Welcome to the stream @{user}")

    #method to start the twitch bot
    def start(self):
        self.send(irc, f"PASS {token}")
        self.send(irc, f"NICK {name}")
        self.send(irc, f"JOIN #{channel}")

        while True:
            data = irc.recv(1024).decode("utf8")
            message = data.split()
            if message[1] == "PRIVMSG":
                self.commands(irc, message)
            for line in data.splitlines():
                if line == "PING :tmi.twitch.tv":
                    self.send(irc, "PONG")
                print(line)

#define a instance of the bot class to start the bot
Bot = bot()
if __name__ == "__main__":
    Bot.start()
