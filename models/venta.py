from dataclasses import dataclass
from datetime import datetime
from typing import List
from models.detalle_venta import DetalleVenta

@dataclass
class Venta:
    id: int
    fecha_hora: datetime
    total: float
    # Lista que contendrá los objetos DetalleVenta asociados
    detalles: List[DetalleVenta] = None

    def __post_init__(self):
        if self.detalles is None:
            self.detalles = []