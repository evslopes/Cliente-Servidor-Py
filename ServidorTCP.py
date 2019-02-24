import socket, psutil, pickle, os, os.path
from datetime import datetime

print("Nome do dispositivo:", os.getenv("SystemDrive"))
print("Formato: ", psutil.disk_partitions(os.getenv("SystemDrive"))[0][2])
print("Total: ", round(psutil.disk_usage(os.getenv("SystemDrive")).total/1024**3, 2), "GB")
print("Disponível: ", round(psutil.disk_usage(os.getenv("SystemDrive")).free/1024**3, 2), "GB")
print(datetime.fromtimestamp(os.stat(os.getenv("SystemDrive")).st_mtime))
print(datetime.fromtimestamp(os.stat(os.getenv("SystemDrive")).st_ctime))

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
  msg = socket_cliente.recv(100)
  nomeDiretorio = os.getenv("SystemDrive")
  tipoDiretorio = psutil.disk_partitions(os.getenv("SystemDrive"))[0][2]
  tamanhoDiretorio = round(psutil.disk_usage(os.getenv("SystemDrive")).total/1024**3, 2), "GB"
  disponivelDiretorio = round(psutil.disk_usage(os.getenv("SystemDrive")).free/1024**3, 2), "GB"
  # localizacaoDiretorio =
  dataCriacaoDiretorio = datetime.fromtimestamp(os.stat(os.getenv("SystemDrive")).st_mtime)
  dataModificacaoDiretorio = datetime.fromtimestamp(os.stat(os.getenv("SystemDrive")).st_ctime)

  # if msg.decode('ascii') == 'fim':
  #     break
  # O COMENTARIO ACIMA QUEBRA O WHILE INFINITO // decode encode usar quando for algo mto especifico

  # Gera a lista de resposta
  resposta = []
  resposta.append(psutil.cpu_percent())
  mem = psutil.virtual_memory()
  mem_percent = mem.used/mem.total
  resposta.append(mem_percent)
  # Prepara a lista para o envio
  bytes_resp = pickle.dumps(nomeDiretorio)
  # Envia os dados
  socket_cliente.send(bytes_resp)
