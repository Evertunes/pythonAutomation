from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep

class ServidorModbus():
   
   #metodo construtor
    def __init__(self, ip, porta):
        #criando banco de dados
        self._db = DataBank()
        #configura servidor
        #parametros mais importante para CLP (automação são o IP e PORTA)
        self._server = ModbusServer(host=ip, port = porta, no_block=True, data_bank=self._db)
    #metodo que altera o servidor
    def run(self):
        try:    
            #Executa apenas uma vez(Seria o Void Setup do arduino) 
            #inicia o servidor
            self._server.start()
            print("Servidor Modbus em operação")
            #acessa banco de dados
            self._db.set_discrete_inputs(0, [False]) #escreve no endereço 0 do modbus
            self._db.set_discrete_inputs(1, [True]) #escreve no endereço 1 do modbus
            self._db.set_coils(0, [True]) #escrev no endereço 0 da coil (seria acionamentos de bobina)
            self._db.set_coils(1, [False]) #escrev no endereço 1 da coil (seria acionamentos de bobina)
            sleep(1)
            #Executa apenas uma vez(Seria o Void Setup do arduino) ^^
           
            while True:
                print("-----------------------")
                print("Tabela Modbus")
                print(f'Discrete Inputs \r\n DIO:{self._db.get_discrete_inputs(0)} \r\n DI1: {self._db.get_discrete_inputs(1)}') #faz a leitura do endereço 0 do ModBus
                print(f'Coils \r\n C0: {self._db.get_coils(0)} \r\n C1:{self._db.get_coils(1)}') #leio os coils
                sleep(5)
        #captura os erros e printa

        except Exception as e:
            print("Erro: ", e.args)

s = ServidorModbus('localhost', 502)
s.run()