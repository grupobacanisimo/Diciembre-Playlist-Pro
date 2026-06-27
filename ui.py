from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QListWidget, QLabel,
    QLineEdit, QSpinBox, QMessageBox
)

import sys
from generator import PlaylistGenerator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Diciembre Playlist Pro")
        self.setGeometry(200, 200, 600, 500)

        self.folders = {}
        self.sequence = []

        self.generator = PlaylistGenerator({})

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Diciembre Playlist Pro")
        layout.addWidget(self.label)

        self.list_folders = QListWidget()
        layout.addWidget(self.list_folders)

        self.btn_add_folder = QPushButton("Agregar carpeta")
        self.btn_add_folder.clicked.connect(self.add_folder)
        layout.addWidget(self.btn_add_folder)

        self.sequence_input = QLineEdit()
        self.sequence_input.setPlaceholderText("Ej: Parranda,Parranda,ID,Tropical")
        layout.addWidget(self.sequence_input)

        self.total_items = QSpinBox()
        self.total_items.setRange(10, 100000)
        self.total_items.setValue(100)
        layout.addWidget(self.total_items)

        self.btn_generate = QPushButton("Generar Playlist")
        self.btn_generate.clicked.connect(self.generate)
        layout.addWidget(self.btn_generate)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder:
            name = folder.split("/")[-1]
            self.folders[name] = folder
            self.list_folders.addItem(f"{name} -> {folder}")

    def generate(self):
        sequence = [x.strip() for x in self.sequence_input.text().split(",") if x.strip()]

        if not sequence:
            QMessageBox.warning(self, "Error", "Debes ingresar una secuencia")
            return

        output_file = QFileDialog.getSaveFileName(
            self, "Guardar playlist", "", "M3U Files (*.m3u)"
        )[0]

        if not output_file:
            return

        playlist = self.generator.generate(
            sequence,
            self.folders,
            output_file,
            self.total_items.value()
        )

        QMessageBox.information(
            self,
            "Listo",
            f"Playlist creada con {len(playlist)} canciones"
        )


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
