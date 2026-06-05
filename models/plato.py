from dataclasses import dataclass

@dataclass
class Plato:
    id: str  # TEXT en SQLite
    nombre: str  # TEXT en SQLite
    precio: float  # REAL en SQLite (Python maneja float para números con decimales) 