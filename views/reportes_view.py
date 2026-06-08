from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QDate, QLocale  # 🌍 Se agrega QLocale para cambiar el idioma
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from controllers.reporte_controller import ReporteController

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.reporte_ctrl = ReporteController("database/RestauranteBuenSabor.db")
        self.init_ui()

    def init_ui(self):
        # Fondo General y forzado de color de texto base a negro absoluto (#000000)
        self.setStyleSheet("background-color: #F3F4F6; color: #000000;")
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(25, 25, 25, 25)
        layout_principal.setSpacing(15)

        # ⬅️ Encabezado superior de navegación
        layout_header = QHBoxLayout()
        self.btn_volver = QPushButton("⬅ Volver al Menú Principal")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setStyleSheet("""
            QPushButton { background-color: #4B5563; color: white; font-weight: bold; 
                          border-radius: 8px; padding: 10px 16px; border: none; }
            QPushButton:hover { background-color: #1F2937; }
        """)
        layout_header.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        
        lbl_status = QLabel("Módulo de Estadísticas")
        lbl_status.setStyleSheet("background-color: #FEF3C7; color: #92400E; font-weight: bold; padding: 6px 12px; border-radius: 20px;")
        layout_header.addWidget(lbl_status, alignment=Qt.AlignmentFlag.AlignRight)
        layout_principal.addLayout(layout_header)

        # Selector de Fecha para el reporte diario
        layout_filtro = QHBoxLayout()
        lbl_titulo = QLabel("📊 Reportes de Rendimiento Comercial")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #000000;")
        layout_filtro.addWidget(lbl_titulo)

        layout_fecha = QHBoxLayout()
        lbl_f = QLabel("Filtrar Día:")
        lbl_f.setStyleSheet("font-weight: bold; color: #000000; font-size: 14px;")
        
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())
        self.input_fecha.setStyleSheet("background-color: white; padding: 6px; border: 1px solid #D1D5DB; border-radius: 6px; color: #000000;")
        
        # 🌍 TRADUCCIÓN A ESPAÑOL DEL CALENDARIO:
        idioma_espanol = QLocale(QLocale.Language.Spanish, QLocale.Country.Spain)
        self.input_fecha.setLocale(idioma_espanol)
        
        self.input_fecha.dateChanged.connect(self.actualizar_reporte_del_dia)
        
        layout_fecha.addWidget(lbl_f)
        layout_fecha.addWidget(self.input_fecha)
        
        # 🛠️ CORRECCIÓN AQUÍ: Se añade el layout y luego se le da la alineación a la derecha
        layout_filtro.addLayout(layout_fecha)
        layout_filtro.setAlignment(layout_fecha, Qt.AlignmentFlag.AlignRight)
        
        layout_principal.addLayout(layout_filtro)

        # 📦 BLOQUE SUPERIOR: Distribución en Paralelo (Tabla vs Gráfico de Torta)
        layout_bloque_superior = QHBoxLayout()
        layout_bloque_superior.setSpacing(20)

        # Tabla resumen izquierda - Forzado de textos de celdas y cabeceras a negro (#000000)
        self.tabla_platos = QTableWidget()
        self.tabla_platos.setColumnCount(2)
        self.tabla_platos.setHorizontalHeaderLabels(["Plato / Producto", "Cant. Vendida"])
        self.tabla_platos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_platos.setStyleSheet("""
            QTableWidget { background-color: white; border-radius: 12px; border: 1px solid #E5E7EB; color: #000000; }
            QTableWidget::item { color: #000000; }
            QHeaderView::section { background-color: #F9FAFB; padding: 8px; font-weight: bold; border: none; color: #000000; }
        """)
        layout_bloque_superior.addWidget(self.tabla_platos, stretch=2)

        # Contenedor del Gráfico de Torta (Pastel) derecho
        self.cv_torta = QChartView()
        self.cv_torta.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.cv_torta.setStyleSheet("border: 1px solid #E5E7EB; border-radius: 12px; background-color: white;")
        layout_bloque_superior.addWidget(self.cv_torta, stretch=3)
        layout_principal.addLayout(layout_bloque_superior, stretch=4)

        # 📦 BLOQUE INFERIOR: Evolución de ventas semanal (Gráfico de Barras)
        self.cv_barras_semanal = QChartView()
        self.cv_barras_semanal.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.cv_barras_semanal.setStyleSheet("border: 1px solid #E5E7EB; border-radius: 12px; background-color: white;")
        layout_principal.addWidget(self.cv_barras_semanal, stretch=3)

        # Carga inicial de datos al abrir la pantalla
        self.actualizar_reporte_del_dia()
        self.dibujar_grafico_semanal()

    def actualizar_reporte_del_dia(self):
        """Lee la fecha seleccionada, llena la tabla y dibuja el gráfico circular."""
        fecha_texto = self.input_fecha.date().toString("yyyy-MM-dd")
        datos_platos = self.reporte_ctrl.obtener_platos_mas_vendidos_del_dia(fecha_texto)

        # 1. Poblar la tabla de datos
        self.tabla_platos.setRowCount(0)
        series_torta = QPieSeries()

        for nombre, cantidad in datos_platos:
            fila = self.tabla_platos.rowCount()
            self.tabla_platos.insertRow(fila)
            
            item_nombre = QTableWidgetItem(nombre)
            item_nombre.setForeground(QColor("#000000")) # Forzado a negro puro
            
            item_cantidad = QTableWidgetItem(f"{cantidad} unidades")
            item_cantidad.setForeground(QColor("#000000")) # Forzado a negro puro
            
            self.tabla_platos.setItem(fila, 0, item_nombre)
            self.tabla_platos.setItem(fila, 1, item_cantidad)
            
            # Añadir rebanada al gráfico circular
            series_torta.append(f"{nombre} ({cantidad})", cantidad)

        # 2. Configurar y renderizar el gráfico de torta
        chart_torta = QChart()
        chart_torta.addSeries(series_torta)
        chart_torta.setTitle(f"Porcentaje de Platos Consumidos el {self.input_fecha.date().toString('dd/MM/yyyy')}")
        
        # Estilos de textos del gráfico a negro
        chart_torta.setTitleBrush(QColor("#000000"))
        chart_torta.legend().setLabelColor(QColor("#000000"))
        
        chart_torta.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart_torta.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        
        if len(datos_platos) > 0:
            # Resaltamos visualmente el plato más vendido del día alejando un poco su rebanada
            rebanada_ganadora = series_torta.slices()[0]
            rebanada_ganadora.setExploded(True)
            rebanada_ganadora.setLabelVisible(True)
            rebanada_ganadora.setLabelBrush(QColor("#000000")) # Texto de etiqueta en negro

        self.cv_torta.setChart(chart_torta)

    def dibujar_grafico_semanal(self):
        """Genera el gráfico inferior de barras con los ingresos de los últimos 7 días con actividad."""
        datos_semana = self.reporte_ctrl.obtener_ventas_ultimos_7_dias()

        set_ingresos = QBarSet("Monto Recaudado ($)")
        set_ingresos.setLabelBrush(QColor("#000000")) # Texto de la leyenda en negro
        categorias = []

        for dia, total in datos_semana:
            set_ingresos.append(total)
            categorias.append(dia)

        series_barras = QBarSeries()
        series_barras.append(set_ingresos)

        chart_barras = QChart()
        chart_barras.addSeries(series_barras)
        chart_barras.setTitle("Flujo Financiero Semanal (Ingresos en los últimos días activos)")
        
        # Estilos de textos del gráfico a negro
        chart_barras.setTitleBrush(QColor("#000000"))
        chart_barras.legend().setLabelColor(QColor("#000000"))
        
        chart_barras.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # Eje X - Fechas
        axis_x = QBarCategoryAxis()
        axis_x.append(categorias)
        axis_x.setLabelsColor(QColor("#000000")) # Etiquetas del eje en negro
        chart_barras.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series_barras.attachAxis(axis_x)

        # Eje Y - Dinero
        axis_y = QValueAxis()
        axis_y.setLabelFormat("$%.2f")
        axis_y.setLabelsColor(QColor("#000000")) # Valores del eje en negro
        chart_barras.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series_barras.attachAxis(axis_y)

        self.cv_barras_semanal.setChart(chart_barras)

    def showEvent(self, event):
        """Garantiza que los gráficos e ingresos se refresquen de inmediato cada vez que el usuario entre a mirar."""
        super().showEvent(event)
        self.actualizar_reporte_del_dia()
        self.dibujar_grafico_semanal()