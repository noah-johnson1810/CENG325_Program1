import numpy as np
import random
import math


def main():
    # prompt for user input 7 4 or 15 11
    mode = input("Enter mode: ")

    # set starter variables based on that
    R = getRMatrix(mode)
    H = getHMatrix(mode)
    G = getGMatrix(mode)


    # define matrices G and H as specified in the assignment handout

    # randomize array to use as p
    p = getPMatrix(mode)

    # create x
    x = getXMatrix(mode, G, p)

    # apply an error to a random bit in x
    x = applyError(mode, x)

    # do a parity check on x (create z)
    z = getZMatrix(x, H)

    # do an error correction on the correct bit (z is in little endian order)
    x = correctMatrix(x, z)

    # decode the corrected message
    Rr = decodeMatrix(x, R)


def getGMatrix(mode):
    if mode == 'H1511':
        return np.array([[1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                         [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
    else:
        return np.array(
            [[1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def getHMatrix(mode):
    if mode == 'H1511':
        return np.array([[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                         [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]])
    else:
        return np.array([[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]])


def getRMatrix(mode):
    if mode == 'H1511':
        return np.array(
            [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
    else:
        return np.array([[0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])


def formatOutput(message, matrix):
    print("{0:17} : {1}".format(message, matrix.flatten()))


def getPMatrix(mode):
    if mode == 'H1511':
        size = 11
    else:
        size = 4
    p = np.empty((size, 1), int)
    for x in range(size):
        randomNumber = round(random.random())
        p[x, 0] = randomNumber
    formatOutput("Message", p)
    return p


def getXMatrix(mode, G, p):
    if mode == 'H1511':
        size = 15
    else:
        size = 7
    tempX = np.matmul(G, p)
    x = np.empty((size, 1), int)
    for index in range(size):
        x[index, 0] = tempX[index, 0] % 2
    formatOutput("Send Vector", x)
    return x


def applyError(mode, matrix):
    if mode == 'H1511':
        size = 15
    else:
        size = 7
    indexToMutate = random.randint(0, size - 1)
    if matrix[indexToMutate, 0] == 0:
        matrix[indexToMutate, 0] = 1
    else:
        matrix[indexToMutate, 0] = 0
    formatOutput("Received Message", matrix)
    return matrix


def getZMatrix(matrixToCheck, HMatrix):
    z = np.matmul(HMatrix, matrixToCheck) % 2
    formatOutput("Parity Check", z)
    return z


def correctMatrix(matrix, z):
    i = 0
    sum = 0
    for arrayEntry in z:
        sum += int((math.pow(2, i) * arrayEntry))
        i += 1
    sum -= 1
    # flip the bit of the detected error
    if matrix[sum, 0] == 0:
        matrix[sum, 0] = 1
    else:
        matrix[sum, 0] = 0
    formatOutput("Corrected Message", matrix)
    return matrix


def decodeMatrix(matrix, R):
    decodedMatrix = np.matmul(R, matrix)
    formatOutput('Decoded Message', decodedMatrix)
    return decodedMatrix


main()
