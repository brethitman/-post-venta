from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTreeWidget, QTreeWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
# 🚀 Usamos tu controlador real existente
from controllers.venta_controller import VentaController

class HistorialVentasView(QWidget):
    def __init__(self):
        super().__init__()
        # 🛠️ Inicialización con tu controlador real de la base de datos
        self.venta_ctrl = VentaController()
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
        
        # Estilos aplicados para asegurar la perfecta visualización del texto en color negro
        self.arbol_ventas.setStyleSheet("""
            QTreeWidget {
                background-color: #FFFFFF; border: 1px solid #E5E7EB;
                border-radius: 12px; padding: 10px; font-size: 14px; color: #000000;
            }
            QTreeView::item { 
                padding: 6px; 
                border-bottom: 1px solid #F3F4F6; 
                color: #000000; 
            }
            QTreeView::item:hover { 
                background-color: #F3F4F6; 
                color: #000000; 
            }
            QTreeView::item:selected { 
                background-color: #E5E7EB; 
                color: #000000; 
            }
            QHeaderView::section {
                background-color: #F9FAFB; padding: 8px; font-weight: bold;
                font-size: 13px; border: none; color: #000000;
            }
        """)
        layout_principal.addWidget(self.arbol_ventas)

        # 🧮 Barra de resumen inferior estática
        self.lbl_resumen_total = QLabel("Total Histórico Acumulado: $0.00")
        self.lbl_resumen_total.setStyleSheet("""
            font-size: 16px; font-weight: bold; color: #000000; 
            background-color: #FFFFFF; border: 1px solid #E5E7EB; 
            padding: 12px; border-radius: 8px; margin-top: 5px;
        """)
        layout_principal.addWidget(self.lbl_resumen_total)

        # Carga inicial de datos
        self.cargar_historial_agrupado()

    def showEvent(self, event):
        """Recarga los datos automáticamente cada vez que se navega a esta pantalla."""
        super().showEvent(event)
        self.cargar_historial_agrupado()

    def cargar_historial_agrupado(self):
        """Consulta la BD mediante VentaController utilizando el mapeo de objetos nativos."""
        self.arbol_ventas.clear()
        
        # Invocamos el método de tu controlador real que lee de RestauranteBuenSabor.db
        ventas = self.venta_ctrl.obtener_todas()
        ventas_por_fecha = {}
        total_historico = 0.0

        # Agrupamos los objetos de tipo Venta por su propiedad fecha_hora
        for venta in ventas:
            fecha_str = venta.fecha_hora.strftime('%d/%m/%Y')
            if fecha_str not in ventas_por_fecha:
                ventas_por_fecha[fecha_str] = []
            ventas_por_fecha[fecha_str].append(venta)
            total_historico += venta.total

        # 🛠️ CORRECCIÓN CLAVE: Ordenamos las fechas de forma CRONOLÓGICA REAL (No alfabética)
        fechas_ordenadas = sorted(
            ventas_por_fecha.keys(), 
            key=lambda x: datetime.strptime(x, '%d/%m/%Y'), 
            reverse=True
        )

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
            # Ordenamos cronológicamente ascendente (del primero al último del día) para enumerar bien los tickets
            ventas_ordenadas_dia = sorted(lista_ventas_del_dia, key=lambda x: x.fecha_hora)
            
            for indice, v_item in enumerate(ventas_ordenadas_dia, start=1):
                nodo_venta = QTreeWidgetItem(nodo_fecha)
                
                # 🛠️ AJUSTE VISUAL AQUÍ: Se eliminó por completo el (BD #{v_item.id}) para dejarlo impecable
                nodo_venta.setText(0, f"📄 Ticket N° {indice}")
                nodo_venta.setText(1, v_item.fecha_hora.strftime('%H:%M:%S'))
                nodo_venta.setText(2, f"${v_item.total:.2f}")
                
                nodo_venta.setFont(0, QFont("Segoe UI", 10, QFont.Weight.Medium))
                for col in range(3):
                    nodo_venta.setForeground(col, Qt.GlobalColor.black)

                # 3️⃣ NIVEL 3: Desglose de ítems comprados en el ticket (Nietos)
                detalles_platos = self.venta_ctrl.obtener_detalles_de_venta(v_item.id)
                for cantidad, nombre_plato, precio_unit in detalles_platos:
                    subtotal_plato = cantidad * precio_unit
                    
                    nodo_detalle = QTreeWidgetItem(nodo_venta)
                    nodo_detalle.setText(0, f"     • {cantidad}x  {nombre_plato}")
                    nodo_detalle.setText(1, f"${precio_unit:.2f}")
                    nodo_detalle.setText(2, f"${subtotal_plato:.2f}")
                    
                    fuente_plato = QFont("Segoe UI", 9)
                    fuente_plato.setItalic(True)
                    
                    for col in range(3):
                        nodo_detalle.setFont(col, fuente_plato)
                        nodo_detalle.setForeground(col, Qt.GlobalColor.black)

        self.lbl_resumen_total.setText(f"💰 Total Histórico Acumulado en Base de Datos: ${total_historico:.2f}")