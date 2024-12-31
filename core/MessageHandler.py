import importlib, pathlib
from core.Storage import Storage
import configparser
import sys,os
class MessageHandler:

    def __init__(self):
        self.modules = {}
        self.storage = Storage()
        self.required_modules = ["PING", "AUTH"]
        self.DENY = ['PART','ACTION','VIEW_SCRIPT','OP','864','SLEEP','850',':auto','880','WEATHER','866','869','ADD_VIEW',':del','854','CHQ','EVENT','870','858','860','332','FOUNDER' ,'366','353','855','884','CURRENT_VERSION', 'ADDON_TAG','881','FO','REMOVE','JOIN','T','863']
        self.services = {}

        self.storage.set("InitCheck",1)
        self.storage.set("COUNT",0)


    
    def res_path(self,rel_path):
        try: 
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, rel_path)

    def load_modules(self):
        modules_path = pathlib.Path(self.res_path("modules"))
        for module_file in modules_path.glob("*.py"):
            module_name = module_file.stem
            module = importlib.import_module(f"modules.{module_name}")
            module_instance = getattr(module, f"{module_name.capitalize()}Module")()

            # Проверка типов пакетов, которые обрабатывает модуль
            if hasattr(module_instance, 'ALLOW') and isinstance(module_instance.ALLOW, list):
                    self.modules[module_name] = module_instance
                    print(f"Загружен модуль: {module_name}")
            else:
                print(f"В модуле {module_name} отсутствует или некорректно задана переменная ALLOW.")

        if not self.modules:
            print("Отсутствуют модули")
            sys.exit()

        for required_module in self.required_modules:
            if required_module not in self.modules:
                print(f"Необходимый модуль '{required_module}' не найден.")
                sys.exit()

    def load_services(self, planets):
        services_path = pathlib.Path(self.res_path("services"))
        for service_file in services_path.glob("*.py"):
            service_name = service_file.stem
            service = importlib.import_module(f"services.{service_name}")
            service_instance = getattr(service, f"{service_name.capitalize()}Service")()

           
            self.services[service_name] = service_instance
            print(f"Загружен сервис: {service_name}")
        
        for service_name, service_instance in self.services.items():
                if service_name == "PlanetsRotator":
                    service_instance.add(planets)
                    
                    print(f"Планет загружено {service_instance.count()}")

        if not self.services:
            print("Отсутствуют сервисы")




    def load_config(self, config):
        for key in config:
            self.storage.set(key, config[key])
            print(f"Загружено из конфига: {key} = {config[key]}")


        

    def handle_message(self, message):
        
        parts = message.split()
        if parts:
            message_type = parts[0]
            for module_name, module_instance in self.modules.items():
                if hasattr(module_instance, 'ALLOW') and message_type in module_instance.ALLOW:
                    
                    return module_instance.process_message(message_type, parts[1:], self.storage, self.services)
                   
            else:
                if message_type not in self.DENY:

                    pass
                    #print(f"Не найден модуль для обработки типа сообщения: {message_type} |  {parts[1:]}")
