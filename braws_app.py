
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import psycopg2
from config import config

class VentanaInicioSesion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BRAWS POS BELEN")  # Cambia el título de la ventana
        self.setFixedSize(500, 400)  # Tamaño fijo de la ventana
        self.centrar_ventana()  # Función para centrar la ventana en la pantalla
        self.setWindowIcon(QIcon("braws_logo.png"))  # Establece el icono de la ventana

        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Alinea el contenido al centro

        # Etiqueta y campo de entrada para el nombre de usuario
        lbl_usuario = QLabel("Usuario:", self)
        lbl_usuario.setMaximumWidth(100)  # Establece el ancho máximo de la etiqueta
        layout.addWidget(lbl_usuario, 0, 0, Qt.AlignmentFlag.AlignRight)  # Agrega la etiqueta en la fila 0, columna 0 y la alinea a la derecha
        self.input_usuario = QLineEdit(self)
        layout.addWidget(self.input_usuario, 0, 1)  # Agrega el campo de entrada en la fila 0, columna 1

        # Etiqueta y campo de entrada para la contraseña
        lbl_contraseña = QLabel("Contraseña:", self)
        lbl_contraseña.setMaximumWidth(100)  # Establece el ancho máximo de la etiqueta
        layout.addWidget(lbl_contraseña, 1, 0, Qt.AlignmentFlag.AlignRight)  # Agrega la etiqueta en la fila 1, columna 0 y la alinea a la derecha
        self.input_contraseña = QLineEdit(self)
        self.input_contraseña.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_contraseña, 1, 1)  # Agrega el campo de entrada en la fila 1, columna 1

        # Botón de inicio de sesión
        btn_iniciar_sesion = QPushButton("Iniciar Sesión", self)
        btn_iniciar_sesion.setMaximumWidth(300)  # Establece el ancho máximo del botón
        layout.addWidget(btn_iniciar_sesion, 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)  # Agrega el botón en la fila 2, columnas 0 y 1 y lo centra
        btn_iniciar_sesion.clicked.connect(self.verificar_credenciales)
        self.input_contraseña.returnPressed.connect(self.verificar_credenciales)

    def centrar_ventana(self):
        # Obtiene la geometría de la pantalla y la geometría de la ventana
        pantalla_geo = QApplication.primaryScreen().availableGeometry()
        ventana_geo = self.frameGeometry()

        # Centra la ventana en la pantalla
        ventana_geo.moveCenter(pantalla_geo.center())
        self.move(ventana_geo.topLeft())

    def verificar_credenciales(self):
        usuario = self.input_usuario.text()
        contraseña = self.input_contraseña.text()

        # Consulta a la base de datos para verificar las credenciales
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Ejecuta la consulta para buscar las credenciales en la base de datos
        cur.execute("SELECT * FROM pos.master WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
        resultado = cur.fetchone()

        if resultado:
            mensaje = QMessageBox()
            mensaje.setWindowTitle("successful")
            mensaje.setText(f" ¡Bienvenido, {usuario}!")
            mensaje.setFixedSize(900,500)
            mensaje.setWindowIcon(QIcon("braws_logo.png"))
            mensaje.exec()

            # QMessageBox.about(self, "Sesion iniciada", f"¡Bienvenido, {usuario}!")
        
            self.hide()
            self.ventana_principal = VentanaPrincipal()
            self.ventana_principal.show()
        else:
            QMessageBox.warning(self, "Inicio de Sesión", "Usuario o contraseña incorrecta")

        # Cierra la conexión y el cursor
        cur.close()
        conn.close()

class VentanaPrincipal(QWidget):
     def __init__(self):
        super().__init__()
        self.setWindowTitle("BRAWS Punto de venta belen")
        self.setFixedSize(500, 400)
        self.centrar_ventana()

        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for i in range(2):
            for j in range(4):
                boton = QPushButton(f"Botón {i*4 + j + 1}", self)
                boton.setMaximumWidth(200)
                layout.addWidget(boton, i, j)

     def centrar_ventana(self):
        pantalla_geo = QApplication.primaryScreen().availableGeometry()
        ventana_geo = self.frameGeometry()
        ventana_geo.moveCenter(pantalla_geo.center())
        self.move(ventana_geo.topLeft())
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_inicio_sesion = VentanaInicioSesion()
    ventana_inicio_sesion.show()
    sys.exit(app.exec())
