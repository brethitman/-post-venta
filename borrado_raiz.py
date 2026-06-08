import os
import sqlite3

# Listamos las dos rutas para limpiar ambas y no errar
rutas_bd = [
    "RestauranteBuenSabor.db",                      # Raíz principal
    os.path.join("database", "RestauranteBuenSabor.db") # Carpeta database
]

for ruta in rutas_bd:
    if not os.path.exists(ruta):
        continue
        
    print(f"\n📦 Inspeccionando base de datos en: {ruta}")
    try:
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()

        # 1. Sacamos las tablas que de verdad existen dentro de ESTE archivo
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas_reales = [t[0] for t in cursor.fetchall()]
        
        if not tablas_reales:
            print("   ⚠️ Este archivo de base de datos está vacío (no tiene tablas).")
            conexion.close()
            continue

        print(f"   📋 Tablas detectadas en este archivo: {tablas_reales}")

        # 2. Buscar cómo se llaman las tablas de ventas (mayúsculas o minúsculas)
        tabla_detalle = None
        tabla_ventas = None

        for t in tablas_reales:
            if t.lower() in ["detalle_venta", "detalle_ventas"]:
                tabla_detalle = t
            if t.lower() in ["venta", "ventas"]:
                tabla_ventas = t

        # 3. Si encontramos las tablas, las vaciamos
        if tabla_detalle:
            print(f"   🔄 Vaciando registros de la tabla: {tabla_detalle}")
            cursor.execute(f"DELETE FROM {tabla_detalle};")
        else:
            print("   ❓ No se encontró tabla de detalles de venta aquí.")

        if tabla_ventas:
            print(f"   🔄 Vaciando registros de la tabla: {tabla_ventas}")
            cursor.execute(f"DELETE FROM {tabla_ventas};")
        else:
            print("   ❓ No se encontró tabla de ventas aquí.")

        # 4. Resetear contadores de ID
        if tabla_ventas or tabla_detalle:
            try:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name IN (?, ?);", (tabla_ventas, tabla_detalle))
            except:
                pass
            conexion.commit()
            print("   ✨ ¡Limpieza exitosa en este archivo!")
        
        conexion.close()

    except sqlite3.Error as e:
        print(f"   ❌ Error procesando este archivo: {e}")

print("\n🚀 Proceso terminado. Abre tu sistema y verifica los reportes.")