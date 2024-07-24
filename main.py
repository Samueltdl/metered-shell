import psutil
import win32process
import win32event
import time
import win32api

class MonitoringSoftware:

    def __init__(self, software, timeout, tempo_cpu):
        self.software = software
        self.timeout = timeout
        self.tempo_cpu = tempo_cpu
    
    def monitorar_cpu(self):
        process_info = win32process.CreateProcess(
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
        proc_handle, thread_handle, proc_id, thread_id = process_info
        process = psutil.Process(proc_id)
        total_cpu_time = 0
        result = win32event.WaitForSingleObject(proc_handle, self.timeout)
        while (total_cpu_time < self.tempo_cpu):
            
            cpu_time_user = process.cpu_times().user
            cpu_time_system = process.cpu_times().system
            total_cpu_time += cpu_time_user+cpu_time_system
            print(f"Tempo de CPU: {total_cpu_time}")
            
            if result == win32event.WAIT_TIMEOUT:
                print("Timeout expirou. Terminando o processo.")
                # Termina o processo forçadamente
                win32api.TerminateProcess(proc_handle, 1)
                total_cpu_time+=9999999999999999999999

            # Aguarde 1 segundo antes de verificar novamente
            time.sleep(1)
            
        print('Medição encerrada.')
        win32api.CloseHandle(proc_handle)
        win32api.CloseHandle(thread_handle)
        


    

if __name__ == "__main__":
    
    process_name = str(input("Digite o nome do processo: ")) #   Testar com o seguinte diretório: C:\\Windows\\System32\\notepad.exe
    tempo_cpu = int(input("Digite um tempo máximo de CPU para o programa: "))
    timeout = int(input("Digite um tempo máximo de execução do programa: "))
    monitoramento = MonitoringSoftware(process_name, timeout, tempo_cpu)
    monitoramento.monitorar_cpu()