import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton
from views.menu_principal_view import MenuPrincipalView
from views.nueva_venta_view import NuevaVentaView
from views.historial_ventas_view import HistorialVentasView  
from views.consulta_ticket_view import ConsultaTicketView  
from views.reportes_view import ReportesView  
from views.configuracion_view import ConfiguracionView  # ⬅️ IMPORTACIÓN DE CONFIGURACIÓN

app = QApplication(sys.argv)

ventana = QMainWindow()
ventana.setWindowTitle("POS El Buen Sabor - Sistema de Ventas")

pantallas = QStackedWidget()

# 1. Instanciar Vistas Reales
vista_menu = MenuPrincipalView(pantallas)
vista_nueva_venta = NuevaVentaView()
vista_consulta_ticket = ConsultaTicketView()  
vista_historial_ventas = HistorialVentasView()  
vista_reportes = ReportesView()  
vista_configuracion = ConfiguracionView()  # ⬅️ INSTANCIA REAL DEL GESTOR DE PLATOS

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
vista_configuracion.btn_volver.clicked.connect(lambda: pantallas.setCurrentIndex(0))  # Retorno de configuración

# 2. Registrar pantallas fijas de arranque
pantallas.addWidget(vista_menu)               # Índice 0 -> Menú principal
pantallas.addWidget(vista_nueva_venta)         # Índice 1 -> Módulo NUEVA VENTA Real

# Guardamos únicamente el relleno del módulo 6 (Ayuda), los demás ya son reales
nombres_modulos = {
    6: "Módulo de Ayuda y Soporte"
}

# Iteramos para armar el StackedWidget en el orden estricto de los botones
for i in range(2, 7):
    if i == 2:
        # Inyectamos la vista de Consultas Real en el Índice 2 exacto
        pantallas.addWidget(vista_consulta_ticket)
    elif i == 3:
        # Inyectamos la vista de Historial Real en el Índice 3 exacto
        pantallas.addWidget(vista_historial_ventas)
    elif i == 4:
        # Inyectamos la vista de Reportes y Gráficos Real en el Índice 4 exacto
        pantallas.addWidget(vista_reportes)
    elif i == 5:
        # Inyectamos la vista de Configuración de Platos Real en el Índice 5 exacto
        pantallas.addWidget(vista_configuracion)
    else:
        # Módulo que sigue en desarrollo temporal (Únicamente el Índice 6)
        p_temp = QWidget()
        lay = QVBoxLayout(p_temp)
        lbl = QLabel(f"📍 {nombres_modulos[i]}\n\n[Sección en desarrollo...]")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #4B5563; padding: 20px;")
        
        btn_back = QPushButton("⬅ Volver al Menú Principal")
        btn_back.setStyleSheet("background-color: #374151; color: white; padding: 10px; border-radius: 8px;")
        btn_back.clicked.connect(lambda checked, idx=0: pantallas.setCurrentIndex(idx))
        
        lay.addWidget(lbl)
        lay.addWidget(btn_back)
        pantallas.addWidget(p_temp)

ventana.setCentralWidget(pantallas)
ventana.showMaximized()

sys.exit(app.exec())