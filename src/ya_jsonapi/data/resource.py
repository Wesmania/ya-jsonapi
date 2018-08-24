from ya_jsonapi.data.jsonobject import JsonObject


class Resource(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.id = None
        self.type = None

        self.attributes = {}
        self.relationships = {}
        self.links = {}
        self.meta = None

    @classmethod
    def from_json(cls, data):
        return cls()    # TODO

    def to_json(self):
        pass    # TODO
