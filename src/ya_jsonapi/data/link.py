from ya_jsonapi.data.jsonobject import JsonObject


class Link(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.href = None
        self.meta = None

    @classmethod
    def from_json(cls, data):
        self = cls()
        if isinstance(data, str):
            self.href = data
        else:
            self.href = data.get("href", None)
            self.meta = data.get("meta", None)
        return self
