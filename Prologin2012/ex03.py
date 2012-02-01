import sys
#import fractions

def pgcd(a, b):
    if a % b == 0:
        return b
    else:
        return pgcd(b, a % b)
    

def nombreDeCommandes(a, b):
    # b > a

    return b / pgcd(a, b)
    
    #n = b / a
    #inv = b - a

    #if b % a != 0: # add b
        #n += 1
    
    #print n
    #for i in xrange(inv, b + 1, inv):
        #if i % a != 0:
            #print ("n:" + str(i))
            #n += 1
    #print n        

    #for i in xrange(inv, 0, -a):
        #if i % a != 0 and i != inv:
            #print ("m:" + str(i))
            #n += 1
    
    #return n

if __name__ == '__main__':
    a = int(raw_input())
    b = int(raw_input())

    print nombreDeCommandes(a, b)