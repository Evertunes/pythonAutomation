# Importa a classe DataBank e ModbusServer da biblioteca pyModbusTCP para criar e gerenciar um servidor Modbus.
from pyModbusTCP.server import DataBank, ModbusServer
# Importa a função sleep do módulo time para adicionar atrasos no código.
from time import sleep
# Importa o módulo tkinter (tk) para criar interfaces gráficas.
import tkinter as tk
# Importa a classe Thread da biblioteca threading para rodar o servidor Modbus em uma thread separada.
from threading import Thread

# Define a classe ServidorModbus para configurar e gerenciar o servidor Modbus.
class ServidorModbus():

    # O método __init__ é o construtor que inicializa a classe com o IP e a porta do servidor Modbus.
    def __init__(self, ip, porta):
        # Cria um DataBank, que é a memória do servidor Modbus.
        self._db = DataBank()
        # Cria o servidor Modbus com o IP e a porta fornecidos, sem bloqueio, usando o DataBank criado.
        self._server = ModbusServer(host=ip, port=porta, no_block=True, data_bank=self._db)

    # Método que inicia o servidor e realiza operações de leitura e escrita no DataBank.
    def run(self):
        try:
            # Inicia o servidor Modbus.
            self._server.start()    
            print("Servidor Modbus em operação")  # Informa que o servidor está operando.

            # Define os valores iniciais das bobinas (coils).
            self._db.set_coils(0, [True])  # Define o valor da bobina 0 como True.
            self._db.set_coils(1, [False]) # Define o valor da bobina 1 como False.
            sleep(1)

            # Loop infinito para monitorar e alterar os valores das entradas discretas (discrete inputs) e bobinas.
            while True:
                print("======================")    
                print("Tabela Modbus")
                # Exibe os valores atuais das entradas discretas e bobinas.
                print(f'Discrete Inputs \r\n DI0: {self._db.get_discrete_inputs(0)} \r\n DI1: {self._db.get_discrete_inputs(1)}')
                print(f'Coils \r\n C0: {self._db.get_coils(0)} \r\n C1: {self._db.get_coils(1)}')
                sleep(3)
                # Altera os valores das entradas discretas.
                self._db.set_discrete_inputs(0, [False])
                self._db.set_discrete_inputs(1, [True])
                sleep(3)
                # Altera os valores das entradas discretas novamente.
                self._db.set_discrete_inputs(0, [True])
                self._db.set_discrete_inputs(1, [False])

        # Captura qualquer exceção que ocorrer durante a execução.
        except Exception as e:
            # Imprime a mensagem de erro, se houver.
            print("Erro: ", e.args)

# Define uma classe ModbusGUI que herda de tk.Tk para criar a interface gráfica (GUI) para o servidor Modbus.
class ModbusGUI(tk.Tk):
    def __init__(self, s):
        super().__init__()
        self.s = s
        self.title("Modbus Interface")  # Define o título da janela GUI.

        # Cria a interface para a bobina 0 com botões para definir o valor como True ou False.
        tk.Label(self, text="COIL 0", bg="black", fg="white", width=20, height=2, font=("Helvetica", 24)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self, text="TRUE", command=self.set_coil_0_true, bg="green", fg="white", width=20, height=2, font=("Helvetica", 24)).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self, text="FALSE", command=self.set_coil_0_false, bg="red", fg="white", width=20, height=2, font=("Helvetica", 24)).grid(row=2, column=0, padx=10, pady=10)

        # Cria a interface para a bobina 1 com botões para definir o valor como True ou False.
        tk.Label(self, text="COIL 1", bg="black", fg="white", width=20, height=2, font=("Helvetica", 24)).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="TRUE", command=self.set_coil_1_true, bg="green", fg="white", width=20, height=2, font=("Helvetica", 24)).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="FALSE", command=self.set_coil_1_false, bg="red", fg="white", width=20, height=2, font=("Helvetica", 24)).grid(row=2, column=1, padx=10, pady=10)

        # Cria a interface para mostrar o status das entradas discretas (DI0 e DI1).
        tk.Label(self, text="DISCRETE INPUT 0", bg="black", fg="white", width=20, height=2, font=("Helvetica", 24)).grid(row=3, column=0, padx=10, pady=10)
        self.di0_status = tk.Label(self, text="FALSE", bg="gray", width=20, height=2, font=("Helvetica", 24))
        self.di0_status.grid(row=4, column=0, padx=10, pady=10)

        tk.Label(self, text="DISCRETE INPUT 1", bg="black", fg="white", width=20, height=2, font=("Helvetica", 24)).grid(row=3, column=1, padx=10, pady=10)
        self.di1_status = tk.Label(self, text="FALSE", bg="gray", width=20, height=2, font=("Helvetica", 24))
        self.di1_status.grid(row=4, column=1, padx=10, pady=10)

        # Inicia o método para atualizar o status das entradas discretas na GUI.
        self.update_status()

    # Métodos para definir os valores das bobinas 0 e 1 (coils) como True ou False.
    def set_coil_0_true(self):
        self.s._db.set_coils(0, [True])

    def set_coil_0_false(self):
        self.s._db.set_coils(0, [False])
    
    def set_coil_1_true(self):
        self.s._db.set_coils(1, [True])

    def set_coil_1_false(self):
        self.s._db.set_coils(1, [False])

    # Método para atualizar o status das entradas discretas (DI0 e DI1) na interface gráfica.
    def update_status(self):
        di0_status = self.s._db.get_discrete_inputs(0)[0]
        di1_status = self.s._db.get_discrete_inputs(1)[0]
        self.di0_status.config(text=str(di0_status))
        self.di1_status.config(text=str(di1_status))
        self.after(1000, self.update_status)  # Atualiza a cada 1 segundo.

# Bloco principal do código, executado quando o script é iniciado diretamente.
if __name__ == "__main__":
    # Cria uma instância do servidor Modbus com o IP e porta fornecidos.
    s = ServidorModbus('localhost', 502)

    # Cria e inicia uma thread separada para rodar o servidor Modbus.
    modbus_thread = Thread(target=s.run)
    modbus_thread.daemon = True
    modbus_thread.start()

    # Cria e executa a interface gráfica (GUI) do Modbus.
    app = ModbusGUI(s)
    app.mainloop()  # Inicia o loop principal da GUI, mantendo a janela aberta.