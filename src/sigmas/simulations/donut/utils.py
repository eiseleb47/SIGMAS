import numpy as np

def validate_parameters(a1, b1, ecc):
    if ecc >= 1 or ecc < 0:
        raise ValueError("Eccentricity must be between 0 and 1.")
    if a1 <= 0 or b1 <= 0:
        raise ValueError("Axes must be positive values.")
    
def calculate_intensity(dist, width):
    return 50 + 200 * np.exp(-dist**2 / (2 * (0.1 * width)**2))

def transform(x, y, x0, y0, cos_inc, sin_inc):
    norm_x = x - x0
    norm_y = y - y0
    transformed_x = norm_x * cos_inc - norm_y * sin_inc
    transformed_y = norm_x * sin_inc + norm_y * cos_inc
    return transformed_x, transformed_y

def create_ring(a1, b1, ecc, inc, ring_ratio, width, height):
    array = np.zeros((height, width), dtype=np.float32)

    x0 = width // 2
    y0 = height // 2

    inc_rad = np.radians(inc)
    cos_inc = np.cos(-inc_rad)
    sin_inc = np.sin(-inc_rad)

    # Outer ellipse
    for y in range(height):
        for x in range(width):
            tx, ty = transform(x, y, x0, y0, cos_inc, sin_inc)
            if (tx**2 / (a1**2 * (1 - ecc**2)) + ty**2 / (b1**2)) <= 1:
                dist = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
                intensity = calculate_intensity(dist, width)
                array[y, x] = intensity

    # Inner ellipse
    a2 = a1 * ring_ratio
    b2 = b1 * ring_ratio
    
    for y in range(height):
        for x in range(width):
            tx_i, ty_i = transform(x, y, x0, y0, cos_inc, sin_inc)
            if tx_i**2 / (a2**2 * (1 - ecc**2)) + ty_i**2 / (b2**2) <= 1:
                array[y, x] = 0

    return array