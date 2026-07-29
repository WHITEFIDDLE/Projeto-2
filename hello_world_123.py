def funcao_complexa(valor):
    resultado = 0

    if valor == 1:
        resultado = valor + 1
    elif valor == 2:
        resultado = valor + 2
    elif valor == 3:
        resultado = valor + 3
    elif valor == 4:
        resultado = valor + 4
    elif valor == 5:
        resultado = valor + 5
    elif valor == 6:
        resultado = valor + 6
    elif valor == 7:
        resultado = valor + 7
    elif valor == 8:
        resultado = valor + 8
    elif valor == 9:
        resultado = valor + 9
    elif valor == 10:
        resultado = valor + 10
    else:
        resultado = -1

    return resultado


def codigo_duplicado_1(x):
    total = 0
    for i in range(20):
        total += x * i

    if total > 100:
        print("maior que 100")
    else:
        print("menor ou igual a 100")

    return total


def codigo_duplicado_2(x):
    total = 0
    for i in range(20):
        total += x * i

    if total > 100:
        print("maior que 100")
    else:
        print("menor ou igual a 100")

    return total


def exception_generico():
    try:
        divisao = 10 / 0
        return divisao
    except:
        return None


def variaveis_nao_usadas():
    nome = "Lucas"
    idade = 19
    cidade = "São Paulo"
    curso = "Defesa Cibernética"

    return nome


for i in range(15):
    print(funcao_complexa(i))