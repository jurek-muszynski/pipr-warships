def modify_hit_input(hit_input):
    x = str.title(hit_input[0])
    x = ord(x)-65
    y = int(hit_input[1])
    return x, y
