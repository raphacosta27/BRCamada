#! /usr/bin/env python
# -*- coding:utf-8 -*-
import enlace
import endescapsulamento
from getType import getType


#Classe que espera o sync
class serverStateMachine(server):
    def __init__(self):
        self.server = server

    def execute(self):
        
