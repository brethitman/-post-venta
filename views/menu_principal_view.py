import os
import sys
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QPushButton, 
                             QLabel, QHBoxLayout, QInputDialog, QLineEdit, 
                             QMessageBox, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QResizeEvent

# 🛠️ FUNCIONES DE GESTIÓN DE CONTRASEÑA (ARCHIVO DE TEXTO EXTERNO)
def obtener_ruta_config():
    """ Apunta a la carpeta física real donde corre el script o el archivo .exe """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        # Sube un nivel desde 'views/' para ir a la raíz del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "config.txt")

def leer_contrasena():
    ruta = obtener_ruta_config()
    # Si el archivo no existe en la PC del cliente, lo creamos con la clave inicial '1234'
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("1234")
        return "1234"
    
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read().strip()


def obtener_ruta_asset(ruta_relativa):
    """ Devuelve la ruta absoluta para recursos internos (imágenes de la carpeta assets) """
    if getattr(sys, 'frozen', False):
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    return os.path.join(base_dir, ruta_relativa)


class MenuPrincipalView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.cards_imagenes = [] # Guardaremos las referencias para redimensionarlas elásticamente
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #F8FAFC;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30) # Márgenes ligeramente reducidos para pantallas chicas

        # ─── ENCABEZADO (Header) ───
        header_layout = QHBoxLayout()
        info_app_layout = QVBoxLayout()
        lbl_titulo = QLabel("POS El Buen Sabor")
        lbl_titulo.setStyleSheet("font-size: 28px; font-weight: 800; color: #0F172A; background: transparent;")
        
        lbl_subtitulo = QLabel("Menú de Ventas Interactivo")
        lbl_subtitulo.setStyleSheet("font-size: 14px; font-weight: 500; color: #64748B; background: transparent;")
        info_app_layout.addWidget(lbl_titulo)
        info_app_layout.addWidget(lbl_subtitulo)
        
        lbl_status = QLabel("Terminal Activa")
        lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_status.setStyleSheet("""
            background-color: #EFF6FF; color: #2563EB; border: 1px solid #E2E8F0; 
            border-radius: 20px; padding: 6px 18px; font-weight: 700; font-size: 13px;
        """)
        header_layout.addLayout(info_app_layout)
        header_layout.addStretch()
        header_layout.addWidget(lbl_status, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        layout_principal.addLayout(header_layout)
        layout_principal.addSpacing(20)

        # ─── CUADRÍCULA DE TARJETAS ELÁSTICA ───
        grid_cards = QGridLayout()
        grid_cards.setSpacing(25) # Espaciado optimizado para que no se encima

        # Configuramos el estiramiento elástico de las 3 columnas (0, 1, 2) y 2 filas (0, 1)
        for i in range(3):
            grid_cards.setColumnStretch(i, 1)
        for i in range(2):
            grid_cards.setRowStretch(i, 1)

        botones_config = [
            ("VENTA", "NUEVA VENTA", 1, "venta.png", False),
            ("CONSULTA", "CONSULTAR", 2, "consulta.png", True),
            ("HISTORIAL\nVENTAS", "VER VENTAS", 3, "listar.png", True),
            ("REPORTES", "VER REPORTES", 4, "reportes.png", True),
            ("CONFIGURACIÓN", "CONFIGURAR", 5, "configurar.png", True),
            ("AYUDA", "SOPORTE", 6, "ayuda.png", False)
        ]

        estilo_tarjeta = "QWidget { background-color: #FFFFFF; border-radius: 16px; border: 1px solid #E2E8F0; }"

        for idx, (titulo_card, texto_btn, pantalla_id, nombre_imagen, requiere_admin) in enumerate(botones_config):
            fila = idx // 3
            columna = idx % 3

            card = QWidget()
            card.setStyleSheet(estilo_tarjeta)
            
            # El secreto: En lugar de un tamaño fijo, le decimos que se expanda en ambas direcciones
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            card.setMinimumHeight(220) # Un mínimo seguro para pantallas muy pequeñas de laptops

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_card = QLabel(titulo_card)
            lbl_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_card.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
            card_layout.addWidget(lbl_card)
            card_layout.addStretch()

            # Imagen adaptable
            lbl_imagen = QLabel()
            lbl_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_imagen.setStyleSheet("border: none; background: transparent;")
            ruta_foto = obtener_ruta_asset(f"assets/images/{nombre_imagen}")
            pixmap = QPixmap(ruta_foto)
            
            if not pixmap.isNull():
                # Guardamos la referencia y el pixmap original para poder redimensionarlo en el evento resize
                lbl_imagen.setPixmap(pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                card.setProperty("original_pixmap", pixmap)
                card.setProperty("label_imagen", lbl_imagen)
                self.cards_imagenes.append(card)
                
            card_layout.addWidget(lbl_imagen)
            card_layout.addStretch()

            # Botón elástico
            btn_accion = QPushButton(texto_btn)
            btn_accion.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_accion.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn_accion.setMaximumWidth(260) # Que no se vuelva gigante horizontalmente en pantallas muy grandes
            btn_accion.setMinimumHeight(40)
            btn_accion.setStyleSheet("""
                QPushButton { background-color: #2563EB; color: white; border: none; border-radius: 10px; font-weight: 700; font-size: 13px; }
                QPushButton:hover { background-color: #1D4ED8; }
            """)
            
            btn_accion.clicked.connect(
                lambda checked, p_id=pantalla_id, req=requiere_admin: self.intentar_acceso(p_id, req)
            )
            
            card_layout.addWidget(btn_accion, alignment=Qt.AlignmentFlag.AlignCenter)
            grid_cards.addWidget(card, fila, columna)

        layout_principal.addLayout(grid_cards)

    def resizeEvent(self, event: QResizeEvent):
        """ Evento nativo de PyQt que detecta cuando la ventana cambia de tamaño """
        super().resizeEvent(event)
        # Redimensionamos de forma inteligente las imágenes según el espacio real disponible en la tarjeta
        for card in self.cards_imagenes:
            pixmap = card.property("original_pixmap")
            lbl_imagen = card.property("label_imagen")
            if pixmap and lbl_imagen:
                # Calculamos un tamaño proporcional basado en la altura actual de la tarjeta
                nuevo_alto = max(50, min(100, int(card.height() * 0.25)))
                lbl_imagen.setPixmap(pixmap.scaled(nuevo_alto, nuevo_alto, 
                                                   Qt.AspectRatioMode.KeepAspectRatio, 
                                                   Qt.TransformationMode.SmoothTransformation))

    # 🛡️ INTERCEPTOR DE SEGURIDAD
    def intentar_acceso(self, pantalla_id, requiere_admin):
        """ Valida la clave si el módulo lo requiere antes de dar acceso """
        if not requiere_admin:
            self.stacked_widget.setCurrentIndex(pantalla_id)
            return

        clave_ingresada, ok = QInputDialog.getText(
            self, 
            "Acceso Restringido", 
            "Ingrese la contraseña de Administrador:", 
            QLineEdit.EchoMode.Password
        )

        if ok and clave_ingresada:
            clave_real = leer_contrasena()
            if clave_ingresada == clave_real:
                self.stacked_widget.setCurrentIndex(pantalla_id)
            else:
                QMessageBox.critical(self, "Error", "Contraseña incorrecta. Acceso denegado.")