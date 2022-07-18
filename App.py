import sys
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QTableWidgetItem, QPushButton, \
    QHBoxLayout, QGridLayout, QComboBox, QLabel, QSpinBox, QDoubleSpinBox, QMessageBox
from Generator import Generator
import pyqtgraph as pg
import numpy as np


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = 1500
        self.height = 700
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.title = 'Generator funkcyjny'
        self.setWindowTitle(self.title)

        layout = QGridLayout()
        layout2 = QHBoxLayout()
        App.setLayout(self, layout)
        App.setLayout(self, layout2)

        self.button = QPushButton('Narysuj wykres', self)
        self.button.clicked.connect(self.on_click)
        self.button.setFixedWidth(200)
        layout.addWidget(self.button, 1, 2)

        self.button2 = QPushButton('Zapisz wykres do pliku .csv', self)
        self.button2.clicked.connect(self.zapis_csv)
        self.button2.setFixedWidth(200)
        layout.addWidget(self.button2, 2, 2)

        self.button3 = QPushButton('Zapisz wykres do pliku .wav', self)
        self.button3.clicked.connect(self.zapis_wav)
        self.button3.setFixedWidth(200)
        layout.addWidget(self.button3, 3, 2)

        self.button4 = QPushButton('Zapisz transformate do pliku .csv', self)
        self.button4.clicked.connect(self.zapis_csv)
        self.button4.setFixedWidth(200)
        layout.addWidget(self.button4, 4, 2)

        self.combobox = QComboBox()
        self.combobox.addItem("Sine")
        self.combobox.addItem("Square")
        self.combobox.addItem("Triangle")
        self.combobox.addItem("Sawtooth")
        self.combobox.addItem("White noise")
        self.combobox.addItem("Sine + Sine")
        self.combobox.addItem("Square + Square")
        self.combobox.addItem("Triangle + Triangle")
        self.combobox.addItem("Sawtooth + Sawtooth")
        layout.addWidget(self.combobox, 0, 0)

        self.SpinBox = QSpinBox(self)
        layout.addWidget(self.SpinBox, 1, 1)
        self.SpinBox.setMaximum(100000)

        self.QDoubleSpinBox = QDoubleSpinBox(self)
        layout.addWidget(self.QDoubleSpinBox, 2, 1)
        self.QDoubleSpinBox.setMaximum(100000.0)

        self.QDoubleSpinBox2 = QDoubleSpinBox(self)
        layout.addWidget(self.QDoubleSpinBox2, 3, 1)
        self.QDoubleSpinBox2.setMaximum(100000.0)

        self.SpinBox2 = QSpinBox(self)
        layout.addWidget(self.SpinBox2, 4, 1)
        self.SpinBox2.setMaximum(100000)

        self.label = QLabel("Długość trwania przebiegu: ", self)
        layout.addWidget(self.label, 1, 0)

        self.label2 = QLabel("Amplituda: ", self)
        layout.addWidget(self.label2, 2, 0)

        self.label3 = QLabel("Częstotliwość przebiegu: ", self)
        layout.addWidget(self.label3, 3, 0)

        self.label4 = QLabel("Częstotliwość próbkowania: ", self)
        layout.addWidget(self.label4, 4, 0)

        self.label5 = QLabel("Zakres dziedziny przebiegu czasowego: ", self)
        layout.addWidget(self.label5, 1, 3)

        self.label6 = QLabel("Zakres dziedziny transformaty Fouriera: ", self)
        layout.addWidget(self.label6, 3, 3)

        self.QDoubleSpinBox3 = QDoubleSpinBox(self)
        self.QDoubleSpinBox3.setMaximum(100000.0)
        layout.addWidget(self.QDoubleSpinBox3, 2, 3)

        self.QDoubleSpinBox4 = QDoubleSpinBox(self)
        self.QDoubleSpinBox4.setMaximum(100000.0)
        layout.addWidget(self.QDoubleSpinBox4, 4, 3)

        self.QDoubleSpinBox5 = QDoubleSpinBox(self)
        layout.addWidget(self.QDoubleSpinBox5, 7, 0)
        self.QDoubleSpinBox5.setMaximum(100000.0)

        self.QDoubleSpinBox6 = QDoubleSpinBox(self)
        layout.addWidget(self.QDoubleSpinBox6, 7, 1)
        self.QDoubleSpinBox6.setMaximum(100000.0)

        self.QDoubleSpinBox7 = QDoubleSpinBox(self)
        layout.addWidget(self.QDoubleSpinBox7, 7, 2)
        self.QDoubleSpinBox7.setMaximum(100000.0)

        self.label7 = QLabel("Amplituda: ", self)
        layout.addWidget(self.label7, 6, 0)

        self.label8 = QLabel("Częstotliwość: ", self)
        layout.addWidget(self.label8, 6, 1)

        self.label9 = QLabel("Przesunięcie fazowe: ", self)
        layout.addWidget(self.label9, 6, 2)

        self.graph = pg.PlotWidget()
        f = self.QDoubleSpinBox2.value()
        a = self.QDoubleSpinBox.value()
        time = self.SpinBox.value()
        sampling = self.SpinBox2.value()
        generator = Generator(f, a, time, sampling)
        generator.sine()
        x = generator.t
        y = generator.y
        self.plot = self.graph.plot(x, y)

        self.graph.setLabel('left', text='<font size=15>Value</font>')
        self.graph.setLabel('bottom', text='<font size=15 > Time < / font > ')
        self.graph.setTitle('<font size=20>y(t)</font>')
        layout.addWidget(self.graph, 5, 0, 1, 2)

        pen = pg.mkPen(color=(255, 128, 0), width=1)
        self.graph2 = pg.PlotWidget()
        self.graph2.setLabel('left', text='<font size=15>Amplitude</font>')
        self.graph2.setLabel('bottom', text='<font size=15 > Frequency < / font > ')
        self.graph2.setTitle('<font size=20>Transformata Fouriera</font>')
        self.plot2 = self.graph2.plot(x, y, pen=pen)
        layout.addWidget(self.graph2, 5, 2, 1, 2)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Dziedzina"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Zbiór wartości"))
        layout.addWidget(self.table, 0, 4, 10, 2)

        global w
        w = self.QDoubleSpinBox6.value()

        self.show()

    def on_click(self):
        f = self.QDoubleSpinBox2.value()
        a = self.QDoubleSpinBox.value()
        time = self.SpinBox.value()
        sampling = self.SpinBox2.value()
        generator = Generator(f, a, time, sampling)

        if self.combobox.currentText() == "Sine":
            generator.sine()
        elif self.combobox.currentText() == "Square":
            generator.square()
        elif self.combobox.currentText() == "Triangle":
            generator.triangle()
        elif self.combobox.currentText() == "Sawtooth":
            generator.sawtooth()
        elif self.combobox.currentText() == "White noise":
            generator.white_noise()
        elif self.combobox.currentText() == "Sine + Sine":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 1)
        elif self.combobox.currentText() == "Square + Square":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 2)
        elif self.combobox.currentText() == "Triangle + Triangle":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 3)
        elif self.combobox.currentText() == "Sawtooth + Sawtooth":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 4)
        self.table.setRowCount(sampling)
        for i in range(sampling):
            self.table.setItem(i, 0, QTableWidgetItem(str(generator.t[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(generator.y[i])))
        x = generator.t
        y = generator.y
        xf, yf = generator.transformata_fouriera()
        self.graph2.setXRange(0, self.QDoubleSpinBox4.value())
        self.plot2.setData(xf, yf)
        self.graph.setXRange(0, self.QDoubleSpinBox3.value())
        self.plot.setData(x, y)

    def zapis_csv(self):
        sender = self.sender()
        f = self.QDoubleSpinBox2.value()
        a = self.QDoubleSpinBox.value()
        time = self.SpinBox.value()
        sampling = self.SpinBox2.value()
        generator = Generator(f, a, time, sampling)
        if self.combobox.currentText() == "Sine":
            generator.sine()
        elif self.combobox.currentText() == "Square":
            generator.square()
        elif self.combobox.currentText() == "Triangle":
            generator.triangle()
        elif self.combobox.currentText() == "Sawtooth":
            generator.sawtooth()
        elif self.combobox.currentText() == "White noise":
            generator.white_noise()
        elif self.combobox.currentText() == "Sine + Sine":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 1)
        elif self.combobox.currentText() == "Square + Square":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 2)
        elif self.combobox.currentText() == "Triangle + Triangle":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 3)
        elif self.combobox.currentText() == "Sawtooth + Sawtooth":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 4)


        if sender == self.button2:
            generator.zapis_csv("Wykres")
        elif sender == self.button4:
            generator.zapis_csv("TransformataF")


    def zapis_wav(self):
        f = self.QDoubleSpinBox2.value()
        a = self.QDoubleSpinBox.value()
        time = self.SpinBox.value()
        sampling = self.SpinBox2.value()
        generator = Generator(f, a, time, sampling)
        if self.combobox.currentText() == "Sine":
            generator.sine()
        elif self.combobox.currentText() == "Square":
            generator.square()
        elif self.combobox.currentText() == "Triangle":
            generator.triangle()
        elif self.combobox.currentText() == "Sawtooth":
            generator.sawtooth()
        elif self.combobox.currentText() == "White noise":
            generator.white_noise()
        elif self.combobox.currentText() == "Sine + Sine":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 1)
        elif self.combobox.currentText() == "Square + Square":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 2)
        elif self.combobox.currentText() == "Triangle + Triangle":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 3)
        elif self.combobox.currentText() == "Sawtooth + Sawtooth":
            generator.sum(self.QDoubleSpinBox5.value(), self.QDoubleSpinBox6.value(), self.QDoubleSpinBox7.value(), 4)
        generator.zapis_wav()


app = QApplication(sys.argv)
ex = App()
app.exec_()
