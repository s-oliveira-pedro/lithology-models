from litholayers_module import Litho_models
import numpy as np
import math

"z = (ax)+(by)"
a = 1
b = 4
thickness = 10

model = Litho_models(a,b)

angle = model.angle_between_plane_and_horizontal()
surf_thick = model.calculate_surface_exposure(10)
surf_thick = model.strike_plane()
