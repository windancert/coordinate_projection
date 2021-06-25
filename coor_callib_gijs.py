import json
import math
import os
import numpy
#from PIL import Image, ImageDraw, ImageFont

#from measurements import *
from projection_functions import *
from plot_measurement import plot_measurement_with_evaluation
import scipy.optimize

PARAMETER_LIST = ["mxx", "myx", "mzx", "mxy", "myy", "mzy", "mxz", "myz", "mzz", "tx", "ty", "tz"]

def _calculate_projection_parameters_fit(measurements, initial_guess=None):

    real_world, screen = zip(*measurements)
    real_world = numpy.vstack(real_world)
    screen = numpy.vstack(screen)
    flattened_screen = flatten_screen_coordinates(screen)

    if initial_guess is None:
        initial_guess = [1]*12

    flattened_projection = lambda *args : flatten_screen_coordinates(project_to_screen_with_perspective_multi(*args)) 
    print("real_world "+ str(real_world))
    print("screen "+ str(flattened_screen))
    p, cov = scipy.optimize.curve_fit(flattened_projection, real_world, flattened_screen, initial_guess)

    return p

def _calibrate(calibration_measurements, initial_guess=None):
    parameters = _calculate_projection_parameters_fit(calibration_measurements, initial_guess)  # there was her cal_meas*2, but I didn't understand : remove

    real_world, screen = zip(*calibration_measurements)
    real_world = numpy.vstack(real_world)
    screen = numpy.vstack(screen)
    linear_screen = project_to_screen_with_perspective_multi(real_world, *parameters)
    linear_screen = numpy.reshape(linear_screen, (len(calibration_measurements), 2))
    residual = numpy.max(numpy.sqrt(numpy.sum(numpy.power(screen-linear_screen, 2), axis=1)))
    print("residual = {}".format(residual))
    return parameters

def load_measurements_from_files(real_world_file, screen_file):
    with open(real_world_file, 'r') as f:
        real_world = json.load(f)
    with open(screen_file, 'r') as f:
        screen = json.load(f)
    indices = set(real_world.keys()).intersection(screen.keys())
    return [((real_world[i]['x'], real_world[i]['y'], real_world[i]['z']), (screen[i]['x'], screen[i]['y'])) for i in indices]

def load_initial_guess_from_file(initial_guess_file):
    with open(initial_guess_file, 'r') as f:
        initial_guess = json.load(f)
    initial = [initial_guess[k] for k in PARAMETER_LIST]
    return initial

#--------------------------------

def run_measurement_set(screen_file, real_world_file, output_file):
    all_measurements = load_measurements_from_files(os.getcwd()+real_world_file, 
                                                    os.getcwd()+screen_file)
    # GIJS : directory/file initial guess data
    # initial_guess = load_initial_guess_from_file(os.getcwd()+'\data\configuration\laser\initial_guess0.json')
    initial_guess = load_initial_guess_from_file(os.getcwd()+'\initial_guess.json')
    
    calibration_measurements = all_measurements[:]

    parameters = _calibrate(calibration_measurements, initial_guess)
    M = ensure_matrix(*parameters)

    with open(os.getcwd()+output_file+".json", 'w', encoding='utf-8') as json_file:
        # mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz
        json_data = dict(zip("mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz".split(", "), parameters.tolist()))
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    with open(os.getcwd()+output_file+".txt", 'w', encoding='utf-8') as data_file:
        for parameter in parameters :
            data_file.write(str(parameter) + '\n')

    plot_measurement_with_evaluation(calibration_measurements, M, True)

# GIJS : directory/file IN/OUT data
run_measurement_set(r'\data\2021.jun.calib-raw0.txt', r'\data\2021.jun.calib-world0.txt', r"\data\021.jun.calibMatrixCalculated0")
run_measurement_set(r'\data\2021.jun.calib-raw1.txt', r'\data\2021.jun.calib-world1.txt', r"\data\021.jun.calibMatrixCalculated1")
run_measurement_set(r'\data\2021.jun.calib-raw2.txt', r'\data\2021.jun.calib-world2.txt', r"\data\021.jun.calibMatrixCalculated2")
# run_measurement_set(r'\data\configuration\laser\calib-raw0.json', r'\data\configuration\laser\CoordsBox0.json', r"\data\configuration\laser\calibMatrixCalculated0")
# run_measurement_set(r'\data\configuration\laser\calib-raw1.json', r'\data\configuration\laser\CoordsBox1.json', r"\data\configuration\laser\calibMatrixCalculated1")
# run_measurement_set(r'\data\configuration\laser\calib-raw2.json', r'\data\configuration\laser\CoordsBox2.json', r"\data\configuration\laser\calibMatrixCalculated2")

