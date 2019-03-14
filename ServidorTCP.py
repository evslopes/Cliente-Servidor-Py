import socket, psutil, pickle, cpuinfo


print(cpuinfo.get_cpu_info()['brand'])

# Funções para coleta de informação do processador ---------------------------------------------------------------------
def info_cpu():
  resposta = 'Nome do processador: ', cpuinfo.get_cpu_info()['brand'], '\nArquitetura do processador: ', cpuinfo.get_cpu_info()['arch'], '\nBits do processador: ', cpuinfo.get_cpu_info()['bits'], '\nNúmero de processadores lógicos: ', psutil.cpu_count(logical=True), '\nNúmero de processadores físicos: ', psutil.cpu_count(logical=False), '\nFrequência atual: ', psutil.cpu_freq().current, 'Frequência max: ',  psutil.cpu_freq().max, '\nPorcentagem por CPU: ', psutil.cpu_percent(percpu=True), '\nPorcentagem total: ', psutil.cpu_percent()
  return resposta

def uso_memoria():
    resposta = []

    # buscando memoria total
    mem = psutil.virtual_memory()
    total = round(mem.total/(1024*1024*1024), 2)
    texto_total = "Memória Total: " + str(total) + "GB"

    # buscando memoria em uso
    mem_a = psutil.virtual_memory()
    available = round(mem.available/(1024*1024*1024), 2)
    texto_available = "Memória em uso: " + str(total - available) + "GB"

    # calculando porcentagem de uso
    porcentagem = 100-((available/total)*100)
    texto_porcentagem = "--- " + str(porcentagem) + "%"

    resposta.append(texto_total + "  " + texto_available +
                    "  " + texto_porcentagem)

    return resposta


def info_redes():
    resposta = []

    dic_interfaces = psutil.net_if_addrs('lo')
    texto = "Interface de rede: " + str(dic_interfaces) + "."

    resposta.append(texto)
    return resposta

def info_processos():

    return resposta

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