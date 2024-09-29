from pydantic import BaseModel
from typing import Optional, List

# conditions endpoint
class ForecasterData(BaseModel):
    name: str
    avatar: Optional[str]

class ObservationData(BaseModel):
    # timestamp: int
    observation: Optional[str]
    rating: Optional[str]
    minHeight: Optional[int]
    maxHeight: Optional[int]
    plus: Optional[bool]
    humanRelation: Optional[str]
    occasionalHeight: Optional[int]

class ConditionsData(BaseModel):
    timestamp: int
    forecastDay: str
    forecaster: Optional[ForecasterData]
    human: bool
    observation: Optional[str]
    am: Optional[ObservationData]
    pm: Optional[ObservationData]

# rating endpoint
class RatingValueData(BaseModel):
    key: str
    value: Optional[float]

class RatingData(BaseModel):
    timestamp: int
    rating: RatingValueData

# tide endpoint
class TideData(BaseModel):
    timestamp: int
    type: str
    height: float

# wind endpoint
class WindData(BaseModel):
    timestamp: int
    speed: float
    gust: Optional[float]
    direction: Optional[float]
    directionType: Optional[str]
    optimalScore: Optional[int]

# weather endpoint
class WeatherData(BaseModel):
    timestamp: int
    temperature: Optional[float]
    pressure: Optional[float]
    condition: str



class SurfData(BaseModel):
    min: Optional[float]
    max: float
    # plus: Optional[bool] = None
    # humanRelation: Optional[str] = None
    # raw: Optional[RawSurfData] = None
    # optimalScore: Optional[int] = None

class SwellData(BaseModel):
    height: float
    period: float
    impact: Optional[float] = None
    power: Optional[float] = None
    direction: Optional[float] = None
    directionMin: Optional[float] = None
    optimalScore: Optional[int] = None

class WaveData(BaseModel):
    timestamp: int
    probability: Optional[float] = None
    surf: SurfData
    power: Optional[float] = None
    swells: Optional[List[SwellData]] = None

class SunlightData(BaseModel):
    midnight: int
    dawn: int
    sunrise: int
    sunset: int
    dusk: int

class SwellDetails(BaseModel):
    height: float
    period: float
    impact: Optional[float]
    power: Optional[float]
    direction: Optional[float]
    directionMin: Optional[float]

class SwellData(BaseModel):
    timestamp: int
    probability: Optional[float]
    power: Optional[float]
    swells: List[SwellDetails]

# FullWaveResponse is now more generic and supports multiple types of data
class FullResponse(BaseModel):
    rating: Optional[List[RatingData]] = None
    conditions: Optional[List[ConditionsData]] = None
    sunlight: Optional[List[SunlightData]] = None
    swells: Optional[List[SwellData]] = None
    tides: Optional[List[TideData]] = None
    wave: Optional[List[WaveData]] = None
    wind: Optional[List[WindData]] = None
    weather: Optional[List[WeatherData]] = None
