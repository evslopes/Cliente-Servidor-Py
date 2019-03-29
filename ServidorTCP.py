#Nome dos alunos: Mayara Lima, Elvis Lopes, Antônio Castillo

import socket, psutil, pickle, cpuinfo, os, nmap, subprocess, platform


# Funções

def apresentacao():
    print("\n--------------------------------------------------------------------------------------" )
    print("\tArquitetura de Computadores, Sistemas Operacionais e Redes - Software Servidor" )
    print("--------------------------------------------------------------------------------------" )

# interecao servidor
def inter_inicio(a):

    print("--------------------------------------------------------------------------------------\n" )
    print("Conectado a:", str(addr))
    print("\nRecebendo solicitação do cliente...")    
    if (a==1):
      print("\nColetando Informações do Processador...")  
    elif (a==2):
      print("\nColentando Informações da Memória...")  
    elif (a==3):
      print("\nColentando Informações do Disco...")  
    elif (a==4):
      print("\nColentando Informações do Diretório...")  
    elif (a==5):
      print("\nColentando Informações de Processo...")  
    elif (a==6):
      print("\nColentando Informações da Rede...")  
    elif (a==7):
      print("\nColentando Informações de Host...")   

def inter_fim():

    print("\nTodos os dados enviados do cliente...\n")
    print("--------------------------------------------------------------------------------------\n" )           

# CPU
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

# Memória
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

# Disco
def info_disco():
    resposta = []
    resposta.append(psutil.disk_usage('/'))
    resposta.append(psutil.disk_partitions('/')[0][2])

    return resposta

# Diretorio
def info_diretorio():

    resposta = {}
    lista = os.listdir()

    for i in lista:
        if os.path.isfile(i):
            resposta[i] = []
            resposta[i].append(os.stat(i).st_size)
            resposta[i].append(os.stat(i).st_ctime)
            resposta[i].append(os.stat(i).st_mtime)


    return resposta

# Processos
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

# Interfaces
def info_redes():
   
    resposta = psutil.net_if_addrs()
    return resposta


# Nmap

# Definindo a plataforma 
plataforma = platform.system()
args = []
if plataforma == "Windows":
    args = ["ping", "-n", "1", "-l", "1", "-w", "100", 'www.google.com']

else:
    args = ['ping', '-c', '1', '-W', '1', 'www.google.com']

ret_cod = subprocess.call(args,
                        stdout=open(os.devnull, 'w'),
                        stderr=open(os.devnull, 'w'))


def retorna_codigo_ping(hostname):
    """Usa o utilitario ping do sistema operacional para encontrar   o host. ('-c 5') indica, 
        em sistemas linux, que deve mandar 5   pacotes. ('-W 3') indica, em sistemas linux, 
            que deve esperar 3   milisegundos por uma resposta. Esta funcao retorna o codigo de   resposta do ping"""
    
    plataforma = platform.system()
    args = []
    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]

    ret_cod = subprocess.call(args,
                                stdout=open(os.devnull, 'w'),
                                stderr=open(os.devnull, 'w'))
    return ret_cod


def verifica_hosts(base_ip):
    
    host_validos = []
    return_codes = dict()
    for i in range(1, 255):

        return_codes[base_ip +
                     '{0}'.format(i)] = retorna_codigo_ping(base_ip + '{0}'.format(i))
        if i % 20 == 0:
            print(".", end="")
        if return_codes[base_ip + '{0}'.format(i)] == 0:
            host_validos.append(base_ip + '{0}'.format(i))

    return host_validos

def obter_hostnames(host_validos):
    nm = nmap.PortScanner()
    for i in host_validos:
        try:
            nm.scan(i)
            print("O IP 10.10.",i, "possui o nome", nm[i].hostname())
        except:
            pass


# ___main___

apresentacao()

# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Obtem o nome da máquina
host = socket.gethostname()
porta = 9998
# Associa a porta
socket_servidor.bind((host, porta))
# Escutando...
socket_servidor.listen()
print("\nServidor de nome", host, "esperando conexão na porta", porta)
# Aceita alguma conexão
(socket_cliente,addr) = socket_servidor.accept()

print("\nEstabelecebndo conexão...")
print("\nConectado a:", str(addr))
print("\n\nAguardando solicitação do cliente...\n")    

while True:
    
    try:
        # Recebimento da posição do menu
        bytes_menu = socket_cliente.recv(10240)
        menu = pickle.loads(bytes_menu)

        # Fechar
        if menu == 0:
            print("\nFechando conexão...")
            break

        # CPU
        elif menu == 1:
            inter_inicio(menu)
            resposta = []
            resposta.append(info_cpu())
            bytes_resp = pickle.dumps(resposta)
            # Envia os dados
            socket_cliente.send(bytes_resp)
            inter_fim()

        # RAM
        elif menu == 2:
            inter_inicio(menu)
            resposta = []
            resposta.append(info_memoria())
            # Prepara a lista para o envio
            bytes_resp = pickle.dumps(resposta)
            # Envia os dados
            socket_cliente.send(bytes_resp)
            inter_fim()

        # DISCO
        elif menu == 3:
            inter_inicio(menu)
            # Prepara a lista para o envio
            bytes_resp = pickle.dumps(info_disco())
            # Envia os dados
            socket_cliente.send(bytes_resp)
            inter_fim()

        # DIRETORIO
        elif menu == 4:

            inter_inicio(menu)
            # Prepara a lista para o envio
            bytes_resp = pickle.dumps(info_diretorio())
            # Envia os dados
            socket_cliente.send(bytes_resp)
            inter_fim()

        # PROCESSOS
        elif menu == 5:

            inter_inicio(menu)
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

            inter_fim()

        # Interfaces
        elif menu == 6:
            
            inter_inicio(menu)
            # Prepara a lista para o envio
            bytes_resp = pickle.dumps(info_redes())
            # Envia os dados
            socket_cliente.send(bytes_resp)
            inter_fim()

        # Hosts
        elif menu == 7:

            inter_inicio(menu)
            #Recebe IP
            bytes_ip = socket_cliente.recv(102400)
            ip = pickle.loads(bytes_ip)
            print("IP:",ip)
            
            # valida os hosts
            host_validos = verifica_hosts(ip)
            print("\nHosts válidos; ", host_validos)
            # Prepara a lista para o envio
            bytes_resp = pickle.dumps(host_validos)
            # Envia os hosts válidos
            socket_cliente.send(bytes_resp)    
                
            obter_hostnames(host_validos)

            resposta = []
            resposta.append(host_validos)

            print("\nResposta: ", resposta)

            # Prepara a lista para o envio
            bytes_resp2 = pickle.dumps(resposta)
            # Envia os dados
            socket_cliente.send(bytes_resp2)

            inter_fim()
    
    except Exception as erro:
        print("")
        break    


# Fecha socket do servidor e cliente
print("Fechando conexão...\n")
socket_cliente.close()
print("Conexão encerrada.")
socket_servidor.close()
print("Aplicação finalizada.\n")