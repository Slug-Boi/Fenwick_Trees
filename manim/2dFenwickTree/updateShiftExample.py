while row <= max_rows:
    loop_col = col 
    while loop_col <= max_cols:
        BIT[row][loop_col] += val
        loop_col += (loop_col & -loop_col)
    row += (row & -row)