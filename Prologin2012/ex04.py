import sys

def aiJePerdu(N, capacites):
    max_n = capacites[0]*2
    def stupide(s):
        n = 0
        for i in capacites:
            while i <= s:
                s -= i
                n += 1            
        return n
        
    def intelligent(s):
        def rec(m, best, curr, dept=0):
            if curr >= best:
                return best
            elif m == 0:
                return curr
            else:
                for i in capacites:
                    if i <= m:
                        best = rec(m-i, best, curr+1, dept+1)

                return best
                
        return rec(s, max_n, 0)
    
    for i in xrange(0, max_n):
        if stupide(i) != intelligent(i):
            return 1
    return 0
    

if __name__ == '__main__':
    N = int(raw_input())
    capacites = [int(i) for i in raw_input().split(' ')]

    print aiJePerdu(N, capacites)