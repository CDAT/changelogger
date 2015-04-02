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
        self.urls[instance] = value

class RemoteModel(object):

    data = AsyncRequest()

    def get_headers(self):
        return {}

    def __init__(self, url=None):
        self.data = url
        self.url = url

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
            for field in json:
                if field[-3:] == "url" and len(field) > 3 and field != "html_url":
                    print "Found URL field", json[field]
                    json[field[:-4]] = GithubModel(json[field], self.key, self.agent)
                    del json[field]

    def __init__(self, url=None, key=None, ua="Chaosphere2112GithubModelClient"):
        if key == None:
            key = github_key # let users provide the key to the whole module
        print url
        self.key = key
        self.agent = ua
        super(GithubModel, self).__init__(url=url)