import sys
import random
from sharing import Shamir

def Shamir_test_case(n):
    print "################# TEST CASE " + str(n) + " #################"
    S = random.randint(1, 9999)
    n = random.randint(2, 15)
    k = random.randint(2, n)
    print "S = " + str(S)
    print "n = " + str(n)
    print "k = " + str(k)
    points = Shamir.split_secret(S, int(n), int(k))
    print points
    for i in range(2, n + 1):
        print str(i) + " point(s)"
        secret = Shamir.reconstruct_secret(points[:i])
        if (secret == S):
            print '\033[92m' + "[SUCCESS]" + '\033[0m'
            print secret
            break
        else:
            print '\033[91m' + "[FAIL]" + '\033[0m'

for i in range(1, 2):
    Shamir_test_case(i)
