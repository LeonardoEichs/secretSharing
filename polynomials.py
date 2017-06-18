def print_polynomial(values_list):
    polynomial = ""
    for i in range(len(values_list)):
        polynomial += str(values_list[i]) + "x^" + str(i) + " + "
    print polynomial[:-2]
