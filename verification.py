import numpy
from PIL import Image, ImageDraw

from measurements import *

def _project_to_laser(M, x, y, z):
    result =  numpy.matrix([x, y, z, 1]) @ M
    return numpy.asarray(result[:,]).reshape(-1)

verification_measurements = [back_rest_left, seat]

M = numpy.load("projection_matrix.npy")

with Image.open("stoel_met_coordinaten.png") as im:
    
    draw = ImageDraw.Draw(im)
    for real_world, screen in verification_measurements:

        calibrated = _project_to_laser(M, *real_world)
        x = int(calibrated[0])
        y = int(calibrated[1])
        
        draw.line([(x, y-5), (x, y+5)], fill="#00FF00", width=1)
        draw.line([(x-5, y), (x+5, y)], fill="#00FF00", width=1)

    # write to stdout
    im.save("stoel_met_coordinaten_verification.png")

