#Nome dos alunos: Mayara Lima, Elvis Lopes, Antônio Castillo

import socket, time, pickle

# Função do menu
def menu_cliente():

    print("\nDigite a seguinte tecla para ter informações do servidor:\n\n"
          "\t [1]   Informações do  Processador \n"
          "\t [2]   Informações da  Memória \n"
          "\t [3]   Informações do  Disco \n"
          "\t [4]   Informações do  Diretório \n"
          "\t [5]   Informações dos Processos \n"
          "\t [0]   Para sair \n"
          )

# Execução da função do menu
menu_cliente()

# Opção do menu escolhida
a = int(input("Digite o número da informação que deseja saber: "))

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Tenta se conectar ao servidor
    s.connect((socket.gethostname(), 9999))

    # Loop do menu
    while(a != 0):

        # Requisição da posição do menu
        bytes_menu = pickle.dumps(a)
        s.send(bytes_menu)

        # Menu interno
        if a == 5:
            print('\nInformações de processos:', '\n')

            # Converte os bytes para lista
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)
            for x in range(len(lista[0]['pids'])):
                print(lista[0]['pids'][x], lista[0]['pids_nome'][x], lista[0]['pids_memory'][x])

            pid = int(input("\nDigite o PID: "))
            bytes_menu = pickle.dumps(pid)
            s.send(bytes_menu)
            bytes_menu = s.recv(10240)

            reposta2 = pickle.loads(bytes_menu)

            print(reposta2)
        elif a == 1:
            # Converte os bytes para lista
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)

            print('\nInformações do processador:'
                  '\n\nNome: ', lista[0]['cpu_nome'],
                  '\nNº de núcleos lógicos: ', lista[0]['cpu_logico'],
                  '\nNº de núcleos físicos: ', lista[0]['cpu_fisico'],
                  '\nArquitetura: ', lista[0]['cpu_arq'],
                  '\nBits: ', lista[0]['cpu_bits'],
                  '\n\nFrequência atual: ', lista[0]['cpu_frequencia_atual'], '/ Frequência máxima: ', lista[0]['cpu_frequencia_max'],
                  '\n\nPercentual de uso por núcleo: ', lista[0]['cpu_percentual_nucleo'], '/ Percentual de uso total: ', lista[0]['cpu_percentual'])
        elif a == 3:
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)

            print("Total:", round(lista[0][0]/(1024*1024*1024), 2), "GB")
            print("Em uso:", round(lista[0][1]/(1024*1024*1024), 2), "GB")
            print("Livre:", round(lista[0][2]/(1024*1024*1024), 2), "GB")

            print("Percentual de Disco Usado:", lista[0][3], "%")

        elif a == 4:
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)

            #10 caracteres + 1 de espaço
            titulo = '{:11}'.format("Tamanho")

            # Concatenar com 25 caracteres + 2 de espaços
            titulo = titulo + '{:27}'.format("Data de Modificação")

            # Concatenar com 25 caracteres + 2 de espaços
            titulo = titulo + '{:27}'.format("Data de Criação")
            titulo = titulo + "Nome"
            print(titulo)

            for i in lista:
                kb = (lista[i][0]/1000)
                tamanho = '{:10}'.format(str('{:.2f}'.format(kb)+' KB'))
                print(tamanho, time.ctime(lista[i][2]), " ", time.ctime(lista[i][1]), " ", i)


        else:

            # Converte os bytes para lista
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)
            print('\r', lista, end='')


        a = int(input("\nDigite o número da informação que deseja saber: "))

except Exception as erro:
    # Tratar esse erro criando uma funcao com o cógido acima
    print("A aplicação aprensentou erro: " +
          str(erro) + ", aplicação finalizada.")

# Fecha o socket
s.close()

input("Pressione qualquer tecla para confirmar...")
print("Aplicação Finalizada.")
