import random
def gen_new_data():
    x = []
    y = []
    for i in range(10):
        x.append(random.randint(0,100))
        y.append(random.randint(0,100))
    return x, y

print(gen_new_data())