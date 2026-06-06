import os
import sys
import sqlite3
import uuid  # Generador de IDs únicos de texto automáticamente
from models.plato import Plato

class PlatoController:
    def __init__(self):
        # 🛠️ CORRECCIÓN DE RUTA ABSOLUTA PARA COMPILACIÓN (.EXE)
        # 1. Detectamos si el programa corre congelado (.exe) con PyInstaller o como script (.py)
        if getattr(sys, 'frozen', False):
            # Si es un .exe, la raíz es donde está el ejecutable instalado
            base_dir = os.path.dirname(sys.executable)
        else:
            # Si es modo desarrollo .py, obtenemos la raíz del proyecto subiendo un nivel desde 'controllers/'
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir)

        # 2. Unimos la raíz usando os.path.join de forma limpia para evitar problemas de diagonales
        self.db_path = os.path.join(base_dir, "database", "RestauranteBuenSabor.db")

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def obtener_todos(self) -> list:
        platos = []
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Id, Nombre, Precio FROM Platos ORDER BY Nombre ASC")
            for fila in cursor.fetchall():
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