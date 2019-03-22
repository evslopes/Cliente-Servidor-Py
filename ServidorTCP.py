#Nome dos alunos: Mayara Lima, Elvis Lopes, Antônio Castillo

import socket, psutil, pickle, cpuinfo, os

# Funções
def info_cpu():

  resposta = {"cpu_nome": cpuinfo.get_cpu_info()['brand'],
              "cpu_arq": cpuinfo.get_cpu_info()['arch'],
              "cpu_bits": cpuinfo.get_cpu_info()['bits'],
              "cpu_logico": psutil.cpu_count(logical=True),
              "cpu_fisico": psutil.cpu_count(logical=False),
              "cpu_frequencia_atual": psutil.cpu_freq().current,
              "cpu_frequencia_max":  psutil.cpu_freq().max,
              "cpu_percentual_nucleo": psutil.cpu_percent(percpu=True),
              "cpu_percentual": psutil.cpu_percent()
              }

  return resposta

def info_memoria():

    # buscando memoria total
    mem = psutil.virtual_memory()
    total = round(mem.total/1024**3, 2)

    # buscando memoria em uso
    available = round(total-mem.available/1024**3, 2)

    # calculando porcentagem de uso
    porcentagem = round((available/total)*100,2)

    resposta = {"ram_total": total,
                "ram_uso": available,
                "ram_percentual": porcentagem}

    return resposta

def info_redes():
    resposta = []

    dic_interfaces = psutil.net_if_addrs('lo')
    texto = "Interface de rede: " + str(dic_interfaces) + "."

    resposta.append(texto)
    return resposta

def info_processos():
    pids = psutil.pids()
    pids_nome = []
    pids_cpu = []
    pids_memory = []

    for x in pids:
        pids_nome.append(psutil.Process(x).name())
        pids_memory.append(round(psutil.Process(x).memory_info().rss * 10 ** -6, 2))

    resposta = {"pids": pids,
                "pids_nome": pids_nome,
                "pids_memory": pids_memory,
                "pids_cpu": pids_cpu}

    return resposta

def info_disco():
    resposta = []
    resposta.append(psutil.disk_usage('/'))

    return resposta

def info_diretorio():

    resposta = {}
    lista = os.listdir()

    for i in lista:
        if os.path.isfile(i):
            resposta[i] = []
            resposta[i].append(os.stat(i).st_size)
            resposta[i].append(os.stat(i).st_atime)
            resposta[i].append(os.stat(i).st_mtime)

    return resposta

# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Obtem o nome da máquina
host = socket.gethostname()
porta = 9999
# Associa a porta
socket_servidor.bind((host, porta))
# Escutando...
socket_servidor.listen()
print("Servidor de nome", host, "esperando conexão na porta", porta)
# Aceita alguma conexão
(socket_cliente,addr) = socket_servidor.accept()

print("Conectado a:", str(addr))

while True:
    # Recebimento da posição do menu
    bytes_menu = socket_cliente.recv(10240)
    menu = pickle.loads(bytes_menu)
    print(menu)
    # Fechar
    if menu == 0:
        break

    # CPU
    elif menu == 1:
        resposta = []
        resposta.append(info_cpu())
        bytes_resp = pickle.dumps(resposta)
        # Envia os dados
        socket_cliente.send(bytes_resp)

    # RAM
    elif menu == 2:
        resposta = []
        resposta.append(info_memoria())
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(resposta)
        # Envia os dados
        socket_cliente.send(bytes_resp)

    # DISCO
    elif menu == 3:

        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(info_disco())
        # Envia os dados
        socket_cliente.send(bytes_resp)

    # DIRETORIO
    elif menu == 4:

        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(info_diretorio())
        # Envia os dados
        socket_cliente.send(bytes_resp)

    # PROCESSOS
    elif menu == 5:
        # Cria a variavel de resposta
        resposta = []

        # Adiciona a função de processos ao array resposta
        resposta.append(info_processos())

        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(resposta)

        # Envia os dados
        socket_cliente.send(bytes_resp)

        bytes_menu = socket_cliente.recv(10240)
        pid = pickle.loads(bytes_menu)
        check_pid = pid in resposta[0]["pids"]

        if check_pid == True:
            socket_cliente.send(pickle.dumps(psutil.Process(pid).cpu_percent(interval=1)))

        else:
            erro_pid = "PID Inválido."
            socket_cliente.send(pickle.dumps(erro_pid))


# Fecha socket do servidor e cliente
print("Fechando conexão...")
socket_cliente.close()
socket_servidor.close()
print("Aplicação finalizada.")
