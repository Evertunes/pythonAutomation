from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import struct

class ServidorModbus():
   
   #metodo construtor
    def __init__(self, ip, porta):
        #criando banco de dados
        self._db = DataBank()
        #configura servidor
        #parametros mais importante para CLP (automação são o IP e PORTA)
        self._server = ModbusServer(host=ip, port = porta, no_block=True, data_bank=self._db)
    #metodo que altera o servidor

    #quebra o valor real em dois inteiros enereça eles
    def float_to_registers(self,value):
        packed_value = struct.pack('>f',value)
        registers = struct.unpack('>HH', packed_value)
        return registers
    #une os dois inteiros em um valor real.. traz de volta endereçado para real
    def registers_to_float(self,registers):
        packed_value = struct.pack('>HH', registers[0], registers[1])
        value = struct.unpack('>f', packed_value)[0]
        return value
    
    def run(self):
        try:    
            #Executa apenas uma vez(Seria o Void Setup do arduino) 
            #inicia o servidor
            self._server.start()
            print("Servidor Modbus em operação")
            input_registers = self.float_to_registers(125.66) #qualquer valor real
            holding_registers = self.float_to_registers(844.55)
            self._db.set_input_registers(8, list(input_registers))#escrevendo no endereço 8
            self._db.set_holding_registers(10,list(holding_registers)) #escrevendo no endereço 10

            sleep(1)
            while True:
                print("-----------------------")
                print("Tabela Modbus")
                read_register1 = self._db.get_input_registers(8,2)
                read_register2 = self._db.get_holding_registers(10,2)
                read_value1 = self.registers_to_float(read_register1)
                read_value2 = self.registers_to_float(read_register2)
                print(f'Valor real obtido de IR8 e IR9: {read_value1:.2f}')
                print(f'Valor real obtido de HR10 e HR11: {read_value2:.2f}')
                sleep(5)
        #captura os erros e printa

        except Exception as e:
            print("Erro: ", e.args)

s = ServidorModbus('localhost', 502)
s.run()