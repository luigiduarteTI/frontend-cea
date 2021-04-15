import dash_bootstrap_components as dbc
from .uteis import funcoes

# Resgata todos os valores de diferentes de 'TIPO DE CONTRATO','SUBMERCADO',TIPO DE LEILÃO' e etc que estão presentes na variável "contrato"
def reuni_filtros(contrato):
    filtros = {
        'TIPO DE CONTRATO':[],
        'SUBMERCADO': [],
        'TIPO DE LEILÃO':[],
        'STATUS':[],
        'PRODUTO': [],
        'VENDEDOR': [],
        'INÍCIO DE SUPRIMENTO': [],
        'FIM DE SUPRIMENTO': []
    }
    
    for chave in filtros.keys():
        for cntkey in contrato.keys():
            filtros[chave].append( contrato[cntkey][chave] )
        filtros[chave] = funcoes.remove_repetidos(filtros[chave])
        filtros[chave].sort()
        
    return filtros        
            
            
def cria_checklist(lista,identificador):
    opcoes = []
    valor = []
    
    for item in lista:
        opcoes.append({"label": item, "value": item})
        valor.append(item)        
           
    return dbc.Checklist(options=opcoes,value=valor,id=identificador)