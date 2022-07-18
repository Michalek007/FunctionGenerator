from scipy.fft import fft
import matplotlib.pyplot as plt
import numpy as m
from scipy.io.wavfile import write
import pandas as pd


class Generator:
    def __init__(self, f, a, time, sampling):
        self.f = f
        self.a = a
        self.time = time
        self.z = 0.05
        self.sampling = sampling
        self.audio_data = m.int16(2 ** 15)
        self.y = []
        self.t = []

    def sine(self):
        self.t = m.linspace(0, self.time, self.time * self.sampling)
        self.y = self.a*m.sin(2*m.pi*self.f*self.t)
        self.audio_data = m.int16(self.y * 2 ** 15)

    def square(self):
        self.t = m.linspace(0, self.time, self.time * self.sampling)
        self.y = m.sign(self.a * m.sin(2 * m.pi * self.f * self.t))
        self.audio_data = m.int16(self.y * 2 ** 15)

    def triangle(self):
        self.t = m.linspace(0, self.time, self.time * self.sampling)
        self.y = (2*self.a/m.pi)*m.arcsin(m.sin(2*m.pi*self.f*self.t))
        self.audio_data = m.int16(self.y * 2 ** 15)

    def sawtooth(self):
        self.t = m.linspace(0, self.time, self.time * self.sampling)
        self.y = (2*self.a/m.pi)*m.arctan(m.tan(2*m.pi*self.f*self.t*0.5))
        self.audio_data = m.int16(self.y * 2 ** 15)

    def white_noise(self):
        # amp = 4
        self.t = m.linspace(0, self.time, self.time * self.sampling)
        n = m.random.rand(len(self.t))
        self.y = self.a * n
        # y = a*m.sin(2*m.pi*f*t) + amp * n
        self.audio_data = m.int16(self.y * 2 ** 15)

    def wykres(self):
        plt.plot(self.t, self.y)
        plt.xlim(0, self.z)
        plt.xlabel('t')
        plt.ylabel('y')
        return plt.show()

    def transformata_fouriera(self):
        N = len(self.t)
        dt = self.t[1] - self.t[0]
        yf = 2.0 / N * m.abs(fft(self.y)[0:N // 2])
        xf = m.fft.fftfreq(N, d=dt)[0:N // 2]
        return xf, yf

    def wykres_transformata_fouriera(self):
        N = len(self.t)
        dt = self.t[1] - self.t[0]
        yf = 2.0 / N * m.abs(fft(self.y)[0:N // 2])
        xf = m.fft.fftfreq(N, d=dt)[0:N // 2]
        plt.plot(xf, yf)
        plt.xlim(0, 1000)
        plt.xlabel("frequency (Hz)")
        plt.ylabel("amplitude")
        plt.grid()
        return plt.show()

    def zapis_wav(self):
        write('test.wav', self.sampling, self.audio_data)

    def zapis_csv(self, filename):
        data = {"t": self.t, "y": self.y}
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(filename, index=False, sep="\t")


def wybor(alimit, limit, message):
    print()
    print(message)
    print()
    while 1:
        try:
            value = int(input())
            if alimit < value < limit:
                break

            else:
                print('Podana wartość jest niepoprawna. Podaj wartość jeszcze raz.')

        except (ValueError, TypeError):
            print('Podana wartość jest niepoprawna. Podaj wartość jeszcze raz.')
    return value


def wybor_2(f, a, time, z, x):
    generator = Generator(f, a, time, z)
    if x == 1:
        generator.sine()
    elif x == 2:
        generator.square()
    elif x == 3:
        generator.triangle()
    elif x == 4:
        generator.sawtooth()
    elif x == 5:
        generator.white_noise()

    mode = wybor(0, 3, "Wybierz jedną z poniższych opcji:\n \nZapisanie wykresu[1]      Obliczenie transofrmaty Fouriera[2]")
    if mode == 1:
        zgoda = str(input('Czy chcesz zapisać wykres funkcji do pliku csv? tak/nie '))
        print()

        if zgoda == "tak":
            filename = str(input('Podaj nazwę pliku: '))
            print()
            generator.zapis_csv(filename)
        else:
            pass
    elif mode == 2:
        generator.wykres_transformata_fouriera()
        zgoda = str(input('Czy chcesz zapisać wykres funkcji do pliku wav? tak/nie '))
        print()
        if zgoda == "tak":
            generator.zapis_wav()
        else:
            pass


def wynik(decyzja):
    print()
    a = error_blocker("Podaj amplitudę: ")
    f = error_blocker("Podaj częstotliwość[Hz]: ")
    time = error_blocker_2("Podaj czas generowanego przebiegu[s]: ")
    z = error_blocker_2("Podaj zakres wykresu[s]: ")
    generator = Generator(f, a, time, z)
    if decyzja == 1:
        generator.sine()
        generator.wykres()
        wybor_2(f, a, time, z, 1)

    elif decyzja == 2:
        generator.square()
        generator.wykres()
        wybor_2(f, a, time, z, 2)

    elif decyzja == 3:
        generator.triangle()
        generator.wykres()
        wybor_2(f, a, time, z, 3)

    elif decyzja == 4:
        generator.sawtooth()
        generator.wykres()
        wybor_2(f, a, time, z, 4)

    elif decyzja == 5:
        generator.white_noise()
        generator.wykres()
        wybor_2(f, a, time, z, 5)

    return


def error_blocker(message):
    print(message)
    while 1:
        try:
            value = float(input())
            break
        except (ValueError, TypeError):
            print('Podana wartość jest nieporawna. Podaj wartość jeszcze raz.')
    return value


def error_blocker_2(message):
    print(message)
    while 1:
        try:
            value = int(input())
            if value > 0:
                break

            else:
                print('Podana wartość jest nieporawna. Podaj wartość jeszcze raz.')

        except (ValueError, TypeError):
            print('Podana wartość jest nieporawna. Podaj wartość jeszcze raz.')
    return value


def start():
    decyzja = wybor(0, 6, "Jaki chcesz wygenerować przebieg czasowy? Podaj liczbę z zakresu 1-5.\n \nSine[1]  Square[2]  Triangle[3]  Sawtooth[4]  WhiteNoise[5]")
    wynik(decyzja)


while 1:
    start()
    choice = str(input("Czy uruchomić generator ponownie? (tak/nie) "))
    print()
    if choice != "tak":
        quit(0)

