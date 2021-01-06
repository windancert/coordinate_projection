import numpy
from PIL import Image, ImageDraw

from measurements import *

def _calculate_projection_matrix(measurements):
    N = len(measurements)

    real_world, screen = zip(*measurements)

    C = numpy.matrix(real_world)
    # Add extra column with ones to indicate constant offset
    C = numpy.hstack([C, numpy.ones((N,1))])
    P = numpy.matrix(screen)

    print(C)
    print(P)

    M = numpy.linalg.lstsq(C, P, rcond=None)

    print(M[0])

    return M[0]

def _project_to_laser(M, x, y, z):
    result =  numpy.matrix([x, y, z, 1]) @ M
    return numpy.asarray(result[:,]).reshape(-1)

# calibration_measurements = [front_leg_right, front_leg_left, back_leg, back_rest_right]
calibration_measurements = [a, b, c, d, e, f, g ]

M = _calculate_projection_matrix(calibration_measurements)

numpy.save("projection_matrix.npy", M, allow_pickle=False)

with Image.open("led_doosje.png") as im:
    
    draw = ImageDraw.Draw(im)
    for real_world, screen in calibration_measurements:

        calibrated = _project_to_laser(M, *real_world)
        x = int(calibrated[0])
        y = int(calibrated[1])
        
        draw.line([(x, y-5), (x, y+5)], fill="#00FF00", width=1)
        draw.line([(x-5, y), (x+5, y)], fill="#00FF00", width=1)

    # write to stdout
    im.save("led_doosje_calibration.png")

