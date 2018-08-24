from ya_jsonapi.data.jsonobject import JsonObject


class Document(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.data = None
        self.errors = None
        self.meta = None
        self.jsonapi = None
        self.links = {}
        self.included = []

    @classmethod
    def from_json(cls, data):
        return cls()    # TODO

    def to_json(self):
        pass    # TODO
