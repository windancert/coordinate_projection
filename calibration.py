import numpy
from PIL import Image, ImageDraw

from measurements import *
from perspective_project import *
import scipy.optimize


def _calculate_projection_matrix(measurements):
    N = len(measurements)

    real_world, screen = zip(*measurements)

    C = numpy.matrix(real_world)
    # Add extra column with ones to indicate constant offset
    C = numpy.hstack([C, numpy.ones((N,1))])
    P = numpy.matrix(screen)

    print(C)
    print(P)

    # least square
    M = numpy.linalg.lstsq(C, P, rcond=None)
    M = M[0]
    print('M '+ str(M))

    # curve fit nonleniar
    print ("non linuear")

    print(measurements)
    set_data(measurements)
    p0 = [M[0,0], M[0,1], 1, M[1,0], M[1,1], 1, M[2,0], M[2,1],1 , M[3,0], M[3,1], 1]
    p0 = [2,0,0, 0,1,0, 0,0,1, 0,0,0 ]
    # m11, m12, m13, m21, m22, m23, m31, m32, m33, tx, ty,tz
    popt, pcov = scipy.optimize.curve_fit(perspective_residual, numpy.zeros((N,)), numpy.zeros((N,)), p0, maxfev=26000, method='trf')

    
    print('popt '+ str(popt))



    print(perspective_residual(None,2,0,0, 0,1,0, 0,0,1, 0,0,0 ))
    print(perspective_residual(None,1,0,0, 0,1,0, 0,0,1, 0,0,0 ))


    return M[0]

def _project_to_laser(M, x, y, z):
    result =  numpy.matrix([x, y, z, 1]) @ M
    return numpy.asarray(result[:,]).reshape(-1)

# calibration_measurements = [front_leg_right, front_leg_left, back_leg, back_rest_right]
calibration_measurements = [a, b, c, d, e, f, g ]*2

M = _calculate_projection_matrix(calibration_measurements)

numpy.save("projection_matrix.npy", M, allow_pickle=False)

def draw_coor(draw, Px, Py, str):
        draw.line([(Px, Py-1), (Px, Py+15)], fill="#00FF00", width=3)
        draw.line([(Px-15, Py), (Px+15, Py)], fill="#00FF00", width=3)
        font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf",  30)  
        draw.text((Px, Py), str, font = font, align ="left")  

with Image.open("led_doosje.png") as im:
    
    draw = ImageDraw.Draw(im)
    for real_world, screen in calibration_measurements:

        calibrated = _project_to_laser(M, *real_world)
        x = int(calibrated[0])
        y = int(calibrated[1])

        draw_coor(draw, x, y, "I:"+str(real_world+str(screen)+";C:"+str(calibrated)))

    im.show()
    
    # write to stdout
    im.save("led_doosje_calibration.png")

