#coding: utf-8
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dados import mudaContrato,mudaValorContrato,mudaBalanco,mudaResumo
import requests

r1 = requests.get('https://7b12145af545.ngrok.io/contratos', timeout=300)
if r1.status_code == 200:
    mudaContrato(r1.json())
r4 = requests.get('https://7b12145af545.ngrok.io/ctresumido', timeout=300)
if r4.status_code == 200:
    mudaResumo(r4.json())
# r2 = requests.get('http://af5dfa176871.ngrok.io/valorcontratos')
# if r2.status_code == 200:
#     mudaValorContrato(r2.json())
# r3 = requests.get('http://af5dfa176871.ngrok.io/balanco')
# if r3.status_code == 200:
#     mudaBalanco(r3.json())

from app import app
import callbacks


server = app.server
caminho = '/'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(),
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
    html.Div(
        html.Div([
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
                html.Div(html.Div(html.Div('',id='page-content'),className="container-fluid")
                         ,className="conteudo px-5 py-4"),
                # html.Div(html.Div(dcc.Loading(id="loading-3", children=html.Div('',id='page-content'), type="circle")
                #                   ,className="container-fluid")
                #          ,className="conteudo px-5 py-4"),
            ],className="flex-conteudo"), 
    className="menu"),
    
], style={'minHeight': '100vh'})



if __name__ == '__main__':
    app.run_server(debug=True)