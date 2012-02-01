import sys


def nombreDePesees(N):
    def mult3Suiv(i):
        if i % 3 == 0:
            return i
        else:
            return (i/3 + 1) * 3

    if N > 1:
        print (N)
        d = mult3Suiv(N) / 3
        return nombreDePesees(d)

if __name__ == '__main__':
    N = int(raw_input())

    nombreDePesees(N)en