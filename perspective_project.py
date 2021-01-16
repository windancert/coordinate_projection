import numpy as np

# https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/building-basic-perspective-projection-matrix

measurements = None

def set_data(measurement):
    global measurements
    measurements = measurement

# return pixel x,y
def perspective_residual(zeros, m11, m12, m13, m21, m22, m23, m31, m32, m33, tx, ty,tz):

    N = len(measurements)
    real_world, screen = zip(*measurements)
    X = np.matrix(real_world)
    P = np.matrix(screen)
    
    M = np.matrix([[ m11, m12, m13, m13], [ m21, m22, m23, m23], [ m31, m32, m33, m33], [tx,ty,tz,tz]])

    X = np.hstack([X, np.ones((N,1))])

    result =  X @ M
    d = np.tile(result[:,3], (1,4))  # division by Pz
    result = np.divide(result,d)     # division by Pz

    residual = np.subtract(result[:,:2], P)
    residual = np.sum(np.power(residual,2), axis=1)
    residual = np.asarray(residual.T)
    residual.shape = (N,)
    print(np.sum(residual))

    return np.asarray(residual)
