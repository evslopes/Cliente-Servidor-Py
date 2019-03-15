import socket, psutil, pickle, cpuinfo

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
              "cpu_percentual": psutil.cpu_percent()}

  return resposta

def uso_memoria():

    # buscando memoria total
    mem = psutil.virtual_memory()
    total = round(mem.total/(1024*1024*1024), 2)

    # buscando memoria em uso
    available = round(mem.available/(1024*1024*1024), 2)

    # calculando porcentagem de uso
    porcentagem = 100-((available/total)*100)

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
    print()
    # pids = psutil.pids()
    # pids_nome = []
    # pids_cpu = []

    # for x in pids:
    #     pids_nome.append(psutil.Process(x).name())
    #     pids_cpu.append(psutil.Process(x).cpu_percent())

    # lista = [pids, pids_nome, pids_cpu]

    # for x in range(len(pids)):
    #     print(pids[x], pids_nome[x], pids_cpu[x])

    # resposta = {lista}

    # return resposta

def info_disco():

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
    # Recebe pedido do cliente:
    msg = socket_cliente.recv(1024)
    if msg.decode('ascii') == 'fim':
        break

    # Uso da memória
    elif msg.decode('ascii') == '2':

        bytes_resp = pickle.dumps()
        # Envia os dados
        socket_cliente.send(bytes_resp)

    elif msg.decode('ascii') == '3':
        resposta = []
        resposta.append(psutil.disk_partitions())

        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(resposta)
        # Envia os dados
        socket_cliente.send(bytes_resp)

    elif msg.decode('ascii') == '4':
        resposta = []
        resposta.append(info_cpu())
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(resposta)
        # Envia os dados
        socket_cliente.send(bytes_resp)

    # Uso da rede
    elif msg.decode('ascii') == '5':
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps()
        # Envia os dados
        socket_cliente.send(bytes_resp)

# Fecha socket do servidor e cliente
print("Fechando conexão...")
socket_cliente.close()
socket_servidor.close()
print("Aplicação finalizada.")