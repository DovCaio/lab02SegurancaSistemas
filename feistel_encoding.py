"""
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

TAMANHO_DOS_BLOCOS = 8

def encripta(dados):


        plain_text = dados.encode("ascii")
        cripted = ''

        resto_tamanho = len(plain_text) % TAMANHO_DOS_BLOCOS
        #Caso na divisão de blocos tenhamos um dos blocos que não esteja completo, o completamos com 0's
        if(resto_tamanho != 0):
            for i in range(0, resto_tamanho):
                plain_text = plain_text + b'0'

        for byte in plain_text:
            #primeira parte
            R0 = format(byte, "08b")[:4]
            L0 = format(byte, "08b")[4:]
            #segunda parte
            E = fs(R0)
            #terceira parte
            L1 = R0
            R1 = xor(L0, E)
            #quarta parte
            encriptado = L1 + R1
            cripted += encriptado

        for i in dados.encode():
            print(format(i, "b"), end="")

        print("\n")
        print(cripted)

        a = bytes(cripted)
        print(a.decode())

def fs(R0):
    resultado = ''
    resultado += (R0[3])
    for i in range(0, len(R0) - 1):
        resultado += (R0[i])
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

    encripta("Caio")