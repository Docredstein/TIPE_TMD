import numpy as np


m=1
L=0.15
Op_barre = np.array([
    [0,0,0],
    [0,m*L**2/12,0],
    [0,0,m*L**2/12]
])



def Moment(theta0:float,theta:float) -> float :
    return (theta-theta0)*0.1
def get_J(point,centre) :
    delta = np.array(point) - np.array(centre)
    masse_locale = np.zeros(3,3)
    masse_locale[0][0] = delta[1]**2 + delta[2]**2
    masse_locale[1][1] = delta[0]**2 + delta[2]**2
    masse_locale[2][2] = delta[1]**2 + delta[0]**2

    for i in range(1,3) :
        for j in range(i,3) :
            masse_locale[i][j] = -delta[i]*delta[j]
            masse_locale[j][i] = -delta[i]*delta[j] 
    masse_locale = m* masse_locale
    return Op_barre + masse_locale 
 