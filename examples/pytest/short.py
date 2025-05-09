import pytest

@pytest.fixture
def dictionary():
    return {}

def test_dict(dictionary):
    assert len(dictionary) == len(dictionary.keys()) == 0
    dictionary["key"] = "value"
    assert dictionary["key"] == "value"
    assert len(dictionary) == 1
    del dictionary["key"]
    with pytest.raises(KeyError):
        dictionary["key"]