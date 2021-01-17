import math

import numpy
from PIL import Image, ImageDraw, ImageFont

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
    flattened_screen = flatten_screen_coordinates(screen)

    p0 = [1]*12
    flattened_projection = lambda *args : flatten_screen_coordinates(project_to_screen_with_perspective_multi(*args)) 
    p, cov = scipy.optimize.curve_fit(flattened_projection, real_world, flattened_screen, p0)

    return p

def _calibrate(calibration_measurements):
    parameters = _calculate_projection_parameters_fit(calibration_measurements*2)

    real_world, screen = zip(*calibration_measurements)
    real_world = numpy.vstack(real_world)
    screen = numpy.vstack(screen)
    linear_screen = project_to_screen_with_perspective_multi(real_world, *parameters)
    linear_screen = numpy.reshape(linear_screen, (len(calibration_measurements), 2))
    print(screen)
    print(linear_screen)
    print(numpy.max(numpy.sqrt(numpy.sum(numpy.power(screen-linear_screen, 2), axis=1))))
    return parameters

def _evaluate_and_write_result(filename_base, filename_postfix, M, measurements):
    print(f"Evaluation for {filename_postfix}")

    for world, screen in measurements:
        x, y = project_to_screen_with_perspective(*world, M)
        
        dx = x - screen[0]
        dy = y - screen[1]
        residual = math.sqrt(dx**2+dy**2)
        print(f"({screen[0]}, {screen[1]}) ==> ({x}, {y}) ; ||.|| = {residual}")

    if filename is not None:
        with Image.open(f"{filename_base}.png") as im:
        
            draw = ImageDraw.Draw(im)
            for world, screen in measurements:
                x, y = project_to_screen_with_perspective(*world, M)
                draw.line([(x, y-5), (x, y+5)], fill="#00FF00", width=1)
                draw.line([(x-5, y), (x+5, y)], fill="#00FF00", width=1)

            # write to stdout
            im.save(f"{filename_base}_{filename_postfix}.png")

# 3D geprint doosje
calibration_measurements = doosje_allemaal[:-1]
verification_measurements = doosje_allemaal[-1:]
filename = "led_doosje"

# # Stoel
# calibration_measurements = stoel_allemaal
# verification_measurements = stoel_allemaal
# filename = "stoel_met_coordinaten"

# # Zelf bedachte coordinaten
# calibration_measurements = perspectief_allemaal
# verification_measurements = perspectief_allemaal
# filename = None

# parameters = _calculate_projection_parameters_lsq(calibration_measurements)

parameters = _calibrate(calibration_measurements)
M = ensure_matrix(*parameters)
_evaluate_and_write_result(filename, 'calibration', M, calibration_measurements)
_evaluate_and_write_result(filename, 'verification', M, verification_measurements)


