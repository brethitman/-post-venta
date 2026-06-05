import sqlite3
import uuid  # Generador de IDs únicos de texto automáticamente
from models.plato import Plato

class PlatoController:
    def __init__(self, db_path: str = "database/RestauranteBuenSabor.db"):
        self.db_path = db_path

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def obtener_todos(self) -> list:
        platos = []
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Id, Nombre, Precio FROM Platos ORDER BY Nombre ASC")
            for fila in cursor.fetchall():
                # 🛠️ CORREGIDO: Paréntesis cerrado correctamente al final de la instanciación
                platos.append(Plato(id=str(fila[0]), nombre=fila[1], precio=fila[2]))
        except sqlite3.Error as e:
            print(f"Error al obtener platos: {e}")
        finally:
            conn.close()
        return platos

    def insertar(self, plato: Plato) -> bool:
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            # Generamos un ID de texto único de 6 caracteres (ej: 'A1B2C3')
            id_automatico = uuid.uuid4().hex[:6].upper()
            
            cursor.execute("INSERT INTO Platos (Id, Nombre, Precio) VALUES (?, ?, ?)", 
                           (id_automatico, plato.nombre, plato.precio))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar plato: {e}")
            return False
        finally:
            conn.close()

    def actualizar(self, plato: Plato) -> bool:
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Platos SET Nombre = ?, Precio = ? WHERE Id = ?", 
                           (plato.nombre, plato.precio, plato.id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar plato: {e}")
            return False
        finally:
            conn.close()

    def eliminar(self, id_plato: str) -> bool:
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Platos WHERE Id = ?", (id_plato,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar plato: {e}")
            return False
        finally:
            conn.close()