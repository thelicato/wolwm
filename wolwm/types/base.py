"""
This modules contains the base Pydantic class that enables the 'to_camel' alias generation
"""

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel, extra="forbid"):
    """Empty class"""

    class Config:
        """Configuration for support for alias, name population and enums usage"""

        alias_generator = to_camel
        populate_by_name = True
        use_enum_values = True