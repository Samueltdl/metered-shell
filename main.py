import psutil
import win32process
import time

def monitorar_cpu(pid, time_out):
    process = psutil.Process(pid)
    total_cpu_time = 0

    while (time_out and time_out > 0) or (time_out < 0):
        cpu_time = process.cpu_times().user
        total_cpu_time += cpu_time
        print(f"Tempo de CPU: {cpu_time}")

        # Aguarde 1 segundo antes de verificar novamente
        time.sleep(1)
        time_out -= 1

    print(f"Programa finalizado")

def get_pid_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.pid
    return None

if __name__ == "__main__":
    # Obtenha o PID do Bloco de Notas
    process_name = str(input("Digite o nome do processo: "))
    time_out = int(input("Digite um tempo máximo de execução do programa (0 caso não queira tempo máximo): "))
    pid = get_pid_by_name(process_name + ".exe")

    # Monitore o tempo de CPU do Bloco de Notas
    monitorar_cpu(pid, time_out - 1)
