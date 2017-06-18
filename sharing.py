import random
import math
import operator

def print_polynomial(values_list):
    ''' Prints a list in the format of a polynomial,
        the first value is the x^0 '''
    polynomial = ""
    for i in range(len(values_list)):
        polynomial += str(values_list[i]) + "x^" + str(i) + " + "
    print polynomial[:-2]

class Shamir():
    def __init__(self):
        pass

    @classmethod
    def split_secret(cls, secret_string, num_shares, share_threshold, bits = None):
        ''' You should call the program as:
            Shamir.split_secret(S, n, k, b)
            Where:
            S = secret
            n = number of shares
            k = min number of shares to reconstruct S
            b = order of bits (optional, if not provided will use the number of bits in S) '''
        # S = secret_string
        # n = num_shares
        # k = share_threshold

        # Caso o usuario nao especifique um numero de bits o programa usa
        # automaticamente como limite de tamanho nos numeros aleatorios
        # uma quantidade de bits igual a do segredo
        if (bits != None):
            bits = int(bits)
        else:
            bits = int(secret_string).bit_length()
        secret_int = int(secret_string)
        num_shares = int(num_shares)
        share_threshold = int(share_threshold)
        # Chama uma funcao que cria uma lista de k - 1 numeros aleatorios
        rndm_nmbs = Shamir.crt_rndm_nmb(share_threshold - 1, bits)
        # Polinomio eh igual [S, aleat0, aleat1, ...]
        polyn = [secret_int] + rndm_nmbs
        # Imprime o polinomio, apenas para visualizacao do usuario
        print_polynomial(polyn)
        # Cria as chaves em um formato (x, y)
        # A funcao make_points eh responsavel por criar os pontos com base
        # no polinomio
        shares = zip(range(1, num_shares + 1), Shamir.make_points(polyn, num_shares))
        return shares

    @classmethod
    def interpolate(cls, x_values, y_values):
        ''' Lagrange interpolation, following an computationally
            efficient approach.'''
        x_values = map(float, x_values)
        y_values = map(float, y_values)
        def _basis(j):
            # A formula usada aqui dispensa o uso de x, pois iremos
            # interpolar a funcao para 0
            p = [(x_values[m])/(x_values[m] - x_values[j]) for m in xrange(k) if m != j]
            return reduce(operator.mul, p)
        # Mensagem de erro caso parametros estejam incorretos
        assert len(x_values) != 0 and (len(x_values) == len(y_values)), 'x e y nao podem ser vazios e devem ter o mesmo tamanho'
        k = len(x_values)
        # Realiza o somatorio dos valores
        return int(math.ceil((sum(_basis(j)*y_values[j] for j in xrange(k)))))

    @classmethod
    def reconstruct_secret(cls, points):
        ''' Reconstrct secret based on input points,
            if not enough points are given the returned
            value will be wrong. '''
        x_points, y_points = zip(*points)
        return Shamir.interpolate(x_points, y_points)

    @classmethod
    def crt_rndm_nmb(cls, m, bits):
        ''' Create a list of m random numbers
        with a size constraint of a specified number
        of bits '''
        rndm_nmbs = []
        for i in range(m):
            # Coloca na lista o numero aleatorio gerado
            rndm_nmbs.append(random.getrandbits(bits))
        #rndm_nmbs = [int(x) for x in rndm_nmbs] equivalent to:
        rndm_nmbs = map(int, rndm_nmbs) # more concise
        return rndm_nmbs

    @classmethod
    def make_points(cls, polynomial, num_shares):
        ''' Create a list of points by replacing the x
            of the polynomial by a number.
            This number ranges from 1 to num_shares '''
        points = []
        for i in range(1, num_shares + 1):
            # Reseta valor do ponto
            point = 0
            # Somatorio do valor de cada membro do polinomio
            point = sum(polynomial[j] * math.pow(i, j) for j in range(len(polynomial)))
            # Coloca ponto na lista
            points.append(point)
        points = map(int, points)
        return points
