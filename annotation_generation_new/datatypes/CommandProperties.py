from util_standard import standard_repr
from util_new import return_default_if_none_else_itself
from typing import Dict, Any, Optional

# TODO: use this in construction of Info (under the hood with setter-functions)
class CommandProperties:

    def __init__(self, dict_prop_name_value: Optional[Dict[str, Any]] = None) -> None:
        self.dict_prop_name_value: Dict[str, Any] = return_default_if_none_else_itself(dict_prop_name_value, dict())

    def __repr__(self) -> str:
        return standard_repr(self)

    def set_property(self, prop_name: str, value: Any) -> None:
        self.dict_prop_name_value[prop_name] = value

    def get_property_value(self, prop_name: str):
        return self.dict_prop_name_value.get(prop_name, None)