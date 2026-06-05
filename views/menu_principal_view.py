from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

class MenuPrincipalView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # 🎨 Fondo General: Gris ultra claro y limpio (#F8FAFC) que reduce el cansancio visual
        self.setStyleSheet("background-color: #F8FAFC;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(50, 40, 50, 50)

        # ─── ENCABEZADO (Header) ───
        header_layout = QHBoxLayout()
        
        info_app_layout = QVBoxLayout()
        # Texto Principal en Gris Carbón Oscuro (#0F172A)
        lbl_titulo = QLabel("POS El Buen Sabor")
        lbl_titulo.setStyleSheet("font-size: 28px; font-weight: 800; color: #0F172A; background: transparent;")
        
        # Texto Secundario en Gris Medio (#64748B)
        lbl_subtitulo = QLabel("Menú de Ventas Interactivo")
        lbl_subtitulo.setStyleSheet("font-size: 14px; font-weight: 500; color: #64748B; background: transparent;")
        info_app_layout.addWidget(lbl_titulo)
        info_app_layout.addWidget(lbl_subtitulo)
        
        # Etiqueta de estatus estilizada con la paleta ejecutiva
        lbl_status = QLabel("Terminal Activa")
        lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_status.setStyleSheet("""
            background-color: #EFF6FF; 
            color: #2563EB; 
            border: 1px solid #E2E8F0; 
            border-radius: 20px; 
            padding: 6px 18px; 
            font-weight: 700; 
            font-size: 13px;
        """)
        
        header_layout.addLayout(info_app_layout)
        header_layout.addStretch()
        header_layout.addWidget(lbl_status, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        layout_principal.addLayout(header_layout)
        layout_principal.addSpacing(40)

        # ─── CUADRÍCULA DE TARJETAS (Grid Layout) ───
        grid_cards = QGridLayout()
        grid_cards.setSpacing(35)  # Más aire entre tarjetas para un look más moderno

        # Configuración optimizada con textos unificados usando Gris Carbón (#0F172A)
        botones_config = [
            ("VENTA", "NUEVA VENTA", 1),
            ("CONSULTA", "CONSULTAR", 2),
            ("HISTORIAL\nVENTAS", "VER VENTAS", 3),
            ("REPORTES", "VER REPORTES", 4),
            ("CONFIGURACIÓN", "CONFIGURAR", 5),
            ("AYUDA", "SOPORTE", 6)
        ]

        # Estilo premium para las Cards: fondo blanco puro, bordes sutiles redondeados
        estilo_tarjeta = """
            QWidget {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E2E8F0;
            }
        """

        for idx, (titulo_card, texto_btn, pantalla_id) in enumerate(botones_config):
            fila = idx // 3
            columna = idx % 3

            # Contenedor Blanco (La Card)
            card = QWidget()
            card.setStyleSheet(estilo_tarjeta)
            card.setMinimumHeight(240)
            
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(25, 35, 25, 35)
            card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Etiqueta del título interno de la Card en Gris Carbón Elegante
            lbl_card = QLabel(titulo_card)
            lbl_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_card.setStyleSheet("""
                font-size: 22px; 
                font-weight: 800; 
                color: #0F172A; 
                border: none; 
                background: transparent;
                letter-spacing: 1px;
            """)
            
            # Botón de Acción unificado: Azul Ejecutivo (#2563EB) con cambio dinámico a Azul Enérgico (#1D4ED8)
            btn_accion = QPushButton(texto_btn)
            btn_accion.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_accion.setMinimumWidth(200)
            btn_accion.setMinimumHeight(45)
            btn_accion.setStyleSheet("""
                QPushButton {
                    background-color: #2563EB; 
                    color: white; 
                    border: none; 
                    border-radius: 10px; 
                    padding: 10px; 
                    font-weight: 700; 
                    font-size: 13px;
                    letter-spacing: 0.5px;
                }
                QPushButton:hover {
                    background-color: #1D4ED8;
                }
            """)
            
            # Conservamos exactamente tu lógica original de navegación por índice
            btn_accion.clicked.connect(lambda checked, p_id=pantalla_id: self.stacked_widget.setCurrentIndex(p_id))

            card_layout.addWidget(lbl_card)
            card_layout.addStretch()
            card_layout.addWidget(btn_accion)

            grid_cards.addWidget(card, fila, columna)

        layout_principal.addLayout(grid_cards)