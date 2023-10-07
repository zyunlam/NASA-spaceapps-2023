from vpython import *
import pandas as pd
import numpy as np
from pyquaternion import *

o = 10;
# 2016-08-01 08:00:00,-1114816.221113259,1121070.317038619,-185512.5947212637,0.1503526354830916,-0.2351769266282038,0.02619965142234713,5.309884433883294,1591863.306129811,-0.2739718870682453

xp = -1114816.221113259
yp = 1121070.317038619
zp = -185512.5947212637

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

earth = sphere(pos=vec(0, 0, 0), radius=6371*o)
sat = sphere(pos=vec(x, y, z), radius=3000*o)
# 3.48007    0.130063    -0.339754

B_measured = vec(3.48007, 0.130063, -0.339754)#, -2.59, -3.38)

m = 8e22
mu = 4 * pi * 1e-7
dx = - (3 * m * x * z * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
dy = - (3 * m * y * z * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
dz = (m * (x**2 + y**2 + 2 * (z**2)) * mu) / (4 * pi * (x**2 + y**2 + z**2) ** 1.5)
B_earth_nonmag = vec(dx, dy, dz)
B_earth = B_earth_nonmag.rotate(axis=mag_rot_axis, angle=-mag_rot_angle) * 1e-9

B_imf = B_measured - B_earth

print(B_measured, B_earth, B_imf)
"""
earth_arrow = arrow(pos=earth.pos, 
                  axis=earth_up*1e4*o, 
                  shaftwidth=500*o,
                  color = color.green)
sat_arrow = arrow(pos=sat.pos, 
                  axis=sat_pointing*1e4*o, 
                  shaftwidth=500*o,
                  color = color.green)
mag_arrow = arrow(pos=earth.pos, 
                  axis=mag_vec*1e4*o, 
                  shaftwidth=500*o,
                  color = color.orange)

rot_axis = earth_up.cross(sat_pointing).norm()
rot_angle = earth_up.diff_angle(sat_pointing)
"""
jj = 1e5
earth_arrow = arrow(pos=sat.pos, 
                  axis=B_earth * jj, 
                  shaftwidth=1000*o,
                  color = color.green)
imf_arrow = arrow(pos=sat.pos, 
                  axis=B_imf * jj, 
                  shaftwidth=1000*o,
                  color = color.orange)
net_arrow = arrow(pos=sat.pos, 
                  axis=B_measured * jj, 
                  shaftwidth=1000*o,
                  color = color.purple)

print(B_imf.dot(B_earth) / (B_imf.mag * B_earth.mag))

input()