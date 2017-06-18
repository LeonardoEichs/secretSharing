import random
import math
import polynomials
import operator

class SecretSharer():
    def __init__(self):
        pass

    @classmethod
    def split_secret(cls, secret_string, num_shares, share_threshold, bits = None):
        ''' You should call the program as:
            SecretSharer.split_secret(S, n, k, b)
            Where:
            S = secret
            n = number of shares
            k = min number of shares to reconstruct S
            b = order of bits (optional, if not provided will use the number of bits in S) '''
        if (bits != None):
            bits = int(bits)
        else:
            bits = int(secret_string).bit_length()
        secret_int = int(secret_string)
        num_shares = int(num_shares)
        share_threshold = int(share_threshold)
        rndm_nmbs = SecretSharer.crt_rndm_nmb(share_threshold - 1, bits)
        polyn = [secret_int] + rndm_nmbs
        polynomials.print_polynomial(polyn)
        points = zip(range(1, num_shares + 1), SecretSharer.make_points(polyn, num_shares))
        print points
        return points

    @classmethod
    def interpolate(cls, x, x_values, y_values):
        def _basis(j):
            p = [(x - x_values[m])/(x_values[j] - x_values[m]) for m in xrange(k) if m != j]
            return reduce(operator.mul, p)
        assert len(x_values) != 0 and (len(x_values) == len(y_values)), 'x and y cannot be empty and must have the same length'
        k = len(x_values)
        return sum(_basis(j)*y_values[j] for j in xrange(k))

    @classmethod
    def reconstruct_secret(cls, points):
        x_points, y_points = zip(*points)
        print x_points
        print y_points
        print SecretSharer.interpolate(0, x_points, y_points)

    @classmethod
    def crt_rndm_nmb(cls, m, bits):
        rndm_nmbs = []
        for i in range(m):
            rndm_nmbs.append(random.getrandbits(bits))
        #rndm_nmbs = [int(x) for x in rndm_nmbs] equivalent to:
        rndm_nmbs = map(int, rndm_nmbs) # more concise
        return rndm_nmbs

    @classmethod
    def make_points(cls, polynomial, num_shares):
        points = []
        for i in range(1, num_shares + 1):
            point = 0
            for j in range(len(polynomial)):
                point += polynomial[j] * math.pow(i, j)
            points.append(point)
        points = map(int, points)
        return points
