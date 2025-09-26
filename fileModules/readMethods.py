#Arquivo com os métodos de leitura de arquivos

def dicParameter (fileDir):
    # Método para leitura de parâmetros dados como dicionários. São arquivos CSV em que na primeira coluna há a chave do dicioário e na segunda seu respectivo valor
    # v1.0 (11/09/2017) - Lucas Vieira Guerreiro Rodrigues Peres
    # Inputs: fileDir [string]: caminho de lietura do dicionario
    # Outputs: dicionário com o arquivo tratado

    # Imports iniciais para o método
    import csv

    #Declaração e alocação das variaveis
    dic = dict()
    with open(fileDir, mode='r') as infile:
        reader = csv.reader(infile)
        dic = {rows[0]:rows[1] for rows in reader}
    return(dic)

# Teste unitário deste módulo
if (__name__=='__main__'):
    dic = dicParameter ('parameters/dicItems.txt')
    print(dic)
