import os
import sys
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QInputDialog, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

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
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #F8FAFC;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(50, 40, 50, 50)

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
        layout_principal.addSpacing(40)

        # ─── CUADRÍCULA DE TARJETAS ───
        grid_cards = QGridLayout()
        grid_cards.setSpacing(35)

        # Configuración de botones indicando cuáles requieren protección (True = Protegido, False = Público)
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
            card.setMinimumHeight(340)
            
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(25, 25, 25, 25)
            card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_card = QLabel(titulo_card)
            lbl_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_card.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
            card_layout.addWidget(lbl_card)
            card_layout.addStretch()

            # Imagen
            lbl_imagen = QLabel()
            lbl_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_imagen.setStyleSheet("border: none; background: transparent; padding: 10px 0px;")
            ruta_foto = obtener_ruta_asset(f"assets/images/{nombre_imagen}")
            pixmap = QPixmap(ruta_foto)
            if not pixmap.isNull():
                lbl_imagen.setPixmap(pixmap.scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                card_layout.addWidget(lbl_imagen)
                card_layout.addStretch()

            # Botón
            btn_accion = QPushButton(texto_btn)
            btn_accion.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_accion.setMinimumWidth(200)
            btn_accion.setMinimumHeight(45)
            btn_accion.setStyleSheet("""
                QPushButton { background-color: #2563EB; color: white; border: none; border-radius: 10px; font-weight: 700; font-size: 13px; }
                QPushButton:hover { background-color: #1D4ED8; }
            """)
            
            # 🌟 Conexión inteligente pasándole los parámetros a nuestra función validadora
            btn_accion.clicked.connect(
                lambda checked, p_id=pantalla_id, req=requiere_admin: self.intentar_acceso(p_id, req)
            )
            
            card_layout.addWidget(btn_accion)
            grid_cards.addWidget(card, fila, columna)

        layout_principal.addLayout(grid_cards)

    # 🛡️ INTERCEPTOR DE SEGURIDAD
    def intentar_acceso(self, pantalla_id, requiere_admin):
        """ Valida la clave si el módulo lo requiere antes de dar acceso """
        if not requiere_admin:
            # Si es Nueva Venta o Ayuda, pasa directo
            self.stacked_widget.setCurrentIndex(pantalla_id)
            return

        # Si requiere admin, abrimos la ventana flotante oculta con asteriscos (••••)
        clave_ingresada, ok = QInputDialog.getText(
            self, 
            "Acceso Restringido", 
            "Ingrese la contraseña de Administrador:", 
            QLineEdit.EchoMode.Password
        )

        if ok and clave_ingresada:
            clave_real = leer_contrasena()  # Leemos directo el config.txt externo
            if clave_ingresada == clave_real:
                # ¡Clave correcta! Se le permite ingresar al módulo protegido
                self.stacked_widget.setCurrentIndex(pantalla_id)
            else:
                # Clave incorrecta
                QMessageBox.critical(self, "Error", "Contraseña incorrecta. Acceso denegado.")