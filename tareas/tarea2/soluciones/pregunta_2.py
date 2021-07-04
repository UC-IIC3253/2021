import random


def miller_rabin(n: int, k: int) -> bool:
    """
    Argumentos :
        n: int - n >= 1
        k: int - k >= 1
    Retorna :
        int - True si n es un numero primo , y False en caso contrario .
        La probabilidad de error en el test debe ser menor o
        igual a 2**( -k)
    """

    if n == 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        s = 0
        d = n - 1
        while d % 2 == 0:
            s = s + 1
            d = d // 2
        num = k // 2 + 1
        for i in range(0, num):
            a = random.randint(2, n - 1)
            pot = exp_mod(a, d, n)
            if pot != 1 and pot != n - 1:
                pasar = False
                for j in range(0, s):
                    pot = (pot * pot) % n
                    if pot == n - 1:
                        pasar = True
                        break
                if not pasar:
                    return False
        return True


def generar_primo(largo: int) -> int:
    """
    Argumentos :
        largo: int - largo >= 1
    Retorna :
        int - numero primo con al menos largo digitos . La probabilidad de
        error en la generacion debe ser menor o igual a 2**( - 100)
    """

    while True:
        primo = random.randint(10**(largo - 1), 10**largo - 1)
        if miller_rabin(primo, 100):
            return primo


def alg_ext_euclides(a: int, b: int) -> (int, int, int):
    """
    Argumentos :
        a: int
        b: int - a >= b >= 0 y a > 0
    Retorna :
        (int , int , int) - maximo comun divisor MCD(a, b) entre a y b,
        y numeros enteros s y t tales que MCD(a, b) = s*a + t*b
    """

    r_0 = a
    s_0 = 1
    t_0 = 0
    r_1 = b
    s_1 = 0
    t_1 = 1
    while r_1 > 0:
        r_2 = r_0 % r_1
        s_2 = s_0 - (r_0 // r_1) * s_1
        t_2 = t_0 - (r_0 // r_1) * t_1
        r_0 = r_1
        s_0 = s_1
        t_0 = t_1
        r_1 = r_2
        s_1 = s_2
        t_1 = t_2
    return r_0, s_0, t_0


def mcd(a: int, b: int) -> int:
    """
    Argumentos :
        a: int
        b: int - a > 0 o b > 0
    Retorna :
        maximo comun divisor entre a y b,
    """

    while b > 0:
        temp = b
        b = a % b
        a = temp
    return a


def exp_mod(a: int, b: int, n: int) -> int:
    """
    Argumentos :
        a: int - a >= 0
        b: int - b >= 0
        n: int - n > 0
    Retorna :
        int - a**b en modulo n
    """

    if b == 0:
        return 1
    else:
        res = 1
        pot = a
        while b > 0:
            if b % 2 == 1:
                res = (pot * res) % n
            b = b // 2
            pot = (pot * pot) % n
        return res


def inverso(a: int, n: int) -> int:
    """
    Argumentos :
        a: int - a >= 1
        n: int - n >= 2, a y n son primos relativos
    Retorna :
        int - inverso de a en modulo n
    """

    (r, s, t) = alg_ext_euclides(a, n)
    return s % n


def generar_clave(largo: int):
    """
    Argumentos :
        go: int - largo de las claves a ser generadas
    Retorna :
        genera una clave privada (d, N) y una clave publica (e, N) tales
        que d, e y N tienen al menos l digitos . La clave privada debe
        ser almacenada en un archivo private_key .txt en el formato :
        d
        N
        La clave publica debe ser almacenada de la misma forma en
        en un archivo public_key .txt
    """

    P = generar_primo(largo // 2 + 1)
    Q = generar_primo(largo // 2 + 1)
    N = P * Q
    Phi = (P - 1) * (Q - 1)
    d = random.randint(1, N - 1)

    while (mcd(d, Phi) > 1):
        d = random.randint(1, N - 1)

    e = inverso(d, Phi)

    f = open("private_key.txt", "w")
    f.write(str(d) + "\n" + str(N))
    f.close()
    f = open("public_key.txt", "w")
    f.write(str(e) + "\n" + str(N))
    f.close()


def exp_mod_file(m: int, name: str) -> int:
    """
    Argumentos :
        m: int
        name: str - nombre del archivo con exponente s y modulo n
    Retorna :
        int: (m**s) % n
    """

    file = open(name, "r")
    s = int(file.readline())
    n = int(file.readline())
    file.close()
    return(exp_mod(m, s, n))


def enc(m: int) -> int:
    """
    Argumentos :
        m: int
    Retorna :
        int: cifrado de m de acuerdo con la clave publica almacenada
        en public_key.txt
    """
    return exp_mod_file(m, "public_key.txt")


def dec(m: int) -> int:
    """
    Argumentos :
        m: int
    Retorna :
        int: descifrado de m de acuerdo con la clave privada
        almacenada en private_key.txt
    """
    return exp_mod_file(m, "private_key.txt")


if __name__ == "__main__":
    generar_clave(600)
