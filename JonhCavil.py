# Main do programa de finanças automáticas ... aqui provavelmente virará uma tela, agora são apenas módulos segregados.
# Lucas Vieira Guerreiro Rodrigues Peres
# 11/09/2017

#Imports externos
import re as re #Expressões regulares
#import numpy as np 
#import pandas as pd
#import sys
import datetime #Pacote de manipulação de datas
from dateutil.rrule import rrule, MONTHLY #Funções para geraão de sequencia de datas
import os #Biblioteca com as funções de manipualação de diretório
import PyPDF2

#Classes da solução

class PATHS: 
# Description:  Classe com as constantes de caminho da solução (tipos de dados são escritos em maiúsculo)
# Componentes:
#   - [var] SCR: diretório com os códigos fontes da solução
#   - [var] EXTR: diretório com os extratos das instituições financeiras    
#   - [mod] __init__: inicialização da classe
    def __init__(self): 
    # Description:  Módilo de inicialização da classe de caminhos (todos eles estão hardcoded)
    # Inputs:
    #   - self: os modulos encadeados em python não recebem eles mesmos, é necessário definir na mão estes jovens
        self.scr = "C:\\Users\\semhaga\\Dropbox\\Finances\\JonhCavil\\JonhCavil"
        self.db= "C:\\Users\\semhaga\\Dropbox\\Finances"

class INPUTFILE:
# Description: Classe das constantes com os parâmetros do dados (arquivos) de entrada
# Componentes:
#   - [var] fileID: string com o identificador (no nome do arquivo) do referente tipo de entrada
#   - [var] initDate: data que este arquivo começou a ser colocado na base
#   - [var] endDate: data que este arquivo parou de ser colocado na base (None significa que esta ativo)
    def __init__(self,fileID,initDate,endDate,dir):
    # Description: Método de inicialização da subclasse de arquivos de entrada
    # Inputs:
    #   - fildID: string com o identificador no nome do arquivo
    #   - initDate: data de início de entrada na base
    #   - endDate: data de termino de entrada na base (None = ainda ativo)
    #   - dir: diretório onde ficará os arquivos de cada tipo
        self.fileID =fileID
        self.initDate = initDate
        self.endDate = endDate
        self.dir = dir

class REPORTS:
# Description:  Estrutura com os relatórios de saída da solução. Provavelmente a maioria dos relatórios sairá na tela, porém a primeiro ponto trabalharei com arquivos de saíra
# Componentes: AINDA NÃO SEI
    def __init__(self,fName,line,constants):
    # Módulo de inicialização aqui escreve-se o cabeçalho do arquivo. Inicialmente defini o separador dentro do inicializa~dor, isto pode vir a me dar uma dor de cabelça
        self.sep=';'
        self.dir = constants.paths.reports + '\\' + fName #Diretório do arquivo
        stremmer = open(self.dir,"w") 
        stremmer.write(self.sep.join(line) + '\n') #Criação do cabeçalho 
        stremmer.close()

    def append(self,line):
        stremmer = open(self.dir,"a") 
        stremmer.write(self.sep.join(line) + '\n') 
        stremmer.close()

class CONSTANTS:
# Description: Estrutura com as constantes da solução como por exemplo, data de execução, estrutura de arquivos caminhos das soluções entre outras variáveis
# Componentes:
#   - [var] today: data de execução do código
#   - [var] paths: estrutura de dados com os caminhos definidos na init da classe PATHS
#   - [var] inputsType: dicionário com todos os tipos de arquivo de entrada
#   - [var] reports: dicionário com os arquivos de saída

    def __init__(self):
    # Description: Módulo de inicialização da classe de constantes da solução
        self.today = datetime.datetime.now() #Data de hoje
        self.paths = PATHS() #Inicialização dos caminhos da solução
        self.paths.reports = 'C:\\Users\\semhaga\\Desktop\\'+self.today.strftime('%Y%m%d') + '_JohnReports'
        if not os.path.exists(self.paths.reports): #Caso não exista o código cria o diretório
            os.makedirs(self.paths.reports)
        self.inputsType = dict() #Dicionário com os tipo de arquivo de entrada (e as datas que devem existir)
        self.inputsType['Extrato Itaú Person'] = INPUTFILE('Itau Personalite - 3757 180496', datetime.datetime(2016,8,1),None,self.paths.db + '\\Extratos' )
        self.reports = dict() #Dicionário com os relatórios de saída
        self.reports['logInputs'] = REPORTS('logInputs.csv',['Erro','Arquivo','Mês'],self)

#Funções da solução

def parseItauPersonExt(targetDir):
# Description: Função que executa o parser do pdf com o extrato do Itaú Personalite e retorna uma estrutura de dados. 
# Input:    -targetDir: string com o endereço com o pdf a ser lido
# Output:   - AINDA NÃO DEFINI COMO RETORNAREI ESTE DADO ESTRUTURADO
    streamer = open(targetDir,'rb') #abertura do arquivo
    pdfReader = PyPDF2.PdfFileReader(streamer) #Pegamo o pdf pelá biblioteca
    pageText = pdfReader.getPage(0).extractText()
    streamer.close() #fechamento do arquivo
    return(pageText) #Final da função

#Inicialização das classes
constants = CONSTANTS() #Inicialização da classe com as constantes do problema 

#Controle de entrada dos arquivos (inicialmente verificarei apenas a existência de arquivo)
for IdType, Value in constants.inputsType.items():
    dirFiles = [f for f in os.listdir(Value.dir) if os.path.isfile(os.path.join(Value.dir, f))] #Lista de arquivos de extrato
    if(Value.endDate==None): #Caso o referente tipo não tenha valor maximo, o gabarito deve ser feito até o dia de hoje
        allMonths = [dt.strftime("%Y%m") for dt in rrule(MONTHLY, dtstart=Value.initDate, until=constants.today)] #Lista com todos os meses entre a data de gabarito e a data atual
    else:
        allMonths = [dt.strftime("%Y%m") for dt in rrule(MONTHLY, dtstart=Value.initDate, until=Value.endDate)] #Lista com todos os meses entre a data de gabarito e a data atual
    crtHave = [tMonth + ' - ' + Value.fileID + '.pdf' for tMonth in allMonths] #Critério de existência de arquivo (único teste que farei agora)
    for tCrt in crtHave: #Laço para escrevermos no arquivo
        if (tCrt not in dirFiles ): #Caso não tenhamos o código gera o log de saída
            constants.reports['logInputs'].append(['Erro 01: Ausência de entrada',IdType,allMonths[crtHave.index(tCrt)]])
       #else: #Caso tenha o arquivo eu preciso le-lo (



#Imports internos
#from fileModules import readMethods as fileRead



##Definição da estrutura de dados de caminhos
#paths = dict()
#paths['rawInputs'] = 'dumpsterInputs' #Local onde colocarei os arquivos de entrada brutos (todos serão deletados após a inclusão nas bases oficiais)
#paths['parameters'] = 'parameters'
#paths['outputs'] = 'outputs' #Local onde temos as saídas dos extratos tratados (solução intermediária para utilizarmos o YNAB ainda)

##Definição dos nomes dos arquivos de entrada (terei que verificar estas saidas)
#names = dict()
#names['rawExtratoItau'] = paths['rawInputs'] + '/' + 'raw extrato cc itaú.txt' #Arquivo de saída da minha conta do itaú
#names['rawTicketRest']= paths['rawInputs'] + '/' + 'raw extrato ticket restaurante.txt' #Arquivo de saída da minha conta do ticket restaurante
#names['rawTicketSuper']= paths['rawInputs'] + '/' + 'raw extrato ticket supermercado.txt' #Arquivo de saída da minha conta do ticket restaurante
#names['dicItems']= paths['parameters'] + '/' + 'dicItems.txt' #Dicionário com o tratamento das entradas do banco para valores mais palataveis
#names['dicCategory']=paths['parameters'] + '/' + 'dicCategory.txt' #Dicionário com o tratamento as categorias de cada item

#outputs = dict()
#outputs['errorLog'] = paths['outputs'] + '/' + today.strftime('%Y%m%d') + '_logErro.txt' #Arquivo de saída com o log de erro
#outputs['treatedTicketRest'] = paths['outputs'] + '/' + today.strftime('%Y%m%d') + '_treatedTicketRest.csv' #Arquivo de saída da minha conta do ticket restaurante
#outputs['treatedTicketSuper'] = paths['outputs'] + '/' + today.strftime('%Y%m%d') + '_treatedTicketSuper.csv' #Arquivo de saída da minha conta do ticket restaurante
#outputs['treatedCCItau'] = paths['outputs'] + '/' + today.strftime('%Y%m%d') + '_treatedCCItau.csv' #Arquivo de saída da minha conta corrente do Itaú


#dicItem=dict()
#dicItem=fileRead.dicParameter(names['dicItems']) #Dicionário com o nome tratado dos items
#dicCategory=dict()
#dicCategory=fileRead.dicParameter(names['dicCategory']) #Dicionário com o nome tratado dos items

##Tratamento dos extratos do Ticket 
#pointerLogerror = open(outputs['errorLog'],"w") #Abertura do arquio de log de erro (talvez faça o esquema dque fiz no banco de init ... mas primeiro vamos fazer dessa forma)
#pointerLogerror.write("Arquivo;# Errro; Des;Data;Observação\n")
#pointerLogerror.close()
#pointerTreatedFile = open(outputs['treatedTicketRest'],"w") #Abertura do arquio de log de erro (talvez faça o esquema dque fiz no banco de init ... mas primeiro vamos fazer dessa forma)
#pointerTreatedFile.write("Date,Payee,Category,Memo,Outflow,Inflow\n")
#pointerTreatedFile.close()
#pointerTreatedFile = open(outputs['treatedTicketSuper'],"w") #Abertura do arquio de log de erro (talvez faça o esquema dque fiz no banco de init ... mas primeiro vamos fazer dessa forma)
#pointerTreatedFile.write("Date,Payee,Category,Memo,Outflow,Inflow\n")
#pointerTreatedFile.close()
#for target in ['Rest','Super']: #Laço pois temos dois extratos diferentes
#    rawData = np.genfromtxt(names['rawTicket' + target],delimiter=' \t',names=True,dtype=None) #arquivo de extrato
#    for i in range (len(rawData)): #Laço no arquivo de dados brutos
#        #Tratamento da data (preciso colocar qual ano é o bendito payee)
#        rawDate = rawData[i][0].decode() #Data do input
#        if (rawDate.split('/')[1]=='12'): #Quando tiver mudança de ano tem que tomar cuidado
#            treatedDate = rawDate + '/' + str(today.year-1)
#        else:
#            treatedDate = rawDate + '/' + str(today.year)
#        #Tratamento da descrição 
#        rawDes = rawData[i][1].decode()
#        if (rawDes in dicItem.keys()):
#            treatedDes = dicItem[rawDes]
#        else:
#            treatedDes = rawDes
#            pointerLogerror = open(outputs['errorLog'],"a")
#            pointerLogerror.write("Ticket" + target + ";1;Chave não encontrada;" + treatedDate + ";" + rawDes + "\n")
#            pointerLogerror.close()
#        #Identificação da categoria da entrada
#        if (treatedDes in dicCategory.keys()):
#            categ = dicCategory[treatedDes]
#        else:
#            categ = ''
#            pointerLogerror = open(outputs['errorLog'],"a")
#            pointerLogerror.write("Ticket" + target + ";2;Categoria não encontrada;" + treatedDate + ";" + rawDes + "\n")
#            pointerLogerror.close();
#        #Tratamento do valor (transformar de vírgula para ponto)
#        treatedValue = rawData[i][2].decode().replace(",",".")
#        #Escrita no arquivo tratado
#        pointerTreatedFile = open(outputs['treatedTicket' + target],"a")
#        if (treatedDes=='Salário'): #Não tem diferenciação de valor na entrada manual então tem que fazer hard coded
#            pointerTreatedFile.write(treatedDate + "," + treatedDes + "," + categ + ",,," + treatedValue + "\n")
#        else:
#            pointerTreatedFile.write(treatedDate + "," + treatedDes + "," + categ + ",," + treatedValue + ",\n")
#        pointerTreatedFile.close()


##Tratamento do extrato do Itaú
#rawData=np.genfromtxt(names['rawExtratoItau'],delimiter=';',names=True,dtype=None) #arquivo de extrato
#pointerTreatedFile = open(outputs['treatedCCItau'],"w") #Abertura do arquio de log de erro (talvez faça o esquema dque fiz no banco de init ... mas primeiro vamos fazer dessa forma)
#pointerTreatedFile.write("Date,Payee,Category,Memo,Outflow,Inflow\n")
#pointerTreatedFile.close()
#for i in range (len(rawData)): #Laço no arquivo com os dados brutos
#    treatedDate = rawData[i][0].decode() #Não temos que tratar as datas do extrato do itaú
#    treatedValue = float(rawData[i][2].decode().replace(",",".")) #tratamento do valor de entrada (para este caso tem valores positivos e negativos)
#    #Tratamento da descrição
#    rawDes =  rawData[i][1].decode() #Pra não dar esse comando várias vezes
#    #Casos em que vem na frente a string RSHOP (tratamento diferenciado)
#    if (bool(re.match("^RSHOP",rawDes))): 
#        preTreatedDes = str.split(rawDes,'-')[1] #Pegando a informação importante entre as classificações
#        if(preTreatedDes in dicItem.keys()):
#            treatedDes = dicItem[preTreatedDes]
#        else:
#            treatedDes = rawDes
#            pointerLogerror = open(outputs['errorLog'],"a")
#            pointerLogerror.write("CC Itaú;1;Chave não encontrada;" + treatedDate + ";" + rawDes + "\n")
#            pointerLogerror.close()
#        if (treatedDes in dicCategory.keys()):
#            categ = dicCategory[treatedDes]
#        else:
#            categ = ''
#            pointerLogerror = open(outputs['errorLog'],"a")
#            pointerLogerror.write("CC Itaú;2;Categoria não encontrada;" + treatedDate + ";" + rawDes + "\n")
#            pointerLogerror.close();
#        pointerTreatedFile = open(outputs['treatedCCItau'],"a")
#        if (treatedValue < 0): #se a linha for uma saída
#            pointerTreatedFile.write(treatedDate + "," + treatedDes + "," + categ + ",," + str(abs(treatedValue)) + ",\n")
#        else:
#            pointerTreatedFile.write(treatedDate + "," + treatedDes + "," + categ + ",,," + str(treatedValue) + "\n")
#        pointerTreatedFile.close()
#    #Casso em que a linha é um saque em dinheiro
#    elif (bool(re.search("SAQUE",rawDes))): 
#        pointerTreatedFile = open(outputs['treatedCCItau'],"a")
#        pointerTreatedFile.write(treatedDate + ",Transfer : [Dinheiro]  Carteira,,," + str(abs(float(treatedValue))) + ",\n")
#        pointerTreatedFile.close()
#    #Casso em que a linha é um pagamento da conta de celular
#    elif (bool(re.search("VIVO-SP",rawDes))): 
#        pointerTreatedFile = open(outputs['treatedCCItau'],"a")
#        pointerTreatedFile.write(treatedDate + ",VIVO,Recorrentes: Contas Variáveis,," + str(abs(float(treatedValue))) + ",\n")
#        pointerTreatedFile.close()
#    #Compra de Câmbio vem com uma tag inicial
#    elif(bool(re.match("^AG. VD CAMBIO",rawDes))): 
#        pointerTreatedFile = open(outputs['treatedCCItau'],"a")
#        pointerTreatedFile.write(treatedDate + ",Compra de moeda estrangeira,Planos Futuros: Férias,," + str(abs(treatedValue)) + ",\n")
#        pointerTreatedFile.close()
#   #Para os pagamentos de conta de luz é necessário dividir entre eu e o daniel
#    elif (bool(re.match("^ELETROPAULO",rawDes))): 
#        pointerTreatedFile = open(outputs['treatedCCItau'],"a")
#        partialValue = int(abs(float(treatedValue))*100)
#        if (partialValue % 2 == 0 ): #Se o valor dado é divisível por 2 (não temos que colocar um centavo a mais na conta)
#            partialValue = partialValue // 2
#            treatedValue1 = partialValue / 100
#            treatedValue2 = treatedValue1
#        else:
#            partialValue = partialValue // 2
#            treatedValue1 = partialValue / 100
#            treatedValue2 = (partialValue + 1) / 100
#        pointerTreatedFile.write(treatedDate + ",Transfer : [Dividas] Daniel,,Luz " + datetime.datetime.strptime(treatedDate,"%d/%m/%Y").strftime("%m/%Y") + "," + str(treatedValue1) + ",\n")
#        pointerTreatedFile.write(treatedDate + ",Eletropaulo,Recorrentes: Contas Variáveis,," + str(treatedValue2) + ",\n")
#        pointerTreatedFile.close()
#    #Demais casos (até agora)
#    else:
#        if(rawDes in dicItem.keys()):
#            treatedDes = dicItem[rawDes]
#        else:
#            treatedDes = rawDes
#            pointerLogerror = open(outputs['errorLog'],"a")
#            pointerLogerror.write("CC Itaú;1;Chave não encontrada;" + treatedDate + ";" + rawDes + "\n")
#            pointerLogerror.close()
#        if (treatedDes in dicCategory.keys()):
#            categ = dicCategory[treatedDes]
#        else:
#            categ = ''
#            pointerLogerror = open(outputs['errorLog'],"a")
#            pointerLogerror.write("CC Itaú;2;Categoria não encontrada;" + treatedDate + ";" + rawDes + "\n")
#            pointerLogerror.close();
#        pointerTreatedFile = open(outputs['treatedCCItau'],"a")
#        if (treatedValue < 0): #se a linha for uma saída
#            pointerTreatedFile.write(treatedDate + "," + treatedDes + "," + categ + ",," + str(abs(treatedValue)) + ",\n")
#        else:
#            pointerTreatedFile.write(treatedDate + "," + treatedDes + "," + categ + ",,," + str(treatedValue) + "\n")
#        pointerTreatedFile.close()