import mock
from ya_jsonapi import data as jdata


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