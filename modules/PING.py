class PingModule:

    ALLOW = ['PING1']

    def process_message(self, key, text, storage):
        print("PING")
        return "PONG"