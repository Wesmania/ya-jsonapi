from ya_jsonapi.data.jsonobject import JsonObject
from ya_jsonapi.data.link import Link
from ya_jsonapi.data.resourceidentifier import ResourceIdentifier
from ya_jsonapi.data.missing import MISSING


class Relationship(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.links = {}
        self.data = MISSING
        self.meta = None

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.links = {k: Link.from_json(v)
                      for k, v in data.get("links", {}).items()}
        self.meta = data.get("meta", None)
        if "data" in data:
            d = data["data"]
            if d is None:
                self.data = d
            elif isinstance(d, dict):
                self.data = ResourceIdentifier.from_json(d)
            else:
                self.data = [ResourceIdentifier.from_json(i) for i in d]
        return self
