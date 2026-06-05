import sqlite3
from datetime import datetime

class ReporteController:
    def __init__(self, db_path: str = "database/RestauranteBuenSabor.db"):
        self.db_path = db_path

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def obtener_platos_mas_vendidos_del_dia(self, fecha_str: str) -> list:
        """
        Retorna una lista de tuplas (NombrePlato, CantidadTotal) 
        vendidos en una fecha específica (YYYY-MM-DD).
        """
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT p.Nombre, SUM(d.Cantidad) as TotalVendido
                FROM DetalleVentas d
                JOIN Ventas v ON d.VentaId = v.Id
                JOIN Platos p ON d.PlatoId = p.Id
                WHERE v.FechaHora LIKE ?
                GROUP BY p.Id
                ORDER BY TotalVendido DESC
            """, (f"{fecha_str}%",))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en ReporteController (Platos): {e}")
            return []
        finally:
            conn.close()

    def obtener_ventas_ultimos_7_dias(self) -> list:
        """
        Retorna los montos totales recaudados en los últimos 7 días con venta 
        para armar un gráfico de línea temporal. Tuplas: (Fecha, MontoTotal)
        """
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT strftime('%d/%m', FechaHora) as Dia, SUM(Total) as TotalDia
                FROM Ventas
                GROUP BY Dia
                ORDER BY FechaHora DESC
                LIMIT 7
            """)
            # Lo revertimos para que el gráfico muestre un orden cronológico de izquierda a derecha
            return cursor.fetchall()[::-1]
        except sqlite3.Error as e:
            print(f"Error en ReporteController (Histórico): {e}")
            return []
        finally:
            conn.close()