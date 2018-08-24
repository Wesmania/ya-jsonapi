from ya_jsonapi.data.jsonobject import JsonObject


class Jsonapi(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.version = None
        self.meta = None

    @classmethod
    def from_json(cls, data):
        return cls()    # TODO

    def to_json(self):
        pass    # TODO
