from pytkdocs.loader import Loader


def test_inheriting_enum_Enum():
    loader = Loader()
    obj = loader.get_object_documentation("inheriting_enum_Enum")
