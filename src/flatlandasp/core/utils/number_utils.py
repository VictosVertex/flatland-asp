def roll_bits(number: int):
    ret = 0
    for i in range(4):
        incoming = (number >> (12-4*i)) & 0xF
        nr = ((incoming & 0b1) << 3) + (incoming >> 1)
        ret = (ret << 4) + nr if i < 3 else (nr << 12) + ret
    return ret


def n_roll_bits(number: int, count: int):
    ret = number
    for _ in range(count):
        ret = roll_bits(ret)
    return ret
