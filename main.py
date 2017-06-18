import sys
from sharing import SecretSharer


S = sys.argv[1]
n = sys.argv[2]
k = sys.argv[3]
b = sys.argv[4]
print "S = " + S
print "n = " + n
print "k = " + k
print "b = " + str(b)
points = SecretSharer.split_secret(S, int(n), int(k), b)
SecretSharer.reconstruct_secret(points[:3])
