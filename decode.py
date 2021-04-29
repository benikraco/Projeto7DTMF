# %%
# Importe todas as bibliotecas

import enum
from suaBibSignal import *
import peakutils  # alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from scipy.io import wavfile



# funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    # *****************************instruções********************************

    # declare um objeto da classe da sua biblioteca de apoio (cedida)
    # algo como:
    signal = signalMeu()

    # voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:

    fs = 48000
    sd.default.samplerate = fs  # taxa de amostragem
    sd.default.channels = 1  # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration = 2  # tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    # calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = fs * duration

    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao
    # use um time.sleep para a espera
    print("Captação iniciando em 5 segundos:")
    time.sleep(5)

    # Ao seguir, faca um print informando que a gravacao foi inicializada
    print("Gravação iniciada.")

    # para gravar, utilize
    som = str(input("Qual som você quer verificar? "))
    samplerate, data = wavfile.read('./sounds/Tecla-{}.wav'.format(som)) #Microfone não identificava o som, tive que gravar um áudio de uma tecla pelo celular e transformar ele em .wav, para assim ler os dados nele contidos.
    sd.wait()
    print("...     FIM")
    #print(audio)

    print(data)
    print(len(data))



    # analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    # extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações).
    # dados = []
    # for e in data:
    #     dados.append(e)

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(-1, 1, len(data))
    # plot do gravico áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) .
    plt.plot(t, data, "r--", label = "Dados da gravação pelo tempo")
    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(data, fs)
    plt.figure("F(y)")
    plt.plot(xf, yf)
    plt.grid()
    plt.title('Fourier audio')

    # agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    # Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    # Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    # "min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.4, min_dist=50)
    # yf é o resultado da transformada de fourier
    print("index de picos {}" .format(index))


    # printe os picos encontrados!
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito

    lista = []

    for frequency in xf[index]:
        if frequency > 0:
            print("Peak frequencies: {}".format(frequency))
            lista.append(frequency)

    # encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    # print o valor tecla!!!

    l1 = ["1", "2", "3", "A"]
    l2 = ["4", "5", "6", "B"]
    l3 = ["7", "8", "9", "C"]
    l4 = ["*", "0", "#", "D"]

    frequencies = [[697, 770, 852, 941], [1209, 1336, 1477, 1633]]

    margem = 20

    lista_2 = []
    lista_2_1 = []
    

    if len(lista) < 2:
        print()
    else:
        for freq in lista:
            for e, i in enumerate(frequencies[0]):
                if (i-margem) < freq < (i+margem):
                    lista_2.append(e)
            for e, i in enumerate(frequencies[1]):
                if (i-margem) < freq < (i+margem):
                    lista_2_1.append(e)
        if lista_2[0] == 0:
            digitChosen = l1[lista_2_1[0]]
        elif lista_2[0] == 1:
            digitChosen = l2[lista_2_1[0]]
        elif lista_2[0] == 2:
            digitChosen = l3[lista_2_1[0]]
        elif lista_2[0] == 3:
            digitChosen = l4[lista_2_1[0]]



        print("O digito escolhido foi: ", digitChosen)


    # Se acertou, parabens! Voce construiu um sistema DTMF

    # Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla.

    # Exiba gráficos do fourier do som gravados
    plt.show()


if __name__ == "__main__":
    main()

# %%
