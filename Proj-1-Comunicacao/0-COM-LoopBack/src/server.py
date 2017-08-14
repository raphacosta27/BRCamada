from enlace import *
import time
import interfaceServer
from tkinter import *

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

def main(window_server):

    # Inicializa enlace
    com = enlace(serialName)
    # Ativa comunicacao
    com.enable()

    txLen = 49284

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png"

    status_label = Label(window_server, text ="Recebendo dados ....")
    status_label.grid(row =1, column =0, sticky = W)

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    rxBuffer, nRx = com.getData(txLen)


    # log
    start_receiving_time = time.time()
    print ("Lido              {} bytes ".format(nRx))

    # Salva imagem recebida em arquivo
    print("-------------------------")
    print ("Salvando dados no arquivo :")
    print (" - {}".format(imageW))
    f = open(imageW, 'wb')
    f.write(rxBuffer)

    # Fecha arquivo de imagem
    f.close()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    finished_receiving_time = time.time() - start_receiving_time
    print("Tempo de recepção: " + str(finished_receiving_time))
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    main()
