import requests

class AsyncRequest(object):
    def __init__(self, retrieved=None):
        self.json = {}
        self.urls = {}
        self.retrieved = retrieved

    def get_url(self, url, headers):
        if url not in self.json:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.cache(url, response.json())
            else:
                raise Exception("Unable to reach %s" % url)
        return self.json[url]

    def cache(self, url, json):
        self.json[url] = json

    def __get__(self, instance, owner):
        url = self.urls[instance]
        json = self.get_url(url, headers=instance.get_headers())
        
        # allow the owner object to do operations on the JSON object
        try:
            instance.parse(json, self.cache)
        except AttributeError:
            pass

        self.cache(url, json)
        return json

    def __set__(self, instance, value):
        if value is None:
            self.urls[instance] = value
            return
        try:
            evaluated = type(instance).validate_url(value)
            if evaluated:
                self.urls[instance] = evaluated
            else:
                raise ValueError("URL %s does not comply to API for %s" % (value, str(type(instance))))
        except AttributeError:
            self.urls[instance] = value

class RemoteModel(object):

    data = AsyncRequest()

    def get_headers(self):
        return {}

    def __init__(self, url=None):
        self.data = url
        self._url = url

    
    def __geturl(self):
        return self._url

    def __seturl(self, value):
        self._url = value
        self.data = value

    url = property(__geturl, __seturl)

    def __dir__(self):
        directory = ["data"]
        if self.data:
            directory.extend(self.data.json().keys())

    def __getitem__(self, key):
        if self.data:
            return self.data[key]

    def __iter__(self):
        if self.data:
            return iter(self.data)

    def __len__(self):
        if self.data:
            return len(self.data)

github_key = None
github_api_url = "api.github.com"

class GithubModel(RemoteModel):
    def get_headers(self):
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": self.agent
        }

        if self.key is not None:
            headers["Authorization"] = "token %s" % self.key

        return headers

    def parse(self, json, cache):
        if type(json) == type([]):
            for obj in json:
                if "url" in obj:
                    cache(obj["url"], obj)
                self.parse(obj, cache)
        else:
            # it's a dict
            to_remove = {}
            for field in json:
                if "url" in field and json[field] is not None and GithubModel.validate_url(json[field]):
                    to_remove[field] = GithubModel(url=json[field], key=self.key, ua=self.agent)
                else:
                    if type(json[field]) in (list, dict):
                        self.parse(json[field], cache)
            for field in to_remove:
                del json[field]
                json[field[:-4]] = to_remove[field]

    @staticmethod
    def validate_url(url):
        if "://" not in url:
            protocol = "https"
        else:
            protocol, url = url.split("://")

        if "{/" in url:
            url = url[:url.index("{/")]

        url_parts = url.split("/")

        if url_parts[0]:
            if url_parts[0] != github_api_url:
                return False

        url_parts = url_parts[1:]

        return "{protocol}://{domain}/{path}".format(protocol=protocol, domain=github_api_url, path="/".join(url_parts))

    def __init__(self, url=None, key=None, ua="Chaosphere2112GithubModelClient"):
        if key == None:
            key = github_key # let users provide the key to the whole module
        self.key = key
        self.agent = ua
        super(GithubModel, self).__init__(url=url)
