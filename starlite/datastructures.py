import os
from copy import copy
from typing import Any, AsyncIterator, Dict, Iterator, Optional, Union, cast

from pydantic import BaseModel, FilePath, validator
from starlette.datastructures import State as StarletteStateClass


class State(StarletteStateClass):
    def __copy__(self) -> "State":
        """
        Returns a shallow copy of the given state object.
        Customizes how the builtin "copy" function will work.
        """
        return self.__class__(copy(self._state))

    def copy(self) -> "State":
        """Returns a shallow copy of the given state object"""
        return copy(self)


class File(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    path: FilePath
    filename: str
    stat_result: Optional[os.stat_result] = None

    @validator("stat_result", always=True)
    def validate_status_code(  # pylint: disable=no-self-argument, no-self-use
        cls, value: Optional[os.stat_result], values: Dict[str, Any]
    ) -> os.stat_result:
        """Set the stat_result value for the given filepath"""
        return value or os.stat(cast(str, values.get("path")))


class Redirect(BaseModel):
    path: str


class Stream(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    iterator: Union[Iterator[Any], AsyncIterator[Any]]
