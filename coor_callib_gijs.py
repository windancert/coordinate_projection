import json
import math
import os
import numpy
#from PIL import Image, ImageDraw, ImageFont

#from measurements import *
from projection_functions import *
import scipy.optimize


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


# def draw_coor(draw, Px, Py, str):
#         draw.line([(Px, Py-1), (Px, Py+15)], fill="#00FF00", width=3)
#         draw.line([(Px-15, Py), (Px+15, Py)], fill="#00FF00", width=3)
#         font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf",  30)  
#         draw.text((Px, Py), str, font = font, align ="left")  


# def _evaluate_and_write_result(filename_base, filename_postfix, M, measurements):
#     print(f"Evaluation for {filename_postfix}")
# 
#     for world, screen in measurements:
#         x, y = project_to_screen_with_perspective(*world, M)
#         
#         dx = x - screen[0]
#         dy = y - screen[1]
#         residual = math.sqrt(dx**2+dy**2)
#         print(f"({screen[0]}, {screen[1]}) ==> ({x}, {y}) ; ||.|| = {residual}")
# 
#     if filename is not None:
#         with Image.open(f"{filename_base}.png") as im:
#         
#             draw = ImageDraw.Draw(im)
#             for world, screen in measurements:
#                 x, y = project_to_screen_with_perspective(*world, M)
#                 draw_coor(draw, x , y, ""+str(x) + " " + str(y))
# 
#             test_world_coord = (90, 90, 22)
#             x, y = project_to_screen_with_perspective(*test_world_coord, M)
#             print("x,y : " + str(x) + " " + str(y) )
#             draw_coor(draw, x , y, str(test_world_coord) +":(" +str(x) + "," + str(y)+")")
# 
#             # write to stdout
#             im.save(f"{filename_base}_{filename_postfix}.png")


#--------------------------------

# number 0
f = open(os.getcwd()+'\data\configuration\laser\calib-raw0.json',) 
calibJson = json.load(f)
f = open(os.getcwd()+'\data\configuration\laser\CoordsBox0.json',) 
boxJson = json.load(f)
measurement_1 = (( boxJson["1"]["x"],  boxJson["1"]["y"],  boxJson["1"]["z"]), (calibJson["1"]["x"], calibJson["1"]["y"]))
measurement_2 = (( boxJson["2"]["x"],  boxJson["2"]["y"],  boxJson["2"]["z"]), (calibJson["2"]["x"], calibJson["2"]["y"]))
measurement_3 = (( boxJson["3"]["x"],  boxJson["3"]["y"],  boxJson["3"]["z"]), (calibJson["3"]["x"], calibJson["3"]["y"]))
measurement_4 = (( boxJson["4"]["x"],  boxJson["4"]["y"],  boxJson["4"]["z"]), (calibJson["4"]["x"], calibJson["4"]["y"]))
measurement_5 = (( boxJson["5"]["x"],  boxJson["5"]["y"],  boxJson["5"]["z"]), (calibJson["5"]["x"], calibJson["5"]["y"]))
measurement_6 = (( boxJson["6"]["x"],  boxJson["6"]["y"],  boxJson["6"]["z"]), (calibJson["6"]["x"], calibJson["6"]["y"]))
measurement_7 = (( boxJson["7"]["x"],  boxJson["7"]["y"],  boxJson["7"]["z"]), (calibJson["7"]["x"], calibJson["7"]["y"]))
measurement_8 = (( boxJson["8"]["x"],  boxJson["8"]["y"],  boxJson["8"]["z"]), (calibJson["8"]["x"], calibJson["8"]["y"]))
measurement_9 = (( boxJson["9"]["x"],  boxJson["9"]["y"],  boxJson["9"]["z"]), (calibJson["9"]["x"], calibJson["9"]["y"]))
measurement_10 = (( boxJson["10"]["x"],  boxJson["10"]["y"],  boxJson["10"]["z"]), (calibJson["10"]["x"], calibJson["10"]["y"]))
measurement_11 = (( boxJson["11"]["x"],  boxJson["11"]["y"],  boxJson["11"]["z"]), (calibJson["11"]["x"], calibJson["11"]["y"]))
measurement_12 = (( boxJson["12"]["x"],  boxJson["12"]["y"],  boxJson["12"]["z"]), (calibJson["12"]["x"], calibJson["12"]["y"]))
measurement_13 = (( boxJson["13"]["x"],  boxJson["13"]["y"],  boxJson["13"]["z"]), (calibJson["13"]["x"], calibJson["13"]["y"]))
measurement_14 = (( boxJson["14"]["x"],  boxJson["14"]["y"],  boxJson["14"]["z"]), (calibJson["14"]["x"], calibJson["14"]["y"]))
measurement_15 = (( boxJson["15"]["x"],  boxJson["15"]["y"],  boxJson["15"]["z"]), (calibJson["15"]["x"], calibJson["15"]["y"]))
measurement_16 = (( boxJson["16"]["x"],  boxJson["16"]["y"],  boxJson["16"]["z"]), (calibJson["16"]["x"], calibJson["16"]["y"]))
all_measurements = [measurement_1, measurement_2, measurement_3, measurement_4, measurement_5, measurement_6, measurement_7, measurement_8, measurement_9, measurement_10, measurement_11, measurement_12, measurement_13, measurement_14, measurement_15, measurement_16]
  
calibration_measurements = all_measurements[:]

parameters = _calibrate(calibration_measurements)
M = ensure_matrix(*parameters)

with open(os.getcwd()+"\data\configuration\laser\calibMatrixCalculated0.json", 'w', encoding='utf-8') as json_file:
    # mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz
    json_data = dict(zip("mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz".split(", "), parameters.tolist()))
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

# number 1
f = open(os.getcwd()+'\data\configuration\laser\calib-raw1.json',) 
calibJson = json.load(f)
f = open(os.getcwd()+'\data\configuration\laser\CoordsBox1.json',) 
boxJson = json.load(f)
measurement_1 = (( boxJson["1"]["x"],  boxJson["1"]["y"],  boxJson["1"]["z"]), (calibJson["1"]["x"], calibJson["1"]["y"]))
measurement_2 = (( boxJson["2"]["x"],  boxJson["2"]["y"],  boxJson["2"]["z"]), (calibJson["2"]["x"], calibJson["2"]["y"]))
measurement_3 = (( boxJson["3"]["x"],  boxJson["3"]["y"],  boxJson["3"]["z"]), (calibJson["3"]["x"], calibJson["3"]["y"]))
measurement_4 = (( boxJson["4"]["x"],  boxJson["4"]["y"],  boxJson["4"]["z"]), (calibJson["4"]["x"], calibJson["4"]["y"]))
measurement_5 = (( boxJson["5"]["x"],  boxJson["5"]["y"],  boxJson["5"]["z"]), (calibJson["5"]["x"], calibJson["5"]["y"]))
measurement_6 = (( boxJson["6"]["x"],  boxJson["6"]["y"],  boxJson["6"]["z"]), (calibJson["6"]["x"], calibJson["6"]["y"]))
measurement_7 = (( boxJson["7"]["x"],  boxJson["7"]["y"],  boxJson["7"]["z"]), (calibJson["7"]["x"], calibJson["7"]["y"]))
measurement_8 = (( boxJson["8"]["x"],  boxJson["8"]["y"],  boxJson["8"]["z"]), (calibJson["8"]["x"], calibJson["8"]["y"]))
measurement_9 = (( boxJson["9"]["x"],  boxJson["9"]["y"],  boxJson["9"]["z"]), (calibJson["9"]["x"], calibJson["9"]["y"]))
measurement_10 = (( boxJson["10"]["x"],  boxJson["10"]["y"],  boxJson["10"]["z"]), (calibJson["10"]["x"], calibJson["10"]["y"]))
measurement_11 = (( boxJson["11"]["x"],  boxJson["11"]["y"],  boxJson["11"]["z"]), (calibJson["11"]["x"], calibJson["11"]["y"]))
measurement_12 = (( boxJson["12"]["x"],  boxJson["12"]["y"],  boxJson["12"]["z"]), (calibJson["12"]["x"], calibJson["12"]["y"]))
measurement_13 = (( boxJson["13"]["x"],  boxJson["13"]["y"],  boxJson["13"]["z"]), (calibJson["13"]["x"], calibJson["13"]["y"]))
measurement_14 = (( boxJson["14"]["x"],  boxJson["14"]["y"],  boxJson["14"]["z"]), (calibJson["14"]["x"], calibJson["14"]["y"]))
measurement_15 = (( boxJson["15"]["x"],  boxJson["15"]["y"],  boxJson["15"]["z"]), (calibJson["15"]["x"], calibJson["15"]["y"]))
measurement_16 = (( boxJson["16"]["x"],  boxJson["16"]["y"],  boxJson["16"]["z"]), (calibJson["16"]["x"], calibJson["16"]["y"]))
all_measurements = [measurement_1, measurement_2, measurement_3, measurement_4, measurement_5, measurement_6, measurement_7, measurement_8, measurement_9, measurement_10, measurement_11, measurement_12, measurement_13, measurement_14, measurement_15, measurement_16]
  
calibration_measurements = all_measurements[:]

parameters = _calibrate(calibration_measurements)
M = ensure_matrix(*parameters)

with open(os.getcwd()+"\data\configuration\laser\calibMatrixCalculated1.json", 'w', encoding='utf-8') as json_file:
    # mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz
    json_data = dict(zip("mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz".split(", "), parameters.tolist()))
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

# number 2
f = open(os.getcwd()+'\data\configuration\laser\calib-raw2.json',) 
calibJson = json.load(f)
f = open(os.getcwd()+'\data\configuration\laser\CoordsBox2.json',) 
boxJson = json.load(f)
measurement_1 = (( boxJson["1"]["x"],  boxJson["1"]["y"],  boxJson["1"]["z"]), (calibJson["1"]["x"], calibJson["1"]["y"]))
measurement_2 = (( boxJson["2"]["x"],  boxJson["2"]["y"],  boxJson["2"]["z"]), (calibJson["2"]["x"], calibJson["2"]["y"]))
measurement_3 = (( boxJson["3"]["x"],  boxJson["3"]["y"],  boxJson["3"]["z"]), (calibJson["3"]["x"], calibJson["3"]["y"]))
measurement_4 = (( boxJson["4"]["x"],  boxJson["4"]["y"],  boxJson["4"]["z"]), (calibJson["4"]["x"], calibJson["4"]["y"]))
measurement_5 = (( boxJson["5"]["x"],  boxJson["5"]["y"],  boxJson["5"]["z"]), (calibJson["5"]["x"], calibJson["5"]["y"]))
measurement_6 = (( boxJson["6"]["x"],  boxJson["6"]["y"],  boxJson["6"]["z"]), (calibJson["6"]["x"], calibJson["6"]["y"]))
measurement_7 = (( boxJson["7"]["x"],  boxJson["7"]["y"],  boxJson["7"]["z"]), (calibJson["7"]["x"], calibJson["7"]["y"]))
measurement_8 = (( boxJson["8"]["x"],  boxJson["8"]["y"],  boxJson["8"]["z"]), (calibJson["8"]["x"], calibJson["8"]["y"]))
measurement_9 = (( boxJson["9"]["x"],  boxJson["9"]["y"],  boxJson["9"]["z"]), (calibJson["9"]["x"], calibJson["9"]["y"]))
measurement_10 = (( boxJson["10"]["x"],  boxJson["10"]["y"],  boxJson["10"]["z"]), (calibJson["10"]["x"], calibJson["10"]["y"]))
measurement_11 = (( boxJson["11"]["x"],  boxJson["11"]["y"],  boxJson["11"]["z"]), (calibJson["11"]["x"], calibJson["11"]["y"]))
measurement_12 = (( boxJson["12"]["x"],  boxJson["12"]["y"],  boxJson["12"]["z"]), (calibJson["12"]["x"], calibJson["12"]["y"]))
measurement_13 = (( boxJson["13"]["x"],  boxJson["13"]["y"],  boxJson["13"]["z"]), (calibJson["13"]["x"], calibJson["13"]["y"]))
measurement_14 = (( boxJson["14"]["x"],  boxJson["14"]["y"],  boxJson["14"]["z"]), (calibJson["14"]["x"], calibJson["14"]["y"]))
measurement_15 = (( boxJson["15"]["x"],  boxJson["15"]["y"],  boxJson["15"]["z"]), (calibJson["15"]["x"], calibJson["15"]["y"]))
measurement_16 = (( boxJson["16"]["x"],  boxJson["16"]["y"],  boxJson["16"]["z"]), (calibJson["16"]["x"], calibJson["16"]["y"]))
all_measurements = [measurement_1, measurement_2, measurement_3, measurement_4, measurement_5, measurement_6, measurement_7, measurement_8, measurement_9, measurement_10, measurement_11, measurement_12, measurement_13, measurement_14, measurement_15, measurement_16]
  
calibration_measurements = all_measurements[:]

parameters = _calibrate(calibration_measurements)
M = ensure_matrix(*parameters)

with open(os.getcwd()+"\data\configuration\laser\calibMatrixCalculated2.json", 'w', encoding='utf-8') as json_file:
    # mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz
    json_data = dict(zip("mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz".split(", "), parameters.tolist()))
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)
