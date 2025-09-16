from __future__ import annotations

# Bitmask optimized solver for counting solutions without storing them.

def total_n_queens(n: int) -> int:
    if n <= 0:
        return 0

    def backtrack(cols: int, d1: int, d2: int, all_ones: int) -> int:
        if cols == all_ones:
            return 1
        count = 0
        # positions available = bits that are 0 in cols|d1|d2 within lower n bits
        free = ~(cols | d1 | d2) & all_ones
        while free:
            bit = free & -free  # least significant 1-bit
            free -= bit
            count += backtrack(
                cols | bit,
                (d1 | bit) << 1 & all_ones,
                (d2 | bit) >> 1,
                all_ones,
            )
        return count

    all_ones = (1 << n) - 1
    return backtrack(0, 0, 0, all_ones)
