import numpy as np
import random
import math

def formatOutput(message, matrix):
    print("{0:17} : {1}".format(message, matrix.flatten()))


# define matrices G and H as specified in the assignment handout
G = np.array([[1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
H = np.array([[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]])
R = np.array([[0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])

# randomize 4-bit array to use as p, create x
p = np.empty((4, 1), int)
for x in range(4):
    randomNumber = round(random.random())
    p[x, 0] = randomNumber
formatOutput("Message", p)
tempx = np.matmul(G, p)
x = np.empty((7, 1), int)
for index in range(7):
     x[index, 0] = tempx[index, 0] % 2
formatOutput("Send Vector", x)


# apply an error to a random bit in x
indexToMutate = random.randint(0, 6)
if x[indexToMutate, 0] == 0:
    x[indexToMutate, 0] = 1
else:
    x[indexToMutate, 0] = 0
formatOutput("Received Message", x)


# do a parity check on x (create z)
z = np.matmul(H, x) % 2
formatOutput("Parity Check", z)

# do an error correction on the correct bit (z is in little endian order)
i = 0
sum = 0

for arrayEntry in z:
    sum += int((math.pow(2, i) * arrayEntry))
    i+=1
sum -= 1

# flip the bit of the detected error
if x[sum, 0] == 0:
    x[sum, 0] = 1
else:
    x[sum, 0] = 0

formatOutput("Corrected Message", x)

Rr = np.matmul(R, x)

formatOutput('Decoded Message', Rr)

# decode the corrected message


def main():
    x = 0

# output will look like:
# Enter number of bits: xxxx
# Message: xxxx
# Send vector: xxxx
# Received message: xxxx
# Parity Check: xxxx
# Corrected Message: xxxx
# Decoded Message: xxxx
