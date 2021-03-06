import mock
import pytest
from ya_jsonapi import data as jdata
from jsonschema import ValidationError


class MockJsonObject:
    def __init__(self):
        pass

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.data = data
        return self


class MockJsonResourceObject(MockJsonObject):
    def __init__(self):
        MockJsonObject.__init__(self)

    @classmethod
    def self_or_id_from_json(cls, data):
        self = cls()
        self.id_data = data
        return self


def document_mock(fn):
    for classes in ['Error', 'Jsonapi', 'Link']:
        fn = mock.patch('ya_jsonapi.data.document.' + classes, MockJsonObject)(fn)
    fn = mock.patch('ya_jsonapi.data.document.Resource', MockJsonResourceObject)(fn)
    return fn


@document_mock
def test_document_from_json():
    data = {
        "data": {"a": 1},
        "meta": 2,
        "jsonapi": {"a": 3},
        "links": {"a": 4},
        "included": [5, 6],
    }
    doc = jdata.Document.from_json(data)
    assert doc.data.id_data == {"a": 1}
    assert doc.meta == 2
    assert doc.jsonapi.data == {"a": 3}
    assert doc.links["a"].data == 4
    assert [i.data for i in doc.included] == [5, 6]


@document_mock
def test_document_from_json_error_only():
    data = {
        "errors": [1, 2, 3]
    }
    doc = jdata.Document.from_json(data)
    assert doc.data is jdata.MISSING
    assert [i.data for i in doc.errors] == [1, 2, 3]
    assert doc.meta is None
    assert doc.jsonapi is None
    assert doc.links == {}
    assert doc.included == []


@document_mock
def test_document_from_json_data_values():
    data = {"data": None}
    doc = jdata.Document.from_json(data)
    assert doc.data is None

    data = {"data": {"a": 1}}
    doc = jdata.Document.from_json(data)
    assert isinstance(doc.data, MockJsonResourceObject)

    data = {"data": []}
    doc = jdata.Document.from_json(data)
    assert doc.data == []

    data = {"data": [{"a": 1}, {"a": 2}]}
    doc = jdata.Document.from_json(data)
    assert isinstance(doc.data[0], MockJsonResourceObject)
    assert [i.id_data for i in doc.data] == [{"a": 1}, {"a": 2}]


@document_mock
def test_document_from_invalid_response():
    with pytest.raises(ValidationError):
        jdata.Document.from_response({})


def error_mock(fn):
    fn = mock.patch('ya_jsonapi.data.error.Link', MockJsonObject)(fn)
    return fn


@error_mock
def test_error_from_json():
    data = {
        "id": 1,
        "links": {"a": 1},
        "status": "200",
        "code": "555",
        "title": "foo",
        "detail": "bar",
        "source": {"a": 2},
        "meta": 2,
    }
    err = jdata.Error.from_json(data)

    assert err.id == 1
    assert err.links["a"].data == 1
    assert err.status == "200"
    assert err.code == "555"
    assert err.title == "foo"
    assert err.detail == "bar"
    assert err.source == {"a": 2}
    assert err.meta == 2


@error_mock
def test_error_from_json_no_data():
    data = {}
    err = jdata.Error.from_json(data)

    assert err.id is None
    assert err.links == {}
    assert err.status is None
    assert err.code is None
    assert err.title is None
    assert err.detail is None
    assert err.source is None
    assert err.meta is None


def test_jsonapi_from_json():
    data = {
        "version": "1",
        "meta": 2,
    }
    ver = jdata.Jsonapi.from_json(data)

    assert ver.version == "1"
    assert ver.meta == 2


def test_jsonapi_from_json_no_data():
    data = {}
    ver = jdata.Jsonapi.from_json(data)
    assert ver.version is None
    assert ver.meta is None


def test_link_from_json():
    data = {
        "href": "link stuff",
        "meta": 1
    }
    link = jdata.Link.from_json(data)
    assert link.href == "link stuff"
    assert link.meta == 1


def test_link_from_json_no_data():
    data = {}
    link = jdata.Link.from_json(data)
    assert link.href is None
    assert link.meta is None


def test_link_from_json_string():
    link = jdata.Link.from_json("link stuff")
    assert link.href == "link stuff"
    assert link.meta is None


def relationship_mock(fn):
    for classes in ['Link', 'ResourceIdentifier']:
        fn = mock.patch('ya_jsonapi.data.relationship.' + classes, MockJsonObject)(fn)
    return fn


@relationship_mock
def test_relationship_from_json():
    data = {
        "links": {"a": 1},
        "data": {"a": 1},
        "meta": 1
    }
    rel = jdata.Relationship.from_json(data)

    assert rel.links["a"].data == 1
    assert rel.data.data == {"a": 1}
    assert rel.meta == 1


@relationship_mock
def test_relationship_from_json_only_data():
    data = {
        "data": {"a": 1},
    }
    rel = jdata.Relationship.from_json(data)

    assert rel.links == {}
    assert rel.data.data == {"a": 1}
    assert rel.meta is None


@relationship_mock
def test_relationship_from_json_data_values():
    data = {
        "links": {"a": 1},
    }
    rel = jdata.Relationship.from_json(data)
    assert rel.data is jdata.MISSING

    data["data"] = None
    rel = jdata.Relationship.from_json(data)
    assert rel.data is None

    data["data"] = {"a": 1}
    rel = jdata.Relationship.from_json(data)
    assert rel.data.data == {"a": 1}

    data["data"] = []
    rel = jdata.Relationship.from_json(data)
    assert rel.data == []

    data["data"] = [{"a": 1}, {"a": 2}]
    rel = jdata.Relationship.from_json(data)
    assert [i.data for i in rel.data] == [{"a": 1}, {"a": 2}]



def resource_mock(fn):
    for classes in ['Relationship', 'ResourceIdentifier', 'Link']:
        fn = mock.patch('ya_jsonapi.data.resource.' + classes, MockJsonObject)(fn)
    return fn


@resource_mock
def test_resource_from_json():
    data = {
        "id": "1",
        "type": "t",
        "attributes": {"a": 1},
        "relationships": {"b": 2},
        "links": {"a": 1},
        "meta": 1
    }
    res = jdata.Resource.from_json(data)

    assert res.id == "1"
    assert res.type == "t"
    assert res.links["a"].data == 1
    assert res.attributes["a"] == 1
    assert res.relationships["b"].data == 2
    assert res.meta == 1


@resource_mock
def test_resource_from_json_no_data():
    data = {
        "id": "1",
        "type": "t",
    }
    res = jdata.Resource.from_json(data)

    assert res.id == "1"
    assert res.type == "t"
    assert res.links == {}
    assert res.attributes == {}
    assert res.relationships == {}
    assert res.meta is None


@resource_mock
def test_resource_self_or_id_from_json():
    data = {
        "id": "1",
        "type": "t",
        "meta": 2,
    }
    res = jdata.Resource.self_or_id_from_json(data)
    # res should be a (mocked) ResourceIdentifier
    assert isinstance(res, MockJsonObject)

    data["attributes"] = {"a": 1}
    res = jdata.Resource.self_or_id_from_json(data)
    assert isinstance(res, jdata.Resource)
    del data["attributes"]

    data["relationships"] = {"a": 1}
    res = jdata.Resource.self_or_id_from_json(data)
    assert isinstance(res, jdata.Resource)
    del data["relationships"]

    data["links"] = {"a": 1}
    res = jdata.Resource.self_or_id_from_json(data)
    assert isinstance(res, jdata.Resource)
    del data["links"]


def test_resource_identifier_from_json():
    data = {
        "id": "1",
        "type": "t",
        "meta": 2,
    }
    res = jdata.ResourceIdentifier.from_json(data)
    assert res.id == "1"
    assert res.type == "t"
    assert res.meta == 2


def test_resource_identifier_from_json_no_data():
    data = {
        "id": "1",
        "type": "t",
    }
    res = jdata.ResourceIdentifier.from_json(data)
    assert res.id == "1"
    assert res.type == "t"
    assert res.meta is None
