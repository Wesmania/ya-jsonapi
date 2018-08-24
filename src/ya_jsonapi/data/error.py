from ya_jsonapi.data.jsonobject import JsonObject


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
        return cls()    # TODO

    def to_json(self):
        pass    # TODO
