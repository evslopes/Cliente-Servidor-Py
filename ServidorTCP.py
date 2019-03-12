import socket, psutil, pickle

def cpu():
  resposta = ['Frequência atual: ', psutil.cpu_freq().current,'Frequência max: ',  psutil.cpu_freq().max, 'Porcentagem por CPU: ', psutil.cpu_percent(percpu=True), 'Porcentagem total: ', psutil.cpu_percent()]
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
        resposta.append(cpu())
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