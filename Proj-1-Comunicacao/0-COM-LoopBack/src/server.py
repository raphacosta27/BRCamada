from enlace import *
import time
import interfaceServer
from tkinter import *
from PIL import Image, ImageTk

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM7"                  # Windows(variacao de)

def main(window_server):

    # Inicializa enlace
    com = enlace(serialName)
    # Ativa comunicacao
    com.enable()

    txLen = 5992

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.jpg"

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    rxBuffer, nRx = com.getData(txLen)


    # log
    start_receiving_time = time.time()
    print ("Lido              {} bytes ".format(nRx))

    status_label1 = Label(window_server, text ="Lido              {} bytes ".format(nRx))
    status_label1.grid(row = 2, column =0, sticky = W)

    # Salva imagem recebida em arquivo
    print("-------------------------")
    print ("Salvando dados no arquivo :")
    print (" - {}".format(imageW))
    f = open(imageW, 'wb')
    f.write(rxBuffer)

    status_label2 = Label(window_server, text ="Salvando dados no arquivo : - {}".format(imageW))
    status_label2.grid(row = 3, column =0, sticky = W)

    # Fecha arquivo de imagem
    f.close()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    finished_receiving_time = time.time() - start_receiving_time
    print("Tempo de recepção: " + str(finished_receiving_time))
    print("-------------------------")
    com.disable()

    status_label3 = Label(window_server, text ="Comunicação encerrada")
    status_label3.grid(row = 4, column =0, sticky = W)

    status_label4 = Label(window_server, text ="Tempo de recepção: " + str(finished_receiving_time))
    status_label4.grid(row = 5, column =0, sticky = W)

    interfaceServer.MyFrame.plot_img(window_server,imageW)

if __name__ == "__main__":
    main()
