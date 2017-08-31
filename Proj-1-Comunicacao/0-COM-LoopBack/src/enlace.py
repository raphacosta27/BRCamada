#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
from construct import *
import endescapsulamento
import getType

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        # endes = endescapsulamento.Empacotamento()
        # packet = endes.buildDataPacket(data)

        self.tx.sendBuffer(data)

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """

        package = self.rx.searchForPacket()
        print("alo"+str(package)) 
        endes = endescapsulamento.Empacotamento()
        data = endes.unpackage(package)
        
        return(data)

    def receive(self):
        endes = endescapsulamento.Empacotamento()
        sync = False
        while sync == False:
            #iniciar timer para esperar um syn
            time.sleep(1)
            if self.rx.getBufferLen() != 0:
                print("recebi algo")
                packet = self.getData()
                packetType = getType.getType(packet)
                if packetType.getPacketType() == 'comando':
                    if packetType.getCommandType() == 'SYN':
                        print("Foi recebido o primeiro Syn")
                        self.sendData(endes.buildAckPacket())
                        time.sleep(3)
                        print("alo")
                        self.sendData(endes.buildSynPacket())
                        #outro timer esprando um ack do client
                        time.sleep(2)
                        packet2 = self.getData()
                        print(packet2)
                        if len(packet2) != 0:
                            packetType2 = getType.getType(packet2)
                            if packetType2.getPacketType() == 'comando':
                                packetType2.getCommandType()
                                if packetType2.getCommandType() == 'ACK':
                                    sync = True
                                    time.sleep(3)
                                    return True
                                else:
                                    print("nao recebeu ultimo ack do server")
                                    continue
                            else:
                                print("server nao mandou ack")
                                continue
                        else:
                            print("nao recebeu nenhum ack do server, reiniciando")
                            continue
                    else:
                        print("server nao mandou syn")
                        continue
                else:
                    print("nao recebeu")
                    continue
            else:
                print("pacote vazio, procurar novamente")
                continue

    def conecta(self):
        endes = endescapsulamento.Empacotamento()
        sync = False
        while sync == False:
            synPacket = endes.buildSynPacket()
            self.sendData(synPacket)
            time.sleep(2)
            # print("lenBuffer" + str(self.tx.getBufferLen())) 
            #inicia timer esperando um ack e um syn
            bufferLen = self.rx.getBufferLen()
            print(bufferLen)
            if bufferLen != 0:
                packet = self.getData()
                packetType = getType.getType(packet)
                if packetType.getPacketType() == 'comando':
                    if packetType.getCommandType() == 'ACK':
                        print("recebe ack")
                        
                        time.sleep(3)
                        packet = self.getData()
                        packetType = getType.getType(packet)    
                        if packetType.getPacketType() == 'comando':
                            if packetType.getCommandType() == 'SYN':    
                                print('recebeu SYN')
                                #iniciar timer para esperar um SYN do server
                                ackPacket = endes.buildAckPacket()
                                print(self.rx.buffer)
                                self.sendData(ackPacket)
                                print(self.rx.buffer)
                                sync = True
                                return True
                    else:
                        print("nao recebeu ack e syn do server")
                        continue
                else:
                    print("nao é um comando")
                    continue
            else:
                print("pacote vazio, reiniciando")
        
                        



        
                    
                    