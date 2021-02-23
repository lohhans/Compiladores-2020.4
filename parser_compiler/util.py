def arvoreExpressao(lista):
    if(lista == None or len(lista) == 0):
        return []
    else:
        listaPrimeiro = lista[0]
        if (len(lista) == 1):
            return [listaPrimeiro]

        listaSegundo = lista[1]
        listaTerceiro = arvoreExpressao(lista[2:])
        return ([listaPrimeiro] + [listaSegundo] + [listaTerceiro])


def expressaoTresEnderecos(lista):
    listaTresEnd = []

    if(lista == None or len(lista) == 0):
        return listaTresEnd

    primeiraVariavel = lista[0]
    if (len(lista) == 1):
        listaTresEnd.append(('mov', 'temp', primeiraVariavel))

    else:
        operacao = lista[1]
        resto = expressaoTresEnderecos(lista[2])
        listaTresEnd.extend(resto)

        if(operacao == "+"):
            listaTresEnd.append(('add', 'temp', primeiraVariavel))

        if(operacao == "*"):
            listaTresEnd.append(('mul', 'temp', primeiraVariavel))

    return listaTresEnd
