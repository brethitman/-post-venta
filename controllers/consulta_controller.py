import sqlite3

class ConsultaController:
    def __init__(self, db_path: str = "database/RestauranteBuenSabor.db"):
        self.db_path = db_path

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def buscar_ticket_por_fecha_y_numero(self, fecha_buscada_str: str, nro_ticket_diario: int) -> dict:
        """
        Busca una venta filtrando por su fecha (YYYY-MM-DD) y su número de ticket diario correlativo.
        Retorna un diccionario con los datos del ticket y sus platos, o None si no existe.
        """
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            # 1. Traemos las ventas de ese día ordenadas por ID de forma ascendente
            cursor.execute("""
                SELECT Id, FechaHora, Total 
                FROM Ventas 
                WHERE FechaHora LIKE ? 
                ORDER BY Id ASC
            """, (f"{fecha_buscada_str}%",))
            filas = cursor.fetchall()
            
            # El número de ticket empieza en 1, por lo que restamos 1 para alinearlo al índice de la lista
            posicion_index = nro_ticket_diario - 1
            if posicion_index < 0 or posicion_index >= len(filas):
                return None  # No hay un ticket con ese número correlativo en este día
                
            fila_ganadora = filas[posicion_index]
            id_venta = fila_ganadora[0]
            fecha_hora_str = fila_ganadora[1]
            total_venta = fila_ganadora[2]
            
            # 2. Con el ID real de la base de datos, extraemos el desglose de los platos
            cursor.execute("""
                SELECT d.Cantidad, p.Nombre, d.PrecioUnitario 
                FROM DetalleVentas d
                JOIN Platos p ON d.PlatoId = p.Id
                WHERE d.VentaId = ?
            """, (id_venta,))
            detalles_platos = cursor.fetchall()
            
            return {
                "id_bd": id_venta,
                "fecha_hora": fecha_hora_str,
                "total": total_venta,
                "detalles": detalles_platos
            }
            
        except sqlite3.Error as e:
            print(f"Error en ConsultaController: {e}")
            return None
        finally:
            conn.close()