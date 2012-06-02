# -*- coding: Utf-8 -*-

def banner(C, revenu):
    """ Complexité temporelle : n * m * n * (m / 2) """
    
    rows, cols = len(C), len(C[0])
    
    """ 
        Calcule une image intégrale permettant de rapidement effectuer
        des sommes sur les rentabilités des rectangles de la carte.
    """
    iimg = [ [0] * (cols + 1) for y in xrange(0, rows + 1) ]
    
    for y in xrange(1, rows + 1):
        for x in xrange(1, cols + 1):
            iimg[y][x] = (revenu - C[y-1][x-1]) + iimg[y][x-1] \
                       + iimg[y-1][x] - iimg[y-1][x-1]
            #print iimg[y][x],
        #print
    
    def somme_rectangle(x, y, w, h):
        return iimg[y+h][x+w] - iimg[y][x+w] - iimg[y+h][x] + iimg[x][y]
        
    def somme_rectangle_cylindre(x, y, w, h):
        if x + w > cols:
            premier_rect_w = cols - x
            second_rect_w = (x + w) % cols
            
            return somme_rectangle(x, y, premier_rect_w, h) \
                 + somme_rectangle(0, y, second_rect_w, h)
        else:
            return somme_rectangle(x, y, w, h)
        
    def rectangles():
        """ Génère tous les rectangles de la carte """
        for y in xrange(0, rows):
            for x in xrange(0, cols):
                for h in xrange(1, rows - y + 1):
                    for w in xrange(1, cols + 1):
                        yield x, y, w, h
                        
    def rectangles_rentabilites():
        """ 
            Génère la rentabilité et la surface de tous les rectangles de la
            carte.
        """
        for x, y, w, h in rectangles():
            yield somme_rectangle_cylindre(x, y, w, h), w * h, (x, y, w, h)
        
    meilleur = (0, 0) # (rentabilité, surface)
    for r, s, rect in rectangles_rentabilites():
        if r > meilleur[0] or (r == meilleur[0] and s < meilleur[1]):
            #print rect, r, s
            meilleur = (r, s)
            
    return meilleur[1]
    
carte = [
    [2, 2, 2, 2],
    [1, 1, 3, 1],
    [2, 1, 3, 2]
]
print (banner(carte, 2))