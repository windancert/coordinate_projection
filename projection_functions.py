import numpy

perspective_matrix = numpy.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, -1], [0, 0, 0, 0]])

def flatten_screen_coordinates(screen_coordinates_as_matrix):
    return screen_coordinates_as_matrix.flatten()

# mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mzz, tx, ty, tz
def ensure_matrix(*args):
    if (len(args) == 1) and isinstance(args[0], numpy.matrix):
        return args[0]
    else:
        M = numpy.matrix([[args[0], args[1], args[2], 0], [args[3], args[4], args[5], 0], \
            [args[6], args[7], args[8], 0], [args[9], args[10], args[11], 0]])
        return M

def convert_matrix_to_parameters(M):
    return M[0,0], M[0,1], M[0,2], M[1,0], M[1,1], M[1,2], M[2,0], M[2,1], M[2,2], M[3,0], M[3,1], M[3,2]

def project_to_screen_with_perspective(x, y, z, *args):
    M = ensure_matrix(*args)
    return _project(x, y, z, M, True)

def project_to_screen_without_perspective(x, y, z, *args):
    M = ensure_matrix(*args)
    return _project(x, y, z, M, False)

def project_to_screen_with_perspective_multi(coordinates, *args):
    M = ensure_matrix(*args)
    result = [_project(x,y,z, M, True) for x,y,z in coordinates]
    stacked = numpy.vstack(result)
    return stacked

def _project(x, y, z, M, include_perspective):
    camera_coordinates =  numpy.matrix([x, y, z, 1]) @ M
    screen_coordinates = camera_coordinates @ perspective_matrix
    screen_coordinates_as_array = numpy.asarray(screen_coordinates).reshape(-1)
    if include_perspective:
        screen_coordinates_as_array = screen_coordinates_as_array / screen_coordinates_as_array[3]
    coordinates_xy_only = screen_coordinates_as_array[:2]
    return coordinates_xy_only.tolist()

