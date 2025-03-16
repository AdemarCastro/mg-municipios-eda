from dataclasses import dataclass
from typing import Optional

@dataclass
class CoordenadaMunicipio:
    municipio: str
    latitude: float
    longitude: float
    escolarizacao: Optional[float] = None