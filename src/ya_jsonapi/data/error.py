from ya_jsonapi.data.jsonobject import JsonObject
from ya_jsonapi.data.link import Link


class Error(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.id = None
        self.links = {}
        self.status = None
        self.code = None
        self.title = None
        self.detail = None
        self.source = None
        self.meta = None

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.id = data.get("id", None)
        self.links = {k: Link.from_json(v)
                      for k, v in data.get("links", {}).items()}
        self.status = data.get("status", None)
        self.code = data.get("code", None)
        self.title = data.get("title", None)
        self.detail = data.get("detail", None)
        self.source = data.get("source", None)
        self.meta = data.get("meta", None)
        return self    # TODO
