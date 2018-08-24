from ya_jsonapi.data.jsonobject import JsonObject
from ya_jsonapi.data.resourceidentifier import ResourceIdentifier
from ya_jsonapi.data.relationship import Relationship
from ya_jsonapi.data.link import Link


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
        self = cls()
        self.id = data["id"]
        self.type = data["type"]
        self.attributes = data.get("attributes", {})
        self.relationships = {
            k: Relationship.from_json(v)
            for k, v in data.get("relationships", {}).items()
        }
        self.links = {k: Link.from_json(v)
                      for k, v in data.get("links", {}).items()}
        self.meta = data.get("meta", None)
        return self

    # Data can be interpreted both as objects and as identifiers, and this is
    # a reasonable way to tell the difference between the two.
    @classmethod
    def self_or_id_from_json(cls, data):
        if any(key in data for key in
               ["attributes", "relationships", "links"]):
            return cls.from_json(data)
        else:
            return ResourceIdentifier.from_json(data)
