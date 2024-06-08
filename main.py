import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QBrush, QPainterPath
import random
import socks

class FallingSquare:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.speed = 1

    def move(self):
        self.y += self.speed

class FallingSquaresWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PROXYPROSE')
        self.setGeometry(100, 100, 800, 600)

        self.squares = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)

        self.proxy_ip_input = QLineEdit(self)
        self.proxy_ip_input.setGeometry(20, 20, 120, 30)
        self.proxy_ip_input.setPlaceholderText('IP прокси')

        self.proxy_port_input = QLineEdit(self)
        self.proxy_port_input.setGeometry(160, 20, 80, 30)
        self.proxy_port_input.setPlaceholderText('Порт')

        self.proxy_type_combobox = QComboBox(self)
        self.proxy_type_combobox.setGeometry(280, 20, 100, 30)
        self.proxy_type_combobox.addItems(['SOCKS4', 'SOCKS5', 'HTTP'])
        self.proxy_type_combobox.setCurrentText('SOCKS4')

        self.message_label = QLabel('', self)
        self.message_label.setGeometry(20, 60, 300, 30)

        connect_button = QPushButton('Подключиться', self)
        connect_button.setGeometry(20, 100, 120, 40)
        connect_button.clicked.connect(self.connect_to_proxy)

        check_button = QPushButton('Проверить прокси', self)
        check_button.setGeometry(160, 100, 120, 40)
        check_button.clicked.connect(self.check_proxy)

        search_button = QPushButton('Поиск прокси', self)
        search_button.setGeometry(300, 100, 120, 40)
        search_button.clicked.connect(self.search_proxy_in_file)

        # Атрибут для хранения текущего соединения
        self.socks_connection = None

    def connect_to_proxy(self):
        proxy_ip = self.proxy_ip_input.text()
        proxy_port = self.proxy_port_input.text()
        proxy_type = socks.SOCKS4 if self.proxy_type_combobox.currentText() == 'SOCKS4' else socks.SOCKS5

        if not proxy_ip or not proxy_port:
            self.message_label.setText('Введите IP и порт прокси')
            return

        # Закрываем предыдущее соединение, если оно существует
        if self.socks_connection:
            self.socks_connection.close()

        try:
            self.socks_connection = socks.socksocket()
            self.socks_connection.set_proxy(proxy_type, proxy_ip, int(proxy_port))
            self.socks_connection.connect(('google.com', 80))
            self.message_label.setText('Подключение к прокси...')
        except Exception as e:
            self.message_label.setText(f'Ошибка при подключении к прокси: {str(e)}')

    def check_proxy(self):
        proxy_ip = self.proxy_ip_input.text()
        proxy_port = self.proxy_port_input.text()
        proxy_type = socks.SOCKS4 if self.proxy_type_combobox.currentText() == 'SOCKS4' else socks.SOCKS5

        if not proxy_ip or not proxy_port:
            self.message_label.setText('Введите IP и порт прокси')
            return

        try:
            socks.setdefaultproxy(proxy_type, proxy_ip, int(proxy_port))
            socket = socks.socksocket()
            socket.connect(('google.com', 80))
            socket.close()
            QMessageBox.information(self, 'Результат проверки', 'Прокси работает корректно.')
        except Exception as e:
            QMessageBox.critical(self, 'Результат проверки', f'Ошибка при проверке прокси: {str(e)}')

    def search_proxy_in_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '.', 'Текстовые файлы (*.txt)')
        if not filename:
            return

        with open(filename, 'r') as file:
            proxies = file.readlines()

        if proxies:
            proxy = random.choice(proxies).strip().split(':')
            if len(proxy) == 2:
                self.proxy_ip_input.setText(proxy[0])
                self.proxy_port_input.setText(proxy[1])
                self.message_label.setText('Прокси найден в файле')
            else:
                self.message_label.setText('Неверный формат прокси в файле')
        else:
            self.message_label.setText('Файл с прокси пуст')

    def update_animation(self):
        self.generate_square()
        self.move_squares()
        self.update()

    def generate_square(self):
        if random.random() < 0.05:  # Шанс создания нового квадратика
            x = random.randint(0, self.width())
            y = 0
            square = FallingSquare(x, y)
            self.squares.append(square)

    def move_squares(self):
        for square in self.squares:
            square.move()
            if square.y > self.height():  # Удалить квадратик, если он вышел за пределы окна
                self.squares.remove(square)

    def paintEvent(self, event):
        painter = QPainter(self)
        for square in self.squares:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(0, 255, 0, 128)))  # Зеленый цвет, немного прозрачный
            path = QPainterPath()
            path.addRoundedRect(square.x, square.y, square.size, square.size, 10, 10)  # Заокругленные края
            painter.drawPath(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FallingSquaresWindow()
    window.show()
    sys.exit(app.exec_())
