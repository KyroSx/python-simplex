def is_valid_col_row(col: int, row: int) -> bool:
    if type(col) is int and type(row) is int:
        if col > 0 and row > 0:
            return True

    return False
