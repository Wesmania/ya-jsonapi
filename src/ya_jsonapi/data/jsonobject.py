class JsonObject:
    @classmethod
    def from_json(cls, data):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError
