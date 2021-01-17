import numpy
from PIL import Image, ImageDraw

from measurements import *
from projection_functions import *
import scipy.optimize


def _calculate_projection_parameters_lsq(measurements):
    N = len(measurements)

    real_world, screen = zip(*measurements)

    C = numpy.matrix(real_world)
    # Add extra column with ones to indicate constant offset
    C = numpy.hstack([C, numpy.ones((N,1))])
    P = numpy.matrix(screen)

    # least square
    M = numpy.linalg.lstsq(C, P, rcond=None)
    M = M[0]

    return M[0,0], M[1,0], M[2,0], M[0,1], M[1,1], M[2,1]

def _calculate_projection_parameters_fit(measurements):

    real_world, screen = zip(*measurements)

    real_world = numpy.vstack(real_world)
    screen = numpy.vstack(screen)
    screen = linearize_screen_coordinates(screen)

    p0 = 2, 0, 0, 0, 2, 0, 0, 0, 2, 1, 4, 8
    p, cov = scipy.optimize.curve_fit(project_to_screen_with_perspective_multi, real_world, screen, p0)

    return p

# calibration_measurements = [front_leg_right, front_leg_left, back_leg, back_rest_right]
calibration_measurements = [a, b, c, d, e, f, g]*2

parameters = _calculate_projection_parameters_lsq(calibration_measurements)

parameters = _calculate_projection_parameters_fit(calibration_measurements)


real_world, screen = zip(*calibration_measurements)
real_world = numpy.vstack(real_world)
screen = numpy.vstack(screen)
linear_screen = project_to_screen_with_perspective_multi(real_world, *parameters)
linear_screen = numpy.reshape(linear_screen, (len(calibration_measurements), 2))
print(screen)
print(linear_screen)


# numpy.save("projection_matrix.npy", M, allow_pickle=False)

with Image.open("led_doosje.png") as im:
    
    draw = ImageDraw.Draw(im)
    for x,y in linear_screen:

        draw.line([(x, y-5), (x, y+5)], fill="#00FF00", width=1)
        draw.line([(x-5, y), (x+5, y)], fill="#00FF00", width=1)

    # write to stdout
    im.save("led_doosje_calibration.png")

