import os
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class AyudaView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #F3F4F6;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        
        # ⬅️ BOTÓN VOLVER (Obligatorio para que main.py conecte el clic de regreso)
        self.btn_volver = QPushButton("⬅ Volver al Menú Principal")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setStyleSheet("""
            QPushButton { background-color: #4B5563; color: white; font-weight: bold; 
                          border-radius: 8px; padding: 10px 15px; border: none; }
            QPushButton:hover { background-color: #1F2937; }
        """)
        layout_principal.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Título de la sección
        lbl_titulo = QLabel("Guía de Usuario - Paso a Paso")
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1F2937; margin: 15px 0;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(lbl_titulo)
        
        # Área de Scroll (Configurada para soportar contenido gigante)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        # Asegura que las barras de scroll aparezcan si la imagen supera la ventana
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        contenedor_pasos = QWidget()
        layout_pasos = QVBoxLayout(contenedor_pasos)
        layout_pasos.setSpacing(35)  # Más espacio entre tarjetas grandes
        layout_pasos.setContentsMargins(15, 15, 15, 15)
        
        # Obtener ruta de las imágenes
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
            
        ruta_imagenes = os.path.join(base_path, "assets", "images")
        
        # Renderizar consecutivamente de guia1.png a guia4.png
        for i in range(1, 5):
            nombre_archivo = f"guia{i}.png"
            ruta_completa = os.path.join(ruta_imagenes, nombre_archivo)
            
            card_paso = QWidget()
            card_paso.setStyleSheet("background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E5E5E5;")
            layout_card = QVBoxLayout(card_paso)
            layout_card.setContentsMargins(20, 20, 20, 20)
            
            lbl_subtitulo = QLabel(f"<b>Paso {i}</b>")
            lbl_subtitulo.setStyleSheet("font-size: 16px; color: #1F2937; border: none; background: transparent; font-weight: bold;")
            layout_card.addWidget(lbl_subtitulo)
            
            lbl_imagen = QLabel()
            lbl_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_imagen.setStyleSheet("border: none; background: transparent;")
            
            pixmap = QPixmap(ruta_completa)
            if not pixmap.isNull():
                # 🚀 CAMBIO CLAVE: Escalado aumentado a 1400 píxeles de ancho para máxima visibilidad
                lbl_imagen.setPixmap(pixmap.scaledToWidth(1400, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_imagen.setText(f"⚠️ Imagen faltante: {nombre_archivo}\nBúsquela en: {ruta_imagenes}")
                lbl_imagen.setStyleSheet("color: #EF4444; font-weight: bold; border: none; background: transparent; padding: 10px;")
                
            layout_card.addWidget(lbl_imagen)
            layout_pasos.addWidget(card_paso)
            
        scroll.setWidget(contenedor_pasos)
        layout_principal.addWidget(scroll)