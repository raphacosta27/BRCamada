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

# start_receiving_time = time.time()
# finished_receiving_time = time.time() - start_receiving_time

# Construct Struct
from construct import *
import endescapsulamento
import getType

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

import math

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
                        print("é um syn")
                        self.sendData(endes.buildAckPacket())
                        print("Enviando Ack")
                        time.sleep(3)
                        self.sendData(endes.buildSynPacket())
                        print("Enviando Syn")
                        #outro timer esprando um ack do client
                        time.sleep(2)
                        packet2 = self.getData()
                        if len(packet2) != 0:
                            packetType2 = getType.getType(packet2)
                            if packetType2.getPacketType() == 'comando':
                                if packetType2.getCommandType() == 'ACK':
                                    print("Recebeu Ack")
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
            print("Mandando Syn")

            # start_receiving_time = time.time()
            # finished_receiving_time = time.time() - start_receiving_time
            
            time.sleep(2)
            # print("lenBuffer" + str(self.tx.getBufferLen())) 
            #inicia timer esperando um ack e um syn
            bufferLen = self.rx.getBufferLen()
            
            if bufferLen != 0:
                packet = self.getData()
                packetType = getType.getType(packet)
                if packetType.getPacketType() == 'comando':
                    if packetType.getCommandType() == 'ACK':
                        print("Recebendo Ack")
                        
                        time.sleep(3)
                        packet = self.getData()
                        packetType = getType.getType(packet)    
                        if packetType.getPacketType() == 'comando':
                            if packetType.getCommandType() == 'SYN':    
                                print('Recebendo Syn')
                                #iniciar timer para esperar um SYN do server
                                ackPacket = endes.buildAckPacket()
                                # print(self.rx.buffer)
                                self.sendData(ackPacket)
                                print("Mandando Ack")
                                # print(self.rx.buffer)
                                sync = True
                                time.sleep(2)
                                return True
                            else:
                                print("nao recebeu SYN do server")
                                continue
                                
                    else:
                        print("nao recebeu ACK do server")
                        continue
                else:
                    print("nao é um comando")
                    continue
            else:
                print("pacote vazio, reiniciando")
        
    def confirm_client(self):  
        time.sleep(2)
        if self.rx.getBufferLen() != 0 :
            packet = self.getData()
            if packet != 0: 
                packetType = getType.getType(packet)
                if packetType.getPacketType() == 'comando':
                    if packetType.getCommandType() == 'ACK':
                        return True
                    elif packetType.getCommandType() == 'NACK':
                        print("Pacote não recebido, reenviando")
                        # endes = endescapsulamento.Empacotamento()
                        # packet = endes.buildDataPacket(txBuffer)    
                        # self.sendData(packet)
                        return False
        else:
            print('Aguardando confirmação de recebimento de pacote')
            continue
        
        # sent = False
        # return True

    def confirm_server(self):
        received = False
        endes = endescapsulamento.Empacotamento()
        while received == False:
            if self.rx.getBufferLen == 0:
                nackPacket = endes.buildNackPacket()
                self.sendData(nackPacket)
            else:
                rxBuffer = self.getData()
                print("recebi pacote")
                ackPacket = endes.buildAckPacket()
                self.sendData(ackPacket)
                received = True
                # break
        received = False
        return rxBuffer


    def parsePacket(self, payload):
        endes = endescapsulamento.Empacotamento()
        offset = 0
        nPacotes = math.ceil(len(payload)/2048)
        packetCounter = 0
        while packetCounter <= nPacotes:
            if (len(payload) - offset) >= 2048:
                pacote = endes.buildDataPacket((payload[offset:offset+2048]),packetCounter,nPacotes)
                self.sendData(pacote)
                confirmacao = self.confirm_client()
                if confirmacao == True:    
                    offset += 2048
                    packetCounter += 1
                else:
                    continue
            else:
                pacote = endes.buildDataPacket((payload[offset:]),packetCounter,nPacotes)
                self.sendData(pacote)
                confirmacao = self.confirm_client()
                if confirmacao == True:    
                    packetCounter += 1
                else:
                    continue
        
    def receive_packets(self):
        

                
            
        

        
                    
                    