from ya_jsonapi.data.jsonobject import JsonObject
from ya_jsonapi.data.error import Error
from ya_jsonapi.data.jsonapi import Jsonapi
from ya_jsonapi.data.link import Link
from ya_jsonapi.data.resource import Resource
from ya_jsonapi.data.missing import MISSING
from ya_jsonapi.data.validate import validate

class Document(JsonObject):
    def __init__(self):
        JsonObject.__init__(self)
        self.data = MISSING
        self.errors = None
        self.meta = None
        self.jsonapi = None
        self.links = {}
        self.included = []

    @classmethod
    def from_json(cls, data):
        self = cls()

        if "data" in data:
            d = data["data"]
            if d is None:
                self.data = d
            elif isinstance(d, dict):
                self.data = Resource.self_or_id_from_json(d)
            else:
                self.data = [Resource.self_or_id_from_json(i) for i in d]
        if "errors" in data:
            self.errors = [Error.from_json(i) for i in data["errors"]]
        self.meta = data.get("meta", None)
        if "jsonapi" in data:
            self.jsonapi = Jsonapi.from_json(data["jsonapi"])
        if "links" in data:
            self.links = {k: Link.from_json(v)
                          for k, v in data["links"].items()}
        if "included" in data:
            self.included = [Resource.from_json(i) for i in data["included"]]

        return self

    @classmethod
    def from_response(cls, data):
        validate(data)
        return cls.from_json(data)
