# TODO:
# - member names. Probably too inconvenient to validate via jsonschema,
#   for now we accept everything.
# - Common namespace for fields, relationships, type and id. Again, not
#   convenient to do in jsonschema, so we'll just consistently prefer some
#   over others.
# - "relationships" and "links" items in fields are forbidden, but we don't
#   bother with recursive checking. Perhaps we'll have to treat them
#   differently in future specs.
# - No separate validation for single / multiple resource
#
# Maybe we'll give an IValidator to jsonschema.validate to implement the things
# above.
import jsonschema
import json


__all__ = ["validate"]


# As provided by jsonapi.org/schema
SCHEMA = json.loads(r"""
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "JSON API Schema",
  "description": "This is a schema for responses in the JSON API format. For more, see http://jsonapi.org",
  "oneOf": [
    {
      "$ref": "#/definitions/success"
    },
    {
      "$ref": "#/definitions/failure"
    },
    {
      "$ref": "#/definitions/info"
    }
  ],
  
  "definitions": {
    "success": {
      "type": "object",
      "required": [
        "data"
      ],
      "properties": {
        "data": {
          "$ref": "#/definitions/data"
        },
        "included": {
          "description": "To reduce the number of HTTP requests, servers **MAY** allow responses that include related resources along with the requested primary resources. Such responses are called \"compound documents\".",
          "type": "array",
          "items": {
            "$ref": "#/definitions/resource"
          },
          "uniqueItems": true
        },
        "meta": {
          "$ref": "#/definitions/meta"
        },
        "links": {
          "description": "Link members related to the primary data.",
          "allOf": [
            {
              "$ref": "#/definitions/links"
            },
            {
              "$ref": "#/definitions/pagination"
            }
          ]
        },
        "jsonapi": {
          "$ref": "#/definitions/jsonapi"
        }
      },
      "additionalProperties": false
    },
    "failure": {
      "type": "object",
      "required": [
        "errors"
      ],
      "properties": {
        "errors": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/error"
          },
          "uniqueItems": true
        },
        "meta": {
          "$ref": "#/definitions/meta"
        },
        "jsonapi": {
          "$ref": "#/definitions/jsonapi"
        },
        "links": {
          "$ref": "#/definitions/links"
        }
      },
      "additionalProperties": false
    },
    "info": {
      "type": "object",
      "required": [
        "meta"
      ],
      "properties": {
        "meta": {
          "$ref": "#/definitions/meta"
        },
        "links": {
          "$ref": "#/definitions/links"
        },
        "jsonapi": {
          "$ref": "#/definitions/jsonapi"
        }
      },
      "additionalProperties": false
    },
    
    "meta": {
      "description": "Non-standard meta-information that can not be represented as an attribute or relationship.",
      "type": "object",
      "additionalProperties": true
    },
    "data": {
      "description": "The document's \"primary data\" is a representation of the resource or collection of resources targeted by a request.",
      "oneOf": [
        {
          "$ref": "#/definitions/resource"
        },
        {
          "description": "An array of resource objects, an array of resource identifier objects, or an empty array ([]), for requests that target resource collections.",
          "type": "array",
          "items": {
            "$ref": "#/definitions/resource"
          },
          "uniqueItems": true
        },
        {
          "description": "null if the request is one that might correspond to a single resource, but doesn't currently.",
          "type": "null"
        }
      ]
    },
    "resource": {
      "description": "\"Resource objects\" appear in a JSON API document to represent resources.",
      "type": "object",
      "required": [
        "type",
        "id"
      ],
      "properties": {
        "type": {
          "type": "string"
        },
        "id": {
          "type": "string"
        },
        "attributes": {
          "$ref": "#/definitions/attributes"
        },
        "relationships": {
          "$ref": "#/definitions/relationships"
        },
        "links": {
          "$ref": "#/definitions/links"
        },
        "meta": {
          "$ref": "#/definitions/meta"
        }
      },
      "additionalProperties": false
    },

    "relationshipLinks": {
      "description": "A resource object **MAY** contain references to other resource objects (\"relationships\"). Relationships may be to-one or to-many. Relationships can be specified by including a member in a resource's links object.",
      "type": "object",
      "properties": {
        "self": {
          "description": "A `self` member, whose value is a URL for the relationship itself (a \"relationship URL\"). This URL allows the client to directly manipulate the relationship. For example, it would allow a client to remove an `author` from an `article` without deleting the people resource itself.",
          "$ref": "#/definitions/link"
        },
        "related": {
          "$ref": "#/definitions/link"
        }
      },
      "additionalProperties": true
    },
    "links": {
      "type": "object",
      "additionalProperties": {
        "$ref": "#/definitions/link"
      }
    },
    "link": {
      "description": "A link **MUST** be represented as either: a string containing the link's URL or a link object.",
      "oneOf": [
        {
          "description": "A string containing the link's URL.",
          "type": "string",
          "format": "uri-reference"
        },
        {
          "type": "object",
          "required": [
            "href"
          ],
          "properties": {
            "href": {
              "description": "A string containing the link's URL.",
              "type": "string",
              "format": "uri-reference"
            },
            "meta": {
              "$ref": "#/definitions/meta"
            }
          }
        }
      ]
    },

    "attributes": {
      "description": "Members of the attributes object (\"attributes\") represent information about the resource object in which it's defined.",
      "type": "object",
      "patternProperties": {
        "^(?!relationships$|links$|id$|type$)\\w[-\\w_]*$": {
          "description": "Attributes may contain any valid JSON value."
        }
      },
      "additionalProperties": false
    },

    "relationships": {
      "description": "Members of the relationships object (\"relationships\") represent references from the resource object in which it's defined to other resource objects.",
      "type": "object",
      "patternProperties": {
        "^(?!id$|type$)\\w[-\\w_]*$": {
          "properties": {
            "links": {
              "$ref": "#/definitions/relationshipLinks"
            },
            "data": {
              "description": "Member, whose value represents \"resource linkage\".",
              "oneOf": [
                {
                  "$ref": "#/definitions/relationshipToOne"
                },
                {
                  "$ref": "#/definitions/relationshipToMany"
                }
              ]
            },
            "meta": {
              "$ref": "#/definitions/meta"
            }
          },
          "anyOf": [
            {"required": ["data"]},
            {"required": ["meta"]},
            {"required": ["links"]}
          ],
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "relationshipToOne": {
      "description": "References to other resource objects in a to-one (\"relationship\"). Relationships can be specified by including a member in a resource's links object.",
      "anyOf": [
        {
          "$ref": "#/definitions/empty"
        },
        {
          "$ref": "#/definitions/linkage"
        }
      ]
    },
    "relationshipToMany": {
      "description": "An array of objects each containing \"type\" and \"id\" members for to-many relationships.",
      "type": "array",
      "items": {
        "$ref": "#/definitions/linkage"
      },
      "uniqueItems": true
    },
    "empty": {
      "description": "Describes an empty to-one relationship.",
      "type": "null"
    },
    "linkage": {
      "description": "The \"type\" and \"id\" to non-empty members.",
      "type": "object",
      "required": [
        "type",
        "id"
      ],
      "properties": {
        "type": {
          "type": "string"
        },
        "id": {
          "type": "string"
        },
        "meta": {
          "$ref": "#/definitions/meta"
        }
      },
      "additionalProperties": false
    },
    "pagination": {
      "type": "object",
      "properties": {
        "first": {
          "description": "The first page of data",
          "oneOf": [
            { "type": "string", "format": "uri-reference" },
            { "type": "null" }
          ]
        },
        "last": {
          "description": "The last page of data",
          "oneOf": [
            { "type": "string", "format": "uri-reference" },
            { "type": "null" }
          ]
        },
        "prev": {
          "description": "The previous page of data",
          "oneOf": [
            { "type": "string", "format": "uri-reference" },
            { "type": "null" }
          ]
        },
        "next": {
          "description": "The next page of data",
          "oneOf": [
            { "type": "string", "format": "uri-reference" },
            { "type": "null" }
          ]
        }
      }
    },
    
    "jsonapi": {
      "description": "An object describing the server's implementation",
      "type": "object",
      "properties": {
        "version": {
          "type": "string"
        },
        "meta": {
          "$ref": "#/definitions/meta"
        }
      },
      "additionalProperties": false
    },
    
    "error": {
      "type": "object",
      "properties": {
        "id": {
          "description": "A unique identifier for this particular occurrence of the problem.",
          "type": "string"
        },
        "links": {
          "$ref": "#/definitions/links"
        },
        "status": {
          "description": "The HTTP status code applicable to this problem, expressed as a string value.",
          "type": "string"
        },
        "code": {
          "description": "An application-specific error code, expressed as a string value.",
          "type": "string"
        },
        "title": {
          "description": "A short, human-readable summary of the problem. It **SHOULD NOT** change from occurrence to occurrence of the problem, except for purposes of localization.",
          "type": "string"
        },
        "detail": {
          "description": "A human-readable explanation specific to this occurrence of the problem.",
          "type": "string"
        },
        "source": {
          "type": "object",
          "properties": {
            "pointer": {
              "description": "A JSON Pointer [RFC6901] to the associated entity in the request document [e.g. \"/data\" for a primary data object, or \"/data/attributes/title\" for a specific attribute].",
              "type": "string"
            },
            "parameter": {
              "description": "A string indicating which query parameter caused the error.",
              "type": "string"
            }
          }
        },
        "meta": {
          "$ref": "#/definitions/meta"
        }
      },
      "additionalProperties": false
    }
  }
}
""")


def validate(data):
    jsonschema.validate(data, SCHEMA)