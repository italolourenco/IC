#!/usr/bin/env python


import os
import time
import thread
import psutil, signal, multiprocessing

def leituraFerramentas(): #Busca as ferramentas no arquivo. 
	listFerramentas = []
	arquivo = 'ferramentas.txt'
	ARQ = open(arquivo, 'r')
	linha = ARQ.readline()
	while linha!='\n' and linha!='':
		listFerramentas.append(linha)
		linha = ARQ.readline()
	return listFerramentas #Retorna uma lista de ferramentas necessarias pra realizacao dos testes.

def verificarDependecias(): #Verifica se as ferramentas estao instaladas.
	print '\n'
	print 'Iniciando a Verificacao das Ferramentas de monitoramento'
	listFerramentas = leituraFerramentas()
	cont = 0 
	while cont < len(listFerramentas):
		ferramenta = listFerramentas[cont]
		print '=================================='
		print 'Verificando a Ferramenta = %s' %ferramenta
		comando = 'which'
		comandoTerminal = comando + ' ' + ferramenta
		teste = os.system(comandoTerminal)
		if teste == 0:
			print 'Ferramenta Ja Instalada'
			print '\n'
		else:
			print 'Ferramenta nao Encontrada - Iniciando processo de Instalcao'
			instalacao = 'sudo apt-get install'
			comandoTerminal = instalacao + ' ' + ferramenta
			os.system(comandoTerminal)
		cont+=1
	print 'Verificacao Realizada com sucesso'

def inicia_servidor():
	print '\n'
	print 'SERVIDOR ON'
	os.system("iperf -s&") #O caracter '&' e para indicar que o comando deve rodar o servidor em backgroud
			       #O caracter '>' arquivo.txt ` e para indicar que a saida do comando deve ser salva no arquivo 
def inicia_cliente():
	print '\n'
	print 'CLIENTE ON'
	#FAZER UM ARQUIVO PARA CONFIGURACAO DAS OPCOES DO IPERF - TALVEZ ()
	os.system("iperf -c 172.17.104.254 -i 5 -t 20 > dadostrasmissao.txt&")
	#Verificar como deixar essa thread "dormindo"

def monitor_cpu(): 
	print '\n'
	print 'INICIANDO MONITOR CPU'
	os.system("python cpu_reader.py > monitorcpu.txt&")
	print 'Leitura Finalizada'

def ligar_firewall():
	print '\n'
	print 'ATIVANDO FIREWALL'
	os.system("sudo su&")
	os.system("./firewall.sh start")
	#verificar o pq do comando sudo su n esta funcionando pelo programa.
	
def salvar_logIptables():
	print '\n'
	print 'Salvando logs dos teste'
	os.system("iptables -nL --verbose > logIptables.txt")
	#Verificar se  a lista de regras esta correta.


def matar_processo(proc):
  # stop process
  for child in psutil.Process(proc.pid).children(recursive=True):
    child.kill() # kill child processes
  os.kill(proc.pid, signal.SIGKILL) # kill parent process
  proc.join()

def main():

	th_servidor = th_cliente = th_monitorCpu = th_monitorRede = th_monitorMemoria = thread 

	#Ativar funcao apenas para novos computadores
	#verificarDependecias()

	#Definir o Script do Firewall - (Criar um bom script ())
	ligar_firewall()

	#Iniciar Thread do servidor - (x)
	th_servidor = multiprocessing.Process(target = inicia_servidor(), args=())
	th_servidor.start()
	

	#Iniciar Thread do cliente/transmissao de dados - (x)
	th_cliente = multiprocessing.Process(target = inicia_cliente(), args=())
	th_cliente.start()
	

	#Iniciar Thread de Leitura cpu - (x)
	th_monitorCpu = multiprocessing.Process(target = monitor_cpu(), args=())
	th_monitorCpu.start()

	#Iniciar Thread de Leitura da placa de rede - (x) #Encotrar uma ferramenta melhor
	#th_monitorRede.star_new_thread = (monitor_rede()) 

	#Iniciar Thread de Leitura da memoria - () #Encontrar alguma ferramenta
	#th_monitorMemoria.star_new_thread = (monitor_memoria())

	#Fechar Servidor
	#Fechar leituras
	#Verificar os logs do iptables - (x)
	salvar_logIptables()
if __name__ == '__main__':
	main()
