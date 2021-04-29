# %%
#importe as bibliotecas
# import sys
# sys.append("")
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    signal = signalMeu()

    frequencies = [[697, 770, 852, 941], [1209, 1336, 1477, 1633]]
    freq_digit = [[], []]

    digit = str(input("Digite uma tecla do teclado numérico: \n"))
    print("Digit chosen: {}".format(digit))

    l1 = ["1", "2", "3", "A"]
    l2 = ["4", "5", "6", "B"]
    l3 = ["7", "8", "9", "C"]
    l4 = ["*", "0", "#", "D"]

    if digit in l1:
        freq_digit[0].append(frequencies[0][0])
        if digit == "1":
            freq_digit[1].append(frequencies[1][0])
        elif digit == "2":
            freq_digit[1].append(frequencies[1][1])
        elif digit == "3":
            freq_digit[1].append(frequencies[1][2])
        elif digit == "A":
            freq_digit[1].append(frequencies[1][3])

    elif digit in l2:
        freq_digit[0].append(frequencies[0][1])
        if digit == "4":
            freq_digit[1].append(frequencies[1][0])
        elif digit == "5":
            freq_digit[1].append(frequencies[1][1])
        elif digit == "6":
            freq_digit[1].append(frequencies[1][2])
        elif digit == "B":
            freq_digit[1].append(frequencies[1][3])

    elif digit in l3:
        freq_digit[0].append(frequencies[0][2])
        if digit == "7":
            freq_digit[1].append(frequencies[1][0])
        elif digit == "8":
            freq_digit[1].append(frequencies[1][1])
        elif digit == "9":
            freq_digit[1].append(frequencies[1][2])
        elif digit == "C":
            freq_digit[1].append(frequencies[1][3])

    elif digit in l4:
        freq_digit[0].append(frequencies[0][3])
        if digit == "*":
            freq_digit[1].append(frequencies[1][0])
        elif digit == "0":
            freq_digit[1].append(frequencies[1][1])
        elif digit == "#":
            freq_digit[1].append(frequencies[1][2])
        elif digit == "D":
            freq_digit[1].append(frequencies[1][3])

    #Senoides
    
    T = 1
    fs = 44100
    t = np.linspace(-T, T, T*fs)
    sd.default.samplerate = fs
    sd.default.channels = 1


    x0, y0 = signal.generateSin(freq_digit[0][0], 1, T, fs)
    x1, y1 = signal.generateSin(freq_digit[1][0], 1, T, fs)
    s = y0 + y1

    print("Sound produced by digit {}".format(s))
    
    sd.play(s, fs)


    #Desenhando gráficos
    plt.plot(t, y0, "b-.", label = "Frequency: {} Hz".format(freq_digit[0][0]))
    plt.plot(t, y1, "r--", label = "Frequency: {} Hz".format(freq_digit[1][0]))
    plt.plot(t, s, "g--", label = "Sum of Frequencies {0} and {1}: ".format(y0,y1))
    plt.grid(True)

    plt.title("Graph related to digit's {} frequency".format(digit))
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.xlim(0, 0.0135)
    plt.legend()
    plt.show()

    plt.savefig("img/digit{}_graph.png".format(digit), format="png")

    sd.wait()

if __name__ == "__main__":
    main()

# %%
