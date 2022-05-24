import threading, requests, json, time

class APIProvider:

    api_providers = []
    delay = 0
    status = True

    def __init__(self, target, delay=0):
        PROVIDERS = json.load(open('apidata.json', 'r'))
        self.config = None
        self.target = target
        self.index = 0
        self.lock = threading.Lock()
        APIProvider.delay = delay
        providers = PROVIDERS.get("sms", {})
        APIProvider.api_providers = providers.get("multi", [])

    def format(self):
        config_dump = json.dumps(self.config)
        config_dump = config_dump.replace('{target}', self.target)
        self.config = json.loads(config_dump)
    
    def select_api(self):
        try:
            if len(APIProvider.api_providers) == 0:
                raise IndexError
            self.index += 1
            if self.index >= len(APIProvider.api_providers):
                self.index = 0
        except IndexError:
            self.index = -1
            return
        self.config = APIProvider.api_providers[self.index]
        perma_headers = {"User-Agent":
                         "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0)"
                         " Gecko/20100101 Firefox/72.0"}
        if "headers" in self.config:
            self.config["headers"].update(perma_headers)
        else:
            self.config["headers"] = perma_headers
        self.format()

    def remove(self):
        try:
            del APIProvider.api_providers[self.index]
            return True
        except Exception:
            return False
    
    def request(self):
        self.select_api()
        if not self.config:
            return None
        identifier = self.config.pop("identifier", "").lower()
        del self.config['name']
        self.config['timeout'] = 10
        response = requests.request(**self.config)
        return identifier in response.text.lower()
    
    def hit(self):
        try:
            if not APIProvider.status:
                return
            time.sleep(APIProvider.delay)
            self.lock.acquire()
            response = self.request()
            if response is False:
                self.remove()
            elif response is None:
                APIProvider.status = False
            return response
        except Exception as e:
            print(f"Error from Hit function\n{e}")
            response = False
        finally:
            self.lock.release()
            return response