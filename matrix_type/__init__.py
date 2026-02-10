from .band import generate_band
from .rand_spd import generate_rand_spd
from .user_def import generate_user
import numpy as np

def generate_matrix(kind, n, **kwargs) -> np.ndarray:
    if(kind == "band"):
        return generate_band(n)
    elif (kind =="random"):
        return generate_rand_spd(n)
    elif (kind == 'user'):
        return generate_user(**kwargs)
    else:
        raise ValueError(f"Unknown Matrix of Type {kind}")
    