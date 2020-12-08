from typing import Any, Dict, List


class C:
    def __init__(self):
        # https://github.com/pawamoy/pytkdocs/issues/73
        self.dict_annotation: Dict[str, Any] = {}

        # https://github.com/pawamoy/pytkdocs/issues/75
        self.list_annotation: List[str] = []
