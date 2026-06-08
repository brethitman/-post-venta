import os
import sys
import sqlite3
from datetime import datetime
from models.venta import Venta

class VentaController:
    def __init__(self):
        # 🛠️ CORRECCIÓN DE RUTA ABSOLUTA PARA COMPILACIÓN (.EXE)
        # 1. Detectamos si el programa corre empaquetado (.exe) con PyInstaller o como script (.py)
        if getattr(sys, 'frozen', False):
            # Si es un .exe, la raíz es donde está el ejecutable instalado
            base_dir = os.path.dirname(sys.executable)
        else:
            # Si es modo desarrollo .py, obtenemos la raíz del proyecto subiendo un nivel desde 'controllers/'
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir)

        # 2. Unimos la raíz de forma limpia usando os.path.join para evitar conflictos de diagonales en Windows
        self.db_path = os.path.join(base_dir, "database", "RestauranteBuenSabor.db")

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def obtener_ticket_del_dia(self, fecha_hora_obj) -> int:
        """Cuenta cuántas ventas ocurrieron en la misma fecha para reiniciar el correlativo a diario."""
        conn = self._conectar()
        cursor = conn.cursor()
        fecha_solo = fecha_hora_obj.strftime("%Y-%m-%d")
        try:
            cursor.execute("SELECT COUNT(*) FROM Ventas WHERE FechaHora LIKE ?", (f"{fecha_solo}%",))
            cantidad_hoy = cursor.fetchone()[0]
            return cantidad_hoy + 1
        except sqlite3.Error:
            return 1
        finally:
            conn.close()

    def registrar_venta(self, venta: Venta) -> int:
        """Registra una venta. Retorna el NÚMERO DE TICKET DIARIO si sale bien, o 0 si falla."""
        ticket_diario = self.obtener_ticket_del_dia(venta.fecha_hora)
        
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            fecha_str = venta.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO Ventas (FechaHora, Total) VALUES (?, ?)",
                (fecha_str, venta.total)
            )
            
            venta_id = cursor.lastrowid
            
            for detalle in venta.detalles:
                cursor.execute(
                    """INSERT INTO DetalleVentas (VentaId, PlatoId, Cantidad, PrecioUnitario) 
                       VALUES (?, ?, ?, ?)""",
                    (venta_id, detalle.plato_id, detalle.cantidad, detalle.precio_unitario)
                )
            
            conn.commit()
            return ticket_diario
        except sqlite3.Error as e:
            print(f"Error crítico al registrar la venta: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def obtener_todas(self) -> list:
        """Consulta la base de datos y retorna una lista con el historial completo de ventas."""
        ventas = []
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Id, FechaHora, Total FROM Ventas ORDER BY FechaHora DESC")
            filas = cursor.fetchall()
            
            for fila in filas:
                id_venta = fila[0]
                fecha_hora_str = str(fila[1]).strip()
                total_venta = fila[2]
                
                # 🛠️ SOLUCIÓN: Limpieza dinámica de microsegundos (.0967216) si existen en la BD
                if "." in fecha_hora_str:
                    fecha_hora_str = fecha_hora_str.split(".")[0]
                
                try:
                    fecha_hora_obj = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M:%S")
                except (ValueError, TypeError):
                    try:
                        # Respaldo por si algún registro se guardó sólo con formato de fecha corta
                        fecha_hora_obj = datetime.strptime(fecha_hora_str, "%Y-%m-%d")
                    except (ValueError, TypeError):
                        fecha_hora_obj = datetime.now()
                
                venta = Venta(id=id_venta, fecha_hora=fecha_hora_obj, total=total_venta)
                ventas.append(venta)
        except sqlite3.Error as e:
            print(f"Error al recuperar el historial de ventas: {e}")
        finally:
            conn.close()
        return ventas

    def obtener_detalles_de_venta(self, venta_id: int) -> list:
        """Retorna una lista de tuplas (Cantidad, NombrePlato, PrecioUnitario) de una venta específica."""
        detalles = []
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT d.Cantidad, p.Nombre, d.PrecioUnitario 
                FROM DetalleVentas d
                JOIN Platos p ON d.PlatoId = p.Id
                WHERE d.VentaId = ?
            """, (venta_id,))
            detalles = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al recuperar detalles de la venta {venta_id}: {e}")
        finally:
            conn.close()
        return detalles

    def calcular_ticket_diario_para_historial(self, venta_id: int, fecha_hora_obj) -> int:
        """Calcula retrospectivamente qué número de ticket le tocó a una venta vieja en su día."""
        conn = self._conectar()
        cursor = conn.cursor()
        fecha_solo = fecha_hora_obj.strftime("%Y-%m-%d")
        try:
            # 🌟 Ajuste de consulta estricta para garantizar que cuente correctamente las filas anteriores
            cursor.execute("""
                SELECT COUNT(*) FROM Ventas 
                WHERE FechaHora LIKE ? AND Id <= ?
            """, (f"{fecha_solo}%", venta_id))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 1
        except sqlite3.Error:
            return 1
        finally:
            conn.close() 