# Esse arquivo foi criado porque o Dash ainda não lida de forma satisfatória com url e paginação, 
# Existem algumas callbacks que precisam ser disparadas para movimentar os eventos de filtro das páginas
# E essas callbacks são disparadas e ficam escutando alterações independente da página em que estiver
# Então por exemplo, se eu defino uma callback no contratos, ela vale para toda a aplicacao, dessa forma os inputs dessa callback precisam
# Existir independentemente da página que estiver sendo exibida.
# Esse arquivo é para listar todos os componentes de input de todas as callbacks para que nenhuma página sofra um erro de não chamar algum input

# This file was created because Dash does not yet handle url and pagination satisfactorily,
# There are some callbacks that need to be triggered to move the filter events of the pages
# And these callbacks are triggered and listen for changes regardless of the page you are on
# So for example, if I define a callback in contracts, it applies to the whole application, so the inputs of this callback need
# Exists regardless of the page being displayed.
# This file is to list all the input components of all callbacks so that no page suffers an error of not calling any input

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
df = pd.DataFrame()
elementos = [
    
    html.H3('Contratos > Anual > Detalhado > MWh', className="titulo", id="titulo-pagina"),
    
    html.H5('MWh por Data e Subsistema', id="titulo-grafico"),
    
    html.Div(dcc.RadioItems(
                    options=[
                        {'label': 'Gráfico de Subsistema', 'value': 'sub'},
                        {'label': 'Gráfico com total', 'value': 'tol'}
                    ],
                    id="selecao-grafico",
                    value='sub',
                    inputClassName="selecao-input",
                    labelClassName="selecao-grafico",
                ),className="d-none"),
    
    dbc.DropdownMenu(
        label="Menu",
        toggleClassName="btn-menu",
        children=[
            dbc.DropdownMenuItem("Anual", id="mes-ano"),
            dbc.DropdownMenuItem("Resumido", id="det-res"),
            dbc.DropdownMenuItem("MWm", id="unidade"),
        ],
    ),
    
    dbc.Button("Mensal", id="mes", className="btn-menu mr-3"),
    dbc.Button("Anual", id="ano", className="btn-menu"),
    html.Button(
                html.Img(src="assets/imgs/eraser-solid.png",className="botao-limpa"),
                id="borracha",
                style={'width': '30px', 'height':'30px', 'padding': '0px','border':'2px #4479F5 solid', 'border-radius': '.25rem', 'marginRight': '15px'}),
    dbc.Button("Filtros", id="open", className="btn-filtros"),
    
    html.Div(dcc.Graph(id='grafico') ,id="container-grafico"),
    
    html.Div(id="container-tabela"),
    
    dash_table.DataTable(id='tabela',columns=[{"name": i, "id": i} for i in df.columns],page_size=25),
    
    dcc.DatePickerRange(
                        calendar_orientation='vertical',
                        display_format='DD/MM/YYYY',
                        className="pl-3 mb-1", 
                        id="date-picker"),  
    dcc.RangeSlider(id='range-slider',min=0,max=264,step=1,value=[0, 59],allowCross=False),
    
    dbc.ModalBody([
        html.Div([
            html.H5('TIPO DE CONTRATO'),
            html.Div([
                    html.Button(id="btn-tipo-contrato", className="dropbtn"),
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-tipo-contrato-todos",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-tipo-contrato-valores",
                            ),
                        ], id="check-list-tipo-contrato", className="dropdown-content2"
                    ),
                ],className="dropdown2")
        ], className="modal-item"),
        
        html.Div([
            html.H5('SUBMERCADO'),
            html.Div([
                    html.Button('Todos', id="btn-submercado", className="dropbtn"),
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-submercado-todos",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-submercado-valores",
                            ),
                        ], id="check-list-submercado", className="dropdown-content2"
                    ),
                ],className="dropdown2")
        ], className="modal-item"),
        
        html.Div([
            html.H5('LEILÃO'),
            html.Div([
                    html.Button('Todos', id="btn-leilao", className="dropbtn"),
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-leilao-todos",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-leilao-valores",
                            ),
                        ], id="check-list-leilao", className="dropdown-content2"
                    ),
                ],className="dropdown2")
        ], className="modal-item"),
        
        html.Div([
            html.H5('STATUS'),
            html.Div([
                    html.Button('Todos', id="btn-status", className="dropbtn"),
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-status-todos",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-status-valores",
                            ),
                        ], id="check-list-status", className="dropdown-content2"
                    ),
                ],className="dropdown2")
        ], className="modal-item"),
        
        html.Div([
            html.H5('PRODUTO'),
            html.Div([
                    html.Button('Todos', id="btn-produto", className="dropbtn"),
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-produto-todos",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-produto-valores",
                            ),
                        ], id="check-list-produto", className="dropdown-content2"
                    ),
                ],className="dropdown2")
        ], className="modal-item"),
        
        html.Div([
            html.H5('VENDEDOR'),
            html.Div([
                    html.Button('Todos', id="btn-vendedor", className="dropbtn"),
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-vendedor-todos",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-vendedor-valores",
                            ),
                        ], id="check-list-vendedor", className="dropdown-content2"
                    ),
                ],className="dropdown2")
        ], className="modal-item"),
        
        html.Div([
            html.H5('INÍCIO DE SUPRIMENTO'),
            html.Div([
                    html.Button('Todos', id="btn-inicio-suprimento", className="dropbtn"),
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-inicio-suprimento-todos",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-inicio-suprimento-valores",
                            ),
                        ], id="check-list-inicio-suprimento", className="dropdown-content2"
                    ),
                ],className="dropdown2")
        ], className="modal-item"),
        
        html.Div([
            html.H5('FIM DE SUPRIMENTO'),
            html.Div([
                    html.Button('Todos', id="btn-fim-suprimento", className="dropbtn"),
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-fim-suprimento-todos",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Todos", "value": 'TD'},
                                ],
                                value=['TD'],
                                id="checklist-fim-suprimento-valores",
                            ),
                        ], id="check-list-fim-suprimento", className="dropdown-content2"
                    ),
                ],className="dropdown2")
        ], className="modal-item"),
    ]),
    
    dbc.ModalFooter([
        dbc.Button("Limpar Alterações", id="limpar-alteracoes", color="primary", className="mr-auto", style={'display': 'inline-block', 'marginLeft':'20px'}),
        dbc.Button("Fechar", id="close", color="danger", className="ml-auto", style={'display': 'inline-block', 'marginRight':'20px'}),
        ]
    ),
    
    
    dbc.ModalHeader(html.Span([
            html.Span(id="titulo-modal-ipca", className="pt-2"),
            dbc.Button("Mensal", id="mes-ipca", className="btn-menu", style={'display': 'inline-block', 'marginRight':'20px'}),
            dbc.Button("Anual", id="ano-ipca", className="btn-menu", style={'display': 'inline-block', 'marginRight':'20px'}),
        ])),
    dbc.ModalBody([
        html.Div([
            
            html.Div([
                html.Div(id="container-tabela-ipca"),
                html.Div([
                        dcc.DatePickerRange(
                        calendar_orientation='vertical',
                        display_format='DD/MM/YYYY',
                        className="datepicker-ipca mb-1", 
                        id="date-picker-ipca"),  
                    dcc.RangeSlider(id='range-slider-ipca',min=0,max=252,step=1,value=[0, 59],allowCross=False, className="slider-ipca")
                ],className="container-slider-datepicker"),
                ], className="container-tabela-ipca"),
            html.Div([
                html.Div(dcc.Graph(id='grafico-ipca'), style={'width':'700px','height':'500px','backgroundColor':'blue'}),
                html.Div([
                    html.Div([
                            html.Div("0,25%", className="estatistica-variacao",id="variacao-1"),
                            html.Div("Projeção de Variação Mensal para 2021", className="estatistica-texto",id="texto-variacao-1")
                        ],className="item-estatisca"),
                    html.Div([
                            html.Div("0,25%", className="estatistica-variacao",id="variacao-2"),
                            html.Div("Projeção de Variação Mensal para 2022", className="estatistica-texto",id="texto-variacao-2")
                        ],className="item-estatisca"),
                    html.Div([
                            html.Div("0,27%", className="estatistica-variacao",id="variacao-3"),
                            html.Div("Projeção de Variação Mensal para 2023 e Posteriores", className="estatistica-texto",id="texto-variacao-3")
                        ],className="item-estatisca")
                    ],className="container-estatisticas"),
                ], className="container-grafico-estatisticas-ipca"),
            
        ],className="container-ipca"),
    ]),
    dbc.ModalFooter([
        dbc.Button("Fechar", id="close2", color="danger", className="ml-auto", style={'display': 'inline-block', 'marginRight':'20px'}),
        ]
    )
    
    
]