import socket, time, pickle
# Função que imprime a lista formatada
def imprime(l):
  texto = ''
  for i in l:
      texto = texto + '{:>8.2f}'.format(i)
  print(texto)

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Tenta se conectar ao servidor
s.connect((socket.gethostname(), 9999))
while True:
    opcao = int(input("Escolha uma Opção:\n1 - Informações do TP4\n2 - Informações do TP5\n3 - Informações do TP6\n4 - Informações do TP7\n"))
    if(opcao == 1):
        try:
          msg = ' '
          print('{:>8}'.format('%CPU')+'{:>8}'.format('%MEM'))
          for i in range(2):
              # Envia mensagem vazia apenas para indicar a requisição
              s.send(msg.encode('ascii'))
              bytes = s.recv(1024)
              # Converte os bytes para lista
              lista = pickle.loads(bytes)
              
              # enviando dado único
              print(lista)
              
              imprime(lista)
              time.sleep(2)
          #msg = 'fim'
          #a mensagem acima funciona como um finalizador da requesição
          s.send(msg.encode('ascii'))
        except Exception as erro:
          print(str(erro))  
    elif(opcao == 2):
        print("ok")
    elif(opcao == 3):
        print("ok")
    elif(opcao == 4):
        print("ok")
    else:
        print("Digite uma opção válida")

# Fecha o socket
s.close()