def calculate_rgb_color(frecuency):
    rgb = [0, 255, 255]
    dec = 10
    rgb[2] -= frecuency * dec

    if rgb[2] < 0:
        rgb[0] -= rgb[2]
        rgb[2] = 0

    if rgb[0] > 255:
        rgb[1] -= rgb[0] - 255
        rgb[0] = 255

    rgb[1] = max(0, rgb[1])

    return tuple(rgb)
