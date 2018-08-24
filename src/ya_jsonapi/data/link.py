from ya_jsonapi.data.jsonobject import JsonObject


class Link(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.href = None
        self.meta = None

    @classmethod
    def from_json(cls, data):
        return cls()    # TODO

    def to_json(self):
        pass    # TODO
