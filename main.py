# https://github.com/stevenlovegrove/Pangolin/tree/master/examples/HelloPangolin

import OpenGL.GL as gl
import pangolin
from PIL import Image
import numpy as np

focalLength = 750
centerX = 640
centerY = 380
scalingFactor = .800

def getPointsAndColors(file):
    """
    Projects the points of the RGB image into 3d.
    This function returns the points, the colors of the points and the semantic segmentation of the points

    :param file: the file name in data
    :return: returns 3 numpy arrays of the same size.
             The first array contains the points, the second one contains the color of the points and the third one
             contains the semantic segmentation of the points

    example usage:

    points, colors, sem = getPointsAndColors("000020.png")
    """
    rgb = Image.open("data/RGB_" + file)
    depth = Image.open("data/DEPTH_" + file)
    semantic =  Image.open("data/SEM_" + file)

    points = []
    colors = []
    sem = []

    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):
            colors.append(np.array(rgb.getpixel((u, v))) / 255)
            sem.append(np.array(semantic.getpixel((u, v))[:3]) / 255)

            # print(depth.getpixel((u, v)))
            Z = depth.getpixel((u, v))[0] * scalingFactor
            #if Z == 0: continue
            X = (u - centerX) * Z / focalLength
            Y = (v - centerY) * Z / focalLength
            points.append((X,Y,Z))

    return np.array(points), np.array(colors), np.array(sem)

def main(showSemSegmentation=False):
    # create window
    pangolin.CreateWindowAndBind('Main', 640, 480)
    gl.glEnable(gl.GL_DEPTH_TEST)

    # Define Projection and initial ModelView matrix
    scam = pangolin.OpenGlRenderState(
        pangolin.ProjectionMatrix(640, 480, -420, -420, 320, 240, 0.2, 50),
        pangolin.ModelViewLookAt(0, 0, -.01, 0, 0, 0, pangolin.AxisDirection.AxisY))
    handler = pangolin.Handler3D(scam)

    # Create Interactive View in window
    dcam = pangolin.CreateDisplay()
    dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0 / 480.0)
    dcam.SetHandler(handler)
    points, colors, sem = getPointsAndColors("000020.png")

    # If we want to show the semantic segmentations
    if showSemSegmentation:
        colors = colors * 0.5 + sem * 0.5

    while not pangolin.ShouldQuit():
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        dcam.Activate(scam)

        gl.glPointSize(2)
        gl.glColor3f(1.0, 0.0, 0.0)

        # access numpy array directly(without copying data), array should be contiguous.
        pangolin.DrawPoints(points, colors)
        pangolin.FinishFrame()

if __name__ == '__main__':
    main(showSemSegmentation=True)
