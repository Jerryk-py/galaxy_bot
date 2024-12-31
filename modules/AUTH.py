import hashlib

class AuthModule():
    ALLOW = ['HAAAPSI','DOMAINS', '999','REGISTER', '452', '900', "471"]

    def dechaaaspi(self, haaas):
        h = hashlib.md5(str.encode(haaas))
        p = h.hexdigest()
        text = p [::-1]
        WithZero = '0'.join(text)
        fan = WithZero[5:15]
        return fan
    


    def process_message(self, key, text, storage, services):
        print(f" Key: {key} | {text}")
        if key == "HAAAPSI":
            storage.set(key, text[0])

            return "RECOVER " + storage.get("kod")
            
        elif key == "DOMAINS":
            pass
        elif key == "999":
            for service_name, service_instance in services.items():
                if service_name == "PlanetsRotator":
                    pl = service_instance.next()
            print(pl)
            return ["FWLISTVER 311","ADDONS 251778 1","MYADDONS 251778 1","PHONE 1920 1080 0 2 :chrome 131.0.0.0",f"JOIN {pl}"]
        elif key == "900":
            print(f"На планете {text[0]} ")

        
        
        
        elif key == "REGISTER":
            storage.set("UserId", text[0])
            storage.set("UserPass", text[1])
            storage.set("UserName", text[2])

            dec = self.dechaaaspi(storage.get("HAAAPSI"))

            return "USER " + storage.get("UserId") + " " + storage.get("UserPass")  + " " + storage.get("UserName") + " " + dec 

        elif key == "452":
            print("Пользователь в сети")


    
