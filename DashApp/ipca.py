import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import dash_table
import dash
from .app import app
from dash.dependencies import Input, Output
from .dados import ipca
from datetime import date
from .uteis import funcoes


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
    'width': '350px',
    'height':'592px',
    'overflowY': 'auto'
}

style_data_conditional=[
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': '#C5E5EA'
    }
]


def controiTabelaIpca(ipca,inicioData,fimData,mes_ano):
    
    ipcas = []
    for i in ipca:
        ipcas.append(i) 
    
    if mes_ano == 'Mensal':
        tabela = {
            'Data': [], 
            'IPCA': [], 
            'Variação Mensal': [], 
        }
        for x in range(len(ipcas) -1,-1,-1):
            data = date(int(ipcas[x]['data'].split('-')[2]),int(ipcas[x]['data'].split('-')[1]),int(ipcas[x]['data'].split('-')[0]))
            inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
            fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
            if inicio <= data <= fim:
                continue
            else:
                ipcas.pop(x)
        for i in ipcas:
            tabela['Data'].append(i['data'])
            tabela['IPCA'].append(i['ipca'])
            tabela['Variação Mensal'].append(i['variacao ipca'])
            
        return tabela
    else:
        tabela = {
            'Data': [], 
            'IPCA': [], 
            'Variação Anual': [], 
        }
        datas = []
        for i in ipca:
            datas.append(i['data'])
            
        datas = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))
        
        n = 0
        var = 0
        for i in ipcas:
            if '01-12' in i['data']:
                if i['data'] == '01-12-2019':
                    tabela['IPCA'].append(i['ipca'])
                    tabela['Variação Anual'].append('4,31%')
                    n = i['ipca']
                else:
                    var = ((i['ipca'] / n) - 1) * 100
                    n = i['ipca']
                    tabela['IPCA'].append(n)
                    tabela['Variação Anual'].append(str(round(var,3)).replace('.',',')  + '%')
                    
        tabela['Data'] = datas
            
        return tabela


def gera_grafico_ipca(ipca,inicioData,fimData,mes_ano):
    
    template = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]

    ipcas = []
    for i in ipca:
        ipcas.append(i) 
    
    if mes_ano == 'Mensal':
    
        for x in range(len(ipcas) -1,-1,-1):
            data = date(int(ipcas[x]['data'].split('-')[2]),int(ipcas[x]['data'].split('-')[1]),int(ipcas[x]['data'].split('-')[0]))
            inicio = date(int(inicioData.split('-')[0]),int(inicioData.split('-')[1]),int(inicioData.split('-')[2]))
            fim = date(int(fimData.split('-')[0]),int(fimData.split('-')[1]),int(fimData.split('-')[2]))
            if inicio <= data <= fim:
                continue
            else:
                ipcas.pop(x)
        
        valores = {
            "cor": "#118dff",
            "datas": [],
            "valores": []
        }
        
        for i in ipcas:
            valores['datas'].append(i['data'])
            valores['valores'].append(i['ipca'])
        
        valores['datas'] = list(map(funcoes.transforma_data,valores['datas']))
    else:
        datas = []
        for i in ipca:
            datas.append(i['data'])
            
        datas = funcoes.remove_repetidos(map(funcoes.separa_anos,datas))
        
        valores = {
            "cor": "#118dff",
            "datas": [],
            "valores": []
        }
        for i in ipcas:
            if '01-12' in i['data']:
                valores['valores'].append(i['ipca'])
        
        valores['datas'] = datas
       
    fig = go.Figure()
    fig.add_trace(go.Bar(x=valores['datas'],
                    y=valores['valores'],
                    marker_color=valores["cor"]
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
            titlefont_size=16,
            tickfont_size=14,
        ),
        barmode='group',
        bargap=0.05, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    
    return fig
    


ipca = [
    dbc.ModalHeader([
        html.Span(id="titulo-modal-ipca", className="pt-2"),
        html.Span([
            dbc.Button("Mensal", id="mes-ipca", className="btn-menu", style={'display': 'inline-block', 'marginRight':'20px'}),
            dbc.Button("Anual", id="ano-ipca", className="btn-menu", style={'display': 'inline-block', 'marginRight':'20px'}),
        ])
    ]),
    dbc.ModalBody([
        html.Div([
            html.Div([
                html.Div(id="container-tabela-ipca"),
                html.Div([
                        dcc.DatePickerRange(
                        calendar_orientation='vertical',
                        display_format='DD/MM/YYYY',
                        min_date_allowed=date(2020, 1, 1),
                        max_date_allowed=date(2040, 12, 31),
                        start_date=date(2020, 1, 1),
                        end_date=date(2023, 12, 31),
                        className="datepicker-ipca mb-1", 
                        id="date-picker-ipca"),  
                    dcc.RangeSlider(id='range-slider-ipca',min=0,max=252,step=1,value=[0, 59],allowCross=False, className="slider-ipca")
                ],className="container-slider-datepicker"),
            ], className="container-tabela-ipca"),
            html.Div([
                html.Div(dcc.Graph(id='grafico-ipca'), style={'width':'700px','height':'500px','backgroundColor':'blue'}),
                html.Div([
                    html.Div([
                            html.Div("3,63%", className="estatistica-variacao",id="variacao-1"),
                            html.Div("Projeção de Variação Anual para 2021", className="estatistica-texto",id="texto-variacao-1")
                        ],className="item-estatisca"),
                    html.Div([
                            html.Div("3,07%", className="estatistica-variacao",id="variacao-2"),
                            html.Div("Projeção de Variação Anual para 2022", className="estatistica-texto",id="texto-variacao-2")
                        ],className="item-estatisca"),
                    html.Div([
                            html.Div("3,23%", className="estatistica-variacao",id="variacao-3"),
                            html.Div("Projeção de Variação Anual para 2023 e Posteriores", className="estatistica-texto",id="texto-variacao-3")
                        ],className="item-estatisca")
                    ],className="container-estatisticas", id="container-estatisticas"),
                ], className="container-grafico-estatisticas-ipca"),
            
        ],className="container-ipca"),
    ]),
    dbc.ModalFooter([
        dbc.Button("Fechar", id="close2", color="danger", className="ml-auto", style={'display': 'inline-block', 'marginRight':'20px'}),
        ]
    )
]



