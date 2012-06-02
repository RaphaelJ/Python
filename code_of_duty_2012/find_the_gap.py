def find_the_gap (M, N, R):
    operateurs = list(R)
    
    ma = 0
    for nombres in listes(0, M, N):
        possibles = [False] * 170 # Maximum = (8+9) * 10 / 1 = 170
        for perm in permutations(nombres):
            gap(possibles, perm, operateurs)
            
        for i in range(1, 171):
            if not possibles[i-1]:
                if i > ma:
                    ma = i
                break
    return ma
    
def permutations(l):
    if l == []:
        yield []
    else:
        for i, v in enumerate(l):
            for sub in permutations(l[:i] + l[i+1:]):
                yield [v] + sub
    
def listes(Mi, Ma, N):
    """ Liste les listes des nombres possibles entre ]Mi, Ma] """
    if N == 0:
        yield []
    elif Ma - Mi < N:
        yield None
    else:
        # Avec Mi + 1
        for reste in listes(Mi + 1, Ma, N - 1):
            if reste != None:
                yield [Mi + 1] + reste
                
        # Sans Mi + 1
        for reste in listes(Mi + 1, Ma, N):
            if reste != None:
                yield reste
                
def gap(possibles, nombres, operateurs, operandes=[], s=""):
    """ 
        Teste toutes les combinaisons d'expression en utilisant la syntaxe
        polonaise inversée
    """
    if len(operandes) == 1:
        #if not possibles[operandes[0]-1]:
            possibles[operandes[0]-1] = True
            #print (operandes[0], "=", s)

    def supr_liste(liste, item):
        return [ i for i in liste if i != item ]

    if len(operandes) >= 2:
        op1 = operandes[-2]
        op2 = operandes[-1]
        
        def peut_diviser(o1, o2):
            return o1 % o2 == 0
            
        def peut_soustraire():
            return op1 - op2 >= 0 # Positifs ou positifs + nuls ?
        
        supr_op = lambda o: supr_liste(operateurs, o)

        for o in operateurs:                
            if o == '/':
                if peut_diviser(op1, op2):
                    gap(
                        possibles, nombres, supr_op('/'), 
                        operandes[:-2] + [op1/op2], s + ' /'
                    )
                #elif peut_diviser(op2, op1):
                    #gap(
                        #possibles, nombres, supr_op('/'), 
                        #operandes[:-2] + [op2/op1]
                    #)
            elif o == '−' or o == '-':
                if peut_soustraire():
                    gap(
                        possibles, nombres, supr_op('-'), 
                        operandes[:-2] + [op1-op2], s + ' -'
                    )
                #else:
                    #gap(
                        #possibles, nombres, supr_op('-'), 
                        #operandes[:-2] + [op2-op1]
                    #)
            elif o == '+':
                gap(
                    possibles, nombres, supr_op('+'),
                    operandes[:-2] + [op1+op2], s + ' +'
                )
            elif o == '*':
                gap(
                    possibles, nombres, supr_op('*'), 
                    operandes[:-2] + [op1*op2], s + ' *'
                )
            elif o == '%':
                gap(
                    possibles, nombres, supr_op('%'), 
                    operandes[:-2] + [op1%op2], s + ' %'
                )
    
    if nombres != []:
        gap(
            possibles, nombres[1:], operateurs, operandes + [nombres[0]],
            s + ' ' + str(nombres[0])
        )
        gap(possibles, nombres[1:], operateurs, operandes, s)

print (find_the_gap(5, 2, "+ * −"))

#possibles = [False] * 170 # Maximum = (8+9) * 10 / 1 = 170
#for perm in permutations([1, 3]):
    #gap(possibles, perm, ['+', '-', '*'])
    
#for i in range(1, 171):
    #if not possibles[i-1]:
        #print (i)
        #break