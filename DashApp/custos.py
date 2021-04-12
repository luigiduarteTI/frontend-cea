import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import date,timedelta,datetime
from dash_extensions import Download
from .modal import modal
from .ipca import ipca
from .inputsNecessarios import elementos
from .uteis import funcoes


layout = html.Div([
    html.Div(children=elementos,className="d-none"),
    dcc.Location(id='url1', refresh=False),
    html.Div('',id="output-url", className="d-none"),
    html.Div([
        html.H3('Custos > Mensal > Detalhado > Unitário', className="titulo", id="titulo-pagina"),
        dbc.DropdownMenu(
            label="Menu",
            toggleClassName="btn-menu",
            children=[
                dbc.DropdownMenuItem("Anual", id="mes-ano"),
                dbc.DropdownMenuItem("Resumido", id="det-res"),
                dbc.DropdownMenuItem("Total", id="unidade"),
            ],
         )
        ],
        className="titulo-menu"),
    html.Div(
        html.Div([
            
            html.Div([
                html.H5('MWh por Data e Subsistema', id="titulo-grafico"),
                dcc.RadioItems(
                    options=[
                        {'label': 'Gráfico de Subsistema', 'value': 'sub'},
                        {'label': 'Gráfico com total', 'value': 'tol'}
                    ],
                    id="selecao-grafico",
                    value='sub',
                    inputClassName="selecao-input",
                    labelClassName="selecao-grafico",
                )
            ], className="titulo-grafico-selecao"),
            
            dcc.Loading(id="loading-1", children=[html.Div(dcc.Graph(id='grafico') ,id="container-grafico")], type="circle"),
            
            html.Div('OBS: Valores Consolidados até ' + funcoes.mesAnoConsolidado(),className="mb-4 pl-3"),
            
            html.Div([
                html.Div([
                    dcc.DatePickerRange(
                        calendar_orientation='vertical',
                        display_format='DD/MM/YYYY',
                        min_date_allowed=date(2020, 1, 1),
                        max_date_allowed=date(2040, 12, 31),
                        start_date=date(2020, 1, 1),
                        end_date=date(2023, 12, 31),
                        className="pl-3 mb-1", 
                        id="date-picker"),  
                    dcc.RangeSlider(id='range-slider',min=0,max=252,step=1,value=[0, 59],allowCross=False)
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
                    html.Button(
                        html.Img(src="assets/imgs/eraser-solid.png",className="botao-limpa"),
                        id="borracha",
                        style={'width': '30px', 'height':'30px', 'padding': '0px','border':'2px #4479F5 solid', 'border-radius': '.25rem', 'marginRight': '15px'}),
                    dbc.Button("Filtros", id="open", className="btn-filtros mr-3"),
                    dbc.Button("Estimativa IPCA", id="open2", className="btn-filtros", style={'fontSize': '13px'}),
                    ], style={'display':'inline-block'})
            ], className="slider-filtros mb-4"),
            dcc.Loading(id="loading-2", children=[html.Div(id="container-tabela")], type="circle"),
            ]
            ,className="px-4 pt-4 pb-5"),  
        className="bg-branco"
    ),
    dbc.Modal(
        modal,
        id="modal",
        size="xl"
    ),
    dbc.Modal(
        ipca,
        id="ipca",
        size="xl"
    ),
])