import socket
import psutil
import pickle


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
(socket_cliente, addr) = socket_servidor.accept()
print("Conectado a:", str(addr))

while True:
    # Recebe pedido do cliente:
    msg = socket_cliente.recv(1024)
    if msg.decode('ascii') == 'fim':
        break

    elif msg.decode('ascii') == '2':
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
        porcentagem = (available/total)*100
        texto_porcentagem = "% em uso: " + str(porcentagem) + "%"

        resposta.append(texto_total + "  " + texto_available + "  " + texto_porcentagem)

        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(resposta)
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
        resposta.append(psutil.cpu_freq())
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(resposta)
        # Envia os dados
        socket_cliente.send(bytes_resp)


# Fecha socket do servidor e cliente
socket_cliente.close()
socket_servidor.close()
