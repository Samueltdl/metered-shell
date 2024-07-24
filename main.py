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
    
    def abrir_programa(self): #      Essa é a função principal, que inicia o processo (abre o programa)
        #   Inicia o processo (abre o programa)
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

    def monitorar_cpu(self):
        process_info = self.abrir_programa()
        
        #   Pega as informações do processo
        proc_handle, thread_handle, proc_id, thread_id = process_info
        
        #   Inicia a coleta de dados do processo inicializado.
        process = psutil.Process(proc_id)
        
        total_cpu_time = 0
        
        #   Aguarda o fechamento do programa, ou encerramento pelo timeout.
        result = win32event.WaitForSingleObject(proc_handle, self.timeout)
        
        #   Loop que monitora o tempo de CPU, e encerra o programa caso chegue ao máximo.
        while (total_cpu_time < self.tempo_cpu):
            #   Pega a soma do tempo de CPU para user e system e armazena no total
            cpu_time_user = process.cpu_times().user
            cpu_time_system = process.cpu_times().system
            total_cpu_time += cpu_time_user+cpu_time_system
            print(f"Tempo de CPU: {total_cpu_time}")
            
            #   Verifica de o resultado do aguardo do timeout expirou, ou não.
            if result == win32event.WAIT_TIMEOUT:
                print("Timeout expirou. Terminando o processo.")
                
                #   Caso tenha expirado, encerra o loop do tempo de cpu forçadamente
                break

            # Aguarde 1 segundo antes de verificar novamente
            time.sleep(1)
        
        # Termina o processo.
        win32api.TerminateProcess(proc_handle, 1)
        print('Medição encerrada.')
        win32api.CloseHandle(proc_handle)
        win32api.CloseHandle(thread_handle)
        


    

if __name__ == "__main__":
    
    process_name = str(input("Digite o nome do processo: ")) #   Testar com o seguinte diretório: C:\\Windows\\System32\\notepad.exe
    tempo_cpu = int(input("Digite um tempo máximo de CPU para o programa: "))
    timeout = int(input("Digite um tempo máximo de execução do programa: "))
    monitoramento = MonitoringSoftware(process_name, timeout*1000, tempo_cpu)
    monitoramento.monitorar_cpu()