import numpy as np

THETA_SAMPLES = 10
PHI_SAMPLES = 10
r = 1
R = 3
OUTPUT_FILE = "torus10x10.obj"

def toroidal_to_cartesian(r, R, theta, phi):
    coords = []
    x = (R+r*np.cos(theta))*np.cos(phi)
    y = (R+r*np.cos(theta))*np.sin(phi)
    z = r*np.sin(theta)
    return [x, y, z]

# return 1d index 
def unravel_index(i, j, N_I):
    return j*N_I + i

if __name__=="__main__":

    v_theta = np.linspace(0,2*np.pi,THETA_SAMPLES+1)
    v_theta = v_theta[:-1]

    v_phi = np.linspace(0,2*np.pi, PHI_SAMPLES+1 )
    v_phi = v_phi[:-1]

    vertices = []

    for theta_i in v_theta:
        for phi_i in v_phi:
            coords = toroidal_to_cartesian(r, R, theta_i, phi_i)
            vertices.append(coords)

    faces = []

    for j in range(THETA_SAMPLES):
        for i in range(PHI_SAMPLES):

            if i == PHI_SAMPLES-1:
                i_plus_1 = 0
            else:
                i_plus_1 = i+1
            if j == THETA_SAMPLES-1:
                j_plus_1 = 0
            else:
                j_plus_1 = j+1
            
            v1 = unravel_index(i,j,PHI_SAMPLES)
            v2 = unravel_index(i,j_plus_1,PHI_SAMPLES)
            v3 = unravel_index(i_plus_1,j,PHI_SAMPLES)
            v4 = unravel_index(i_plus_1,j_plus_1,PHI_SAMPLES)

            faces.append([v2+1,v1+1,v3+1])
            faces.append([v2+1,v3+1,v4+1])

    # serialise obj
    f = open(OUTPUT_FILE, "w")
    for v in vertices:
        f.write(f"v {v[0]} {v[1]} {v[2]}\n")

    for face in faces:
        f.write("f ")
        for i in face:
            f.write(f"{i} ")
        f.write("\n")
    f.close()