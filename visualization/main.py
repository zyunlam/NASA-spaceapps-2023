from vpython import *
import pandas as pd
import numpy as np
import json

o = 10;
jj = 1e5

# 2016-08-01 08:00:00,-1114816.221113259,1121070.317038619,-185512.5947212637,0.1503526354830916,-0.2351769266282038,0.02619965142234713,5.309884433883294,1591863.306129811,-0.2739718870682453

with open('visualization/combined.json') as f:
    d = json.loads(f.read())

earth = sphere(pos=vec(0, 0, 0), radius=6371*o)
sat = sphere(pos=vec(0, 0, 0), radius=3000*o)
earth_arrow = arrow(pos=sat.pos, 
                axis=vec(0,1,0), 
                shaftwidth=1000*o,
                color = color.green)
imf_arrow = arrow(pos=sat.pos, 
                axis=vec(0,1,0), 
                shaftwidth=1000*o,
                color = color.orange)
net_arrow = arrow(pos=sat.pos, 
                axis=vec(0,1,0), 
                shaftwidth=1000*o,
                color = color.purple)

for entry in d.keys():
    print(entry)
    xp = d[entry]['X']
    if (type(xp) != float or xp == None):
        continue
    yp = d[entry]['Y']
    if (type(yp) != float or yp == None):
        continue
    zp = d[entry]['Z']
    if (type(zp) != float or zp == None):
        continue
    bx = d[entry]['bx']
    if (type(bx) != float or bx == None):
        continue
    by = d[entry]['by']
    if (type(by) != float or by == None):
        continue
    bz = d[entry]['bz']
    if (type(bz) != float or bz == None):
        continue


    earth_up = vec(0, 1, 0)
    sat_pointing = vec(-xp, -yp, -zp).norm()
    sat_loc = vec(xp, yp, zp)

    magnetic_lat = radians(86.494)
    magnetic_long = radians(162.867)

    mag_vec_up = vec(cos(magnetic_lat), sin(magnetic_lat), 0)
    mag_vec = mag_vec_up.rotate(angle=magnetic_long, axis=earth_up)

    mag_rot_axis = earth_up.cross(mag_vec).norm()
    mag_rot_angle = earth_up.diff_angle(mag_vec)

    sat_mag_loc = sat_loc.rotate(angle=mag_rot_angle, axis=mag_rot_axis)
    x, y, z = sat_mag_loc.x, sat_mag_loc.y, sat_mag_loc.z
    
    sat.pos = vec(xp, yp, zp)

    B_measured = vec(bx, by, bz)

    m = 8e22
    mu = 4 * pi * 1e-7
    dx = - (3 * m * x * z * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
    dy = - (3 * m * y * z * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
    dz = (m * (x**2 + y**2 + 2 * (z**2)) * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
    B_earth_nonmag = vec(dx, dy, dz)
    B_earth = B_earth_nonmag.rotate(axis=mag_rot_axis, angle=-mag_rot_angle) * 1e-9

    B_imf = B_measured - B_earth
    earth_arrow.pos = sat.pos
    imf_arrow.pos = sat.pos
    net_arrow.pos = sat.pos
    earth_arrow.axis = B_earth * jj
    imf_arrow.axis = B_imf * jj
    net_arrow.axis = B_measured * jj

    print(B_measured, B_earth, B_imf)



    print(B_imf.dot(B_earth) / (B_imf.mag * B_earth.mag))
    rate(50)
input()