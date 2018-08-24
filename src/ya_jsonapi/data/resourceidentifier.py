from ya_jsonapi.data.jsonobject import JsonObject


class ResourceIdentifier(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.id = None
        self.type = None
        self.meta = None

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.id = data["id"]
        self.type = data["type"]
        self.meta = data.get("meta", None)
        return self
