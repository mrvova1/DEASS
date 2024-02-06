import json
import base64
import math
import random

from PIL import Image, ImageDraw, ImageFont
import qrcode
from PIL import Image
from io import BytesIO
from os import listdir
from os.path import isfile, join
import os
import hashlib


def perevod(n):
    string = []
    while n > 0:
        string.append(n % 255)
        n //= 255
    string.reverse()
    return string


def shifrator(f, key1 = 'just', key2 = 'Monika', path_of_end_file='shifr.txt'):
    if len(key1) != 4:
        print('The value of the second argument must be str with a length of 4 characters')
        return None
    s = json.dumps(f)
    ss = [''.join(
        [chr(ord(s[i + ii]) + ord(key1[ii]) + ord(key2[i // 4 % len(key2)])) for ii in range(4) if i + ii < len(s)]) for
          i in range(0, len(s), 4)]
    key3 = len(s)
    img = Image.new('RGB', (math.ceil(len(ss) ** 0.5) * 2, math.ceil(len(ss) ** 0.5) * 2), 'black')
    pixels = img.load()
    width, height = img.size
    n = len(ss) + 1
    a = [i for i in range(n + 1)]
    a[1] = 0
    lst = []
    i = 2
    while i <= n:
        if a[i] != 0:
            lst.append(a[i])
            for j in range(i * 2, n + 1, i):
                a[j] = 0
        i += 1
    while lst[-1] >= len(ss):
        del lst[-1]
    postlst = [i for i in range(len(ss)) if i not in lst]
    kk = 0
    for i in lst:
        for iy in range(2):
            for ix in range(2):
                if len(ss[kk]) - 1 >= iy * 2 + ix:
                    kko = ord(ss[kk][iy * 2 + ix])
                    pr = perevod(kko)
                    pr = [0, ] * (3 - len(pr)) + pr
                    pixels[(i % (width // 2)) * 2 + ix, (i // (width // 2)) * 2 + iy] = int(pr[0]), int(pr[1]), int(
                        pr[2]), 0
        kk += 1
    for i in postlst:
        for iy in range(2):
            for ix in range(2):
                if len(ss[kk]) - 1 >= iy * 2 + ix:
                    kko = ord(ss[kk][iy * 2 + ix])
                    pr = perevod(kko)
                    pr = [0, ] * (3 - len(pr)) + pr
                    pixels[(i % (width // 2)) * 2 + ix, (i // (width // 2)) * 2 + iy] = int(pr[0]), int(pr[1]), int(
                        pr[2]), 0
        kk += 1
    img.save('test1.png')
    with open("test1.png", "rb") as image_file:
        i = image_file.read()
        encoded_string = base64.b64encode(i)
    asd = open(path_of_end_file, 'w')
    asd.write(str(encoded_string)[2:-1])
    asd.close()
    return key3


def deshifrator(encoded_string, key1, key2, key3):
    newjpgtxt = encoded_string
    b = base64.b64decode(newjpgtxt)
    im = Image.open(BytesIO(b))
    im.save('out.png')

    img = Image.open('out.png')
    pixels = img.load()
    width, height = img.size

    n = key3 // 4
    if key3 % 4 != 0:
        n += 1
    a = [i for i in range(n + 1)]
    a[1] = 0
    lst = []
    i = 2
    while i <= n:
        if a[i] != 0:
            lst.append(a[i])
            for j in range(i * 2, n + 1, i):
                a[j] = 0
        i += 1
    while lst[-1] >= n:
        del lst[-1]
    postlst = [i for i in range(n) if i not in lst]
    str4k = []
    kk = 0
    asd = ('0' * key3)
    ss = [asd[i:i+4] for i in range(0, key3, 4)]
    for i in lst:
        str4 = ''
        for iy in range(2):
            for ix in range(2):
                if len(ss[kk]) - 1 >= iy * 2 + ix:
                    p = pixels[(i % (width // 2)) * 2 + ix, (i // (width // 2)) * 2 + iy]
                    str4 += chr(p[0] * 255 ** 2 + p[1] * 255 + p[2])
        str4k.append(str4)
        kk += 1
    for i in postlst:
        str4 = ''
        for iy in range(2):
            for ix in range(2):
                if len(ss[kk]) - 1 >= iy * 2 + ix:
                    p = pixels[(i % (width // 2)) * 2 + ix, (i // (width // 2)) * 2 + iy]
                    str4 += chr(p[0] * 255 ** 2 + p[1] * 255 + p[2])
        str4k.append(str4)
        kk += 1
    str1 = ''
    for i in range(len(str4k)):
        for ii in range(len(str4k[i])):
            str1 += chr(ord(str4k[i][ii]) - ord(key1[ii % len(key1)]) - ord(key2[i % len(key2)]))
    out = json.loads(str1)
    return out


def VUShifrator(f=dict, key1=list, key2=list, kolvo=int, path='shifr.txt'):
    dd = []
    if key1 is not list:
        key1 = [key1]
    if key2 is not list:
        key2 = [key2]
    while len(key1) < kolvo:
        key1.append(key1[-1])
    while len(key2) < kolvo:
        key2.append(key2[-1])
    for i in range(kolvo):
        s = shifrator(f, key1[i], key2[i], path)
        dd.append(s)
        asd = open(path, 'r').read()
        f = asd
    return [dd, f]


def VUDeshifrator(key1=list, key2=list, key3=list):
    qrr = key3[1]
    while len(key1) < len(qrr):
        key1.append(key1[-1])
    while len(key2) < len(qrr):
        key2.append(key2[-1])
    for i in range(len(key3[0])):
        s = key3[0][-i - 1]
        d = deshifrator(qrr, key1[i], key2[i], s)
        qrr = d
    return qrr


def PS(n):
    a = [chr(i) for i in range(80)]
    b = [ord(i) for i in n]
    mib = min(b)
    mab = max(b)
    b = [chr(i) for i in range(mib, mab + 1)]
    lb = len(b)
    sni = []
    nn = [n[i:i+1000] for i in range(0, len(n), 1000)]
    for ii in nn:
        ni = ''
        s = sum([b.index(ii[i]) * (lb ** i) for i in range(len(ii))])
        while s != 0:
            ni += a[s % 80]
            s //= 80
        sni.append(ni)
    sni = chr(80).join(sni)
    return [sni, mib, mab + 1]


def autoShifrForManyFiles(name_of_begin_file, name_of_end_file):
    onlyfiles = [f for f in listdir(name_of_begin_file) if isfile(join(name_of_begin_file, f))]
    list_of_key3 = []
    if 'protected' not in os.listdir(name_of_end_file):
        os.mkdir(name_of_end_file + "/protected")
    for i in onlyfiles:
        f = open(name_of_begin_file + '/' + i).read()
        a = json.loads(f)
        if a['level'] == 1:
            s = shifrator(a['info'], a['key1'], a['key2'], name_of_end_file + '/' + i)
            # protecter_generate(open(name_of_end_file + '/' + i).read(), a['key1'], a['key2'], s, name_of_end_file + '/protected/' + i)
            protecter_generate(open(name_of_end_file + '/' + i).read(), a['key1'], a['key2'], s, name_of_end_file + '/protected/protected.txt')
            list_of_key3.append([s, name_of_end_file + '/' + i])
        else:
            s = VUShifrator(a['info'], a['key1'], a['key2'], a['level'], name_of_end_file + '/' + i)
            # protecter_generate(s[1], a['key1'], a['key2'], s[0], name_of_end_file + '/protected/' +  i)
            protecter_generate(s[1], a['key1'], a['key2'], s[0], name_of_end_file + '/protected/protected.txt' +  i)
            list_of_key3.append([s[0], name_of_end_file + '/' + i])
    f = open(name_of_end_file + '/' + 'name_key3', 'w')
    f.write(json.dumps(list_of_key3, indent=4))
    f.close()



def protecter_generate(a, k1, k2, n, file_path='poka_shto_tak.txt'):
    pr = {
        'sh': a,
        'personal_key1': k1,
        'personal_key2': k2,
        'server_key': serverKey
    }
    prd = json.dumps(pr, separators=(',', ':'))
    h = hashlib.sha512(prd.encode()).hexdigest()
    f = open(file_path, 'a')
    d = {h: n}
    f.write(json.dumps(d)[1:-1] + ',')
    f.close()


def protecter(a, k1, k2):
    s = json.loads('{' + open('poka_shto_tak.txt', 'r').read()[:-1] + '}')
    pr = {
        'sh': a,
        'personal_key1': k1,
        'personal_key2': k2,
        'server_key': serverKey
    }
    prd = json.dumps(pr, separators=(',', ':'))
    h = hashlib.sha512(prd.encode()).hexdigest()
    if h in s:
        return s[h]
    else:
        return False


def kod_segodneshnego_dna(n):
    l = ['00000000'[:7-len(str(i))] + str(i) for i in range(100000, 10000000)]
    random.shuffle(l)
    return l[:n]


serverKey = '88005553535' * 100000

# autoShifrForManyFiles('need shifr', 'suda')

# personK1 = input()
# personK2 = input()
# personKod = open(input()).read()
# print(personKod)
# d = protecter(personKod, personK1, personK2)
# if d:
#     otv = deshifrator(personKod, personK1, personK2, d)
#     print(otv)
# else:
#     print('This person is not in base')

# for i in range(1000):
#     f = open(f'need shifr/test{i}', 'w')
#     d = {
#         'key1': 'key1',
#         'key2': f'key2{i}',
#         'level': random.randint(1, 3),
#         'info': {
#             'i': i,
#             'numb': i ** 2,
#             'ladno': 'ladno' * i
#         }
#     }
#     f.write(json.dumps(d))
#     f.close()