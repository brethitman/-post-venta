from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QDateEdit, QSpinBox, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from controllers.consulta_controller import ConsultaController  # 🔌 Importamos el nuevo controlador

class ConsultaTicketView(QWidget):
    def __init__(self):
        super().__init__()
        # Instanciamos el controlador específico de consultas
        self.consulta_ctrl = ConsultaController("database/RestauranteBuenSabor.db")
        self.init_ui()

    def init_ui(self):
        # 🎨 Fondo General de la paleta: Gris ultra claro limpio (#F8FAFC)
        self.setStyleSheet("background-color: #F8FAFC;")
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(50, 40, 50, 40)
        layout_principal.setSpacing(20)

        # ─── ENCABEZADO CON BOTÓN DE RETORNO ───
        layout_header = QHBoxLayout()
        self.btn_volver = QPushButton("⬅ Volver al Menú Principal")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setStyleSheet("""
            QPushButton { 
                background-color: #64748B; color: white; font-weight: 700; 
                border-radius: 8px; padding: 10px 18px; border: none; font-size: 13px;
            }
            QPushButton:hover { background-color: #475569; }
        """)
        layout_header.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Estado de módulo estilizado (Módulo de Auditoría)
        lbl_status = QLabel("Módulo de Auditoría")
        lbl_status.setStyleSheet("""
            background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5;
            font-weight: 700; padding: 6px 16px; border-radius: 15px; font-size: 12px;
        """)
        layout_header.addWidget(lbl_status, alignment=Qt.AlignmentFlag.AlignRight)
        layout_principal.addLayout(layout_header)

        # Título de la Sección en Gris Carbón Oscuro (#0F172A)
        lbl_titulo = QLabel("Buscador de Tickets Diarios")
        lbl_titulo.setStyleSheet("font-size: 26px; font-weight: 800; color: #0F172A; background: transparent;")
        layout_principal.addWidget(lbl_titulo)

        # ─── 🗂️ TARJETA CENTRAL DE FILTROS ───
        # Agrupamos los filtros en un contenedor blanco de tamaño controlado para evitar deformaciones
        card_filtros = QWidget()
        card_filtros.setMaximumWidth(700)  # Evita que se estire horizontalmente al maximizar
        card_filtros.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }
            QLabel {
                border: none; background: transparent;
                font-size: 13px; font-weight: 700; color: #475569;
            }
        """)
        
        layout_filtros = QHBoxLayout(card_filtros)
        layout_filtros.setContentsMargins(25, 20, 25, 20)
        layout_filtros.setSpacing(20)

        # Filtro de fecha
        div_fecha = QVBoxLayout()
        lbl_f = QLabel("Seleccione Fecha:")
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())
        self.input_fecha.setStyleSheet("""
            QDateEdit {
                background-color: white; padding: 8px 12px; border: 1px solid #CBD5E1; 
                border-radius: 8px; font-size: 13px; color: #0F172A; min-width: 160px;
            }
            QDateEdit:focus { border: 2px solid #2563EB; }
        """)
        div_fecha.addWidget(lbl_f)
        div_fecha.addWidget(self.input_fecha)
        layout_filtros.addLayout(div_fecha)

        # Filtro de Número de ticket diario
        div_ticket = QVBoxLayout()
        lbl_t = QLabel("Número de Ticket del Día:")
        self.input_ticket = QSpinBox()
        self.input_ticket.setRange(1, 9999)
        self.input_ticket.setValue(1)
        self.input_ticket.setStyleSheet("""
            QSpinBox {
                background-color: white; padding: 8px 12px; border: 1px solid #CBD5E1; 
                border-radius: 8px; font-size: 13px; color: #0F172A; min-width: 140px;
            }
            QSpinBox:focus { border: 2px solid #2563EB; }
        """)
        div_ticket.addWidget(lbl_t)
        div_ticket.addWidget(self.input_ticket)
        layout_filtros.addLayout(div_ticket)

        # Botón de búsqueda unificado a Azul Ejecutivo (#2563EB)
        self.btn_buscar = QPushButton("🔍 Buscar Ticket")
        self.btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_buscar.setStyleSheet("""
            QPushButton { 
                background-color: #2563EB; color: white; font-weight: 700; 
                font-size: 13px; border-radius: 8px; padding: 10px 22px; border: none;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """)
        self.btn_buscar.clicked.connect(self.ejecutar_busqueda)
        layout_filtros.addWidget(self.btn_buscar, alignment=Qt.AlignmentFlag.AlignBottom)
        
        # Agregamos la tarjeta de filtros alineada a la izquierda
        layout_principal.addWidget(card_filtros, alignment=Qt.AlignmentFlag.AlignLeft)

        # ─── 🧾 TARJETA DE RESULTADOS (Ticket) ───
        self.card_resultado = QWidget()
        self.card_resultado.setVisible(False)
        self.card_resultado.setStyleSheet("background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E2E8F0;")
        
        layout_card = QVBoxLayout(self.card_resultado)
        layout_card.setContentsMargins(30, 25, 30, 25)

        self.lbl_info_cabecera = QLabel("")
        self.lbl_info_cabecera.setStyleSheet("""
            font-size: 14px; color: #334155; line-height: 150%;
            border-bottom: 2px dashed #E2E8F0; padding-bottom: 15px; margin-bottom: 10px;
        """)
        layout_card.addWidget(self.lbl_info_cabecera)

        # Tabla de Detalles Premium
        self.tabla_detalles = QTableWidget()
        self.tabla_detalles.setColumnCount(4)
        self.tabla_detalles.setHorizontalHeaderLabels(["Cant.", "Descripción del Plato", "P. Unitario", "Subtotal"])
        self.tabla_detalles.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_detalles.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_detalles.setStyleSheet("""
            QTableWidget { 
                border: none; background-color: white; color: #0F172A; font-size: 13px;
            }
            QTableWidget::item {
                padding: 10px; border-bottom: 1px solid #F1F5F9;
            }
            QHeaderView::section { 
                background-color: #F8FAFC; padding: 8px; font-weight: 700; 
                border: none; color: #64748B; font-size: 12px; text-transform: uppercase;
            }
        """)
        layout_card.addWidget(self.tabla_detalles)

        # Monto Total resaltado en Verde Esmeralda (#059669)
        self.lbl_monto_total = QLabel("")
        self.lbl_monto_total.setStyleSheet("""
            font-size: 22px; font-weight: 800; color: #059669; 
            background: transparent; border: none; margin-top: 15px;
        """)
        layout_card.addWidget(self.lbl_monto_total, alignment=Qt.AlignmentFlag.AlignRight)

        layout_principal.addWidget(self.card_resultado, stretch=1)

    def ejecutar_busqueda(self):
        fecha_texto = self.input_fecha.date().toString("yyyy-MM-dd")
        nro_ticket = self.input_ticket.value()

        # Usamos el nuevo controlador independiente
        ticket_encontrado = self.consulta_ctrl.buscar_ticket_por_fecha_y_numero(fecha_texto, nro_ticket)

        if ticket_encontrado:
            self.lbl_info_cabecera.setText(
                f"<span style='font-size: 16px; color: #0F172A;'><b>🧾 Ticket del Día N° {nro_ticket}</b></span><br><br>"
                f"📅 <b>Fecha/Hora de Venta:</b> {ticket_encontrado['fecha_hora']}<br>"
                f"🆔 <b>Código único de Auditoría (BD):</b> <span style='color: #2563EB;'>#{ticket_encontrado['id_bd']}</span>"
            )
            
            self.tabla_detalles.setRowCount(0)
            for cant, nombre_plato, precio_unit in ticket_encontrado['detalles']:
                subtotal = cant * precio_unit
                fila = self.tabla_detalles.rowCount()
                self.tabla_detalles.insertRow(fila)
                
                # Elementos de la tabla
                item_cant = QTableWidgetItem(str(cant))
                item_cant.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                self.tabla_detalles.setItem(fila, 0, item_cant)
                self.tabla_detalles.setItem(fila, 1, QTableWidgetItem(nombre_plato))
                self.tabla_detalles.setItem(fila, 2, QTableWidgetItem(f"${precio_unit:.2f}"))
                self.tabla_detalles.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))

            self.lbl_monto_total.setText(f"TOTAL COBRADO: ${ticket_encontrado['total']:.2f}")
            self.card_resultado.setVisible(True)
        else:
            self.card_resultado.setVisible(False)
            QMessageBox.information(
                self, "Sin Resultados", 
                f"No se encontró ningún Ticket N° {nro_ticket} generado en la fecha {self.input_fecha.date().toString('dd/MM/yyyy')}."
            )