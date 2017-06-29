import sys, math, random
from operator import mul
import primes

class AsmuthBloom():
    def __init__(self):
        pass

    @classmethod
    def _extendedEuclid(cls, a,b):
        ''' Executes the extended Euclid algorithm  '''
    	if b==0:
    		return (a,1,0)
    	tPrime = AsmuthBloom._extendedEuclid(b,a % b)
    	return [tPrime[0], tPrime[2], (tPrime[1] - (a//b) * tPrime[2])]

    @classmethod
    def _chineseRemainder(cls, N,a,n):
        ''' Executes the Chinese Remainder Theorem  '''
    	N = int(N)
    	prod_n = reduce(mul, n)
    	p = list()
    	for i in xrange(0,N):
    		p.append(prod_n//n[i])
    	t = list()
    	for i in xrange(0,N):
    		t.append((AsmuthBloom._extendedEuclid(p[i],n[i])[1]) % n[i])
    	A = 0
    	for i in xrange(0,N):
    		A += a[i] * t[i] * p[i]
    	A = A % prod_n
    	return	A

    @classmethod
    def generate_shares(cls, secret, n, k):
        ''' Create the shares  '''
        print "Criando parcelas..."
        print "------------------ENTRADAS------------------"
        print "S", secret
        print "n", n
        print "k", k
        print "--------------------------------------------"
        # Escolhe o proximo primo depois do segredo,
        # obedecendo que m0 eh um primo e m0 > d
    	m = primes.generatePrimesList(secret, 1)
        # Eh gerado uma lista m de tamanho n contendo uma
        # sequencia de numeros primos onde m0 < m1 < ... < mn
    	for x in primes.generatePrimesList(m[0]*3,n):
    		m.append(x)
        print 'm', m
        # Faz o produtorio para descobrir m1 ... mk
        mdash = m[1:k+1]
    	mi = reduce(mul, mdash)
        # Faz o produtorio para descobrir m0 * mn-k+2 ... mn
        mdash = m[k+1:n+1]
    	mk = m[0] * reduce(mul, mdash)
        # Faz o teste para ver se eh valido
        # if mi > mk:
        # 	print 'Success'
        # else:
        # 	print 'Condition failed'
        assert mi > mk, "Condition failed"
        M = reduce(mul, m)
    	y = secret
        bit_l = max(m).bit_length()
        # Cria um "a" que com certeza ira formar um S + a*m0 maior
        # que qualquer elemento m.
        # Isso eh garantido gerando um "a" maior que o maior
        # elemento de m
        while(True):
          a = int(random.random()*100)
          print 'a: ',a
          # Aplicacao de formula
          y = secret + a*m[0]
          if y < 0 or y > M:
            pass
          else:
            break
    	Y = list()
    	for x in xrange(1,n+1):
    		yi = y % m[x]
            # Cada y eh colocado em uma lista
    		Y.append(yi)
        # Lista de m1 ate mn
        M = m[1:]
        # Junta listas Y e M
        shares = zip(Y, M)
        print 'shares', shares
        return m[0], shares

    @classmethod
    def reconstruct(cls, m0, shares):
        ''' Receives the shares to
        reconstruct the secret  '''
        print "Reconstruindo segredos..."
        print "------------------ENTRADAS------------------"
        print "shares", shares
        print "--------------------------------------------"
        y, m = zip(*shares)
        # Ms eh o produtorio de todos os m
    	Ms = reduce(mul, m)
        # Chinese Remainder Theorem para resolver o sistema
    	yp = AsmuthBloom._chineseRemainder(len(y), y, m)
        # Eh tirado o modulo do resultado
    	d = (yp % m0)
    	print 'secret: ', d

m0, shares = AsmuthBloom.generate_shares(12, 5, 3)
AsmuthBloom.reconstruct(m0, shares[:4])
