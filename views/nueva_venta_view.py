from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QScrollArea, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextDocument, QFont
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog  # 🖨️ Componentes nativos de impresión
from datetime import datetime
from controllers.plato_controller import PlatoController
from controllers.venta_controller import VentaController
from models.venta import Venta
from models.detalle_venta import DetalleVenta

class NuevaVentaView(QWidget):
    def __init__(self):
        super().__init__()
        # 🛠️ CORRECCIÓN AQUÍ: Dejamos los constructores vacíos para usar la ruta absoluta automatizada
        self.plato_ctrl = PlatoController()
        self.venta_ctrl = VentaController()
        
        # Carrito temporal en memoria
        self.carrito = {}
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #F3F4F6;")
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        # 📄 SECCIÓN IZQUIERDA: Selector de Platos
        seccion_platos = QVBoxLayout()
        
        self.btn_volver = QPushButton("⬅ Volver al Menú Principal")
        self.btn_volver.setStyleSheet("""
            QPushButton { background-color: #4B5563; color: white; font-weight: bold; 
                          border-radius: 8px; padding: 10px; border: none; }
            QPushButton:hover { background-color: #1F2937; }
        """)
        seccion_platos.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        
        lbl_menu = QLabel("Menú de Platos Disponibles")
        lbl_menu.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937; margin: 10px 0;")
        seccion_platos.addWidget(lbl_menu)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        contenedor_grid = QWidget()
        self.grid_platos = QGridLayout(contenedor_grid)
        self.grid_platos.setSpacing(15)
        self.grid_platos.setContentsMargins(5, 5, 5, 5)
        
        scroll.setWidget(contenedor_grid)
        seccion_platos.addWidget(scroll)
        
        # 🧾 SECCIÓN DERECHA: Detalle Financiero y Carrito
        seccion_total = QVBoxLayout()
        
        card_resumen = QWidget()
        card_resumen.setStyleSheet("""
            QWidget { background-color: #FFFFFF; border-radius: 16px; border: 1px solid #E5E5E5; }
            QLabel { border: none; background: transparent; }
        """)
        layout_resumen = QVBoxLayout(card_resumen)
        layout_resumen.setContentsMargins(20, 20, 20, 20)
        
        lbl_pedido_titulo = QLabel("<b>Detalle del Pedido</b>")
        lbl_pedido_titulo.setStyleSheet("font-size: 16px; color: #1F2937;")
        layout_resumen.addWidget(lbl_pedido_titulo)
        
        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(5)
        self.tabla_carrito.setHorizontalHeaderLabels(["Plato", "Cant.", "P. Unit", "Subtotal", "Quitar"])
        self.tabla_carrito.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_carrito.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        # ❌ DESHABILITAR EDICIÓN EN LA TABLA
        self.tabla_carrito.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_carrito.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Solo seleccionar filas

        self.tabla_carrito.setStyleSheet("""
            QTableWidget { border: none; background-color: white; gridline-color: #F3F4F6; }
            QHeaderView::section { background-color: #F9FAFB; padding: 6px; font-weight: bold; border: none; }
        """)
        layout_resumen.addWidget(self.tabla_carrito)
        
        self.lbl_cant_articulos = QLabel("Items seleccionados: 0")
        self.lbl_cant_articulos.setStyleSheet("font-size: 14px; color: #4B5563; margin-top: 5px;")
        layout_resumen.addWidget(self.lbl_cant_articulos)
        
        self.lbl_total = QLabel("TOTAL: $0.00")
        self.lbl_total.setStyleSheet("font-size: 26px; font-weight: 900; color: #10B981; margin: 10px 0;")
        layout_resumen.addWidget(self.lbl_total)
        
        self.btn_cobrar = QPushButton("🖨️ Confirmar e Imprimir")
        self.btn_cobrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cobrar.setStyleSheet("""
            QPushButton { background-color: #2563EB; color: white; font-size: 16px; 
                          font-weight: bold; border-radius: 10px; padding: 14px; border: none; }
            QPushButton:hover { background-color: #1D4ED8; }
        """)
        self.btn_cobrar.clicked.connect(self.procesar_venta)
        layout_resumen.addWidget(self.btn_cobrar)

        self.btn_vaciar = QPushButton("Vaciar Todo")
        self.btn_vaciar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_vaciar.setStyleSheet("color: #EF4444; font-weight: bold; background: transparent; border: none; margin-top: 5px;")
        self.btn_vaciar.clicked.connect(self.limpiar_carrito)
        layout_resumen.addWidget(self.btn_vaciar, alignment=Qt.AlignmentFlag.AlignCenter)

        seccion_total.addWidget(card_resumen)

        layout_principal.addLayout(seccion_platos, stretch=3)
        layout_principal.addLayout(seccion_total, stretch=2)

        self.dibujar_cuadricula_platos()

    def dibujar_cuadricula_platos(self):
        """Consulta la base de datos y dibuja los botones del catálogo."""
        platos = self.plato_ctrl.obtener_todos()
        columnas_maximas = 2 
        
        for idx, plato in enumerate(platos):
            fila = idx // columnas_maximas
            columna = idx % columnas_maximas

            btn_plato = QPushButton()
            btn_plato.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_plato.setMinimumHeight(120)
            btn_plato.setStyleSheet("""
                QPushButton {
                    background-color: white; border: 1px solid #D1D5DB; border-radius: 12px;
                }
                QPushButton:hover { background-color: #EFF6FF; border: 2px solid #3B82F6; }
            """)
            
            btn_layout = QVBoxLayout(btn_plato)
            btn_layout.setContentsMargins(10, 10, 10, 10)
            
            lbl_texto_plato = QLabel(f"{plato.nombre}\n\n${plato.precio:.2f}")
            lbl_texto_plato.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_texto_plato.setWordWrap(True)
            lbl_texto_plato.setStyleSheet("font-size: 13px; font-weight: bold; color: #374151; border: none; background: transparent;")
            
            btn_layout.addWidget(lbl_texto_plato)
            
            btn_plato.clicked.connect(lambda checked, p=plato: self.agregar_al_carrito(p))
            self.grid_platos.addWidget(btn_plato, fila, columna)

    def actualizar_menu(self):
        """Limpia los botones obsoletos de la cuadrícula y redibuja el menú actualizado de la base de datos."""
        while self.grid_platos.count():
            item = self.grid_platos.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        self.dibujar_cuadricula_platos()

    def agregar_al_carrito(self, plato):
        if plato.id in self.carrito:
            self.carrito[plato.id]['cantidad'] += 1
        else:
            self.carrito[plato.id] = {'plato': plato, 'cantidad': 1}
        self.actualizar_interfaz_carrito()

    def eliminar_del_carrito(self, plato_id):
        if plato_id in self.carrito:
            if self.carrito[plato_id]['cantidad'] > 1:
                self.carrito[plato_id]['cantidad'] -= 1
            else:
                del self.carrito[plato_id]
        self.actualizar_interfaz_carrito()

    def actualizar_interfaz_carrito(self):
        self.tabla_carrito.setRowCount(0)
        total_acumulado = 0.0
        items_totales = 0

        for plato_id, item in self.carrito.items():
            plato = item['plato']
            cant = item['cantidad']
            subtotal = plato.precio * cant
            
            total_acumulado += subtotal
            items_totales += cant

            fila = self.tabla_carrito.rowCount()
            self.tabla_carrito.insertRow(fila)
            
            self.tabla_carrito.setItem(fila, 0, QTableWidgetItem(plato.nombre))
            self.tabla_carrito.setItem(fila, 1, QTableWidgetItem(str(cant)))
            self.tabla_carrito.setItem(fila, 2, QTableWidgetItem(f"${plato.precio:.2f}"))
            self.tabla_carrito.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))
            
            btn_eliminar = QPushButton("❌")
            btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_eliminar.setStyleSheet("""
                QPushButton {
                    background-color: #FEE2E2; color: #EF4444; border: none;
                    border-radius: 4px; padding: 4px 8px; font-weight: bold; font-size: 11px;
                }
                QPushButton:hover { background-color: #EF4444; color: white; }
            """)
            btn_eliminar.clicked.connect(lambda checked, pid=plato_id: self.eliminar_del_carrito(pid))
            self.tabla_carrito.setCellWidget(fila, 4, btn_eliminar)

        self.lbl_cant_articulos.setText(f"Items seleccionados: {items_totales}")
        self.lbl_total.setText(f"TOTAL: ${total_acumulado:.2f}")

    def procesar_venta(self):
        if not self.carrito:
            QMessageBox.warning(self, "Carrito Vacío", "No puedes registrar una venta sin platos.")
            return

        total_venta = sum(item['plato'].precio * item['cantidad'] for item in self.carrito.values())
        fecha_actual = datetime.now()
        
        nueva_venta = Venta(id=0, fecha_hora=fecha_actual, total=total_venta)
        
        for item in self.carrito.values():
            plato = item['plato']
            detalle = DetalleVenta(
                id=0, venta_id=0, plato_id=plato.id,
                cantidad=item['cantidad'], precio_unitario=plato.precio
            )
            nueva_venta.detalles.append(detalle)

        nro_ticket_diario = self.venta_ctrl.registrar_venta(nueva_venta)
        
        if nro_ticket_diario > 0:
            self.imprimir_ticket(nueva_venta, nro_ticket_diario)
            self.limpiar_carrito()
        else:
            QMessageBox.critical(self, "Error", "Ocurrió un problema en la BD al guardar la venta.")

    def generar_bloque_texto_ticket(self, tipo_copia: str, venta: Venta, ticket_diario: int) -> list:
        """Helper para construir las líneas individuales de cada copia conservando tu formato original."""
        lineas = []
        lineas.append("=========================================")
        lineas.append(f"            *** {tipo_copia} *** ")
        lineas.append("=========================================")
        lineas.append("         RESTAURANTE BUEN SABOR          ")
        lineas.append("=========================================")
        lineas.append(f"            *** TICKET N° {ticket_diario} *** ")
        lineas.append("=========================================")
        lineas.append(f"Fecha: {venta.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
        lineas.append("-----------------------------------------")
        lineas.append(f"{'Cant. Plato':<22} {'P.Unit':<8} {'Subtotal':<8}")
        lineas.append("-----------------------------------------")
        
        for item in self.carrito.values():
            plato = item['plato']
            cant = item['cantidad']
            sub = plato.precio * cant
            nombre_corto = plato.nombre[:18] 
            lineas.append(f"{cant}x {nombre_corto:<19} ${plato.precio:<7.2f} ${sub:<7.2f}")
            
        lineas.append("-----------------------------------------")
        lineas.append(f"TOTAL A PAGAR:                  ${venta.total:.2f}")
        lineas.append("=========================================")
        lineas.append("         ¡Gracias por su preferencia!     ")
        lineas.append("================================*********")
        lineas.append("\n✂ - - - - - - - - - - - - - - - - - - - ✂\n")
        return lineas

    def imprimir_ticket(self, venta: Venta, ticket_diario: int):
        """Genera el contenido en texto uniendo las 3 copias y despliega tu diálogo nativo original."""
        texto_ticket_completo = []
        
        # Unimos los 3 bloques seguidos uno tras otro en la misma tira
        texto_ticket_completo.extend(self.generar_bloque_texto_ticket("COPIA CAJA", venta, ticket_diario))
        texto_ticket_completo.extend(self.generar_bloque_texto_ticket("COPIA COCINA", venta, ticket_diario))
        texto_ticket_completo.extend(self.generar_bloque_texto_ticket("COPIA CLIENTE", venta, ticket_diario))
        
        # Añadimos unos saltos de línea finales para que el rollo avance y no se corte el último ticket
        texto_ticket_completo.append("\n\n\n")

        cuerpo_ticket = "\n".join(texto_ticket_completo)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialogo = QPrintDialog(printer, self)
        
        if dialogo.exec() == QPrintDialog.DialogCode.Accepted:
            documento = QTextDocument()
            fuente = QFont("Courier New", 10)
            documento.setDefaultFont(fuente)
            documento.setPlainText(cuerpo_ticket)
            documento.print(printer)
        else:
            print("Impresión cancelada por el usuario.")

    def limpiar_carrito(self):
        self.carrito.clear()
        self.actualizar_interfaz_carrito()