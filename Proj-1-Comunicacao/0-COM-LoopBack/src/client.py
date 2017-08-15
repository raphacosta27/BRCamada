from enlace import *
import time
import interfaceClient
from tkinter import *

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)

def main(window_client, filename):

    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser transmitida
    imageR = filename

    start_time = time.time()

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega imagem
    print ("Carregando imagem para transmissão")

    new_label = Label(window_client, text="Carregando imagem para transmissão :")
    new_label.grid(row=2, column=0, sticky=W)

    print (" - {}".format(imageR))
    print("-------------------------")
    txBuffer = open(imageR, 'rb').read()
    txLen    = len(txBuffer)
    print(txLen)

    # Transmite imagem
    print("Transmitindo .... {} bytes".format(txLen))
    com.sendData(txBuffer)

    new_label2 = Label(window_client, text="Transmitindo .... {} bytes".format(txLen))
    new_label2.grid(row=3, column=0, sticky=W)

    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass

    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()
    print ("Transmitido       {} bytes ".format(txSize))


    # interfaceClient.MyFrame.finished(window)
    elapsed_time = time.time() - start_time
    print("tempo de transmissao " + str(elapsed_time))

    new_label2 = Label(window_client, text="tempo de transmissao " + str(elapsed_time))
    new_label2.grid(row=4, column=0, sticky=W)

    # quit_button = Button(window_client, text="Quit", command = quit(window_client))
    # quit_button.grid(row=5, column=0, sticky=W)


# def quit(window):
#     interfaceClient.MyFrame.finished(window)

if __name__ == "__main__":
    main()
