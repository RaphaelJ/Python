import sys


def estEligible(D, M, Y):
    return int(Y > 1991 or (Y == 1991 and M >= 5))


if __name__ == '__main__':
    D = int(raw_input())
    M = int(raw_input())
    Y = int(raw_input())

    print (estEligible(D, M, Y))