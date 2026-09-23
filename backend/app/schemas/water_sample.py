from datetime import datetime
import math
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _ensure_finite(v: float) -> float:
    if not math.isfinite(v):
        raise ValueError("必须是有限数值")
    return v


class WaterSampleCreate(BaseModel):
    pond_id: int = Field(..., alias="pondId")
    sampled_at: datetime = Field(..., alias="sampledAt")
    temp_c: float = Field(..., alias="tempC")
    salinity_ppt: float = Field(..., alias="salinityPpt")
    do_mg_l: float = Field(..., alias="doMgL")
    ph: float
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("do_mg_l")
    @classmethod
    def validate_do(cls, v: float) -> float:
        _ensure_finite(v)
        # 硬边界：溶氧必须严格大于 0，0 与负数一律拒绝
        if v <= 0:
            raise ValueError("溶解氧必须大于 0 mg/L")
        return v

    @field_validator("ph")
    @classmethod
    def validate_ph(cls, v: float) -> float:
        _ensure_finite(v)
        # 硬边界闭区间 [6, 9]
        if v < 6 or v > 9:
            raise ValueError("酸碱度 pH 必须在 6 到 9 之间")
        return v

    @field_validator("temp_c")
    @classmethod
    def validate_temp(cls, v: float) -> float:
        _ensure_finite(v)
        # 硬边界闭区间 [5, 40]
        if v < 5 or v > 40:
            raise ValueError("水温必须在 5 到 40 °C 之间")
        return v


class WaterSampleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    pond_id: int = Field(serialization_alias="pondId")
    sampled_at: datetime = Field(serialization_alias="sampledAt")
    temp_c: float = Field(serialization_alias="tempC")
    salinity_ppt: float = Field(serialization_alias="salinityPpt")
    do_mg_l: float = Field(serialization_alias="doMgL")
    ph: float
    notes: Optional[str] = None
