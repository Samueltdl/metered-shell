import psutil
import win32process
import win32event
import time
import win32api

class MonitoringSoftware:

    def __init__(self, software, timeout, tempo_cpu): #     Inicializa o objeto com o diretório, timeout e tempo de cpu inseridos pelo usuário.
        self.software = software
        self.timeout = timeout
        self.tempo_cpu = tempo_cpu
    
    def abrir_programa(self): # Essa é a função principal, que inicia o processo (abre o programa)
        return win32process.CreateProcess(
            self.software,
            None,
            None,
            None,
            False,
            win32process.CREATE_NEW_CONSOLE,
            None,
            None,
            win32process.STARTUPINFO()
        )

    def monitorar_cpu(self): # Essa é a função que roda um loop que monitora o programa
        process_info = self.abrir_programa()
        
        #   Pega as informações do processo
        proc_handle, thread_handle, proc_id, thread_id = process_info
        
        #   Inicia a coleta de dados do processo inicializado.
        process = psutil.Process(proc_id)
        
        total_cpu_time = 0
        
        #   Aguarda o fechamento do programa, ou encerramento pelo timeout.
        time_out_max = self.timeout
        #   Loop que monitora o tempo de CPU, e encerra o programa caso chegue ao máximo.
        while True:
            #   Pega a soma do tempo de CPU para user e system e armazena no total
            
            cpu_time_user = process.cpu_times().user
            cpu_time_system = process.cpu_times().system
            total_cpu_time += cpu_time_user+cpu_time_system
            print(f"Tempo de CPU: {total_cpu_time}")
            print(f"Timeout: {time_out_max}")
            time_out_max -= 1
            
            #   Verifica de o resultado do aguardo do timeout expirou, ou não.
            if time_out_max <= 0:
                print("Timeout expirou. Terminando o processo.")
                
                break #   Caso tenha expirado, encerra o loop do tempo de cpu forçadamente

            time.sleep(1) # Aguarde 1 segundo antes de verificar novamente
        
        if total_cpu_time >self.tempo_cpu:
            print(f'QUOTA TEMPO TOTAL DE CPU EXPIRADO.\n\n Tempo restante: {self.tempo_cpu - total_cpu_time}')
        else:
            print(f'Tempo restante: {self.tempo_cpu - total_cpu_time}')
        # Termina o processo.
        win32api.TerminateProcess(proc_handle, 1)
        win32api.CloseHandle(proc_handle)
        win32api.CloseHandle(thread_handle)

        # Printa os resultados no terminal
        print('Medição encerrada.')
        print(f'Tempo de CPU total consumido: {total_cpu_time}')
        


if __name__ == "__main__":
    
    software = str(input("Digite o caminho do processo: ")) #   Testar com o seguinte diretório: C:\\Windows\\System32\\notepad.exe
    tempo_cpu = int(input("Digite um tempo máximo de CPU para o programa: "))
    timeout = int(input("Digite um tempo máximo de execução do programa: "))

    monitoramento = MonitoringSoftware(software, timeout, tempo_cpu)
    monitoramento.monitorar_cpu()
    