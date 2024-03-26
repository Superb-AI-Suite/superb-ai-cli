def print_table(
    data
):
    longest_cols = [
        (max([len(str(row[i])) for row in data]) + 3)
        for i in range(len(data[0]))
    ]
    row_format = "".join(
        [
            "{:<" + str(longest_col) + "}"
            for longest_col in longest_cols
        ]
    )
    for row in data:
        print(row_format.format(*row))


__all__ = (
    "print_table",
)
