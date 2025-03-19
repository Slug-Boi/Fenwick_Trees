while x <= matrix_size:
    loop_y = y 
    while loop_y <= matrix_size:
        BIT[x][loop_y] += val
        loop_y += (loop_y & -loop_y)
    x += (x & -x)