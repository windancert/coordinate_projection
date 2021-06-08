
from projection_functions import project_to_screen_with_perspective
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy

def plot_measurement_with_evaluation(measurement, M, block=False):
    world_coordinates = [m[0] for m in measurement]
    projected = [project_to_screen_with_perspective(*world, M) for world in world_coordinates]
    plot_measurement(zip(world_coordinates, projected), block)

def plot_measurement(measurements, block=False):
    real_world, screen = zip(*measurements)
    real_world = numpy.vstack(real_world)
    screen     = numpy.vstack(screen)

    X = numpy.zeros(len(real_world))
    Y = numpy.zeros(len(real_world))
    Z = numpy.zeros(len(real_world))
    for i, rw in enumerate(real_world):
        X[i] = rw[0]
        Y[i] = rw[1]
        Z[i] = rw[2]

    Sx = numpy.zeros(len(screen))
    Sy = numpy.zeros(len(screen))

    for i,sc in enumerate(screen):
        Sx[i] = sc[0]
        Sy[i] = sc[1]
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(211, projection='3d')
    ax1.scatter(X, Y, Z, zdir='z', c= 'red')
    for i in range(len(X)):
        ax1.text(X[i], Y[i], Z[i], i)
    ax2 = fig1.add_subplot(212)
    ax2.scatter(Sx, Sy, c='green')
    for i in range(len(Sx)):
        #ax2.annotate(i, (Sx[i], Sx[i]))
        ax2.text(Sx[i], Sy[i], i)
    if block:
        plt.show()
