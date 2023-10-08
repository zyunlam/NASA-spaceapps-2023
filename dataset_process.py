from scipi import *
import numpy as np
from math import *
import math

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


earth_up = np.array([0, 1, 0])

magnetic_lat = radians(86.494)
magnetic_long = radians(162.867)

mag_vec_up = np.array([cos(magnetic_lat), sin(magnetic_lat), 0])
mag_vec = np.dot(rotation_matrix(earth_up, magnetic_long), mag_vec_up)

mag_rot_axis = unit_vector(np.cross(earth_up, mag_vec))
mag_rot_angle = angle_between(earth_up, mag_vec)


m = 8e22
mu = 4 * pi * 1e-7
vec = {}
def process_datapoint(xp, yp, zp, bx, by, bz):
    sat_loc = np.array([xp, yp, zp])
    sat_mag_loc = np.dot(rotation_matrix(mag_rot_axis, mag_rot_angle), sat_loc)
    x, y, z = sat_mag_loc[0], sat_mag_loc[1], sat_mag_loc[2]
    dx = - (3 * m * x * z * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
    dy = - (3 * m * y * z * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
    dz = (m * (x**2 + y**2 + 2 * (z**2)) * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
    B_earth_nonmag = np.array([dx, dy, dz])
    B_earth = np.dot(rotation_matrix(mag_rot_axis, -mag_rot_angle), B_earth_nonmag) * 1e-9
    B_imf = np.array([bx, by, bz]) - B_earth
    val = B_imf.dot(B_earth) / (np.linalg.norm(B_imf) * np.linalg.norm(B_earth))
    return val

# Read the json file
import json
file = open("combined.json")
js = json.loads(file.read())
data = {}
for k, v in js.items():
    try:
        data[k] = (process_datapoint(v["X"], v["Y"], v["Z"], v["bx"], v["by"], v["bz"]))
    except:
        pass
import csv

with open('values.csv', 'w') as csvfile:
    csvfile.write("Time,Value\n")
    for k, v in data.items():
        csvfile.write(f"{k},{v}\n")

