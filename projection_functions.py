import numpy

perspective_matrix = numpy.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, -1], [0, 0, 0, 0]])

def convert_parameters_to_matrix(mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mxx, tx, ty, tz):
    M = numpy.matrix([[mxx, myx, mzx, 0], [myx, myy, myz, 0], [mzx, mzy, mzz, 0], [tx, ty, tz, 0]])
    return M1

def convert_matrix_to_parameters(M):
    return M[0,0], m[0,1], m[0,2], M[1,0], M[1,1], M[1,2], M[2,0], M[2,1], M[2,2], M[3,0], M[3,1], M[3,2]

def project_to_screen_matrix( x, y, z, M):
    camera_coordinates =  numpy.matrix([x, y, z, 1]) @ M
    screen_coordinates = camera_coordinates @ perspective_matrix
    screen_coordinates_as_array = numpy.asarray(screen_coordinates).reshape(-1)
    perspective_coordinates = screen_coordinates_as_array / screen_coordinates_as_array[3]
    perspective_xy_only = perspective_coordinates[:2]
    return result_xy_only.tolist()

def project_to_screen_parameters(x, y, z, mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mxx, tx, ty, tz):
    M = convert_parameters_to_matrix(mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mxx, tx, ty, tz)
    return project_to_screen_matrix(M, x, y, z)

def project_to_screen_multi(coordinates, mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mxx, tx, ty, tz):
    f = lambda x,y,z : project_to_screen_parameters(x, y, z, mxx, myx, mzx, mxy, myy, mzy, mxz, myz, mxx, tx, ty, tz)
    result = [f(x,y,z) for x,y,z in coordinates]
    return numpy.vstack(result)
