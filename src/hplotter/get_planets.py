import subprocess
import numpy as np
import os
import pandas as pd
import json

#with open('kepler.json') as json_file:
#    planets = json.load(json_file)

data = pd.read_csv("planets_2020.03.14_13.39.11.csv")
planets = data['pl_name'].to_list()
stars = data['pl_hostname'].to_list()

planets = [planet.replace(" ","") for planet in planets[4000:]]
stars = [star.replace(" ","") for star in stars[4000:]]
print(planets)
try:
    os.mkdir("planets_full")
except FileExistsError:
    pass

command = "ds9 -dss name {} -contour yes -contour nlevels 10 -contour smooth 3 -contour color white -contour save {}.ctr image -scale limits 300000 300001 -saveimage png {}.png".format(stars[0], "planets_full/" + planets[0], "planets_full/" + planets[0]) 
print(command)
for i,planet in enumerate(planets[1:]):
    command += " -dss frame current -dss name {} -contour save {}.ctr image -saveimage png {}.png".format(stars[i], "planets_full/" + planet, "planets_full/" + planet)

if __name__ == "__main__":
    subprocess.call(command, shell=True)
