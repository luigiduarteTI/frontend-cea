import dash
import pandas as pd
import dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from datetime import date,timedelta,datetime
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
from dash.exceptions import PreventUpdate
from . import grafico as gf
from . import tabela as tb
from .modal import modal
from . import ipca as ip
from .app import app
from . import contratos 
from . import balanco
from . import custos
from .dados import contratoB,valorContratoB,balancoA,resumido,custosContratosA,ipca
from .uteis import funcoes
from . import filtros
import requests




flts = {
    'TIPO DE CONTRATO': False,
    'SUBMERCADO': False,
    'TIPO DE LEILÃO': False,
    'STATUS': False,
    'PRODUTO': False,
    'VENDEDOR': False,
    'INÍCIO DE SUPRIMENTO': False,
    'FIM DE SUPRIMENTO': False
}
caminho = '/'
contrato = contratoB
valorContrato = {}
custosContratos = {}
balanço = []
ipca = []

tabela = {}#tb.constroi_tabela_cnt_cts(contrato,valorContrato,flts,'2019-1-1','2023-12-1','Mensal','Detalhado','MWh')
df = pd.DataFrame() #tabela
#grafico_atual = gf.gera_grafico_cnt_cts(contrato,valorContrato,flts,'2019-1-1','2023-12-1','Mensal','MWh',True)
df2 = pd.DataFrame() #gf.retorna_grafico()




# @app.callback(Output('output-url', 'children'),
#               Input('url1', 'pathname'))
# def valor_url(pathname):
#     global caminho
#     caminho = pathname
#     return ''

@app.callback(
    Output('container-tabela', 'children'),
    Output('container-grafico', 'children'),
    Output('date-picker', 'style'),
    Output('range-slider', 'className'),
    Output('mes-ano','children'),
    Output('det-res','children'),
    Output('unidade','children'),
    Output('titulo-pagina','children'),
    Output('titulo-grafico','children'),
    [
        Input("mes", "n_clicks"),
        Input("ano", "n_clicks"),
        Input("mes-ano", "n_clicks"),
        Input("det-res", "n_clicks"),
        Input("unidade", "n_clicks"),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('checklist-tipo-contrato-valores', 'value'),
        Input('checklist-submercado-valores', 'value'),
        Input('checklist-leilao-valores', 'value'),
        Input('checklist-status-valores', 'value'),
        Input('checklist-produto-valores', 'value'),
        Input('checklist-vendedor-valores', 'value'),
        Input('checklist-inicio-suprimento-valores', 'value'),
        Input('checklist-fim-suprimento-valores', 'value'),
        Input('selecao-grafico', 'value'),
        Input('url1', 'pathname')
     ]
)
def update_grafico_tabela(n_mes,n_ano,n_mes_ano, n_det_res, n_unidade, start_date, end_date,tipo_contrato_value,
                    submercado_value,leilao_value,status_value,produto_value,vendedor_value,inicio_suprimento_value,fim_suprimento_value,selecao_value,url):
    
    
    
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if n_mes_ano == None:
        displayDatePicker = {'display': 'block'}
        displayRangeSlider = 'd-block'
        mes_ano_child = 'Anual'
        mes_ano_atual = 'Mensal'
    else:
        if n_mes_ano % 2 == 0:
            displayDatePicker = {'display': 'block'}
            displayRangeSlider = 'd-block'
            mes_ano_child = 'Anual'
            mes_ano_atual = 'Mensal'
        else: 
            displayDatePicker = {'display': 'none'}
            displayRangeSlider = 'd-none'
            mes_ano_child = 'Mensal'
            mes_ano_atual = 'Anual'
            
    if n_det_res == None:
        det_res_child = 'Resumido'
        det_res_atual = 'Detalhado'
    else:
        if n_det_res % 2 == 0:
            det_res_child = 'Resumido'
            det_res_atual = 'Detalhado'
        else: 
            det_res_child = 'Detalhado'
            det_res_atual = 'Resumido'
    if url == '/' or url == '/contratos':
        if n_unidade == None:
            mwh_mwm_child = 'MWm'
            mwh_mwm_atual = 'MWh'
        else:
            if n_unidade % 2 == 0:
                mwh_mwm_child = 'MWm'
                mwh_mwm_atual = 'MWh'
            else: 
                mwh_mwm_child = 'MWh'
                mwh_mwm_atual = 'MWm'
    else:
        if n_unidade == None:
            uni_tot_child = 'Total'
            uni_tot_atual = 'Unitário'
        else:
            
            if n_unidade % 2 == 0:
                uni_tot_child = 'Total'
                uni_tot_atual = 'Unitário'
            else: 
                uni_tot_child = 'Unitário'
                uni_tot_atual = 'Total'
    
    
    # flts = {
    #     'TIPO DE CONTRATO':False,
    #     'SUBMERCADO': False,
    #     'TIPO DE LEILÃO':False,
    #     'STATUS':False,
    #     'PRODUTO': False,
    #     'VENDEDOR': False,
    #     'INÍCIO DE SUPRIMENTO': False,
    #     'FIM DE SUPRIMENTO': False
    # }
    
    
    flts = {
        'TIPO DE CONTRATO':[],
        'SUBMERCADO': [],
        'TIPO DE LEILÃO':[],
        'STATUS':[],
        'PRODUTO': [],
        'VENDEDOR': [],
        'INÍCIO DE SUPRIMENTO': [],
        'FIM DE SUPRIMENTO': []
    }
    b1 = True
    b2 = True 
    b3 = True
    b4 = True
    b5 = True 
    b6 = True 
    b7 = True
    b8 = True                  
    for chave in flts.keys():
        for i in filtros.reuni_filtros(contrato)[chave]:
            if chave == 'TIPO DE CONTRATO':
                if b1:
                    b1 = i in tipo_contrato_value
            if chave == 'SUBMERCADO':
                if b2:
                    b2 = i in submercado_value
            if chave == 'TIPO DE LEILÃO':
                if b3:
                    b3 = i in leilao_value
            if chave == 'STATUS':
                if b4:
                    b4 = i in status_value
            if chave == 'PRODUTO':
                if b5:
                    b5 = i in produto_value
            if chave == 'VENDEDOR':
                if b6:
                    b6 = i in vendedor_value
            if chave == 'INÍCIO DE SUPRIMENTO':
                if b7:
                    b7 = i in inicio_suprimento_value
            if chave == 'FIM DE SUPRIMENTO':
                if b8:
                    b8 = i in fim_suprimento_value       
        
    if tipo_contrato_value == [] or b1 :
        flts['TIPO DE CONTRATO'] = False
    else:
        for i in filtros.reuni_filtros(contrato)['TIPO DE CONTRATO']:
            condicao = i in tipo_contrato_value
            if not condicao:
                flts['TIPO DE CONTRATO'].append(i)
                
    if submercado_value == [] or b2:
        flts['SUBMERCADO'] = False
    else:
        for i in filtros.reuni_filtros(contrato)['SUBMERCADO']:
            condicao = i in submercado_value
            if not condicao:
                flts['SUBMERCADO'].append(i)
    
    if leilao_value == [] or b3:
        flts['TIPO DE LEILÃO'] = False
    else:
        for i in filtros.reuni_filtros(contrato)['TIPO DE LEILÃO']:
            condicao = i in leilao_value
            if not condicao:
                flts['TIPO DE LEILÃO'].append(i)
    
    if status_value == [] or b4:
        flts['STATUS'] = False
    else:
        for i in filtros.reuni_filtros(contrato)['STATUS']:
            condicao = i in status_value
            if not condicao:
                flts['STATUS'].append(i)
    
    if produto_value == [] or b5:
        flts['PRODUTO'] = False
    else:
        for i in filtros.reuni_filtros(contrato)['PRODUTO']:
            condicao = i in produto_value
            if not condicao:
                flts['PRODUTO'].append(i)
    
    if vendedor_value == [] or b6:
        flts['VENDEDOR'] = False
    else:
        for i in filtros.reuni_filtros(contrato)['VENDEDOR']:
            condicao = i in vendedor_value
            if not condicao:
                flts['VENDEDOR'].append(i)
    
    if inicio_suprimento_value == [] or b7:
        flts['INÍCIO DE SUPRIMENTO'] = False
    else:
        for i in filtros.reuni_filtros(contrato)['INÍCIO DE SUPRIMENTO']:
            condicao = i in inicio_suprimento_value
            if not condicao:
                flts['INÍCIO DE SUPRIMENTO'].append(i)
    
    if fim_suprimento_value == [] or b8:
        flts['FIM DE SUPRIMENTO'] = False
    else:
        for i in filtros.reuni_filtros(contrato)['FIM DE SUPRIMENTO']:
            condicao = i in fim_suprimento_value
            if not condicao:
                flts['FIM DE SUPRIMENTO'].append(i)    
            
        
    if url == '/' or url == '/contratos':
        
        titulo_pagina = 'Contratos > ' + mes_ano_atual + ' > ' + det_res_atual + ' > ' + mwh_mwm_atual
        if selecao_value == 'sub':
            titulo_grafico = mwh_mwm_atual + ' por Data e Subsistema'
        else:
            titulo_grafico = mwh_mwm_atual + ' por Data'
        if det_res_atual == 'Detalhado':
            tabela = tb.constroi_tabela_cnt(contrato,valorContrato,flts,start_date,end_date,mes_ano_atual,det_res_atual,mwh_mwm_atual)
        else:
            tabela = tb.constroi_tabela_cnt(resumido,valorContrato,flts,start_date,end_date,mes_ano_atual,det_res_atual,mwh_mwm_atual)
        if n_mes_ano != None or  n_unidade != None:
            grafico_atual = gf.gera_grafico_cnt(contrato,valorContrato,flts,start_date,end_date,mes_ano_atual,mwh_mwm_atual,selecao_value)
        else:
            grafico_atual = gf.gera_grafico_cnt(contrato,valorContrato,flts,start_date,end_date,mes_ano_atual,mwh_mwm_atual,selecao_value)     
            
    elif url == '/balanco':
        mes_ano_atual = 'Anual' if trigger_id == 'ano' else 'Mensal'
        titulo_pagina = 'Balanço > ' + mes_ano_atual
        titulo_grafico = 'Total de Contratos, Carga e Sobra por Data'
        tabela = tb.constroi_tabela_balanco(balanço, start_date, end_date, mes_ano_atual)
        if n_mes_ano != None or  n_unidade != None:
            grafico_atual = gf.gera_grafico_balanco(balanço,start_date,end_date,mes_ano_atual)
        else:
            grafico_atual = gf.gera_grafico_balanco(balanço,start_date,end_date,mes_ano_atual)
            
    elif url == '/custos':
        
        titulo_pagina = 'Custos > ' + mes_ano_atual + ' > ' + det_res_atual + ' > ' + uni_tot_atual
        if selecao_value == 'sub':
            titulo_grafico = 'Custo ' + uni_tot_atual + ' por Data e Subsistema'
        else:
            titulo_grafico = 'Custo ' + uni_tot_atual + ' por Data'
        if det_res_atual == 'Detalhado':
            tabela = tb.constroi_tabela_cts(contrato,custosContratos,flts,start_date,end_date,mes_ano_atual,det_res_atual,uni_tot_atual)
        else:
            tabela = tb.constroi_tabela_cts(resumido,custosContratos,flts,start_date,end_date,mes_ano_atual,det_res_atual,uni_tot_atual)
        if n_mes_ano != None or  n_unidade != None:
            grafico_atual = gf.gera_grafico_cts(contrato,custosContratos,flts,start_date,end_date,mes_ano_atual,uni_tot_atual,selecao_value)
        else:
            grafico_atual = gf.gera_grafico_cts(contrato,custosContratos,flts,start_date,end_date,mes_ano_atual,uni_tot_atual,selecao_value)
         
    df= pd.DataFrame(tabela)
    component_tabela = dash_table.DataTable(id='tabela',columns=[{"name": i, "id": i} for i in df.columns],data=df.to_dict('records'),page_size=25,style_header=tb.style_header,style_cell=tb.style_cell,style_table=tb.style_table,style_data_conditional=tb.style_data_conditional)
    
    graficoLayout = dcc.Graph(id='grafico', figure=grafico_atual)
    
    if url == '/' or url == '/contratos':
        return component_tabela,graficoLayout,displayDatePicker,displayRangeSlider,mes_ano_child,det_res_child,mwh_mwm_child,titulo_pagina,titulo_grafico
    else:
        return component_tabela,graficoLayout,displayDatePicker,displayRangeSlider,mes_ano_child,det_res_child,uni_tot_child,titulo_pagina,titulo_grafico



@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("ipca", "is_open"),
    [Input("open2", "n_clicks"), Input("close2", "n_clicks")],
    [State("ipca", "is_open")],
)
def toggle_ipca(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(Output("download-grafico", "data"), [Input("btn-exp-grafico", "n_clicks"),Input('url1', 'pathname'),Input('grafico', 'figure')])
def func(n_nlicks,url,fig):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id != 'btn-exp-grafico':
        raise PreventUpdate
    else:
        nome_arquivo = 'arquivo.xlsx'
        if url == '/' or url == '/contratos':
            nome_arquivo = 'grafico_contratos.xlsx'
        if url == '/balanco':
            nome_arquivo = 'grafico_balanço.xlsx'
        if url == '/custos':
            nome_arquivo = 'grafico_custos.xlsx'
            
        if n_nlicks != None:
            df2 = pd.DataFrame(gf.retorna_grafico(fig))
            return send_data_frame(df2.to_excel, nome_arquivo, index=False)

@app.callback(Output("download-tabela", "data"), [Input("btn-exp-tabela", "n_clicks"),Input('url1', 'pathname'),Input('tabela', 'data')])
def func(n_nlicks,url,dados):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id != 'btn-exp-tabela':
        raise PreventUpdate
    else:
        nome_arquivo = 'arquivo.xlsx'
        if url == '/' or url == '/contratos':
            nome_arquivo = 'tabela_contratos.xlsx'
        if url == '/balanco':
            nome_arquivo = 'tabela_balanço.xlsx'
        if url == '/custos':
            nome_arquivo = 'tabela_custos.xlsx'
        
        df = pd.DataFrame(dados) 
        if n_nlicks != None:
            return send_data_frame(df.to_excel, nome_arquivo, index=False)

@app.callback(
    Output('date-picker', 'start_date'),
    Output('date-picker', 'end_date'),
    Output('range-slider', 'value'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('range-slider', 'value'),
     Input('url1', 'pathname')]
)
def update_slider(start_date,end_date,slider_value,url):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if url == '/' or url == '/contratos' or url == '/balanco':
        if trigger_id == 'date-picker':
            inicio = funcoes.diff_month(date.fromisoformat(start_date),date(2019,1,1))
            fim = funcoes.diff_month(date.fromisoformat(end_date),date(2019,1,1))
            return dash.no_update,dash.no_update,[inicio,fim]
        elif trigger_id == 'range-slider':
            dataInicial = funcoes.add_months(date(2019,1,1),slider_value[0])
            dataFinal = funcoes.add_months(date(2019,1,1),slider_value[1])
            return dataInicial,dataFinal,dash.no_update
        else:
            
            return date(2019,1,1),date(2020,12,1),[0,24]
    else:
        if trigger_id == 'date-picker':
            inicio = funcoes.diff_month(date.fromisoformat(start_date),date(2020,1,1))
            fim = funcoes.diff_month(date.fromisoformat(end_date),date(2020,1,1))
            return dash.no_update,dash.no_update,[inicio,fim]
        elif trigger_id == 'range-slider':
            dataInicial = funcoes.add_months(date(2020,1,1),slider_value[0])
            dataFinal = funcoes.add_months(date(2020,1,1),slider_value[1])
            return dataInicial,dataFinal,dash.no_update
        else:
            return date(2020,1,1),date(2021,12,1),[0,24]
        


@app.callback(
    Output('date-picker-ipca', 'start_date'),
    Output('date-picker-ipca', 'end_date'),
    Output('range-slider-ipca', 'value'),
    [Input('date-picker-ipca', 'start_date'),
     Input('date-picker-ipca', 'end_date'),
     Input('range-slider-ipca', 'value')]
)
def update_slider_ipca(start_date,end_date,slider_value):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'date-picker-ipca':
        inicio = funcoes.diff_month(date.fromisoformat(start_date),date(2019,1,1))
        fim = funcoes.diff_month(date.fromisoformat(end_date),date(2019,1,1))
        return dash.no_update,dash.no_update,[inicio,fim]
    elif trigger_id == 'range-slider-ipca':
        dataInicial = funcoes.add_months(date(2019,1,1),slider_value[0])
        dataFinal = funcoes.add_months(date(2019,1,1),slider_value[1])
        return dataInicial,dataFinal,dash.no_update
    else:
        return date(2019,1,1),date(2040,12,1),[0,263]
    

@app.callback(
    Output('container-tabela-ipca', 'children'),
    Output('grafico-ipca', 'figure'),
    Output('date-picker-ipca', 'style'),
    Output('range-slider-ipca', 'className'),
    Output('titulo-modal-ipca','children'),
    Output('variacao-1','children'),
    Output('texto-variacao-1','children'),
    Output('variacao-2','children'),
    Output('texto-variacao-2','children'),
    Output('variacao-3','children'),
    Output('texto-variacao-3','children'),
    [
        Input("mes-ipca", "n_clicks"),
        Input("ano-ipca", "n_clicks"),
        Input('date-picker-ipca', 'start_date'),
        Input('date-picker-ipca', 'end_date'),
     ]
)
def update_grafico_tabela_ipca(n_mes,n_ano, start_date, end_date):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    variacao2021 = ''
    variacao2022 = ''
    variacao2023 = ''
    textoVariacao2021 = ''
    textoVariacao2022 = ''
    textoVariacao2023 = ''

    if trigger_id == 'ano-ipca':
        mes_ano_atual = 'Anual'
        displayDatePicker = {'display': 'none'}
        displayRangeSlider = 'd-none'
        n = 0
        var = 0
        ipcaAnos = []
        for i in ipca:
            if '01-12' in i['data']:
                if i['data'] == '01-12-2019':
                    n = i['ipca']
                    ipcaAnos.append('4,31%')
                else:
                    var = ((i['ipca'] / n) - 1) * 100
                    ipcaAnos.append(str(round(var,2)) + '%')
                    n = i['ipca']
        variacao2021 = ipcaAnos[2].replace('.',',')
        variacao2022 = ipcaAnos[3].replace('.',',')
        variacao2023 = ipcaAnos[4].replace('.',',')
        textoVariacao2021 = 'Projeção de Variação ' + mes_ano_atual + ' para 2021'
        textoVariacao2022 = 'Projeção de Variação ' + mes_ano_atual + ' para 2022'
        textoVariacao2023 = 'Projeção de Variação ' + mes_ano_atual + ' para 2023 e Posteriores'
    else:
        mes_ano_atual = 'Mensal'
        displayDatePicker = {'display': 'block'}
        displayRangeSlider = 'd-block slider-ipca'
        n = 0
        var = 0
        ipcaAnos = []
        for i in ipca:
            if '01-12' in i['data']:
                if i['data'] == '01-12-2019':
                    n = i['ipca']
                    ipcaAnos.append('4,31%')
                else:
                    var = ((i['ipca'] / n) - 1) * 100
                    ipcaAnos.append(str(round(var,2)) + '%')
                    n = i['ipca']
        variacao2021 = ipcaAnos[2].replace('.',',')
        variacao2022 = ipcaAnos[3].replace('.',',')
        variacao2023 = ipcaAnos[4].replace('.',',')
        textoVariacao2021 = 'Projeção de Variação Anual para 2021'
        textoVariacao2022 = 'Projeção de Variação Anual para 2022'
        textoVariacao2023 = 'Projeção de Variação Anual para 2023 e Posteriores'
        #for i in ipca:
        #    if i['data'] == '01-12-2021':
        #        variacao2021 = i['variacao ipca'].replace('.',',')
        #    if  i['data'] == '01-12-2022':
        #        variacao2022 = i['variacao ipca'].replace('.',',')
        #    if  i['data'] == '01-12-2023':
        #        variacao2023 = i['variacao ipca'].replace('.',',')
        #textoVariacao2021 = 'Projeção de Variação ' + mes_ano_atual + ' para 2021'
        #textoVariacao2022 = 'Projeção de Variação ' + mes_ano_atual + ' para 2022'
        #textoVariacao2023 = 'Projeção de Variação ' + mes_ano_atual + ' para 2023 e Posteriores'
                 
    titulo_pagina = 'IPCA ' + mes_ano_atual + ' Aplicado na Projeção dos Custos'
    fig = ip.gera_grafico_ipca(ipca,start_date,end_date,mes_ano_atual)    
    tabela = ip.controiTabelaIpca(ipca,start_date,end_date,mes_ano_atual)
    df = pd.DataFrame(tabela)
    component_tabela = dash_table.DataTable(id='tabela-ipca',columns=[{"name": i, "id": i} for i in df.columns],data=df.to_dict('records'),page_size=25,page_action='none',style_header=ip.style_header,style_cell=ip.style_cell,style_table=ip.style_table,style_data_conditional=ip.style_data_conditional)
    
    return component_tabela,fig,displayDatePicker,displayRangeSlider,titulo_pagina,variacao2021,textoVariacao2021,variacao2022,textoVariacao2022,variacao2023,textoVariacao2023


    

@app.callback(Output('page-content', 'children'),
              Output('contratos', 'className'),
              Output('balanco', 'className'),
              Output('custos', 'className'),
              Input('url', 'pathname'))
def display_page(pathname):
    global caminho
    global valorContrato
    global balanço
    global custosContratos
    global ipca
    caminho = pathname
    if pathname == '/':
        if valorContrato == {}:
            r = requests.get('http://localhost:8030/valorcontratostest')
            if r.status_code == 200:
                valorContrato = r.json()
            else:
                print('Valor Contrato falhou')
        return contratos.layout,'sidebar-item-selected','sidebar-item','sidebar-item'
    elif pathname == '/contratos':
        if valorContrato == {}:
            r = requests.get('http://localhost:8030/valorcontratostest')
            if r.status_code == 200:
                valorContrato = r.json()
            else:
                print('Valor Contrato falhou')
        return contratos.layout,'sidebar-item-selected','sidebar-item','sidebar-item'
    elif pathname == '/balanco':
        if balanço == []:
            r = requests.get('http://localhost:8030/balanco')
            if r.status_code == 200:
                balanço = r.json()
            else:
                print('Balanço falhou')
        return balanco.layout,'sidebar-item','sidebar-item-selected','sidebar-item'
    elif pathname == '/custos':
        if custosContratos == {}:
            r = requests.get('http://localhost:8030/custoscontratos')
            if r.status_code == 200:
                custosContratos = r.json()
            else:
                print('Custos falhou')
        if ipca == []:
            r = requests.get('http://localhost:8030/ipca')
            if r.status_code == 200:
                ipca = r.json()
            else:
                print('IPCA falhou')
        return custos.layout,'sidebar-item','sidebar-item','sidebar-item-selected'
    else:
        return '404'