import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from random import randint
from .app import app
from .uteis import funcoes
from datetime import datetime,date
#import locale

#import contratos
#Usadas anteriormente, talvez sejam úteis ainda
#import plotly.express as px
#import pandas as pd

fig = go.Figure()
fig1 = go.Figure()
grafico_selecionado = 'sub'
template = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def gera_grafico_cnt(contrato,valorContrato,filtros,inicioData,fimData,mes_ano,mwh_mwm,sub_tot):
    
    fig = go.Figure()
    
    datas = []
    valores = {
        0: {
            "Submercado":"Nordeste",
            "cor": "#118dff",
            "valores": []}, 
        1: {
            "Submercado":"Norte",
            "cor": "#12239e",
            "valores": []}, 
        2: {
            "Submercado":"Sudeste",
            "cor": "#e66c37",
            "valores": []}, 
        3: {
            "Submercado":"Sul",
            "cor": "#6b007b",
            "valores": []}, 
        4: {
            "Submercado":"Nordeste-Projetado",
            "cor": "#41a4ff",
            "valores": []},
        5: {
            "Submercado":"Norte-Projetado",
            "cor": "#414fb1",
            "valores": []},
        6: {
            "Submercado":"Sudeste-Projetado",
            "cor": "#eb895f",
            "valores": []},
        7: {
            "Submercado":"Sul-Projetado",
            "cor": "#893395",
            "valores": []},
        8: {
            "Submercado":"Total",
            "cor": "#118dff",
            "valores": []},
        }
    
    for chave in valorContrato.keys():
        datas.append(chave[-10:])
            
    datas = funcoes.remove_repetidos(datas)
    datas.sort(key=lambda l: l.split('-')[2] + '-' + l.split('-')[1] + '-' + l.split('-')[0])
    
    if mes_ano == 'Anual':      
        v=''  
    else: 
        for x in range(len(datas) -1,-1,-1):
            data = date(int(datas[x].split('-')[2]),int(datas[x].split('-')[1]),int(datas[x].split('-')[0]))
            inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
            fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
            if inicio <= data <= fim:
                continue
            else:
                datas.pop(x) 
    
    valoresContrato = {}
    for chave in valorContrato.keys():
        valoresContrato.update({chave: valorContrato[chave]})
        
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
    
    totalValor = 0
    totalNordeste = 0
    totalNorte = 0
    totalSudeste = 0
    totalSul = 0
    keys = valoresContrato.keys()
    
    for x in range(len(datas)): 
        if mes_ano == 'Mensal':
            totalValor = 0
            totalNordeste = 0
            totalNorte = 0
            totalSudeste = 0
            totalSul = 0
        
        for cntKey in contratos.keys():
            
            idValorContrato = str(cntKey + '-' + datas[x])
            if mes_ano == 'Mensal':
                if idValorContrato in keys:
                    if mwh_mwm == 'MWh':
                        totalValor += valoresContrato[idValorContrato]['mwh']
                    elif mwh_mwm == 'MWm':
                        totalValor += valoresContrato[idValorContrato]['mwm'] 
                    else:
                        break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'NORDESTE':
                        if mwh_mwm == 'MWh':
                            totalNordeste += valoresContrato[idValorContrato]['mwh']
                        elif mwh_mwm == 'MWm':
                            totalNordeste += valoresContrato[idValorContrato]['mwm'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'NORTE':
                        if mwh_mwm == 'MWh':
                            totalNorte += valoresContrato[idValorContrato]['mwh']
                        elif mwh_mwm == 'MWm':
                            totalNorte += valoresContrato[idValorContrato]['mwm'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'SUDESTE':
                        if mwh_mwm == 'MWh':
                            totalSudeste += valoresContrato[idValorContrato]['mwh']
                        elif mwh_mwm == 'MWm':
                            totalSudeste += valoresContrato[idValorContrato]['mwm'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'SUL':
                        if mwh_mwm == 'MWh':
                            totalSul += valoresContrato[idValorContrato]['mwh']
                        elif mwh_mwm == 'MWm':
                            totalSul += valoresContrato[idValorContrato]['mwm'] 
                        else:
                            break
                else:
                    continue
            else:
                AnoDaVez = datas[x].split('-')[2]
                if idValorContrato in keys:
                    if mwh_mwm == 'MWh' and idValorContrato[-4:] == AnoDaVez:
                        totalValor += valoresContrato[idValorContrato]['mwh']
                    elif mwh_mwm == 'MWm' and idValorContrato[-4:] == AnoDaVez:
                        totalValor += valoresContrato[idValorContrato]['mwm'] 
                    else:
                        break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'NORDESTE':
                        if mwh_mwm == 'MWh' and idValorContrato[-4:] == AnoDaVez:
                            totalNordeste += valoresContrato[idValorContrato]['mwh']
                        elif mwh_mwm == 'MWm' and idValorContrato[-4:] == AnoDaVez:
                            totalNordeste += valoresContrato[idValorContrato]['mwm'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'NORTE':
                        if mwh_mwm == 'MWh' and idValorContrato[-4:] == AnoDaVez:
                            totalNorte += valoresContrato[idValorContrato]['mwh']
                        elif mwh_mwm == 'MWm' and idValorContrato[-4:] == AnoDaVez:
                            totalNorte += valoresContrato[idValorContrato]['mwm'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'SUDESTE':
                        if mwh_mwm == 'MWh' and idValorContrato[-4:] == AnoDaVez:
                            totalSudeste += valoresContrato[idValorContrato]['mwh']
                        elif mwh_mwm == 'MWm' and idValorContrato[-4:] == AnoDaVez:
                            totalSudeste += valoresContrato[idValorContrato]['mwm'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'SUL':
                        if mwh_mwm == 'MWh' and idValorContrato[-4:] == AnoDaVez:
                            totalSul += valoresContrato[idValorContrato]['mwh']
                        elif mwh_mwm == 'MWm' and idValorContrato[-4:] == AnoDaVez:
                            totalSul += valoresContrato[idValorContrato]['mwm'] 
                        else:
                            break
                else:
                    continue
        
        if mes_ano == 'Mensal':               
            valores[0]["valores"].append(totalNordeste)
            valores[1]["valores"].append(totalNorte)
            valores[2]["valores"].append(totalSudeste)
            valores[3]["valores"].append(totalSul)
            valores[8]["valores"].append(totalValor)
        else:
            if datas[x][:5] == '01-12':
                if mwh_mwm == 'MWm':
                    horas = funcoes.numero_horas_ano(datas[x][-4:])
                    totalNordeste = totalNordeste / horas
                    totalNorte = totalNorte / horas
                    totalSudeste = totalSudeste / horas
                    totalSul = totalSul / horas
                    totalValor = totalValor / horas
                valores[0]["valores"].append(totalNordeste)
                valores[1]["valores"].append(totalNorte)
                valores[2]["valores"].append(totalSudeste)
                valores[3]["valores"].append(totalSul)
                valores[8]["valores"].append(totalValor)
                totalValor = 0
                totalNordeste = 0
                totalNorte = 0
                totalSudeste = 0
                totalSul = 0
               
            
    
        
    if mes_ano == 'Mensal':  
        datas = list(map(funcoes.transforma_data,datas))
        datas = list(map(funcoes.data_ptBr,datas))
    else:
        datas = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))    
    if sub_tot == 'sub':
        
        for i in range(4):
            fig.add_trace(go.Bar(x=datas,
                        y=valores[i]["valores"],
                        name=valores[i]["Submercado"],
                        marker_color=valores[i]["cor"]
                        ))
    else:
        fig.add_trace(go.Bar(x=datas,
                        y=valores[8]["valores"],
                        name=valores[8]["Submercado"],
                        marker_color=valores[8]["cor"]
                        ))
    
    if mwh_mwm == 'MWm':
        fig.update_layout(yaxis=dict(title='MWm'))
    else:
        fig.update_layout(yaxis=dict(title='MWh'))
        
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        template=template[1],
        xaxis=dict(
            title='Data',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.12,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)',
            orientation="h",
            tracegroupgap=100
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )

    return fig
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


def gera_grafico_balanco(balanco,inicioData,fimData,mes_ano):
    
    fig = go.Figure()
    datas = []
    valores = {
        0: {
            "Legenda":"Total Contratos",
            "cor": "#118dff",
            "valores": []}, 
        1: {
            "Legenda":"Carga",
            "cor": "#12239e",
            "valores": []}, 
        2: {
            "Legenda":"Sobra (MWh)",
            "cor": "#e66c37",
            "valores": []}, 
        }
    
    for blc in balanco:
        datas.append(blc['data'])      
    
    if mes_ano == 'Anual':      
        datas = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))  
    else: 
        for x in range(len(datas) -1,-1,-1):
            data = date(int(datas[x].split('-')[2]),int(datas[x].split('-')[1]),int(datas[x].split('-')[0]))
            inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
            fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
            if inicio <= data <= fim:
                continue
            else:
                datas.pop(x)
    
    balanço = []
    for blc in balanco:
        balanço.append(blc)
        
    for x in range(len(datas)):
        totalContratos = 0
        carga = 0
        sobra = 0
        for blc in balanço:
            if mes_ano == 'Anual':
                if blc['data'].split('-')[2] == datas[x]:
                    totalContratos = totalContratos + blc['total_mwh']
                    carga = carga + blc['carga']
            else:
                if blc['data'] == datas[x]:
                    totalContratos = blc['total_mwh']
                    carga = blc['carga']
        sobra = totalContratos - carga
        valores[0]["valores"].append(totalContratos)
        valores[1]["valores"].append(carga)
        valores[2]["valores"].append(sobra)
    
    if mes_ano == 'Mensal':  
        datas = list(map(funcoes.transforma_data,datas))
        datas = list(map(funcoes.data_ptBr,datas))
       

    for i in range(3):
        fig.add_trace(go.Bar(x=datas,
                    y=valores[i]["valores"],
                    name=valores[i]["Legenda"],
                    marker_color=valores[i]["cor"]
                    ))

    
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        template=template[1],
        xaxis=dict(
            title='Data',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            title='MWh',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.12,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)',
            orientation="h",
            tracegroupgap=100
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    
    return fig
    
    
    
    
    
    
    
    
    
    
    
    

    
def gera_grafico_cts(contrato,valorContrato,filtros,inicioData,fimData,mes_ano,uni_tot,sub_tot):
    
    fig = go.Figure()
    datas = []
    valores = {
        0: {
            "Submercado":"Nordeste",
            "cor": "#118dff",
            "valores": []}, 
        1: {
            "Submercado":"Norte",
            "cor": "#12239e",
            "valores": []}, 
        2: {
            "Submercado":"Sudeste",
            "cor": "#e66c37",
            "valores": []}, 
        3: {
            "Submercado":"Sul",
            "cor": "#6b007b",
            "valores": []}, 
        4: {
            "Submercado":"Nordeste-Projetado",
            "cor": "#41a4ff",
            "valores": []},
        5: {
            "Submercado":"Norte-Projetado",
            "cor": "#414fb1",
            "valores": []},
        6: {
            "Submercado":"Sudeste-Projetado",
            "cor": "#eb895f",
            "valores": []},
        7: {
            "Submercado":"Sul-Projetado",
            "cor": "#893395",
            "valores": []},
        8: {
            "Submercado":"Total",
            "cor": "#118dff",
            "valores": []},
        }
    
    for chave in valorContrato.keys():
        datas.append(chave[-10:])
            
    datas = funcoes.remove_repetidos(datas)
    datas.sort(key=lambda l: l.split('-')[2] + '-' + l.split('-')[1] + '-' + l.split('-')[0])
    
    if mes_ano == 'Anual':      
        v=''  
    else: 
        for x in range(len(datas) -1,-1,-1):
            data = date(int(datas[x].split('-')[2]),int(datas[x].split('-')[1]),int(datas[x].split('-')[0]))
            inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
            fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
            if inicio <= data <= fim:
                continue
            else:
                datas.pop(x) 
    
    valoresContrato = {}
    for chave in valorContrato.keys():
        valoresContrato.update({chave: valorContrato[chave]})
        
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
    
    totalValorReais = 0
    totalNordesteReais  = 0
    totalNorteReais  = 0
    totalSudesteReais  = 0
    totalSulReais  = 0

    totalValorMWh = 0
    totalNordesteMWh = 0
    totalNorteMWh = 0
    totalSudesteMWh = 0
    totalSulMWh = 0
    keys = valoresContrato.keys()
    
    for x in range(len(datas)): 
        if mes_ano == 'Mensal':
            totalValorReais = 0
            totalNordesteReais  = 0
            totalNorteReais  = 0
            totalSudesteReais  = 0
            totalSulReais  = 0

            totalValorMWh = 0
            totalNordesteMWh = 0
            totalNorteMWh = 0
            totalSudesteMWh = 0
            totalSulMWh = 0
        
        for cntKey in contratos.keys():
            
            idValorContrato = str(cntKey + '-' + datas[x])
            if mes_ano == 'Mensal':
                if idValorContrato in keys:
                    if uni_tot == 'Unitário':
                        totalValorMWh += valoresContrato[idValorContrato]['mwh']
                        totalValorReais += valoresContrato[idValorContrato]['custo_total']
                    elif uni_tot == 'Total':
                        totalValorReais += valoresContrato[idValorContrato]['custo_total'] 
                    else:
                        break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'NORDESTE':
                        if uni_tot == 'Unitário':
                            totalNordesteMWh += valoresContrato[idValorContrato]['mwh']
                            totalNordesteReais += valoresContrato[idValorContrato]['custo_total'] 
                        elif uni_tot == 'Total':
                            totalNordesteReais += valoresContrato[idValorContrato]['custo_total'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'NORTE':
                        if uni_tot == 'Unitário':
                            totalNorteMWh += valoresContrato[idValorContrato]['mwh']
                            totalNorteReais += valoresContrato[idValorContrato]['custo_total'] 
                        elif uni_tot == 'Total':
                            totalNorteReais += valoresContrato[idValorContrato]['custo_total'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'SUDESTE':
                        if uni_tot == 'Unitário':
                            totalSudesteMWh += valoresContrato[idValorContrato]['mwh']
                            totalSudesteReais += valoresContrato[idValorContrato]['custo_total'] 
                        elif uni_tot == 'Total':
                            totalSudesteReais += valoresContrato[idValorContrato]['custo_total'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'SUL':
                        if uni_tot == 'Unitário':
                            totalSulMWh += valoresContrato[idValorContrato]['mwh']
                            totalSulReais += valoresContrato[idValorContrato]['custo_total'] 
                        elif uni_tot == 'Total':
                            totalSulReais += valoresContrato[idValorContrato]['custo_total'] 
                        else:
                            break
                else:
                    continue
            else:
                AnoDaVez = datas[x].split('-')[2]
                if idValorContrato in keys:
                
                    if uni_tot == 'Unitário' and idValorContrato[-4:] == AnoDaVez:
                        totalValorMWh += valoresContrato[idValorContrato]['mwh']
                        totalValorReais += valoresContrato[idValorContrato]['custo_total']
                    elif uni_tot == 'Total' and idValorContrato[-4:] == AnoDaVez:
                        totalValorReais += valoresContrato[idValorContrato]['custo_total']
                    else:
                        break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'NORDESTE':
                        if uni_tot == 'Unitário' and idValorContrato[-4:] == AnoDaVez:
                            totalNordesteMWh += valoresContrato[idValorContrato]['mwh']
                            totalNordesteReais += valoresContrato[idValorContrato]['custo_total'] 
                        elif uni_tot == 'Total' and idValorContrato[-4:] == AnoDaVez:
                            totalNordesteReais += valoresContrato[idValorContrato]['custo_total'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'NORTE':
                        if uni_tot == 'Unitário' and idValorContrato[-4:] == AnoDaVez:
                            totalNorteMWh += valoresContrato[idValorContrato]['mwh']
                            totalNorteReais += valoresContrato[idValorContrato]['custo_total'] 
                        elif uni_tot == 'Total' and idValorContrato[-4:] == AnoDaVez:
                            totalNorteReais += valoresContrato[idValorContrato]['custo_total'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'SUDESTE':
                        if uni_tot == 'Unitário' and idValorContrato[-4:] == AnoDaVez:
                            totalSudesteMWh += valoresContrato[idValorContrato]['mwh']
                            totalSudesteReais += valoresContrato[idValorContrato]['custo_total'] 
                        elif uni_tot == 'Total' and idValorContrato[-4:] == AnoDaVez:
                            totalSudesteReais += valoresContrato[idValorContrato]['custo_total'] 
                        else:
                            break
                    
                    if contratos[cntKey]['SUBMERCADO'] == 'SUL':
                        if uni_tot == 'Unitário' and idValorContrato[-4:] == AnoDaVez:
                            totalSulMWh += valoresContrato[idValorContrato]['mwh']
                            totalSulReais += valoresContrato[idValorContrato]['custo_total'] 
                        elif uni_tot == 'Total' and idValorContrato[-4:] == AnoDaVez:
                            totalSulReais += valoresContrato[idValorContrato]['custo_total'] 
                        else:
                            break
                else:
                    continue
        
        if mes_ano == 'Mensal':
            if uni_tot == 'Unitário':
                if totalValorMWh != 0:
                    totalValorReais /= totalValorMWh
                if totalNordesteMWh != 0:
                    totalNordesteReais /= totalNordesteMWh
                if totalNorteMWh != 0:
                    totalNorteReais /= totalNorteMWh
                if totalSudesteMWh != 0:
                    totalSudesteReais /= totalSudesteMWh
                if totalSulMWh != 0:
                    totalSulReais /= totalSulMWh                          
            valores[0]["valores"].append(totalNordesteReais)
            valores[1]["valores"].append(totalNorteReais)
            valores[2]["valores"].append(totalSudesteReais)
            valores[3]["valores"].append(totalSulReais)
            valores[8]["valores"].append(totalValorReais)
        else:
            if datas[x][:5] == '01-12':
                if uni_tot == 'Unitário':
                    if totalValorMWh != 0:
                        totalValorReais /= totalValorMWh
                    if totalNordesteMWh != 0:
                        totalNordesteReais /= totalNordesteMWh
                    if totalNorteMWh != 0:
                        totalNorteReais /= totalNorteMWh
                    if totalSudesteMWh != 0:
                        totalSudesteReais /= totalSudesteMWh
                    if totalSulMWh != 0:
                        totalSulReais /= totalSulMWh
                valores[0]["valores"].append(totalNordesteReais)
                valores[1]["valores"].append(totalNorteReais)
                valores[2]["valores"].append(totalSudesteReais)
                valores[3]["valores"].append(totalSulReais)
                valores[8]["valores"].append(totalValorReais)
                totalValorReais = 0
                totalNordesteReais  = 0
                totalNorteReais  = 0
                totalSudesteReais  = 0
                totalSulReais  = 0

                totalValorMWh = 0
                totalNordesteMWh = 0
                totalNorteMWh = 0
                totalSudesteMWh = 0
                totalSulMWh = 0
               
            
    
        
    if mes_ano == 'Mensal':  
        datas = list(map(funcoes.transforma_data,datas))
        datas = list(map(funcoes.data_ptBr,datas))
    else:
        datas = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))    
    if sub_tot == 'sub':
        for i in range(4):
            fig.add_trace(go.Bar(x=datas,
                        y=valores[i]["valores"],
                        name=valores[i]["Submercado"],
                        marker_color=valores[i]["cor"]
                        ))
    else:
        fig.add_trace(go.Bar(x=datas,
                        y=valores[8]["valores"],
                        name=valores[8]["Submercado"],
                        marker_color=valores[8]["cor"]
                        ))

    if uni_tot == 'Unitário':
        fig.update_layout(yaxis=dict(title='R$/MWh'))
    else:
        fig.update_layout(yaxis=dict(title='R$'))

    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        template=template[1],
        xaxis=dict(
            title='Data',
            titlefont_size=16,
            tickfont_size=14,
        ),
        yaxis=dict(
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.12,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)',
            orientation="h",
            tracegroupgap=100
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )

    return fig
    
    
    
    
    
        
    
    
    
    
    
    



# @app.callback(
#     Output('grafico', 'figure'),
#     Input('selecao-grafico', 'value'))
# def display_value(value):
#     #global grafico_selecionado
#     if value == 'sub':
#        # grafico_selecionado = 'sub'
#         fig.update_layout(transition_duration=500)
#         return fig
#     else:
#         #grafico_selecionado = 'tot'
#         fig1.update_layout(transition_duration=500)
#         return fig1
    
    
def retorna_grafico(fig):
    tabelaDoGrafico = {' ':[]}
    fig_selected = fig
    for data in fig_selected['data'][0]['x']:
        tabelaDoGrafico.update({data: []})
    for trace in fig_selected['data']:
        tabelaDoGrafico[' '].append(trace['name'])
        for i in range(len(trace['x'])):
            tabelaDoGrafico[trace['x'][i]].append(trace['y'][i])
    return tabelaDoGrafico
    
    