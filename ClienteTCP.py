import socket, time, pickle

# Função do menu
def menu_cliente():

    print("\nDigite a seguinte tecla para ter informações do servidor:\n\n"
          "\t [1]   Informação do Processador \n"
          "\t [2]   Informação da Memória \n"
          "\t [3]   Informação do Disco \n"
          "\t [4]   Informação do Diretório \n"
          "\t [5]   Informação de Processos \n"
          "\t [0]   Para sair \n"
          )

# Execução da função do menu
menu_cliente()

# Criação do array para salvar as opções escolhidas no menu
menu = []

# Opção do menu escolhida
a = int(input("Digite o número da informação que deseja saber: "))

# Adição da Adição da opção escolhida no array
menu.append(a)

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Tenta se conectar ao servidor
    s.connect((socket.gethostname(), 9999))

    # Loop do menu
    while(menu[0] != 0):
        # Requisição da posição do menu
        bytes_menu = pickle.dumps(menu)
        s.send(bytes_menu)

        # Converte os bytes para lista
        bytes = s.recv(10240)
        lista = pickle.loads(bytes)
        print('\r', lista, end='')

        # Menu interno
        if menu[0] == 5:

            pid = int(input("\nDigite o PID: "))
            bytes_menu = pickle.dumps(pid)
            s.send(bytes_menu)
            bytes_menu = s.recv(10240)

            reposta2 = pickle.loads(bytes_menu)

            print(reposta2)

        a = int(input("\nDigite o número da informação que deseja saber: "))
        del menu[0]
        menu.insert(0, a)
        bytes_menu = pickle.dumps(menu)
        s.send(bytes_menu)

except Exception as erro:
    # Tratar esse erro criando uma funcao com o cógido acima
    print("A aplicação aprensentou erro: " +
          str(erro) + ", aplicação finalizada.")

# Fecha o socket
s.close()

input("Pressione qualquer tecla para confirmar...")
print("Aplicação Finalizada.")