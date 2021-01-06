import numpy
from PIL import Image, ImageDraw

from measurements import *

def _project_to_laser(M, x, y, z):
    result =  numpy.matrix([x, y, z, 1]) @ M
    return numpy.asarray(result[:,]).reshape(-1)

# verification_measurements = [back_rest_left, seat]
verification_measurements = [a, b, c, d, e, f, g]

M = numpy.load("projection_matrix.npy")

with Image.open("led_doosje.png") as im:
    
    draw = ImageDraw.Draw(im)
    for real_world, screen in verification_measurements:


        calibrated = _project_to_laser(M, *real_world)
        x = int(calibrated[0])
        y = int(calibrated[1])

        print(f"{real_world}, {screen}, {x},{y}")

        offset = 50
        draw.line([(x, y-offset), (x, y+offset)], fill="#00FF00", width=3)
        draw.line([(x-offset, y), (x+offset, y)], fill="#00FF00", width=3)

    # write to stdout
    im.save("led_doosje_verification.png")

