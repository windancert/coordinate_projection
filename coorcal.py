import numpy
import matplotlib.pyplot as plt

M = None

def project_to_laser(x, y, z):
    result =  numpy.matrix([x, y, z, 1]) @ M
    return numpy.asarray(result[:,]).reshape(-1)

# World coordinate and laser screen coordinates
measurement_1 = (( 1,  1,  1), (200, 250))
measurement_2 = (( 1, -1,  1), (100, 150))
measurement_3 = ((-1, -1,  1), (400, 150))
measurement_4 = ((-1,  1,  1), (600, 250))
measurement_5 = (( 1,  1, -1), (200, 450))
measurement_6 = (( 1, -1, -1), (100, 350))
measurement_7 = ((-1, -1, -1), (400, 350))
measurement_8 = ((-1,  1, -1), (600, 450))

all_measurements = [measurement_1, measurement_2, measurement_3, measurement_4, measurement_5, measurement_6, measurement_7, measurement_8]

N = len(all_measurements)

real_world, screen = zip(*all_measurements)

C = numpy.matrix(real_world)
# Add extra column with ones to indicate constant offset
C = numpy.hstack([C, numpy.ones((N,1))])
P = numpy.matrix(screen)

# least square
M = numpy.linalg.lstsq(C, P, rcond=None)
M = M[0]



x, y = list(zip(*screen))
plt.scatter(x, y, c='r')
plt.gca().invert_yaxis()

projection = C @ M

px = numpy.asarray(projection[:,0]).reshape(-1)
py = numpy.asarray(projection[:,1]).reshape(-1)
plt.scatter(px, py, c='b')

origin = project_to_laser(0, 0, 0)

plt.scatter(origin[0], origin[1], c='g')

plt.show()
