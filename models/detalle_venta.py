from dataclasses import dataclass
from typing import Optional
from models.plato import Plato  # Ajusta el import según tu estructura exacta

@dataclass
class DetalleVenta:
    id: int
    venta_id: int
    plato_id: str
    cantidad: int
    precio_unitario: float
    
    # Propiedades virtuales para navegación de objetos (equivalentes al objeto virtual de C#)
    venta: Optional[object] = None  # Usamos object o string para evitar referencias circulares
    plato: Optional[Plato] = None