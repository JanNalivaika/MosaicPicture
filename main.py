import cv2
from os import listdir
from os.path import isfile, join
import cv2
import numpy as np

def decompose(inputPicture, scale_percent):

    #downscaling
    img = cv2.imread(inputPicture, cv2.IMREAD_UNCHANGED)
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim_small = (width, height)
    resized = cv2.resize(img, dim_small, interpolation = cv2.INTER_AREA)
    cv2.imwrite("scaleddown.jpg", resized)

    pixels = [list(e) for sl in resized for e in sl]


    width = int(width / scale_percent)
    height = int(height / scale_percent)
    dim = (width, height)
    resized = cv2.resize(resized, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("scaledup.jpg", resized)

    return pixels, dim_small

def analyzeInput(inputFolder):
    files = [f for f in listdir(inputFolder) if isfile(join(inputFolder, f))]
    #print(files)
    avg_pxels = []
    counter = 0

    for object in files:
        print("analzying " + str(counter) + " / " + str(len(files)) )
        src_img = cv2.imread( inputFolder + "/" + object)
        average_color_row = np.average(src_img, axis=0)
        average_color = np.average(average_color_row, axis=0)
        avg_pxels.append(list(average_color))
        counter +=1
    #print(avg_pxels)

    return avg_pxels

def findCorresponding(pixels, values):
    corresponding = []
    values = np.array(values)
    for pix in pixels:
        mean = []
        diff = values[:]-pix
        for x in diff:
            mean.append(x[0]**2 + x[1]**2 + x[2]**2)
        best = mean.index(min(mean))
        corresponding.append(best)
        pass
    return corresponding

def build(best, dims, inputFolder, DetailsInOutput):
    files = [f for f in listdir(inputFolder) if isfile(join(inputFolder, f))]
    fin = np.zeros((dims[1]*DetailsInOutput,dims[0]*DetailsInOutput,3))
    counter = 0
    zeile = 0
    spalte = 0

    for bild in best:
        Picture = inputFolder +"/"+ files[bild]
        img = cv2.imread(Picture, cv2.IMREAD_UNCHANGED)
        resized = cv2.resize(img, (DetailsInOutput, DetailsInOutput), interpolation=cv2.INTER_AREA)
        #for x in range(DetailsInOutput):
        #    for y in range(DetailsInOutput):
        #        fin[zeile+x][spalte+y] = resized[x][y]
        fin[zeile:zeile+DetailsInOutput,spalte:spalte+DetailsInOutput] = resized



        counter += 1
        spalte = counter%dims[0]*DetailsInOutput
        if spalte == 0:
            zeile += DetailsInOutput
        print(str(counter) + " / " + str(dims[0] * dims[1]))
    cv2.imwrite("Working.jpg", fin)

if __name__ == '__main__':
    inputPicture = "1.jpg"
    inputFolder = "InputFolder"
    DetailsFromOriginal = 0.03 # 1=max 0=min
    DetailsInOutput = 100 #pixel_dimension
    pixels, dims = decompose(inputPicture, DetailsFromOriginal)
    values = analyzeInput(inputFolder)
    best = findCorresponding(pixels, values)
    build(best,dims, inputFolder, DetailsInOutput)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
