import os
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QDateEdit, QSpinBox, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, QDate, QLocale  # 🌍 Se agrega QLocale para el idioma
from controllers.consulta_controller import ConsultaController  

# 🛠️ FUNCIÓN DE ENTORNO PARA EL .EXE (RUTAS MÁGICAS)
def obtener_ruta_config(nombre_archivo="database/RestauranteBuenSabor.db"):
    """ Apunta a la carpeta física real donde corre el archivo .exe o script """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        # Sube un nivel desde 'views/' para ir a la raíz del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, nombre_archivo)


class ConsultaTicketView(QWidget):
    def __init__(self):
        super().__init__()
        # 🌟 CORRECCIÓN EXECUTABLE: Base de datos con ruta dinámica para que no falle en producción
        ruta_bd = obtener_ruta_config("database/RestauranteBuenSabor.db")
        self.consulta_ctrl = ConsultaController(ruta_bd)
        self.init_ui()

    def init_ui(self):
        # 🎨 Fondo General de la paleta: Gris ultra claro limpio (#F8FAFC) y texto base negro (#000000)
        self.setStyleSheet("background-color: #F8FAFC; color: #000000;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 25, 30, 25)
        layout_principal.setSpacing(15)

        # ─── ENCABEZADO SUPERIOR CON BOTÓN DE RETORNO ───
        layout_header = QHBoxLayout()
        self.btn_volver = QPushButton("⬅ Volver al Menú Principal")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setStyleSheet("""
            QPushButton { 
                background-color: #4B5563; color: white; font-weight: 700; 
                border-radius: 8px; padding: 10px 18px; border: none; font-size: 13px;
            }
            QPushButton:hover { background-color: #1F2937; }
        """)
        layout_header.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Estado de módulo estilizado (Módulo de Auditoría)
        lbl_status = QLabel("Módulo de Auditoría")
        lbl_status.setStyleSheet("""
            background-color: #FEF2F2; color: #991B1B; border: 1px solid #FCA5A5;
            font-weight: 700; padding: 6px 16px; border-radius: 20px; font-size: 12px;
        """)
        layout_header.addWidget(lbl_status, alignment=Qt.AlignmentFlag.AlignRight)
        layout_principal.addLayout(layout_header)

        # Título de la Sección Principal - Forzado a Negro
        lbl_titulo = QLabel("Buscador de Tickets Diarios")
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: 800; color: #000000; background: transparent; padding-bottom: 5px;")
        layout_principal.addWidget(lbl_titulo)

        # ─── 🔄 SECCIÓN CENTRAL DIVIDIDA EN DOS COLUMNAS ───
        layout_split_columnas = QHBoxLayout()
        layout_split_columnas.setSpacing(25)

        # ==========================================
        # PANEL IZQUIERDO: FORMULARIO DE FILTROS
        # ==========================================
        panel_izquierdo = QWidget()
        panel_izquierdo.setStyleSheet("background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E5E7EB; color: #000000;")
        
        layout_izq_interno = QVBoxLayout(panel_izquierdo)
        layout_izq_interno.setContentsMargins(25, 25, 25, 25)
        layout_izq_interno.setSpacing(18)

        lbl_panel_f = QLabel("🔍 Parámetros de Búsqueda")
        lbl_panel_f.setStyleSheet("font-size: 16px; font-weight: bold; color: #000000; border-bottom: 1px solid #E5E7EB; padding-bottom: 10px;")
        layout_izq_interno.addWidget(lbl_panel_f)

        # Estilos forzados a Negro Puro (#000000) para inputs y textos de los campos
        estilo_labels = "font-size: 13px; font-weight: 700; color: #000000; border: none; background: transparent;"
        estilo_inputs = "background-color: #FFFFFF; padding: 10px 12px; border: 1px solid #CBD5E1; border-radius: 8px; font-size: 14px; color: #000000;"

        # Selector de Fecha
        layout_izq_interno.addWidget(QLabel("<b>Seleccione la Fecha:</b>", styleSheet=estilo_labels))
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())
        self.input_fecha.setStyleSheet(estilo_inputs)
        
        # 🌍 TRADUCCIÓN A ESPAÑOL DE LA INTERFAZ DEL CALENDARIO:
        idioma_espanol = QLocale(QLocale.Language.Spanish, QLocale.Country.Spain)
        self.input_fecha.setLocale(idioma_espanol)
        
        layout_izq_interno.addWidget(self.input_fecha)

        # Selector de Número de Ticket
        layout_izq_interno.addWidget(QLabel("<b>Número de Ticket del Día:</b>", styleSheet=estilo_labels))
        self.input_ticket = QSpinBox()
        self.input_ticket.setRange(1, 9999)
        self.input_ticket.setValue(1)
        self.input_ticket.setStyleSheet(estilo_inputs)
        layout_izq_interno.addWidget(self.input_ticket)

        layout_izq_interno.addSpacing(10)

        # Botón de búsqueda Azul Corporativo
        self.btn_buscar = QPushButton("🔎 Ejecutar Búsqueda")
        self.btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_buscar.setMinimumHeight(45)
        self.btn_buscar.setStyleSheet("""
            QPushButton { 
                background-color: #2563EB; color: white; font-weight: 700; 
                font-size: 14px; border-radius: 8px; border: none;
            }
            QPushButton:hover { background-color: #1D4ED8; color: white; }
        """)
        self.btn_buscar.clicked.connect(self.ejecutar_busqueda)
        layout_izq_interno.addWidget(self.btn_buscar)
        
        layout_izq_interno.addStretch()
        
        # Añadir panel izquierdo al split (ocupa 1 parte de espacio)
        layout_split_columnas.addWidget(panel_izquierdo, stretch=1)

        # ==========================================
        # PANEL DERECHO: VISTA DEL TICKET DIGITAL
        # ==========================================
        self.card_resultado = QWidget()
        self.card_resultado.setStyleSheet("background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E5E7EB; color: #000000;")
        
        layout_card = QVBoxLayout(self.card_resultado)
        layout_card.setContentsMargins(25, 25, 25, 25)
        layout_card.setSpacing(15)

        # Cabecera interactiva del ticket
        self.lbl_info_cabecera = QLabel("<br><br><p align='center' style='color: #64748B; font-size: 14px;'><i>Ingrese los parámetros a la izquierda<br>y presione buscar para visualizar el ticket aquí.</i></p>")
        self.lbl_info_cabecera.setStyleSheet("font-size: 13px; color: #000000; line-height: 140%; background: transparent; border: none;")
        layout_card.addWidget(self.lbl_info_cabecera)

        # Tabla de Detalles Premium
        self.tabla_detalles = QTableWidget()
        self.tabla_detalles.setColumnCount(4)
        self.tabla_detalles.setHorizontalHeaderLabels(["Cant.", "Descripción del Plato", "P. Unitario", "Subtotal"])
        self.tabla_detalles.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_detalles.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        # 🔒 Bloqueos de interfaz gráfica para celdas estáticas
        self.tabla_detalles.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  
        self.tabla_detalles.setSelectionMode(QTableWidget.SelectionMode.NoSelection)  
        self.tabla_detalles.setFocusPolicy(Qt.FocusPolicy.NoFocus)                    

        # Aseguramos color negro (#000000) en el texto de las filas y en los títulos de las columnas
        self.tabla_detalles.setStyleSheet("""
            QTableWidget { 
                border: none; background-color: white; color: #000000; font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px; border-bottom: 1px solid #F1F5F9; color: #000000;
            }
            QTableWidget::item:focus {
                background-color: transparent; color: #000000;
            }
            QHeaderView::section { 
                background-color: #F8FAFC; padding: 8px; font-weight: 700; 
                border: none; color: #000000; font-size: 11px; text-transform: uppercase;
            }
        """)
        layout_card.addWidget(self.tabla_detalles)

        # Monto Total resaltado en Verde Esmeralda (#059669)
        self.lbl_monto_total = QLabel("")
        self.lbl_monto_total.setStyleSheet("""
            font-size: 20px; font-weight: 800; color: #059669; 
            background: transparent; border: none; padding-top: 5px;
        """)
        layout_card.addWidget(self.lbl_monto_total, alignment=Qt.AlignmentFlag.AlignRight)

        # Añadir panel derecho al split (ocupa 2 partes de espacio para ser más ancho)
        layout_split_columnas.addWidget(self.card_resultado, stretch=2)

        # Acoplamos las columnas al layout de la pantalla
        layout_principal.addLayout(layout_split_columnas)


    # ─── LÓGICA DE CONTROL (MANTENIDA EXACTAMENTE IGUAL) ───
    def ejecutar_busqueda(self):
        fecha_texto = self.input_fecha.date().toString("yyyy-MM-dd")
        nro_ticket = self.input_ticket.value()

        # Llamada al controlador independiente
        ticket_encontrado = self.consulta_ctrl.buscar_ticket_por_fecha_y_numero(fecha_texto, nro_ticket)

        if ticket_encontrado:
            # Forzamos los textos inyectados por HTML a usar color: #000000 explícitamente
            self.lbl_info_cabecera.setText(
                f"<span style='font-size: 17px; color: #000000;'><b>🧾 Ticket del Día N° {nro_ticket}</b></span><br>"
                f"<hr style='border: 1px dashed #E2E8F0;'><br>"
                f"<span style='color: #000000;'>📅 <b>Fecha/Hora de Venta:</b> {ticket_encontrado['fecha_hora']}</span><br>"
                f"<span style='color: #000000;'>🆔 <b>Código único de Auditoría (BD):</b></span> <span style='color: #2563EB; font-weight: bold;'>#{ticket_encontrado['id_bd']}</span>"
            )
            
            self.tabla_detalles.setRowCount(0)
            for cant, nombre_plato, precio_unit in ticket_encontrado['detalles']:
                subtotal = cant * precio_unit
                fila = self.tabla_detalles.rowCount()
                self.tabla_detalles.insertRow(fila)
                
                item_cant = QTableWidgetItem(str(cant))
                item_cant.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_cant.setForeground(Qt.GlobalColor.black) # Forzado a negro
                
                item_nombre = QTableWidgetItem(nombre_plato)
                item_nombre.setForeground(Qt.GlobalColor.black) # Forzado a negro
                
                item_precio = QTableWidgetItem(f"${precio_unit:.2f}")
                item_precio.setForeground(Qt.GlobalColor.black) # Forzado a negro
                
                item_subtotal = QTableWidgetItem(f"${subtotal:.2f}")
                item_subtotal.setForeground(Qt.GlobalColor.black) # Forzado a negro
                
                self.tabla_detalles.setItem(fila, 0, item_cant)
                self.tabla_detalles.setItem(fila, 1, item_nombre)
                self.tabla_detalles.setItem(fila, 2, item_precio)
                self.tabla_detalles.setItem(fila, 3, item_subtotal)

            self.lbl_monto_total.setText(f"TOTAL COBRADO: ${ticket_encontrado['total']:.2f}")
        else:
            # Si no hay resultados, limpiamos la zona de impresión digital y mostramos el aviso en rojo
            self.lbl_info_cabecera.setText("<br><br><p align='center' style='color: #EF4444; font-size: 14px;'><b>❌ Sin resultados para la última búsqueda.</b></p>")
            self.tabla_detalles.setRowCount(0)
            self.lbl_monto_total.clear()
            
            QMessageBox.information(
                self, "Sin Resultados", 
                f"No se encontró ningún Ticket N° {nro_ticket} generado en la fecha {self.input_fecha.date().toString('dd/MM/yyyy')}."
            )