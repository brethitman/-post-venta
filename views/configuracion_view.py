import os
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from models.plato import Plato
from controllers.plato_controller import PlatoController

# 🛠️ FUNCIONES DE ENTORNO PARA EL .EXE (RUTAS MÁGICAS)
def obtener_ruta_config(nombre_archivo="config.txt"):
    """ Apunta a la carpeta física real donde corre el script o el archivo .exe """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        # Sube un nivel desde 'views/' para ir a la raíz del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, nombre_archivo)

def leer_contrasena():
    ruta = obtener_ruta_config("config.txt")
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("1234")
        return "1234"
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read().strip()


class ConfiguracionView(QWidget):
    def __init__(self):
        super().__init__()
        # 🛠️ CORRECCIÓN EXECUTABLE: Dejamos el constructor vacío. El controlador
        # buscará de forma autónoma la BD en la raíz del entorno ejecutable.
        self.controlador = PlatoController()
        
        self.id_plato_seleccionado = None  
        self.init_ui()

    def init_ui(self):
        # Fondo General y forzado de color base de texto a negro absoluto (#000000)
        self.setStyleSheet("background-color: #F3F4F6; color: #000000;")
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
        
        lbl_status = QLabel("Módulo de Configuración General")
        lbl_status.setStyleSheet("background-color: #E0F2FE; color: #0369A1; font-weight: bold; padding: 6px 12px; border-radius: 20px;")
        layout_header.addWidget(lbl_status, alignment=Qt.AlignmentFlag.AlignRight)
        layout_principal.addLayout(layout_header)

        # ─── CONTENIDO DIVIDIDO EN DOS COLUMNAS (Platos) ───
        layout_contenido = QHBoxLayout()
        layout_contenido.setSpacing(25)

        # FORMULARIO DE EDICIÓN DE PLATOS (IZQUIERDA)
        form_panel = QWidget()
        # Se forza color: #000000 a todos los QLabels y elementos de este panel
        form_panel.setStyleSheet("""
            QWidget { background-color: white; border-radius: 12px; border: 1px solid #E5E7EB; color: #000000; }
            QLabel { color: #000000; border: none; background: transparent; }
        """)
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(12)

        lbl_panel = QLabel("📋 Datos del Menú / Plato")
        lbl_panel.setStyleSheet("font-size: 16px; font-weight: bold; color: #000000; border-bottom: 1px solid #E5E7EB; padding-bottom: 8px;")
        form_layout.addWidget(lbl_panel)
        
        form_layout.addWidget(QLabel("<b>Nombre del Plato:</b>"))
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ej: Asado de Tira con Papas")
        self.txt_nombre.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; background-color: #FFFFFF; color: #000000;")
        form_layout.addWidget(self.txt_nombre)

        form_layout.addWidget(QLabel("<b>Precio de Venta ($):</b>"))
        self.txt_precio = QLineEdit()
        self.txt_precio.setPlaceholderText("Ej: 45.50")
        self.txt_precio.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; background-color: #FFFFFF; color: #000000;")
        form_layout.addWidget(self.txt_precio)

        # Botones de acción del menú
        self.btn_agregar = QPushButton("➕ Agregar como Nuevo")
        self.btn_agregar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_agregar.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; padding: 10px; border-radius: 6px; border: none;")
        self.btn_agregar.clicked.connect(self.agregar_plato)
        form_layout.addWidget(self.btn_agregar)

        self.btn_editar = QPushButton("💾 Guardar Cambios")
        self.btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_editar.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; padding: 10px; border-radius: 6px; border: none;")
        self.btn_editar.clicked.connect(self.editar_plato)
        form_layout.addWidget(self.btn_editar)

        self.btn_eliminar = QPushButton("🗑️ Eliminar Plato Seleccionado")
        self.btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_eliminar.setStyleSheet("background-color: #EF4444; color: white; font-weight: bold; padding: 10px; border-radius: 6px; border: none;")
        self.btn_eliminar.clicked.connect(self.eliminar_plato)
        form_layout.addWidget(self.btn_eliminar)

        self.btn_limpiar = QPushButton("🧹 Limpiar Formulario")
        self.btn_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_limpiar.setStyleSheet("background-color: #F3F4F6; color: #000000; padding: 8px; border-radius: 6px; border: 1px solid #D1D5DB; font-weight: bold;")
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        form_layout.addWidget(self.btn_limpiar)
        
        form_layout.addStretch()
        layout_contenido.addWidget(form_panel, stretch=1)

        # TABLA DE PRODUCTOS (DERECHA)
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID Sistema", "Descripción del Plato", "Precio Unitario"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # 🔒 CONFIGURACIÓN VISUAL: Deshabilita disparadores de edición integrados en las celdas
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Forzado de textos de cabecera y celdas internas de la tabla a negro puro (#000000)
        self.tabla.setStyleSheet("""
            QTableWidget { background-color: white; border-radius: 12px; border: 1px solid #E5E7EB; color: #000000; }
            QTableWidget::item { color: #000000; }
            QHeaderView::section { background-color: #F9FAFB; padding: 8px; font-weight: bold; border: none; color: #000000; }
        """)
        self.tabla.itemSelectionChanged.connect(self.cargar_plato_seleccionado)
        
        layout_contenido.addWidget(self.tabla, stretch=2)
        layout_principal.addLayout(layout_contenido)

        # ─── FORMULARIO CAMBIO DE CONTRASEÑA (ABAJO) ───
        pass_panel = QWidget()
        pass_panel.setStyleSheet("""
            QWidget { background-color: white; border-radius: 12px; border: 1px solid #E5E7EB; color: #000000; }
            QLabel { color: #000000; }
        """)
        pass_layout = QVBoxLayout(pass_panel)
        pass_layout.setContentsMargins(20, 15, 20, 15)

        lbl_pass_titulo = QLabel("🔐 Seguridad del Sistema (Cambiar Contraseña de Administrador)")
        lbl_pass_titulo.setStyleSheet("font-size: 15px; font-weight: bold; color: #000000; padding-bottom: 5px;")
        pass_layout.addWidget(lbl_pass_titulo)

        inputs_layout = QHBoxLayout()
        inputs_layout.setSpacing(15)

        # Estilo forzado para que el texto ingresado de los passwords sea negro puro
        estilo_txt_pass = "padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; background-color: #F9FAFB; color: #000000;"

        self.txt_pass_actual = QLineEdit()
        self.txt_pass_actual.setPlaceholderText("Contraseña Actual")
        self.txt_pass_actual.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass_actual.setStyleSheet(estilo_txt_pass)
        inputs_layout.addWidget(self.txt_pass_actual)

        self.txt_pass_nueva = QLineEdit()
        self.txt_pass_nueva.setPlaceholderText("Nueva Contraseña")
        self.txt_pass_nueva.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass_nueva.setStyleSheet(estilo_txt_pass)
        inputs_layout.addWidget(self.txt_pass_nueva)

        self.txt_pass_confirmar = QLineEdit()
        self.txt_pass_confirmar.setPlaceholderText("Confirmar Nueva Contraseña")
        self.txt_pass_confirmar.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass_confirmar.setStyleSheet(estilo_txt_pass)
        inputs_layout.addWidget(self.txt_pass_confirmar)

        btn_cambiar_pass = QPushButton("Actualizar Clave")
        btn_cambiar_pass.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cambiar_pass.setStyleSheet("""
            QPushButton { background-color: #1F2937; color: white; font-weight: bold; padding: 8px 20px; border-radius: 6px; border: none; }
            QPushButton:hover { background-color: #0F172A; }
        """)
        btn_cambiar_pass.clicked.connect(self.procesar_cambio_clave)
        inputs_layout.addWidget(btn_cambiar_pass)

        pass_layout.addLayout(inputs_layout)
        layout_principal.addWidget(pass_panel)

        # Renderizar la tabla de platos al inicio
        self.listar_platos()

    # ─── MÉTODOS DEL CONTROL DE PLATOS ───
    def listar_platos(self):
        self.tabla.itemSelectionChanged.disconnect(self.cargar_plato_seleccionado)
        self.tabla.setRowCount(0)
        platos = self.controlador.obtener_todos()
        
        for fila, plato in enumerate(platos):
            self.tabla.insertRow(fila)
            
            item_id = QTableWidgetItem(str(plato.id))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_id.setForeground(Qt.GlobalColor.black) # Texto dinámico forzado a negro
            
            item_nombre = QTableWidgetItem(plato.nombre)
            item_nombre.setForeground(Qt.GlobalColor.black) # Texto dinámico forzado a negro
            
            item_precio = QTableWidgetItem(f"${plato.precio:.2f}")
            item_precio.setForeground(Qt.GlobalColor.black) # Texto dinámico forzado a negro
            
            self.tabla.setItem(fila, 0, item_id)
            self.tabla.setItem(fila, 1, item_nombre)
            self.tabla.setItem(fila, 2, item_precio)
            
        self.tabla.itemSelectionChanged.connect(self.cargar_plato_seleccionado)

    def cargar_plato_seleccionado(self):
        filas_seleccionadas = self.tabla.selectedItems()
        if not filas_seleccionadas:
            return
        
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

    # ─── PROCESAR EL CAMBIO DE CONTRASEÑA ───
    def procesar_cambio_clave(self):
        actual = self.txt_pass_actual.text()
        nueva = self.txt_pass_nueva.text()
        confirmar = self.txt_pass_confirmar.text()

        if not actual or not nueva or not confirmar:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor complete todas las casillas de contraseña.")
            return

        if actual != leer_contrasena():
            QMessageBox.critical(self, "Error", "La contraseña actual ingresada es incorrecta.")
            return

        if nueva != confirmar:
            QMessageBox.critical(self, "Error", "La nueva contraseña y la confirmación no coinciden.")
            return

        try:
            ruta = obtener_ruta_config("config.txt")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(nueva.strip())
                
            QMessageBox.information(self, "Éxito", "¡Contraseña del Administrador cambiada correctamente!")
            self.txt_pass_actual.clear()
            self.txt_pass_nueva.clear()
            self.txt_pass_confirmar.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la clave externa: {e}")