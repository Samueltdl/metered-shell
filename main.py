import psutil
import time
import subprocess


class MonitoringSoftware():
    def __init__(self, software, timeout, max_cpu): # Inicializa o objeto com o diretório, timeout e tempo de cpu inseridos pelo usuário.
        self.software = software
        self.timeout = timeout
        self.max_cpu = max_cpu

    def open_program(self): # método que abre o programa do caminho especificado
        return subprocess.Popen([self.software])

    def reestart(self):
        new_timeout = int(input("\nDigite um novo tempo máximo de execução do programa (0 caso não queira tempo máximo): "))
        self.timeout = new_timeout
        self.monitor_cpu()
        
    
    def monitor_cpu(self): # método que roda um loop que fica monitorando o programa
        
        proc = self.open_program()
        print('\n\n...')
        time.sleep(1)
        print('....')
        time.sleep(1)
        print('.....')
        time.sleep(1)
        print('......\n\n')
        # sleep adicionado só para dar tempo de o programa iniciar completamente (pode ser pouco tempo se o programa demora para iniciar)

        process = psutil.Process(proc.pid)
        
        time_out = self.timeout
        if time_out == 0:
            time_out = True
        
        while True:
            if not process.is_running(): # vericica se o programa não foi fechado forçadamente
                print("\n\n--------------ATENÇÃO---------------")
                print("\nPrograma encerrado antes de terminar a a medição!")
                break

            if type(time_out) != bool:
                if time_out <= 0: # condição que encerra o programa automaticamente caso tenha atingido o tempo máximo
                    process.terminate()
                    break
                
            user_time = process.cpu_times().user
            system_time = process.cpu_times().system
            total_cpu_time = user_time + system_time
            
            print(f"Tempo de CPU (user): {user_time}")
            print(f"Tempo de CPU (system): {system_time}")

            # Aguarde 1 segundo antes de verificar novamente
            time.sleep(1)
            
            if type(time_out) != bool:
                time_out -= 1

        print(f'\n\n---------------------------------------------')
        print(f"\nPrograma finalizado.\n\n")
        print(f"Tempo de CPU total consumido: {total_cpu_time}\n\n")
        
        if total_cpu_time < self.max_cpu:
            print(f'Você ainda tem quota de tempo de CPU restante: {self.max_cpu - total_cpu_time}\n')
            reestart = int(input("\nDeseja reiniciar o monitoramento? (0: não, 1: sim): "))
            if reestart == 1: 
                self.max_cpu -= total_cpu_time
                self.reestart()
        else:
            print(f'\nQuota de tempo de CPU excedida em: {total_cpu_time - self.max_cpu}')
            


software = str(input("\nDigite o caminho do processo: "))
timeout = int(input("\nDigite um tempo máximo de execução do programa (0 caso não queira tempo máximo): "))
max_cpu = int(input("\nDigite uma quota máxima de tempo de CPU para o programa: "))

monitoramento = MonitoringSoftware(software, timeout, max_cpu)
monitoramento.monitor_cpu()


################################## ALGUNS DIRETÓRIOS DO MEU PC ###############################

# C:\Program Files\CPUID\HWMonitor\HWMonitor
# C:\Users\samue\AppData\Local\Discord\app-1.0.9155\Discord
# C:\Program Files\Windows NT\Accessories\wordpad.exe
# C:\Program Files (x86)\Steam\steam.exe
# C:\Users\vitor\AppData\Local\Programs\Opera GX\opera.exe
# C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe