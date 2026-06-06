import sys
import os  # Gestión de rutas del sistema
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon  # Manejo del icono de la ventana

# ─── IMPORTACIÓN DE TODAS LAS VISTAS REALES ───
from views.menu_principal_view import MenuPrincipalView
from views.nueva_venta_view import NuevaVentaView
from views.historial_ventas_view import HistorialVentasView  
from views.consulta_ticket_view import ConsultaTicketView  
from views.reportes_view import ReportesView  
from views.configuracion_view import ConfiguracionView  
from views.ayuda_view import AyudaView  # 🆕 Importación de tu vista real de ayuda

# 🛠️ FUNCIÓN PARA OBTENER RUTAS EN DESARROLLO O EN .EXE
def obtener_ruta_asset(ruta_relativa):
    """ Devuelve la ruta absoluta para recursos internos tanto en VS Code como empaquetado """
    if getattr(sys, 'frozen', False):
        # Si corre empaquetado como un único .exe
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # Si corre en modo desarrollo desde la raíz del proyecto
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    return os.path.join(base_dir, ruta_relativa)

# 📦 COMPATIBILIDAD EXTERNA: Compartimos la función con los demás archivos views/ para sus imágenes
import builtins
builtins.obtener_ruta_asset = obtener_ruta_asset

app = QApplication(sys.argv)

ventana = QMainWindow()
ventana.setWindowTitle("POS El Buen Sabor - Sistema de Ventas")

# 🌟 ENLACE DEL LOGO DE LA APLICACIÓN (Barra de título)
ruta_logo = obtener_ruta_asset("assets/images/logoOficial.png")
ventana.setWindowIcon(QIcon(ruta_logo))

pantallas = QStackedWidget()

# 1. Instanciar Vistas Reales
vista_menu = MenuPrincipalView(pantallas)
vista_nueva_venta = NuevaVentaView()
vista_consulta_ticket = ConsultaTicketView()  
vista_historial_ventas = HistorialVentasView()  
vista_reportes = ReportesView()  
vista_configuracion = ConfiguracionView()  
vista_ayuda = AyudaView()  # 🆕 Instancia real de tu manual de ayuda

# 🆕 FUNCIÓN INTERCEPTORA DE CAMBIO DE PANTALLA
def controlar_cambio_pantalla(indice):
    """Detecta de forma automática cuándo se entra a la sección de ventas para refrescar el menú."""
    if indice == 1:  # El Índice 1 corresponde a la pantalla de Nueva Venta
        vista_nueva_venta.actualizar_menu()  # 🔄 Reconsulta la BD y redibuja en tiempo real

# 🆕 CONECTAR EL EVENTO DE CAMBIO DE PANTALLA DEL STACKEDWIDGET
pantallas.currentChanged.connect(controlar_cambio_pantalla)

# Enlazar botones de retorno al menú principal (Índice 0)
vista_nueva_venta.btn_volver.clicked.connect(lambda: pantallas.setCurrentIndex(0))
vista_consulta_ticket.btn_volver.clicked.connect(lambda: pantallas.setCurrentIndex(0))  
vista_historial_ventas.btn_volver.clicked.connect(lambda: pantallas.setCurrentIndex(0)) 
vista_reportes.btn_volver.clicked.connect(lambda: pantallas.setCurrentIndex(0))  
vista_configuracion.btn_volver.clicked.connect(lambda: pantallas.setCurrentIndex(0))  
vista_ayuda.btn_volver.clicked.connect(lambda: pantallas.setCurrentIndex(0))  # 🆕 Conexión de retorno para ayuda

# 2. Registrar pantallas fijas en orden estricto (Eliminado el bucle for problemático)
pantallas.addWidget(vista_menu)               # Índice 0 -> Menú principal
pantallas.addWidget(vista_nueva_venta)         # Índice 1 -> Módulo NUEVA VENTA Real
pantallas.addWidget(vista_consulta_ticket)     # Índice 2 -> Módulo CONSULTA Real
pantallas.addWidget(vista_historial_ventas)    # Índice 3 -> Módulo HISTORIAL Real
pantallas.addWidget(vista_reportes)            # Índice 4 -> Módulo REPORTES Real
pantallas.addWidget(vista_configuracion)       # Índice 5 -> Módulo CONFIGURACIÓN Real
pantallas.addWidget(vista_ayuda)               # Índice 6 -> Módulo AYUDA Real 👈 Aquí se integra tu interfaz

ventana.setCentralWidget(pantallas)
ventana.showMaximized()

sys.exit(app.exec())