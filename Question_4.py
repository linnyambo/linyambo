def product_of_multiples(factor, limit):
    product = 1

    for num in range(factor, limit, factor):
        product *= num

    return product


result = product_of_multiples(3, 10)
print(result)
