from django.http import JsonResponse
import datetime
import pycep_correios

def validar_cpf(request):
    cpf = request.GET['cpf']

    if not cpf:
        return JsonResponse({'valid':'false','message': 'CPF inválido!'})

    cpfs_conhecidos = ['00000000000','11111111111','22222222222','33333333333','44444444444',
                       '55555555555','66666666666','77777777777','88888888888','99999999999']

    if cpf in cpfs_conhecidos:
        return JsonResponse({'valid':'false','message': 'O CPF informado é inválido!'})

    if len(cpf) == 11 and cpf not in cpfs_conhecidos:
        #Cria variaveis para validacao
        cpf_list = list(cpf)
        elementos = list(range(10,1,-1))
        validar = 0
        index = 10
        #Gera o numero para validar o primeiro digito verificador
        for num1 in range(0,9):
        	validar += int(cpf_list[num1]) * elementos[num1]
        	index -= 1

        #Gera o primeiro digito verificador
        resto = (float(validar) * 10) % 11
        if resto == 10.0:
            resto = 0
        #Valida primeiro digito verificador
        digitos_verificadores = cpf_list[9:]

        primeiro_digito_valid = False
        primeiro_digito = int(digitos_verificadores[0])

        if (int(resto) == primeiro_digito):
        	primeiro_digito_valid = True
        #Zera variaveis para validacao do segundo digito verificador
        elementos = list(range(11,1,-1))
        validar = 0
        index = 11
        resto = 0
        #Gera o numero para validar o segundo digito verificador
        for num2 in range(0, 10):
        	validar += int(cpf_list[num2]) * elementos[num2]
        	index -= 1
        #Gera o segundo digito verificador
        resto = (float(validar) * 10) % 11
        if resto == 10.0:
            resto = 0
        #Valida o segundo digito verificador e imprime o CPF final
        segundo_digito_valid = False
        segundo_digito = int(digitos_verificadores[1])
        if (int(resto) == segundo_digito):
            segundo_digito_valid=True

        if primeiro_digito_valid and segundo_digito_valid:
            return JsonResponse({'valid':'true'}, status=200)
        else:
            return JsonResponse({'valid':'false','message': 'O CPF informado é inválido!'})
    else:
        return JsonResponse({'valid':'false','message': ' '})


def validar_cep(request):
    cep = request.GET['cep']

    if not cep:
        return JsonResponse({'valid':'false','message': 'CEP inválido!'})

    cep_correios = {}
    if len(cep) == 8:
        try:
            cep_correios = pycep_correios.consultar_cep(cep)
            print(cep_correios)
            return JsonResponse({'valid':'true', 'message': 'okok'}, status=200)
        except Exception:
            return JsonResponse({'valid':'false','message': 'O CEP informado é inválido!'})
    return JsonResponse({'valid':'false','message': ' '})


def validar_data_nascimento(request):
    data_nascimento = request.GET['data_nascimento']

    if not data_nascimento:
        return JsonResponse({'valid':'false','message': 'A data de nascimento informada é inválida!'})

    ano_atual = datetime.datetime.now().year
    if len(data_nascimento) == 8:
        data_split = list(data_nascimento)
        dia, mes, ano = int(''.join(data_split[:2])), int(''.join(data_split[2:-4])), int(''.join(data_split[4:]))

        if ano >= ano_atual:
            return JsonResponse({'valid':'false','message': 'A data de nascimento informada é inválida!'})
        try:
            datetime.datetime(ano, mes, dia)
            return JsonResponse({'valid':'true'}, status=200)
        except Exception:
            return JsonResponse({'valid':'false','message': 'A data de nascimento informada é inválida!'})
    return JsonResponse({'valid':'false','message': ' '})
