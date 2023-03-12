import numpy as np

THETA_SAMPLES = 20
PHI_SAMPLES = 50
OUTPUT_FILE = "sphere.obj"
R = 1

def spherical_to_cartesian(r, phi, theta):

    coords = []

    x = r*np.sin(phi)*np.cos(theta)
    y = r*np.sin(phi)*np.sin(theta)
    z = r*np.cos(phi)
    return [x, y, z]

# return 1d index 
def unravel_index(i, j, N_I):
    return j*N_I + i

if __name__=="__main__":


    # vertices = [[0,0,0],[1,0,0],[0,1,0]]
    # faces = [[1,2,3]]

    # generate theta vector but discard north and south poles
    v_theta = np.linspace(0, np.pi, THETA_SAMPLES+2)
    v_theta = v_theta[1:-1]
    # generate phi vector but discard last vertices (prime meridian)
    v_phi = np.linspace(0,2*np.pi, PHI_SAMPLES+1)
    v_phi = v_phi[0:-1]

    vertices = []

    for theta_i in v_theta:
        for phi_i in v_phi:
            coords = spherical_to_cartesian(R, theta_i, phi_i)
            vertices.append(coords)

    # add the north and south poles
    north_pole = spherical_to_cartesian(R,0,0)
    vertices.append(north_pole)
    north_pole_i = len(vertices)-1
    south_pole = spherical_to_cartesian(R,np.pi,0)
    vertices.append(south_pole)
    south_pole_i = len(vertices)-1

    faces = []

    for j in range(THETA_SAMPLES-1):
        for i in range(PHI_SAMPLES):
            v1 = unravel_index(i,j,PHI_SAMPLES)
            v2 = unravel_index(i,j+1,PHI_SAMPLES)
            # handle the case where we have to glue the edges of the sheet together
            if i == PHI_SAMPLES-1:
                v3 = unravel_index(0,j,PHI_SAMPLES)
                v4 = unravel_index(0,j+1,PHI_SAMPLES)
            else:
            # other general case
                v3 = unravel_index(i+1,j,PHI_SAMPLES)
                v4 = unravel_index(i+1,j+1,PHI_SAMPLES)
            faces.append([v2+1,v4+1,v3+1,v1+1])

    # do the north pole     
    j=0
    for i in range(PHI_SAMPLES):
        # create a triangle
        v1 = north_pole_i
        v2 = i 
        if i==PHI_SAMPLES-1:
            v3 = 0
        else:
            v3 = i+1 
        faces.append([v1+1,v2+1,v3+1])

    # do the south pole
    j = THETA_SAMPLES-1
    for i in range(PHI_SAMPLES):
        # create a triangle
        v1 = south_pole_i
        v2 = unravel_index(i,j,PHI_SAMPLES)
        if i==PHI_SAMPLES-1:
            v3 = unravel_index(0,j,PHI_SAMPLES)
        else:
            v3 = unravel_index(i+1,j,PHI_SAMPLES)
        faces.append([v1+1,v2+1,v3+1])


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
