import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import date,timedelta,datetime
from dash_extensions import Download
from .modal import modal
from .inputsNecessarios import elementos
from .uteis import funcoes

layout = html.Div([
    html.Div(children=elementos,className="d-none"),
    dcc.Location(id='url1', refresh=False),
    html.Div('',id="output-url", className="d-none"),
    html.Div([
        html.H3('Contratos > Anual > Detalhado > MWh', className="titulo", id="titulo-pagina"),
        dbc.DropdownMenu(
            label="Menu",
            toggleClassName="btn-menu",
            children=[
                dbc.DropdownMenuItem("Anual", id="mes-ano"),
                dbc.DropdownMenuItem("Resumido", id="det-res"),
                dbc.DropdownMenuItem("MWm", id="unidade"),
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
                    html.Button(
                        html.Img(src="assets/imgs/eraser-solid.png",className="botao-limpa"),
                        id="borracha",
                        style={'width': '30px', 'height':'30px', 'padding': '0px','border':'2px #4479F5 solid', 'border-radius': '.25rem', 'marginRight': '15px'}),
                    dbc.Button("Filtros", id="open", className="btn-filtros"),
                    ], style={'display':'inline-block'})
            ], className="slider-filtros mb-4"),
            
            # html.Div([
            #         html.Div([
            #             html.Button(html.Img(src="assets/imgs/ellipsis-h-solid.png",className="botao-limpa", id="img"), id="btn", className="btn-exportacao"),
            #             Download(id="download")
            #         ]),
            #         dbc.FormGroup(
            #             [
            #                 dbc.Checklist(
            #                     options=[
            #                         {"label": "Todos", "value": 'TD'},
            #                     ],
            #                     value=['TD'],
            #                     id="checklist-tipo-contrato-todos",
            #                 ),
            #             ], id="check-list-tipo-contrato", className="dropdown-exportacao-content"
            #         ),
            #     ],className="dropdown-exportacao"),
            # html.A(, id='my-link'),
            dcc.Loading(id="loading-2", children=[html.Div(id="container-tabela")], type="circle"),
           
            # dash_table.DataTable(
            #     id='tabela',
            #     columns=[{"name": i, "id": i} for i in df.columns],
            #     data=df.to_dict('records'),
            #     style_table={'overflowX': 'auto'},
            #     )
            ]
            ,className="px-4 pt-4 pb-5"),    #dcc.Input(id="input-1", type="email", placeholder="name@example.com", className="form-control mt-4"),
        className="bg-branco"
    ),
    dbc.Modal(
        modal,
        id="modal",
        size="xl"
    ),
])








