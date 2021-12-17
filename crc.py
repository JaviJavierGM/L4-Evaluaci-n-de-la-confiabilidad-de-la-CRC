from bitarray import bitarray
import numpy as np

success_count = 0

def cyclic_redundancy_check(filename: str, divisor: str, len_crc: int) -> int:
    """
    This function computes the CRC of a plain-text file 
    arguments:
    filename: the file containing the plain-text
    divisor: the generator polynomium
    len_crc: The number of redundant bits (r)
    """
    redundancy = len_crc * bitarray('0')
    bin_file = bitarray()

    p = bitarray(divisor)
    len_p = len(p)
    with open(filename, 'rb') as file:
        bin_file.fromfile(file)

    cw = bin_file + redundancy
    rem = cw[0 : len_p] # Residuo
    end = len(cw)
    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p
        if i < end:
            rem = rem << 1 
            rem[-1] = cw[i]

    text = bin_file + rem[len_p-len_crc : len_p]    
    return text

def error_generator(encode_text: int, n: int, r: int, seed: int) -> int:
    rng = np.random.default_rng(seed)
    begin_point = rng.integers(low = 0, high = len(encode_text)-n-1) #Inicio de la rafaga aleatoria
    fin = begin_point + n -1
    encode_text[begin_point] = not encode_text[begin_point]

    if n <= r:
        for i in range(1, n):
            begin_point += 1
            flip_coin = rng.integers(low = 0, high = 2)
            if flip_coin == 1:
                encode_text[begin_point] = not encode_text[begin_point]
    else:
        encode_text[fin] = not encode_text[fin]
        for i in range(1, n-1):
            begin_point += 1
            flip_coin = rng.integers(low = 0, high = 2)
            if flip_coin == 1:
                encode_text[begin_point] = not encode_text[begin_point]

    return encode_text


def decoder(encode_text_aux: int, divisor: str, len_crc: int) -> int:
    p = bitarray(divisor)
    len_p = len(p)
    rem = encode_text_aux[0 : len_p] # Residuo
    end = len(encode_text_aux)

    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p
        if i < end:
            rem = rem << 1 
            rem[-1] = encode_text_aux[i]

    return rem[len_p-len_crc : len_p]

def validator(rem: int) -> None:
    global success_count
    success = True
    for i in range(len(rem)):
        if rem[i] == 1:
            success_count += 1
            break

"""
Prueba del funcionamiento de la función cyclic_redundacy_check
http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
"""
div = '10011'
r = 4
n = 6
print("Processing ...")
for i in range(1000000, 1001000):
    c = cyclic_redundancy_check('test.txt', div, r)
    c = error_generator(c, n, r, i)
    rem = decoder(c, div, r)
    validator(rem)
    
print(f"\n\t\t\t   Validados: {success_count}")
print("\n\t\t---------------------------------------")
print(f"\n\t\t\t  Probability: {(success_count/1000)}")
