from math import ceil

TAMANHO_DOS_BLOCOS = 64 #bits
NUMERO_DE_RODADAS = 4
TAMEMBYTES = TAMANHO_DOS_BLOCOS // 8


"""
Encriptação

Primeira parte: dividir os bytes em duas partes R0 e L0
Segunda parte: R0 é códificada usando o algorítmo fs e armazenada em E
Algorítimo fs:
        imagine que vamos criptografar a, b e c
        a primeira letra vai para o segundo lugar
        a segunda letra vai para o terceiro lugar
        a terceira letra vai para o primeiro lugar

        porém fazemos isso com bits, e dividimos o byte de três em trẽs

Terceira parte: L1 vai receber R0 e R1 vai receber L0 xor E, lembrando que essas variáveis representam estados de lado
esquerdo e lado direito
Quarta parte: contatenar L1 com R1 e esse vai ser o resultado do encript


É possível manipular os bits de uma string, transfomando ela em bytes, com string.encode("ascii"), assim cada byte
da string meio que vira um inteiro, e com o inteiros usamos o format(inteiro, "b") assim obtemos uma lista de bits.
"""
def encripta(plain_text):
        resultado = bytes()

        cripted = ''
        
        emBits = byteToString(plain_text)
    
        div = len(emBits) / TAMANHO_DOS_BLOCOS

        #Caso na divisão de blocos tenhamos um dos blocos que não esteja completo, o completamos com 0's
        zeros = ""
        if(div < 1):
            for i in range(0, TAMANHO_DOS_BLOCOS - len(emBits)):

                zeros += "0"
        elif (div > 1):
            for i in range(0, div * TAMANHO_DOS_BLOCOS - len(emBits)):
                zeros += "0"
        
        emBits = emBits + zeros
   
        qtdBlocos = ceil(div)
        
        for i in range(0, qtdBlocos * TAMANHO_DOS_BLOCOS , TAMANHO_DOS_BLOCOS):
            #primeira parte
            R0 = emBits[TAMANHO_DOS_BLOCOS // 2 + (TAMANHO_DOS_BLOCOS * i): i * TAMANHO_DOS_BLOCOS + TAMANHO_DOS_BLOCOS]
            L0 = emBits[i:TAMANHO_DOS_BLOCOS // 2 + (TAMANHO_DOS_BLOCOS * i)]
            #segunda parte
            E = fs(R0)
            #terceira parte
            L1 = R0
            R1 = xor(L0, E)
            #quarta parte
            cripted += L1 + R1

        resultado =  stringToByte(cripted)
        return resultado


def criptografa(valor):
    resultado = bytes()
    resultado = encripta(valor.encode("utf-8"))
    for r in range(0, NUMERO_DE_RODADAS - 1):
        resultado = encripta(resultado)
    return resultado




"""
Descriptação

Primeiro passo: Separamos as partes do ciper text em duas, L1 e R1.
Segundo passo:  R0 vai ser o L1
Terceiro passo: o L0 vai ser o R1 xor com inverso da fs, inversFs(R0) 
Quarto passo: Juntar L0 com R0
"""
def decript(encripted):

    emBits =  byteToString(encripted)   

    div = len(encripted) / TAMANHO_DOS_BLOCOS

    qtdBlocos = ceil(div)

    decripted = ""

    for i in range(0, qtdBlocos * TAMANHO_DOS_BLOCOS , TAMANHO_DOS_BLOCOS):
        #primeira parte
        R1 = emBits[TAMANHO_DOS_BLOCOS // 2 + (TAMANHO_DOS_BLOCOS * i): i * TAMANHO_DOS_BLOCOS + TAMANHO_DOS_BLOCOS]
        L1 = emBits[i:TAMANHO_DOS_BLOCOS // 2 + (TAMANHO_DOS_BLOCOS * i)]
        #Segunda parte
        R0 =  L1
        #Terceira parte
        L0 = xor(R1, inversFs(R0))
        #Quarta parte
        decripted +=  L0 + R0

    return stringToByte(decripted)


def descriptografa(cifra):
    resultado = cifra
    for i in range(0, NUMERO_DE_RODADAS):
        resultado = decript(resultado)
    return resultado


def byteToString(bytes):
    emBits = ""
    for i in bytes:
        emBits += format(i, f"08b")
    return emBits

#Transforma os caracteres, que representam os bits, em um valor realmente binário
def stringToByte(string):
    resultado = bytes()
    for i in range(0, len(string) // 8):

        bloco =  int(string[(8*i): i + ((i + 1)*(7)) + 1], 2)
        resultado += bytes([bloco])
    return resultado


def fs(R0):

    L  = R0[:len(R0) // 2]
    R = R0[len(R0) // 2:]


    return apliFs(L) + apliFs(R)

def apliFs(text):
    resultado = text[len(text) - 1]
    for i in range(0, len(text) - 1):
        resultado += text[i]

    return resultado


def inversFs(R1):
    L =  R1[: len(R1) // 2]
    R = R1[len(R1) // 2:]

    return apliInverseFs(L) + apliInverseFs(R)


def apliInverseFs(text):
    resultado = ""
    for i in range(1, len(text)):
        resultado +=  text[i]
    resultado += text[0]
    return resultado


def xor(string1, string2):
    resultado = ""
    if len(string1) == len(string2):
        for i in range(0, len(string1)):
            if string1[i] != string2[i]:
                resultado += "1"
            else:
                resultado += "0"
    return resultado


if __name__ == "__main__":
    plain =  "Ola"
    cript =  criptografa(plain)
    descrpit  = descriptografa(cript)

    print(plain, cript, descrpit)
