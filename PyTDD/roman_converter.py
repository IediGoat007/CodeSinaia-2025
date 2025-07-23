def roman_converter(num):
<<<<<<< HEAD
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
=======
    if not isinstance(num, int):
        return None
    
    if num <= 0 or num >= 4000:
        return None
    
    ROMAN_NUMS = [
        (1, "I")
    ]

    out = ''
    while num >= 5:
        out += 'V'
        num -= 5
    while num >= 1:
        out += 'I'
        num -= 1

>>>>>>> 9acbaf18bb99f7d6895d8d125fdfcba3807b2a33
    return out