def is_this_prime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                break
        else:
            return True

    else:
        return False


def count():
    # Initialising a count variable
    counter = 1

    for i in range(1, 101):

        # Checking if current number is a multiple of 10
        if counter % 5 == 0 and counter % 10 == 0 :
            print("ten")

        # Checking if current number is a multiple of 3
        elif counter % 3 == 0 :
            print("third")

        elif is_this_prime(i):
            print("prime")

        else:
            print(i)

        counter += 1


count()


# def counter():
#     for i in range(1, 101):
#         if i