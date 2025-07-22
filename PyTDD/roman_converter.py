def roman_converter(num):
    if not isinstance(num, int) or num <= 0 or num >= 4000:
        return None
    ROMAN_NUMS = [
        (1000, "M"),
        (500, "D"),
        (100, "C"),
        (50, "L"),
        (10, "X"),
        (5, "V"),
        (1, "I")
    ]
    out = ""
    for values, symbols in ROMAN_NUMS:
        while num >= values:
            out += symbols
            num -= values
    return out