
#coding: utf-8
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from . import dados
import requests

# Recuperando as informações dos contratos detalhadamente e resumidamente
r1 = requests.get('http://localhost:8030/contratos')
if r1.status_code == 200:
   dados.mudaContrato(r1.json())
r4 = requests.get('http://localhost:8030/ctresumido')
if r4.status_code == 200:
   dados.mudaResumo(r4.json())

from .app import app
from . import callbacks

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    # Cabeçalho padrão
    html.Nav(
        dcc.Link([
            html.Div(
                html.Img(src="assets/imgs/logo.png",className="logo-nav", alt="Logo da Engenho"),
                className="side-logo"),
            html.Div(
                html.Img(src="assets/imgs/logo-extenso.png",className="img-nav", alt="Logo da Engenho"),
                className="center-logo")
        ],
        className="nav-flex", href="/"),
    className="py-2 bg-engenho"),
    # Corpo da aplicação
    html.Div(
        html.Div([
            ### Ínicio SideBar ###
            html.Div([
                dcc.Link(html.Div([
                    html.Div(
                        html.Img(src="assets/imgs/contrato.png", className="sidebar-img", alt="Ir para a página dos contratos", style={'marginLeft':'13px', 'max-height':'42px'}),
                        className="sidebar-container-img"
                    ),
                    html.Div(
                        'Contratos',
                        className="sidebar-container-title"
                    )
                ],
                    id="contratos"
                ), href='/contratos', className="sidebar-link"),
                dcc.Link(html.Div([
                    html.Div(
                        html.Img(src="assets/imgs/balanco.png", className="sidebar-img", alt="Ir para a página dos contratos"),
                        className="sidebar-container-img"
                    ),
                    html.Div(
                        'Balanço',
                        className="sidebar-container-title"
                    )
                ],
                    id="balanco"
                ), href='/balanco', className="sidebar-link"),
                dcc.Link(html.Div([
                    html.Div(
                        html.Img(src="assets/imgs/custo.png", className="sidebar-img", alt="Ir para a página dos contratos"),
                        className="sidebar-container-img"
                    ),
                    html.Div(
                        'Custos',
                        className="sidebar-container-title"
                    )
                ],
                    id="custos"
                ), href='/custos', className="sidebar-link")
            ],className="sidebar"),
            ### Fim SideBar ###
            # Conteúdo variante:
            html.Div(html.Div(html.Div('',id='page-content'),className="container-fluid")
                        ,className="conteudo px-5 py-4"),
        ],className="flex-conteudo"), 
    className="menu"),
    
], style={'minHeight': '100vh'})



# if __name__ == 'DashApp':
#     app.run_server(debug=True)
