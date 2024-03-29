import calendar
from datetime import datetime,date

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

# Função legado para transforma um dicionio numa string no formato csv.
def dictToString(dicionario):
    string = u''
    cabecalho = dicionario.keys()
    for cb in cabecalho:
        string = string + cb + ';'
    string = string + '\n'
    valores = list(dicionario.values())
    for i in range(len(valores[0])):
        for j in range(len(valores)):
            valor = str(valores[j][i])
            string = string + valor + ';'
        string = string + '\n' 
        
    return string

# A partir de uma data e o número de meses retorna uma outra data com meses a mais ou a menos
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return date(year, month, day)

# Retorna a diferença de meses entre duas datas
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

# A partir de um array de datas, retorna somente o ano da data.
def separa_anos(data):
    arrayData = data.split('-')
    return arrayData[2]

# Retorna o número de horas num ano
def numero_horas_ano(ano):
    inicio = date(int(ano),1,1)
    fim = date(int(ano) + 1,1,1)
    numeroHoras = (fim - inicio).days * 24
    return numeroHoras

# Transforma o formato 01-01-2019 para JAN/2019
def transforma_data(string):
    return datetime.strptime(string, "%d-%m-%Y").strftime("%b/%Y").capitalize()

# Pega um valor no formato FEB/2019 e traduz.
def data_ptBr(string):
    arrayString = string.split('/')
    if arrayString[0] == "Jan":
        return string 
    elif arrayString[0] == "Feb":
        return str('Fev/' + arrayString[1])
    elif arrayString[0] == "Mar":
        return string
    elif arrayString[0] == "Apr":
        return str('Abr/' + arrayString[1])
    elif arrayString[0] == "May":
        return str('Mai/' + arrayString[1])
    elif arrayString[0] == "Jun":
        return string
    elif arrayString[0] == "Jul":
        return string
    elif arrayString[0] == "Aug":
        return str('Ago/' + arrayString[1])
    elif arrayString[0] == "Sep":
        return str('Set/' + arrayString[1])
    elif arrayString[0] == "Oct":
        return str('Out/' + arrayString[1])
    elif arrayString[0] == "Nov":
        return string
    elif arrayString[0] == "Dec":
        return str('Dez/' + arrayString[1])
    else:
        return string

# Descrição do mês em que os dados estão consolidados, se for depois do dia 15 eles já estão passíveis de estar consolidados.
def mesAnoConsolidado():
    if int(date.today().strftime("%d")) >= 15:
        consolidado = add_months(date.today(), -2) 
    else:
        consolidado = add_months(date.today(), -3)
    
    if int(consolidado.strftime("%m")) == 1:
        return 'Janeiro de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 2:
        return 'Fevereiro de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 3:
        return 'Março de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 4:
        return 'Abril de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 5:
        return 'Maio de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 6:
        return 'Junho de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 7:
        return 'Julho de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 8:
        return 'Agosto de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 9:
        return 'Setembro de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 10:
        return 'Outubro de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 11:
        return 'Novembro de ' + consolidado.strftime("%Y")
    if int(consolidado.strftime("%m")) == 12:
        return 'Dezembro de ' + consolidado.strftime("%Y")
