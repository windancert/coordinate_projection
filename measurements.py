import numpy

# # Coordinaten stoel
# # wereld coordinaten (dit keer in [cm]) en pixel coordinaten

front_leg_right = ((0, 0, 0), (553, 1077)) # rechter voor poot
front_leg_left = ((0, 41, 0), (307, 973)) # linker voor poot
back_leg = ((40, 1.5, 0), (626, 884)) # achter poot
back_rest_right = ((49, -1.5, 103), (704, 245)) # rug leuning
back_rest_left = ((49, 41.5, 103), (426, 232)) # rug leuning
seat = ((14, 14, 46.5), (501, 736)) # zitvlak

stoel_allemaal = [front_leg_right, front_leg_left, back_leg, back_rest_right, back_rest_left, seat]

# Coordinaten doosje
doosje_a = ((0, 44, 0), (420, 1752))
doosje_b = ((0, 0, 180), (469, 334))
doosje_c = ((180, 0, 0), (1679, 1468))
doosje_d = ((0, 0, 0), (571, 1899))
doosje_e = ((0, 44, 180), (301, 287))
doosje_f = ((180, 44, 180), (1532, 168))
doosje_g = ((180, 0, 180), (1751, 194))

doosje_allemaal = [doosje_a, doosje_b, doosje_c, doosje_d, doosje_e, doosje_f, doosje_g]


# Coordinaten met perspectief
perspectief_a = ((1,0,2),(0.5, 0))
perspectief_b = ((2,0,2),(1, 0))
perspectief_c = ((-1,0,2),(-0.5, 0))
perspectief_d = ((-2,0,2),(-1, 0))
perspectief_e = ((0,1,2),(0, 0.5))
perspectief_f = ((0,2,2),(0, 1))
perspectief_g = ((1,0,4),(0.25, 0))

perspectief_allemaal = [perspectief_a, perspectief_b, perspectief_c, perspectief_d, perspectief_e, perspectief_f, perspectief_g]

# testen van gijs.

fout = {
    "1": {
        "x": 433.0,
        "y": 70.0
    },
    "10": {
        "x": 522.0,
        "y": 372.0
    },
    "11": {
        "x": 632.0,
        "y": 387.0
    },
    "12": {
        "x": 561.0,
        "y": 394.0
    },
    "2": {
        "x": 508.0,
        "y": 38.0
    },
    "3": {
        "x": 530.0,
        "y": 612.0
    },
    "4": {
        "x": 447.0,
        "y": 601.0
    },
    "5": {
        "x": 549.0,
        "y": 127.0
    },
    "6": {
        "x": 616.0,
        "y": 102.0
    },
    "7": {
        "x": 640.0,
        "y": 583.0
    },
    "8": {
        "x": 568.0,
        "y": 576.0
    },
    "9": {
        "x": 441.0,
        "y": 382.0
    }
}
goed = {
    "1": {
        "x": 267.0,
        "y": 86.0
    },
    "10": {
        "x": 429.0,
        "y": 545.0
    },
    "11": {
        "x": 418.0,
        "y": 462.0
    },
    "12": {
        "x": 323.0,
        "y": 466.0
    },
    "2": {
        "x": 412.0,
        "y": 82.0
    },
    "3": {
        "x": 435.0,
        "y": 769.0
    },
    "4": {
        "x": 318.0,
        "y": 773.0
    },
    "5": {
        "x": 300.0,
        "y": 125.0
    },
    "6": {
        "x": 404.0,
        "y": 120.0
    },
    "7": {
        "x": 424.0,
        "y": 646.0
    },
    "8": {
        "x": 335.0,
        "y": 649.0
    },
    "9": {
        "x": 301.0,
        "y": 550.0
    }
}

wereld = {
  "1": {
    "x": 0.0,
    "y": 600.0,
    "z": 0.0
  },
  "2": {
    "x": 0.0,
    "y": 40.0,
    "z": 0.0
  },
  "3": {
    "x": 0.0,
    "y": 40.0,
    "z": 3269.0
  },
  "4": {
    "x": 0.0,
    "y": 600.0,
    "z": 3263.0
  },
  "5": {
    "x": 1240.0,
    "y": 560.0,
    "z": 0.0
  },
  "6": {
    "x": 1240.0,
    "y": 0.0,
    "z": 0.0
  },
  "7": {
    "x": 1240.0,
    "y": 0.0,
    "z": 3253.0
  },
  "8": {
    "x": 1240.0,
    "y": 560.0,
    "z": 3242.0
  },
  "9": {
    "x": 0.0,
    "y": 600.0,
    "z": 2000.0
  },
  "10": {
    "x": 0.0,
    "y": 40.0,
    "z": 2000.0
  },
  "11": {
    "x": 1240.0,
    "y": 0.0,
    "z": 2000.0
  },
  "12": {
    "x": 1240.0,
    "y": 560.0,
    "z": 2000.0
  }

}



measurement_1 = (( wereld["1"]["x"],  wereld["1"]["y"],  wereld["1"]["z"]), (goed["1"]["x"], goed["1"]["y"]))
measurement_2 = (( wereld["2"]["x"],  wereld["2"]["y"],  wereld["2"]["z"]), (goed["2"]["x"], goed["2"]["y"]))
measurement_3 = (( wereld["3"]["x"],  wereld["3"]["y"],  wereld["3"]["z"]), (goed["3"]["x"], goed["3"]["y"]))
measurement_4 = (( wereld["4"]["x"],  wereld["4"]["y"],  wereld["4"]["z"]), (goed["4"]["x"], goed["4"]["y"]))
measurement_5 = (( wereld["5"]["x"],  wereld["5"]["y"],  wereld["5"]["z"]), (goed["5"]["x"], goed["5"]["y"]))
measurement_6 = (( wereld["6"]["x"],  wereld["6"]["y"],  wereld["6"]["z"]), (goed["6"]["x"], goed["6"]["y"]))
measurement_7 = (( wereld["7"]["x"],  wereld["7"]["y"],  wereld["7"]["z"]), (goed["7"]["x"], goed["7"]["y"]))
measurement_8 = (( wereld["8"]["x"],  wereld["8"]["y"],  wereld["8"]["z"]), (goed["8"]["x"], goed["8"]["y"]))
measurement_9 = (( wereld["9"]["x"],  wereld["9"]["y"],  wereld["9"]["z"]), (goed["9"]["x"], goed["9"]["y"]))
measurement_10 = (( wereld["10"]["x"],  wereld["10"]["y"],  wereld["10"]["z"]), (goed["10"]["x"], goed["10"]["y"]))
measurement_11 = (( wereld["11"]["x"],  wereld["11"]["y"],  wereld["11"]["z"]), (goed["11"]["x"], goed["11"]["y"]))
measurement_12 = (( wereld["12"]["x"],  wereld["12"]["y"],  wereld["12"]["z"]), (goed["12"]["x"], goed["12"]["y"]))
all_measurements_goed = [measurement_1, measurement_2, measurement_3, measurement_4, measurement_5, measurement_6, measurement_7, measurement_8,measurement_9,
        measurement_10,measurement_11,measurement_12  ]

real_world, screen = zip(*all_measurements_goed)
real_world = numpy.vstack(real_world)
screen     = numpy.vstack(screen)

X = numpy.zeros(len(real_world))
Y = numpy.zeros(len(real_world))
Z = numpy.zeros(len(real_world))
i = 0
for rw in real_world:
    X[i] = rw[0]
    Y[i] = rw[1]
    Z[i] = rw[2]
    i += 1

Sx = numpy.zeros(len(screen))
Sy = numpy.zeros(len(screen))
i = 0
for sc in screen:
    Sx[i] = sc[0]
    Sy[i] = sc[1]
 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.scatter(X, Y, Z, zdir='z', c= 'red')
plt.savefig("goedworld.png")

  
measurement_1 = (( wereld["1"]["x"],  wereld["1"]["y"],  wereld["1"]["z"]), (fout["1"]["x"], fout["1"]["y"]))
measurement_2 = (( wereld["2"]["x"],  wereld["2"]["y"],  wereld["2"]["z"]), (fout["2"]["x"], fout["2"]["y"]))
measurement_3 = (( wereld["3"]["x"],  wereld["3"]["y"],  wereld["3"]["z"]), (fout["3"]["x"], fout["3"]["y"]))
measurement_4 = (( wereld["4"]["x"],  wereld["4"]["y"],  wereld["4"]["z"]), (fout["4"]["x"], fout["4"]["y"]))
measurement_5 = (( wereld["5"]["x"],  wereld["5"]["y"],  wereld["5"]["z"]), (fout["5"]["x"], fout["5"]["y"]))
measurement_6 = (( wereld["6"]["x"],  wereld["6"]["y"],  wereld["6"]["z"]), (fout["6"]["x"], fout["6"]["y"]))
measurement_7 = (( wereld["7"]["x"],  wereld["7"]["y"],  wereld["7"]["z"]), (fout["7"]["x"], fout["7"]["y"]))
measurement_8 = (( wereld["8"]["x"],  wereld["8"]["y"],  wereld["8"]["z"]), (fout["8"]["x"], fout["8"]["y"]))
measurement_1 = (( wereld["9"]["x"],  wereld["9"]["y"],  wereld["9"]["z"]), (fout["9"]["x"], fout["9"]["y"]))
measurement_2 = (( wereld["10"]["x"],  wereld["10"]["y"],  wereld["10"]["z"]), (fout["10"]["x"], fout["10"]["y"]))
measurement_1 = (( wereld["11"]["x"],  wereld["11"]["y"],  wereld["11"]["z"]), (fout["11"]["x"], fout["11"]["y"]))
measurement_2 = (( wereld["12"]["x"],  wereld["12"]["y"],  wereld["12"]["z"]), (fout["12"]["x"], fout["12"]["y"]))
all_measurements_fout = [measurement_1, measurement_2, measurement_3, measurement_4, measurement_5, measurement_6, measurement_7, measurement_8,measurement_9,
        measurement_10,measurement_11,measurement_12]
real_world, screen = zip(*all_measurements_fout)
screen = numpy.vstack(screen)
print("fout" )
for s  in screen : 
    print(str(s[0]) + "," + str(s[1]))


