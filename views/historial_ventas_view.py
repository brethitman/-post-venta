from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTreeWidget, QTreeWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from controllers.venta_controller import VentaController

class HistorialVentasView(QWidget):
    def __init__(self):
        super().__init__()
        self.venta_ctrl = VentaController("database/RestauranteBuenSabor.db")
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #F3F4F6;")
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        # ⬅️ Encabezado con botón de retorno al Menú Principal
        layout_header = QHBoxLayout()
        self.btn_volver = QPushButton("⬅ Volver al Menú Principal")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setStyleSheet("""
            QPushButton { background-color: #4B5563; color: white; font-weight: bold; 
                          border-radius: 8px; padding: 10px 16px; border: none; }
            QPushButton:hover { background-color: #1F2937; }
        """)
        layout_header.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        
        lbl_status = QLabel("Módulo de Historial")
        lbl_status.setStyleSheet("background-color: #DBEAFE; color: #1E40AF; font-weight: bold; padding: 6px 12px; border-radius: 20px;")
        layout_header.addWidget(lbl_status, alignment=Qt.AlignmentFlag.AlignRight)
        layout_principal.addLayout(layout_header)

        lbl_titulo = QLabel("Historial de Ventas Registradas")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #1F2937; margin-top: 5px;")
        layout_principal.addWidget(lbl_titulo)

        # 🌳 Componente de Árbol Jerárquico de 3 Columnas
        self.arbol_ventas = QTreeWidget()
        self.arbol_ventas.setColumnCount(3)
        self.arbol_ventas.setHeaderLabels(["Código / Fecha / Plato", "Hora / P. Unit", "Monto Total Cobrado"])
        self.arbol_ventas.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.arbol_ventas.setStyleSheet("""
            QTreeWidget {
                background-color: #FFFFFF; border: 1px solid #E5E7EB;
                border-radius: 12px; padding: 10px; font-size: 14px; color: #374151;
            }
            QTreeView::item { padding: 6px; border-bottom: 1px solid #F3F4F6; }
            QTreeView::item:hover { background-color: #F9FAFB; }
            QHeaderView::section {
                background-color: #F9FAFB; padding: 8px; font-weight: bold;
                font-size: 13px; border: none; color: #4B5563;
            }
        """)
        layout_principal.addWidget(self.arbol_ventas)

        # 🧮 Barra de resumen inferior estática
        self.lbl_resumen_total = QLabel("Total Histórico Acumulado: $0.00")
        self.lbl_resumen_total.setStyleSheet("""
            font-size: 16px; font-weight: bold; color: #111827; 
            background-color: #FFFFFF; border: 1px solid #E5E7EB; 
            padding: 12px; border-radius: 8px; margin-top: 5px;
        """)
        layout_principal.addWidget(self.lbl_resumen_total)

        # Carga inicial de datos
        self.cargar_historial_agrupado()

    # 🔄 NUEVO MÉTODO IMPORTANTE: Sobrescribimos el evento de mostrarse en pantalla
    def showEvent(self, event):
        """Cada vez que el QStackedWidget cambie a esta vista, los datos se recargarán desde la BD."""
        super().showEvent(event)
        self.cargar_historial_agrupado()

    def cargar_historial_agrupado(self):
        """Consulta la BD y divide las ventas en Fechas, Tickets Diarios y sus respectivos Platos."""
        self.arbol_ventas.clear()
        
        ventas = self.venta_ctrl.obtener_todas()
        ventas_por_fecha = {}
        total_historico = 0.0

        # Agrupamos las ventas por la cadena de fecha simple (DD/MM/YYYY)
        for venta in ventas:
            fecha_str = venta.fecha_hora.strftime('%d/%m/%Y')
            if fecha_str not in ventas_por_fecha:
                ventas_por_fecha[fecha_str] = []
            ventas_por_fecha[fecha_str].append(venta)
            total_historico += venta.total

        fechas_ordenadas = sorted(ventas_por_fecha.keys(), reverse=True)

        for fecha in fechas_ordenadas:
            lista_ventas_del_dia = ventas_por_fecha[fecha]
            total_del_dia = sum(v.total for v in lista_ventas_del_dia)
            cant_ventas = len(lista_ventas_del_dia)

            # 1️⃣ NIVEL 1: Nodo de Fecha (Raíz)
            nodo_fecha = QTreeWidgetItem(self.arbol_ventas)
            nodo_fecha.setText(0, f"📅 {fecha}  ({cant_ventas} ventas)")
            nodo_fecha.setText(2, f"${total_del_dia:.2f}")
            
            nodo_fecha.setFlags(nodo_fecha.flags() | Qt.ItemFlag.ItemIsEnabled)
            for col in range(3):
                nodo_fecha.setFont(col, QFont("Segoe UI", 11, QFont.Weight.Bold))
                nodo_fecha.setForeground(col, Qt.GlobalColor.black)
            
            # 2️⃣ NIVEL 2: Los Tickets de esa fecha (Hijos)
            for venta in lista_ventas_del_dia:
                # 🛠️ CAMBIO AQUÍ: Calculamos el número correlativo que le correspondió ese día específico
                ticket_diario = self.venta_ctrl.calcular_ticket_diario_para_historial(venta.id, venta.fecha_hora)
                
                nodo_venta = QTreeWidgetItem(nodo_fecha)
                # Mostramos de forma amigable el número diario e internamente su ID único de BD
                nodo_venta.setText(0, f"📄 Ticket N° {ticket_diario}  (BD #{venta.id})")
                nodo_venta.setText(1, venta.fecha_hora.strftime('%H:%M:%S'))
                nodo_venta.setText(2, f"${venta.total:.2f}")
                
                nodo_venta.setFont(0, QFont("Segoe UI", 10, QFont.Weight.Medium))
                nodo_venta.setForeground(0, Qt.GlobalColor.darkBlue)
                nodo_venta.setForeground(1, Qt.GlobalColor.darkGray)

                # 3️⃣ NIVEL 3: Los artículos de este Ticket específico (Nietos)
                detalles_platos = self.venta_ctrl.obtener_detalles_de_venta(venta.id)
                for cantidad, nombre_plato, precio_unit in detalles_platos:
                    subtotal_plato = cantidad * precio_unit
                    
                    nodo_detalle = QTreeWidgetItem(nodo_venta)
                    nodo_detalle.setText(0, f"     • {cantidad}x  {nombre_plato}")
                    nodo_detalle.setText(1, f"${precio_unit:.2f}")
                    nodo_detalle.setText(2, f"${subtotal_plato:.2f}")
                    
                    fuente_plato = QFont("Segoe UI", 9)
                    fuente_plato.setItalic(True)
                    nodo_detalle.setFont(0, fuente_plato)
                    nodo_detalle.setFont(1, fuente_plato)
                    nodo_detalle.setFont(2, fuente_plato)
                    
                    nodo_detalle.setForeground(0, Qt.GlobalColor.gray)
                    nodo_detalle.setForeground(1, Qt.GlobalColor.gray)
                    nodo_detalle.setForeground(2, Qt.GlobalColor.gray)

        self.lbl_resumen_total.setText(f"💰 Total Histórico Acumulado en Base de Datos: ${total_historico:.2f}")