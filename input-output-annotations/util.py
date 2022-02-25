def foldl(func, acc0, list):
    acc = acc0
    for el in list:
        acc = func(el, acc)    
    return acc
