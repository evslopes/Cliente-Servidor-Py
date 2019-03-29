#Nome dos alunos: Mayara Lima, Elvis Lopes, Antônio Castillo

import socket, time, pickle

# Função do menu

def apresentacao():
    print("\n--------------------------------------------------------------------------------------" )
    print("\tArquitetura de Computadores, Sistemas Operacionais e Redes - Software Cliente" )
    print("--------------------------------------------------------------------------------------" )

def menu_cliente():

    print("\nDigite a seguinte tecla para ter informações do servidor:\n\n"
          "\t [1]   Informações do Processador \n"
          "\t [2]   Informações da Memória \n"
          "\t [3]   Informações do Disco \n"
          "\t [4]   Informações do Diretório \n"
          "\t [5]   Informações de Processo \n"
          "\t [6]   Informações da Redes \n"
          "\t [7]   Informações via Nmap \n"    
          "\t [0]   Para sair \n"   
          )

#____main___
apresentacao()

# Execução da função do menu
menu_cliente()

# Opção do menu escolhida
a = int(input("Digite o número da informação que deseja saber: "))

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Tenta se conectar ao servidor
    s.connect((socket.gethostname(), 9998))

    # Loop do menu
    while(a != 0):

        # Requisição da posição do menu
        bytes_menu = pickle.dumps(a)
        s.send(bytes_menu)

        # Menu interno

        # Processador
        if a == 1:
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
        
        # Memória
        elif a == 2:
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)
            
            print("\nInformações da memória:" )
            print('Total: ', lista[0]['ram_total'], 'GB')
            print('Em uso: ', lista[0]['ram_uso'], 'GB')
            print('Percentual:', lista[0]['ram_percentual'], '%')

        # Disco
        elif a == 3:
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)

            print('\nInformações do disco:\n')
            print("Total:", round(lista[0][0]/(1024*1024*1024), 2), "GB")
            print("Em uso:", round(lista[0][1]/(1024*1024*1024), 2), "GB")
            print("Livre:", round(lista[0][2]/(1024*1024*1024), 2), "GB")
            print("Arquitetutra:", lista[1])

            print("Percentual de Disco Usado:", lista[0][3], "%")

        # Diretorio
        elif a == 4:
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)

            print('\nInformações do diretório atual:\n')    

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

        # Processos
        elif a == 5:
            print('\nInformações de processos:', '\n')

            # Converte os bytes para lista
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)

            print('{:^5}'.format("PIDs"), '{:^10}'.format("RAM em MB"), "Executavel")
            for x in range(len(lista[0]['pids'])):
                print("{:^5}".format(lista[0]['pids'][x]), "{:^10}".format(lista[0]['pids_memory'][x]), lista[0]['pids_nome'][x])

            pid = int(input("\nDigite o PID: "))
            bytes_menu = pickle.dumps(pid)
            s.send(bytes_menu)
            bytes_menu = s.recv(10240)


            reposta2 = pickle.loads(bytes_menu)

            if reposta2 == "PID Inválido":
                print("\nPID Inválido")
            else:
                print('\nNúcleos por PID: ', round(float(reposta2)/100))

        # Rede            
        elif a == 6:
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)
        
            print('\nInformações de interfaces de rede\n')
            for i in lista:
                print("Interface "+ i)
                for j in lista[i]:
                    print(str(j))      
                print("")

        # Rede
        elif a == 7:
            
            print('\nInformações de host via nmap\n')
            # Recebe IP
            ip_string = input("Digite o ip alvo: ")
            ip_lista = ip_string.split('.')
            base_ip = ".".join(ip_lista[0:3]) + '.'       
            print("O teste sera feito com a base: ", base_ip)
            
            # Envia IP
            bytes_ip = pickle.dumps(base_ip)
            s.send(bytes_ip)

            print("Mapping ready...")    
            
            # Recebe os hosts validos    
            bytes = s.recv(102400)
            lista = pickle.loads(bytes)
            print(bytes_ip)
            print(lista)
                
        else:

            # Converte os bytes para lista
            bytes = s.recv(10240)
            lista = pickle.loads(bytes)
            print('\r', lista, end='')
        
        print("--------------------------------------------------------------------------------------\n" )
        a = int(input("\nDigite o número da informação que deseja saber: "))
                

except Exception as erro:
    # Tratar esse erro criando uma funcao com o cógido acima
    print("A aplicação aprensentou erro: " +
          str(erro) + ", aplicação finalizada.")

# Fecha o socket
s.close()

input("Pressione qualquer tecla para confirmar...")
print("Aplicação Finalizada.")