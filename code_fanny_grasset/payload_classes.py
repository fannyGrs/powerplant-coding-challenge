from typing import Dict, List, Optional

from pydantic import BaseModel

from enum import Enum

class EnergyType(str, Enum):
    gasfired = "gasfired"
    turbojet = "turbojet"
    windturbine = "windturbine"

class Powerplant(BaseModel):
    name: str
    type: EnergyType
    efficiency: float
    pmin: float
    pmax: float
    effective_pmin: Optional[float]
    effective_pmax: Optional[float]
    cost_1MWh: Optional[float]

class Payload(BaseModel):
    load: float
    fuels: Dict[str, float]
    powerplants: List[Powerplant]


