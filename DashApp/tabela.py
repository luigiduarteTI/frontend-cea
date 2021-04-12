from .uteis import funcoes
from datetime import datetime,date
#import locale

style_header={
    'backgroundColor': '#0D6ABF',
    'color': 'white',
    'fontWeight': 'bold',
    'fontSize': '14px'
}
style_cell={
    'backgroundColor': 'white',
    'color': 'black',
    'border': '1px solid #1F94FF',
    'textAlign': 'center',
    'padding': '7px'
}

style_table={
    'overflowX': 'auto'
}

style_data_conditional=[
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': '#C5E5EA'
    }
]

tabela2 = {}
for x in range(262):
    tabela2["Colunaaaaaa" + str(x)] = []
    for y in range(1200):
        if x == 6:
            tabela2["Colunaaaaaa" + str(x)].append("Lin - {} Coluna maior {} ".format(y,x))
        else:
            tabela2["Colunaaaaaa" + str(x)].append("Lin - {} Col {} ".format(y,x))

#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')





# DEFINIÇÃO DA FUNÇÃO DA TABELA DOS CONTRATOS



def constroi_tabela_cnt(contrato,valorContrato,filtros,inicioData,fimData,mes_ano,det_res,mwh_mwm):
    
    if det_res == 'Detalhado':
        
        datas = []
        for chave in valorContrato.keys():
            datas.append(chave[-10:])
            
        datas = funcoes.remove_repetidos(datas)
        datas.sort(key=lambda l: l.split('-')[2] + '-' + l.split('-')[1] + '-' + l.split('-')[0])
        
        contratos = {}
        for chave in contrato.keys():
            contratos.update({chave: contrato[chave]}) 
   
        for x in range(len(contratos.keys()) -1,-1,-1):
            idContrato = list(contratos.keys())[x]
            if filtros['TIPO DE CONTRATO']:
                if contratos[idContrato]['TIPO DE CONTRATO'] in filtros['TIPO DE CONTRATO']:
                    del contratos[idContrato]
            if filtros['SUBMERCADO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['SUBMERCADO'] in filtros['SUBMERCADO']:
                        del contratos[idContrato]
            if filtros['TIPO DE LEILÃO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['TIPO DE LEILÃO'] in filtros['TIPO DE LEILÃO']:
                        del contratos[idContrato]
            if filtros['STATUS']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['STATUS'] in filtros['STATUS']:
                        del contratos[idContrato]
            if filtros['PRODUTO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['PRODUTO'] in filtros['PRODUTO']:
                        del contratos[idContrato]
            if filtros['VENDEDOR']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['VENDEDOR'] in filtros['VENDEDOR']:
                        del contratos[idContrato]     
            if filtros['INÍCIO DE SUPRIMENTO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['INÍCIO DE SUPRIMENTO'] in filtros['INÍCIO DE SUPRIMENTO']:
                        del contratos[idContrato]
            if filtros['FIM DE SUPRIMENTO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['FIM DE SUPRIMENTO'] in filtros['FIM DE SUPRIMENTO']:
                        del contratos[idContrato]
            
        
        tabela = {
            'ID': [], 
            'TIPO DE CONTRATO': [], 
            'CÓDIGO': [], 
            'INÍCIO DE SUPRIMENTO': [], 
            'FIM DE SUPRIMENTO': [], 
            'STATUS': [], 
            'VENDEDOR': [], 
            'EMPREENDIMENTO': [], 
            'SUBMERCADO': [], 
            'TIPO DE LEILÃO': [], 
            'PRODUTO': [], 
            'DATA': [], 
            'TIPO DE ENERGIA': [], 
            'TIPO DE FONTE': [],
        #  'PREÇO NA DATA DO LEILÃO': [], 
        #   'REAJUSTE': []}
        } 
        for cntKey in contratos.keys():
            tabela['ID'].append(contratos[cntKey]['ID'])
            tabela['TIPO DE CONTRATO'].append(contratos[cntKey]['TIPO DE CONTRATO'])
            tabela['CÓDIGO'].append(contratos[cntKey]['CÓDIGO'])
            tabela['INÍCIO DE SUPRIMENTO'].append(contratos[cntKey]['INÍCIO DE SUPRIMENTO'])
            tabela['FIM DE SUPRIMENTO'].append(contratos[cntKey]['FIM DE SUPRIMENTO'])
            tabela['STATUS'].append(contratos[cntKey]['STATUS'])
            tabela['VENDEDOR'].append(contratos[cntKey]['VENDEDOR'])
            tabela['EMPREENDIMENTO'].append(contratos[cntKey]['EMPREENDIMENTO'])
            tabela['SUBMERCADO'].append(contratos[cntKey]['SUBMERCADO'])
            tabela['TIPO DE LEILÃO'].append(contratos[cntKey]['TIPO DE LEILÃO'])
            tabela['PRODUTO'].append(contratos[cntKey]['PRODUTO'])
            tabela['DATA'].append(contratos[cntKey]['DATA'])
            tabela['TIPO DE ENERGIA'].append(contratos[cntKey]['TIPO DE ENERGIA'])
            tabela['TIPO DE FONTE'].append(contratos[cntKey]['TIPO DE FONTE'])
        
        
        if mes_ano == 'Mensal':
            
            for x in range(len(datas) -1,-1,-1):
                data = date(int(datas[x].split('-')[2]),int(datas[x].split('-')[1]),int(datas[x].split('-')[0]))
                inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
                fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
                # inicio = date(2019,1,1)
                # fim = date(2019,6,1)
                if inicio <= data <= fim:
                    continue
                else:
                    datas.pop(x)
            
            for data in datas:
                tabela.update({data:[]})
            
            cont = 0
            mw = 0
            keys = valorContrato.keys()
            for data in datas:
                for idContrato in tabela['ID']:
                    cont = cont + 1
                    idvlcnt = idContrato + '-' + data
                    if idvlcnt in keys:
                        if mwh_mwm == 'MWh':
                            mw = valorContrato[idvlcnt]['mwh']
                        elif mwh_mwm == 'MWm':
                            mw = valorContrato[idvlcnt]['mwm']
                        else:
                            break
                    else:
                        mw = 0
                    tabela[data].append( str(round(mw, 5)).replace('.',',') )
                    mw = 0
                
            #print(tabela)    
            for data in datas:
                dataptBr = funcoes.transforma_data(data)
                dataptBr = funcoes.data_ptBr(dataptBr).upper()
                tabela[dataptBr] = tabela[data]
                del tabela[data]
        else:
            anos = []
            datas = []
            for chave in valorContrato.keys():
                datas.append(chave[-10:])
                
            datas = funcoes.remove_repetidos(datas)
            
            anos = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))
            
            for ano in anos:
                tabela.update({ano:[]})
            
            mw = 0
            
            keys = valorContrato.keys()
            for ano in anos:
                for idContrato in tabela['ID']:
                    for x in range(1,13):
                        if x <= 9:
                            idvlcnt = idContrato + '-01-0' + str(x) + '-' + ano
                        else:
                            idvlcnt = idContrato + '-01-' + str(x) + '-' + ano
                        if idvlcnt in keys:
                            if mwh_mwm == 'MWh':
                                mw = mw + valorContrato[idvlcnt]['mwh']
                            elif mwh_mwm == 'MWm':
                                mw = mw + valorContrato[idvlcnt]['mwm']
                            else:
                                break
                        else:
                            continue
                    if mwh_mwm == 'MWm':
                        horas = funcoes.numero_horas_ano(ano)
                        mw = mw / horas
                    tabela[ano].append( str(round(mw, 5)).replace('.',',') )
                    mw = 0
            
        tabela.pop('ID')
        return tabela
    else:
        
        resumido = contrato
        resumidos = {}
        for chave in resumido.keys():
            resumidos.update({chave: resumido[chave]}) 
        
        datas = []
        for chave in resumidos.keys():
            datas.append(resumidos[chave]['data'])
            
        datas = funcoes.remove_repetidos(datas)
        datas.sort(key=lambda l: l.split('-')[2] + '-' + l.split('-')[1] + '-' + l.split('-')[0])
        
        for x in range(len(resumidos.keys()) -1,-1,-1):
            idResumido = list(resumidos.keys())[x]
            if filtros['TIPO DE CONTRATO']:
                if resumidos[idResumido]['tipo de contrato'] in filtros['TIPO DE CONTRATO']:
                    del resumidos[idResumido]
            if filtros['TIPO DE LEILÃO']:
                if x < len(resumidos) and idResumido in resumidos.keys(): 
                    if resumidos[idResumido]['tipo de leilao'] in filtros['TIPO DE LEILÃO']:
                        del resumidos[idResumido]
            if filtros['PRODUTO']:
                if x < len(resumidos) and idResumido in resumidos.keys(): 
                    if resumidos[idResumido]['produto'] in filtros['PRODUTO']:
                        del resumidos[idResumido]
          
        tabela = {
            'TIPO DE CONTRATO': [], 
            'TIPO DE LEILÃO': [], 
            'PRODUTO': [], 
            'DATA': [],
        }     
        
        ids=[]
        for rsm in resumidos.keys():
            ids.append(rsm[:-11])
        ids = list(dict.fromkeys(ids))
        for i in ids:
            tabela['TIPO DE CONTRATO'].append(i.split(';')[0] )
            tabela['TIPO DE LEILÃO'].append(i.split(';')[1])
            tabela['PRODUTO'].append(i.split(';')[2])
            tabela['DATA'].append(i.split(';')[3])
         
            
        if mes_ano == 'Mensal':
            
            
            for x in range(len(datas) -1,-1,-1):
                data = date(int(datas[x].split('-')[2]),int(datas[x].split('-')[1]),int(datas[x].split('-')[0]))
                inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
                fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
                # inicio = date(2019,1,1)
                # fim = date(2019,6,1)
                if inicio <= data <= fim:
                    continue
                else:
                    datas.pop(x)
        
            for data in datas:
                tabela.update({data:[]})
        
            mw = 0
         
            for data in datas:
                for x in range(len(tabela['TIPO DE CONTRATO'])):
                    idResumido = str(tabela['TIPO DE CONTRATO'][x] + ';' + tabela['TIPO DE LEILÃO'][x] + ';' + tabela['PRODUTO'][x] + ';' + tabela['DATA'][x] + ';' + data)
                    if mwh_mwm == 'MWh':
                        mw = resumidos[idResumido]['soma mwh']
                    elif mwh_mwm == 'MWm':
                        mw = resumidos[idResumido]['soma mwm']
                    else:
                        break
                    tabela[data].append( str(round(mw, 5)).replace('.',',') )
                    mw = 0
                    
            for data in datas:
                dataptBr = funcoes.transforma_data(data)
                dataptBr = funcoes.data_ptBr(dataptBr).upper()
                tabela[dataptBr] = tabela[data]
                del tabela[data]

        else:
            
            anos = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))
            for ano in anos:
                tabela.update({ano:[]})
                
            mw = 0
            for x in range(len(tabela['TIPO DE CONTRATO'])):
                for data in datas:
                    idResumido = str(tabela['TIPO DE CONTRATO'][x] + ';' + tabela['TIPO DE LEILÃO'][x] + ';' + tabela['PRODUTO'][x] + ';' + tabela['DATA'][x] + ';' + data)
                    if mwh_mwm == 'MWh':
                        mw += resumidos[idResumido]['soma mwh']
                    elif mwh_mwm == 'MWm':
                        mw += resumidos[idResumido]['soma mwh']
                    else:
                        break
                    if data[:5] == '01-12':
                        if mwh_mwm == 'MWm':
                            horas = funcoes.numero_horas_ano(datas[x][-4:])
                            mw = mw / horas
                        tabela[data[-4:]].append( str(round(mw, 5)).replace('.',',') )
                        mw = 0
            
        return tabela
    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    
    

def constroi_tabela_balanco(balanco,inicioData,fimData,mes_ano):
    
    balanço = []
    for blc in balanco:
        balanço.append(blc)
        
    tabela = {
        'DATA': [], 
        'TOTAL CONTRATOS': [], 
        'CARGA': [], 
        'SOBRA (MWh)': [], 
        'SOBRA (%)': [], 
    }
    
    if mes_ano == 'Mensal':
        
        for x in range(len(balanço) -1,-1,-1):
            data = date(int(balanço[x]['data'].split('-')[2]),int(balanço[x]['data'].split('-')[1]),int(balanço[x]['data'].split('-')[0]))
            inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
            fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
            if inicio <= data <= fim:
                continue
            else:
                balanço.pop(x) 
        
        for blc in balanço:
            tabela['DATA'].append(blc['data'])
            tabela['TOTAL CONTRATOS'].append(blc['total_mwh'])
            tabela['CARGA'].append(blc['carga'])
            tabela['SOBRA (MWh)'].append( round(blc['total_mwh'] - blc['carga'], 2))
            tabela['SOBRA (%)'].append( round(((blc['total_mwh'] - blc['carga']) / blc['carga']) * 100, 2) )
        
        tabela['SOBRA (%)']  = list(map(lambda x: str(x) + '%',tabela['SOBRA (%)']))
        
        return tabela
    else:
        anos = []
        for blc in balanço:
            anos.append(blc['data'])
        anos = funcoes.remove_repetidos(map(funcoes.separa_anos,anos))
        
        mwh = 0
        carga = 0
        for ano in anos:
            for blc in balanco:
                ano_balanco = blc['data'].split('-')[2]
                if ano_balanco == ano:
                    mwh = mwh + blc['total_mwh']
                    carga = carga + blc['carga']
                
            tabela['DATA'].append(ano)
            tabela['TOTAL CONTRATOS'].append(round(mwh,2))
            tabela['CARGA'].append(round(carga,2))
            tabela['SOBRA (MWh)'].append( round(mwh - carga, 2))
            tabela['SOBRA (%)'].append( round(((mwh - carga) / carga) * 100, 2) )
        
        tabela['SOBRA (%)']  = list(map(lambda x: str(x) + '%',tabela['SOBRA (%)']))

        return tabela
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def constroi_tabela_cts(contrato,valorContrato,filtros,inicioData,fimData,mes_ano,det_res,uni_tot):
    
    if det_res == 'Detalhado':
        
        datas = []
        for chave in valorContrato.keys():
            datas.append(chave[-10:])
            
        datas = funcoes.remove_repetidos(datas)
        datas.sort(key=lambda l: l.split('-')[2] + '-' + l.split('-')[1] + '-' + l.split('-')[0])
        
        contratos = {}
        for chave in contrato.keys():
            contratos.update({chave: contrato[chave]}) 
   
        for x in range(len(contratos.keys()) -1,-1,-1):
            idContrato = list(contratos.keys())[x]
            if filtros['TIPO DE CONTRATO']:
                if contratos[idContrato]['TIPO DE CONTRATO'] in filtros['TIPO DE CONTRATO']:
                    del contratos[idContrato]
            if filtros['SUBMERCADO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['SUBMERCADO'] in filtros['SUBMERCADO']:
                        del contratos[idContrato]
            if filtros['TIPO DE LEILÃO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['TIPO DE LEILÃO'] in filtros['TIPO DE LEILÃO']:
                        del contratos[idContrato]
            if filtros['STATUS']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['STATUS'] in filtros['STATUS']:
                        del contratos[idContrato]
            if filtros['PRODUTO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['PRODUTO'] in filtros['PRODUTO']:
                        del contratos[idContrato]
            if filtros['VENDEDOR']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['VENDEDOR'] in filtros['VENDEDOR']:
                        del contratos[idContrato]     
            if filtros['INÍCIO DE SUPRIMENTO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['INÍCIO DE SUPRIMENTO'] in filtros['INÍCIO DE SUPRIMENTO']:
                        del contratos[idContrato]
            if filtros['FIM DE SUPRIMENTO']:
                if x < len(contratos) and idContrato in contratos.keys(): 
                    if contratos[idContrato]['FIM DE SUPRIMENTO'] in filtros['FIM DE SUPRIMENTO']:
                        del contratos[idContrato]
            
        
        tabela = {
            'ID': [], 
            'TIPO DE CONTRATO': [], 
            'CÓDIGO': [], 
            'INÍCIO DE SUPRIMENTO': [], 
            'FIM DE SUPRIMENTO': [], 
            'STATUS': [], 
            'VENDEDOR': [], 
            'EMPREENDIMENTO': [], 
            'SUBMERCADO': [], 
            'TIPO DE LEILÃO': [], 
            'PRODUTO': [], 
            'DATA': [], 
            'TIPO DE ENERGIA': [], 
            'TIPO DE FONTE': [],
            'PREÇO NA DATA DO LEILÃO': [], 
            'REAJUSTE': []
        } 
        
        for cntKey in contratos.keys():
            tabela['ID'].append(contratos[cntKey]['ID'])
            tabela['TIPO DE CONTRATO'].append(contratos[cntKey]['TIPO DE CONTRATO'])
            tabela['CÓDIGO'].append(contratos[cntKey]['CÓDIGO'])
            tabela['INÍCIO DE SUPRIMENTO'].append(contratos[cntKey]['INÍCIO DE SUPRIMENTO'])
            tabela['FIM DE SUPRIMENTO'].append(contratos[cntKey]['FIM DE SUPRIMENTO'])
            tabela['STATUS'].append(contratos[cntKey]['STATUS'])
            tabela['VENDEDOR'].append(contratos[cntKey]['VENDEDOR'])
            tabela['EMPREENDIMENTO'].append(contratos[cntKey]['EMPREENDIMENTO'])
            tabela['SUBMERCADO'].append(contratos[cntKey]['SUBMERCADO'])
            tabela['TIPO DE LEILÃO'].append(contratos[cntKey]['TIPO DE LEILÃO'])
            tabela['PRODUTO'].append(contratos[cntKey]['PRODUTO'])
            tabela['DATA'].append(contratos[cntKey]['DATA'])
            tabela['TIPO DE ENERGIA'].append(contratos[cntKey]['TIPO DE ENERGIA'])
            tabela['TIPO DE FONTE'].append(contratos[cntKey]['TIPO DE FONTE'])
            tabela['PREÇO NA DATA DO LEILÃO'].append(contratos[cntKey]['PRECO DATA LEILAO'])
            tabela['REAJUSTE'].append(contratos[cntKey]['REAJUSTE'])
        
        
        if mes_ano == 'Mensal':
            
            for x in range(len(datas) -1,-1,-1):
                data = date(int(datas[x].split('-')[2]),int(datas[x].split('-')[1]),int(datas[x].split('-')[0]))
                inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
                fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
                # inicio = date(2019,1,1)
                # fim = date(2019,6,1)
                if inicio <= data <= fim:
                    continue
                else:
                    datas.pop(x)
            
            for data in datas:
                tabela.update({data:[]})
                
            rs = 0
            keys = valorContrato.keys()
            for data in datas:
                for idContrato in tabela['ID']:
                    idvlcnt = idContrato + '-' + data
                    if idvlcnt in keys:
                        if uni_tot == 'Unitário':
                            rs = valorContrato[idvlcnt]['custo_unitario']
                        elif uni_tot == 'Total':
                            rs = valorContrato[idvlcnt]['custo_total']
                        else:
                            break
                    else:
                        rs = 0
                    #tabela[data].append(locale.currency(round(rs,5)))
                    tabela[data].append(round(rs,5))
                    rs = 0
                
            #print(tabela)    
            for data in datas:
                dataptBr = funcoes.transforma_data(data)
                dataptBr = funcoes.data_ptBr(dataptBr).upper()
                tabela[dataptBr] = tabela[data]
                del tabela[data]
        else:
            anos = []
            datas = []
            for chave in valorContrato.keys():
                datas.append(chave[-10:])
                
            datas = funcoes.remove_repetidos(datas)
            
            anos = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))
            
            for ano in anos:
                tabela.update({ano:[]})
            
            rs = 0
            mw = 0
            keys = valorContrato.keys()
            for ano in anos:
                for idContrato in tabela['ID']:
                    for x in range(1,13):
                        if x <= 9:
                            idvlcnt = idContrato + '-01-0' + str(x) + '-' + ano
                        else:
                            idvlcnt = idContrato + '-01-' + str(x) + '-' + ano
                        if idvlcnt in keys:
                            if uni_tot == 'Unitário':
                                rs += valorContrato[idvlcnt]['custo_total']
                                mw += valorContrato[idvlcnt]['mwh']
                            elif uni_tot == 'Total':
                                rs = rs + valorContrato[idvlcnt]['custo_total']
                            else:
                                break
                        else:
                            continue
                    if uni_tot == 'Unitário':
                        if mw != 0:
                            rs = rs / mw
                            mw = 0
                        else:
                            rs = 0
                    #tabela[ano].append(locale.currency(round(rs,5)))
                    tabela[ano].append(round(rs,5))
                    rs = 0
            
        tabela.pop('ID')
        return tabela
    else:
        
        resumido = contrato
        resumidos = {}
        for chave in resumido.keys():
            resumidos.update({chave: resumido[chave]}) 
        
        datas = []
        for chave in resumidos.keys():
            datas.append(resumidos[chave]['data'])
            
        datas = funcoes.remove_repetidos(datas)
        datas.sort(key=lambda l: l.split('-')[2] + '-' + l.split('-')[1] + '-' + l.split('-')[0])
        
        for x in range(len(resumidos.keys()) -1,-1,-1):
            idResumido = list(resumidos.keys())[x]
            if filtros['TIPO DE CONTRATO']:
                if resumidos[idResumido]['tipo de contrato'] in filtros['TIPO DE CONTRATO']:
                    del resumidos[idResumido]
            if filtros['TIPO DE LEILÃO']:
                if x < len(resumidos) and idResumido in resumidos.keys(): 
                    if resumidos[idResumido]['tipo de leilao'] in filtros['TIPO DE LEILÃO']:
                        del resumidos[idResumido]
            if filtros['PRODUTO']:
                if x < len(resumidos) and idResumido in resumidos.keys(): 
                    if resumidos[idResumido]['produto'] in filtros['PRODUTO']:
                        del resumidos[idResumido]
          
        tabela = {
            'TIPO DE CONTRATO': [], 
            'TIPO DE LEILÃO': [], 
            'PRODUTO': [], 
            'DATA': [],
        }     
        
        ids=[]
        for rsm in resumidos.keys():
            ids.append(rsm[:-11])
        ids = list(dict.fromkeys(ids))
        
        for i in ids:
            tabela['TIPO DE CONTRATO'].append(i.split(';')[0] )
            tabela['TIPO DE LEILÃO'].append(i.split(';')[1])
            tabela['PRODUTO'].append(i.split(';')[2])
            tabela['DATA'].append(i.split(';')[3])
         
            
        if mes_ano == 'Mensal':
            
            
            for x in range(len(datas) -1,-1,-1):
                data = date(int(datas[x].split('-')[2]),int(datas[x].split('-')[1]),int(datas[x].split('-')[0]))
                inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
                fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
                # inicio = date(2019,1,1)
                # fim = date(2019,6,1)
                if inicio <= data <= fim:
                    continue
                else:
                    datas.pop(x)
        
            for data in datas:
                tabela.update({data:[]})
        
            rs = 0
            mw = 0
            for data in datas:
                for x in range(len(tabela['TIPO DE CONTRATO'])):
                    idResumido = str(tabela['TIPO DE CONTRATO'][x] + ';' + tabela['TIPO DE LEILÃO'][x] + ';' + tabela['PRODUTO'][x] + ';' + tabela['DATA'][x] + ';' + data)
                    if uni_tot == 'Unitário':
                        mw = resumidos[idResumido]['soma mwh']
                        rs = resumidos[idResumido]['soma custo total']
                    elif uni_tot == 'Total':
                        rs = resumidos[idResumido]['soma custo total']
                    else:
                        break
                    if uni_tot == 'Unitário':
                        if mw != 0:
                            rs = rs / mw
                            mw = 0
                        else:
                            rs = 0
                    #tabela[data].append(locale.currency(round(rs,5)))
                    tabela[data].append(round(rs,5))
                    rs = 0
                    
            for data in datas:
                dataptBr = funcoes.transforma_data(data)
                dataptBr = funcoes.data_ptBr(dataptBr).upper()
                tabela[dataptBr] = tabela[data]
                del tabela[data]

        else:
            
            anos = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))
            for ano in anos:
                tabela.update({ano:[]})
            
            rs = 0    
            mw = 0
            for x in range(len(tabela['TIPO DE CONTRATO'])):
                for data in datas:
                    idResumido = str(tabela['TIPO DE CONTRATO'][x] + ';' + tabela['TIPO DE LEILÃO'][x] + ';' + tabela['PRODUTO'][x] + ';' + tabela['DATA'][x] + ';' + data)
                    if uni_tot == 'Unitário':
                        mw += resumidos[idResumido]['soma mwh']
                        rs += resumidos[idResumido]['soma custo total']
                    elif uni_tot == 'Total':
                        rs += resumidos[idResumido]['soma custo total']
                    else:
                        break
                    if data[:5] == '01-12':
                        if uni_tot == 'Unitário':
                            if mw != 0:
                                rs = rs / mw
                                mw = 0
                            else:
                                rs = 0
                        #tabela[data[-4:]].append(locale.currency(round(rs,5)))
                        tabela[data[-4:]].append(round(rs,5))
                        rs = 0
            
        return tabela
    
        