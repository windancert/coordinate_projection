import json
import math

import numpy
from PIL import Image, ImageDraw, ImageFont

from measurements import *
from projection_functions import *
import scipy.optimize

from plot_measurement import plot_measurement


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

def draw_coor(draw, Px, Py, str):
        draw.line([(Px, Py-1), (Px, Py+15)], fill="#00FF00", width=3)
        draw.line([(Px-15, Py), (Px+15, Py)], fill="#00FF00", width=3)
        font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf",  30)  
        draw.text((Px, Py), str, font = font, align ="left")  


def _evaluate_and_write_result(filename_base, filename_postfix, M, measurements):
    #print(f"Evaluation for {filename_postfix}")

    for world, screen in measurements:
        x, y = project_to_screen_with_perspective(*world, M)
        
        dx = x - screen[0]
        dy = y - screen[1]
        residual = math.sqrt(dx**2+dy**2)
        # print(f"({screen[0]}, {screen[1]}) ==> ({x}, {y}) ; ||.|| = {residual}")

    if filename_base is not None:
        filename = filename_base+"png"
        # with Image.open(f"{filename_base}.png") as im:
        with Image.open(filename) as im:
            draw = ImageDraw.Draw(im)
            for world, screen in measurements:
                x, y = project_to_screen_with_perspective(*world, M)
                draw_coor(draw, x , y, ""+str(x) + " " + str(y))

            test_world_coord = (90, 90, 22)
            x, y = project_to_screen_with_perspective(*test_world_coord, M)
            print("x,y : " + str(x) + " " + str(y) )
            draw_coor(draw, x , y, str(test_world_coord) +":(" +str(x) + "," + str(y)+")")

            # write to stdout
            outfile = filename_base + "_" + filename_postfix + ".png"
            # im.save(f"{filename_base}_{filename_postfix}.png")
            im.save(outfile)

# 3D geprint doosje
# calibration_measurements = doosje_allemaal[:-1]
# verification_measurements = doosje_allemaal[:]
# filename = "led_doosje"

# # Stoel
# calibration_measurements = stoel_allemaal
# verification_measurements = stoel_allemaal
# filename = "stoel_met_coordinaten"

# # Zelf bedachte coordinaten
# calibration_measurements = perspectief_allemaal
# verification_measurements = perspectief_allemaal
# filename = None

# parameters = _calculate_projection_parameters_lsq(calibration_measurements)

calibration_measurements = doosje_allemaal[:]
verification_measurements = doosje_allemaal[:]
filename = None

parameters = _calibrate(calibration_measurements)
M = ensure_matrix(*parameters)


with open("calibration_matrix.json", 'w', encoding='utf-8') as json_file:
    # mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz
    json_data = dict(zip("mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz".split(", "), parameters.tolist()))
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

with open("calibration_matrix.txt", 'w', encoding='utf-8') as data_file:
    for parameter in parameters :
        data_file.write(str(parameter) + '\n')

_evaluate_and_write_result(filename, 'calibration', M, calibration_measurements)
# _evaluate_and_write_result(filename, 'verification', M, verification_measurements)

plot_measurement(calibration_measurements)

world_coordinates = [m[0] for m in calibration_measurements]
laser = [m[1] for m in calibration_measurements]
print(world_coordinates)
projected = [project_to_screen_with_perspective(*world, M) for world in world_coordinates]
print(laser)
print(projected)

plot_measurement(zip(world_coordinates, projected), True)

