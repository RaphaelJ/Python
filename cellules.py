def cellules(x, y):
    avg = x // y
    rem = x % y
    prec_sum_avg_rem = 0
    for i in range(1, y+1):
        sum_avg_rem = rem * i // y
        print (avg + sum_avg_rem - prec_sum_avg_rem)
        prec_sum_avg_rem = sum_avg_rem