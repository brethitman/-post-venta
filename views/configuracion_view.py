from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from models.plato import Plato
from controllers.plato_controller import PlatoController

class ConfiguracionView(QWidget):
    def __init__(self):
        super().__init__()
        self.controlador = PlatoController("database/RestauranteBuenSabor.db")
        self.id_plato_seleccionado = None  # Se guarda el ID de forma invisible aquí abajo
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #F3F4F6;")
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(25, 25, 25, 25)
        layout_principal.setSpacing(15)

        # Encabezado superior de navegación
        layout_header = QHBoxLayout()
        self.btn_volver = QPushButton("⬅ Volver al Menú Principal")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setStyleSheet("""
            QPushButton { background-color: #4B5563; color: white; font-weight: bold; 
                          border-radius: 8px; padding: 10px 16px; border: none; }
            QPushButton:hover { background-color: #1F2937; }
        """)
        layout_header.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        
        lbl_status = QLabel("Módulo de Configuración")
        lbl_status.setStyleSheet("background-color: #E0F2FE; color: #0369A1; font-weight: bold; padding: 6px 12px; border-radius: 20px;")
        layout_header.addWidget(lbl_status, alignment=Qt.AlignmentFlag.AlignRight)
        layout_principal.addLayout(layout_header)

        layout_contenido = QHBoxLayout()
        layout_contenido.setSpacing(25)

        # ---------------------------------------------------------
        # FORMULARIO DE EDICIÓN (IZQUIERDA) - ¡SOLO NOMBRE Y PRECIO!
        # ---------------------------------------------------------
        form_panel = QWidget()
        form_panel.setStyleSheet("background-color: white; border-radius: 12px; border: 1px solid #E5E7EB;")
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(12)

        lbl_panel = QLabel("📋 Datos del Menú / Plato")
        lbl_panel.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F2937; border-bottom: 1px solid #E5E7EB; padding-bottom: 8px;")
        form_layout.addWidget(lbl_panel)
        
        form_layout.addWidget(QLabel("<b>Nombre del Plato:</b>"))
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ej: Asado de Tira con Papas")
        self.txt_nombre.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px;")
        form_layout.addWidget(self.txt_nombre)

        form_layout.addWidget(QLabel("<b>Precio de Venta ($):</b>"))
        self.txt_precio = QLineEdit()
        self.txt_precio.setPlaceholderText("Ej: 45.50")
        self.txt_precio.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px;")
        form_layout.addWidget(self.txt_precio)

        # Botones de acción
        self.btn_agregar = QPushButton("➕ Agregar como Nuevo")
        self.btn_agregar.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; padding: 10px; border-radius: 6px; border: none;")
        self.btn_agregar.clicked.connect(self.agregar_plato)
        form_layout.addWidget(self.btn_agregar)

        self.btn_editar = QPushButton("💾 Guardar Cambios")
        self.btn_editar.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; padding: 10px; border-radius: 6px; border: none;")
        self.btn_editar.clicked.connect(self.editar_plato)
        form_layout.addWidget(self.btn_editar)

        self.btn_eliminar = QPushButton("🗑️ Eliminar Plato Seleccionado")
        self.btn_eliminar.setStyleSheet("background-color: #EF4444; color: white; font-weight: bold; padding: 10px; border-radius: 6px; border: none;")
        self.btn_eliminar.clicked.connect(self.eliminar_plato)
        form_layout.addWidget(self.btn_eliminar)

        self.btn_limpiar = QPushButton("🧹 Limpiar Formulario")
        self.btn_limpiar.setStyleSheet("background-color: #F3F4F6; color: #4B5563; padding: 8px; border-radius: 6px; border: 1px solid #D1D5DB;")
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        form_layout.addWidget(self.btn_limpiar)
        
        form_layout.addStretch()
        layout_contenido.addWidget(form_panel, stretch=1)

        # ---------------------------------------------------------
        # TABLA DE PRODUCTOS (DERECHA)
        # ---------------------------------------------------------
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID Sistema", "Descripción del Plato", "Precio Unitario"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setStyleSheet("""
            QTableWidget { background-color: white; border-radius: 12px; border: 1px solid #E5E7EB; }
            QHeaderView::section { background-color: #F9FAFB; padding: 8px; font-weight: bold; border: none; color: #4B5563; }
        """)
        self.tabla.itemSelectionChanged.connect(self.cargar_plato_seleccionado)
        
        layout_contenido.addWidget(self.tabla, stretch=2)
        layout_principal.addLayout(layout_contenido)

        self.listar_platos()

    def listar_platos(self):
        self.tabla.itemSelectionChanged.disconnect(self.cargar_plato_seleccionado)
        self.tabla.setRowCount(0)
        platos = self.controlador.obtener_todos()
        
        for fila, plato in enumerate(platos):
            self.tabla.insertRow(fila)
            item_id = QTableWidgetItem(str(plato.id))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.tabla.setItem(fila, 0, item_id)
            self.tabla.setItem(fila, 1, QTableWidgetItem(plato.nombre))
            self.tabla.setItem(fila, 2, QTableWidgetItem(f"${plato.precio:.2f}"))
            
        self.tabla.itemSelectionChanged.connect(self.cargar_plato_seleccionado)

    def cargar_plato_seleccionado(self):
        filas_seleccionadas = self.tabla.selectedItems()
        if not filas_seleccionadas:
            return
        
        # Recuperamos el ID de la tabla para saber a cuál editar/borrar
        self.id_plato_seleccionado = filas_seleccionadas[0].text()
        self.txt_nombre.setText(filas_seleccionadas[1].text())
        
        precio_limpio = filas_seleccionadas[2].text().replace("$", "")
        self.txt_precio.setText(precio_limpio)

    def agregar_plato(self):
        nombre = self.txt_nombre.text().strip()
        precio_txt = self.txt_precio.text().strip()

        if not nombre or not precio_txt:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor ingresa un nombre y un precio.")
            return

        try:
            # El ID va como None temporalmente; el controlador lo creará automáticamente en la BD
            nuevo_plato = Plato(id=None, nombre=nombre, precio=float(precio_txt))
            if self.controlador.insertar(nuevo_plato):
                QMessageBox.information(self, "Éxito", f"'{nombre}' se agregó al menú.")
                self.limpiar_campos()
                self.listar_platos()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar en la base de datos.")
        except ValueError:
            QMessageBox.warning(self, "Formato Incorrecto", "El precio debe ser un número decimal válido.")

    def editar_plato(self):
        if self.id_plato_seleccionado is None:
            QMessageBox.warning(self, "Aviso", "Selecciona un plato de la lista derecha para editar.")
            return

        nombre = self.txt_nombre.text().strip()
        precio_txt = self.txt_precio.text().strip()

        try:
            plato_editado = Plato(id=self.id_plato_seleccionado, nombre=nombre, precio=float(precio_txt))
            if self.controlador.actualizar(plato_editado):
                QMessageBox.information(self, "Modificado", "Cambios aplicados con éxito.")
                self.limpiar_campos()
                self.listar_platos()
        except ValueError:
            QMessageBox.warning(self, "Formato Incorrecto", "El precio debe ser un número decimal válido.")

    def eliminar_plato(self):
        if self.id_plato_seleccionado is None:
            QMessageBox.warning(self, "Aviso", "Selecciona el plato que deseas dar de baja.")
            return

        confirmar = QMessageBox.question(
            self, "Confirmar Baja", 
            "¿Seguro que deseas eliminar este artículo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmar == QMessageBox.StandardButton.Yes:
            if self.controlador.eliminar(self.id_plato_seleccionado):
                self.limpiar_campos()
                self.listar_platos()

    def limpiar_campos(self):
        self.id_plato_seleccionado = None
        self.txt_nombre.clear()
        self.txt_precio.clear()
        self.tabla.clearSelection()