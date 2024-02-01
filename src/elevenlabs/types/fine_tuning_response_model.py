# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .finetuning_state import FinetuningState
from .manual_verification_response_model import ManualVerificationResponseModel
from .verification_attempt_response_model import VerificationAttemptResponseModel

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class FineTuningResponseModel(pydantic.BaseModel):
    is_allowed_to_fine_tune: bool
    fine_tuning_requested: bool
    finetuning_state: FinetuningState
    verification_failures: typing.List[str]
    verification_attempts_count: int
    manual_verification_requested: bool
    verification_attempts: typing.Optional[typing.List[VerificationAttemptResponseModel]]
    slice_ids: typing.Optional[typing.List[str]]
    manual_verification: typing.Optional[ManualVerificationResponseModel]
    language: typing.Optional[str]
    required: typing.Optional[typing.Any]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
