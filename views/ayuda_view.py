import os
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class AyudaView(QWidget):
    def __init__(self):
        super().__init__()
        # Lista para almacenar los pixmaps originales y sus etiquetas correspondientes
        self.imagenes_referencia = []
        self.init_ui()

    def init_ui(self):
        # Fondo General y forzado de color de texto base a negro absoluto (#000000)
        self.setStyleSheet("background-color: #F3F4F6; color: #000000;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        
        # ⬅️ BOTÓN VOLVER
        self.btn_volver = QPushButton("⬅ Volver al Menú Principal")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setStyleSheet("""
            QPushButton { background-color: #4B5563; color: white; font-weight: bold; 
                          border-radius: 8px; padding: 10px 15px; border: none; }
            QPushButton:hover { background-color: #1F2937; }
        """)
        layout_principal.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Título de la sección - Forzado a Negro Puro
        lbl_titulo = QLabel("Guía de Usuario - Paso a Paso")
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #000000; margin: 15px 0;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(lbl_titulo)
        
        # Área de Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        contenedor_pasos = QWidget()
        layout_pasos = QVBoxLayout(contenedor_pasos)
        layout_pasos.setSpacing(35)  # Espacio entre tarjetas grandes
        layout_pasos.setContentsMargins(15, 15, 15, 15)
        
        # 🛠️ SISTEMA DE DETECCIÓN MULTI-RUTA INTELIGENTE 🛠️
        if getattr(sys, 'frozen', False):
            # Si corre empaquetado como .exe
            base_path = os.path.dirname(sys.executable)
        else:
            # Si corre en modo desarrollo desde VS Code
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        # Intento 1: Buscar directamente al lado del ejecutable o script
        ruta_imagenes = os.path.join(base_path, "assets", "images")
        
        # Intento 2 (Respaldo): Si no existe ahí, busca un nivel arriba (útil si el .exe está dentro de 'output')
        if not os.path.exists(ruta_imagenes):
            ruta_imagenes = os.path.join(os.path.dirname(base_path), "assets", "images")
        
        # Renderizar consecutivamente de guia1.png a guia4.png
        for i in range(1, 5):
            nombre_archivo = f"guia{i}.png"
            ruta_completa = os.path.join(ruta_imagenes, nombre_archivo)
            
            card_paso = QWidget()
            card_paso.setStyleSheet("background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E5E5E5; color: #000000;")
            layout_card = QVBoxLayout(card_paso)
            layout_card.setContentsMargins(20, 20, 20, 20)
            
            lbl_subtitulo = QLabel(f"<b>Paso {i}</b>")
            lbl_subtitulo.setStyleSheet("font-size: 16px; color: #000000; border: none; background: transparent; font-weight: bold;")
            layout_card.addWidget(lbl_subtitulo)
            
            lbl_imagen = QLabel()
            lbl_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_imagen.setStyleSheet("border: none; background: transparent;")
            
            pixmap = QPixmap(ruta_completa)
            if not pixmap.isNull():
                # Guardamos la referencia para el escalado elástico posterior
                self.imagenes_referencia.append((lbl_imagen, pixmap))
            else:
                lbl_imagen.setText(f"⚠️ Imagen faltante: {nombre_archivo}\nBúsquela en: {ruta_imagenes}")
                # El texto alternativo de aviso de error ahora se configura en negro con fondo limpio
                lbl_imagen.setStyleSheet("color: #000000; font-weight: bold; border: none; background: transparent; padding: 10px;")
                
            layout_card.addWidget(lbl_imagen)
            layout_pasos.addWidget(card_paso)
            
        scroll.setWidget(contenedor_pasos)
        layout_principal.addWidget(scroll)

        # Forzar una llamada inicial al redimensionamiento para cargar las imágenes elásticas de inmediato
        self.actualizar_imagenes_elasticas()

    def actualizar_imagenes_elasticas(self):
        """Método auxiliar para aplicar el cálculo elástico de tamaño."""
        ancho_disponible = self.width() - 100 
        if ancho_disponible > 1400:
            ancho_disponible = 1400
            
        if ancho_disponible > 100:
            for lbl_imagen, pixmap in self.imagenes_referencia:
                lbl_imagen.setPixmap(pixmap.scaledToWidth(ancho_disponible, Qt.TransformationMode.SmoothTransformation))

    def resizeEvent(self, event):
        """ 
        Este evento se dispara de forma nativa cada vez que la aplicación cambia de tamaño,
        detectando la resolución de cualquier pantalla (PC o Laptop) de manera elástica.
        """
        super().resizeEvent(event)
        self.actualizar_imagenes_elasticas()