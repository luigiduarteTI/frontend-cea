import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import date
from dash_extensions import Download
from .inputsNecessarios import elementos
from .uteis import funcoes

layout = html.Div([
    html.Div(children=elementos,className="d-none"),
    dcc.Location(id='url1', refresh=False),
    html.Div('',id="output-url", className="d-none"),
    html.Div([
        html.H3('Balanço > Mensal', className="titulo", id="titulo-pagina"),
        ],
        className="titulo-menu"),
    html.Div(
        html.Div([
            
            html.Div([
                html.H5('Total de Contratos, Carga e Sobra por Data ', id="titulo-grafico"),
            ], className="titulo-grafico-selecao"),
            
            dcc.Loading(id="loading-1", children=[html.Div(dcc.Graph(id='grafico') ,id="container-grafico")], type="circle"),
            
            html.Div('OBS: Valores Consolidados até ' + funcoes.mesAnoConsolidado(),className="mb-4 pl-3"),
            
            html.Div([
                html.Div([
                    dcc.DatePickerRange(
                        calendar_orientation='vertical',
                        display_format='DD/MM/YYYY',
                        min_date_allowed=date(2019, 1, 1),
                        max_date_allowed=date(2040, 12, 31),
                        start_date=date(2019, 1, 1),
                        end_date=date(2023, 12, 31),
                        className="pl-3 mb-1", 
                        id="date-picker"),  
                    dcc.RangeSlider(id='range-slider',min=0,max=264,step=1,value=[0, 59],allowCross=False)
                    ],
                        style={'width': '400px','height': '75px'}),
                html.Div([
                    dbc.DropdownMenu(
                        label="Exportar Dados",
                        className="d-inline-block mr-3",
                        toggleClassName="btn-exportacao",
                        children=[
                            dbc.DropdownMenuItem(['Exportar os dados do gráfico',Download(id="download-grafico")], id="btn-exp-grafico"),
                            dbc.DropdownMenuItem(['Exportar os dados da tabela',Download(id="download-tabela")], id="btn-exp-tabela"),
                        ],
                    ),
                    dbc.Button("Mensal", id="mes", className="btn-menu mr-3"),
                    dbc.Button("Anual", id="ano", className="btn-menu"),
                    ], style={'display':'inline-block'})
            ], className="slider-filtros mb-4"),

            dcc.Loading(id="loading-2", children=[html.Div(id="container-tabela")], type="circle"),           
            
            ]
            ,className="px-4 pt-4 pb-5"),    
        className="bg-branco"
    ),
    
    
    
])

