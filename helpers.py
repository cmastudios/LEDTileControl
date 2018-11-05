def hsl_to_rgb(h : float, s : float, l : float):
    """
    Convert an HSL color to an RGB value.
    :param h: hue, a float from 0 to 1
    :param s: saturation, a float from 0 to 1
    :param l: lightness, a float from 0 to 1
    :return r, g, b: Three ints in [0, 256) representing
        the r, g, and b values of the color
    """
    if s==0:
        # Achromatic
        return l, l, l
    if l < 0.5:
        q = l * (1 + s)
    else:
        q = l + s - l * s
    p = 2 * l - q
    r = int(hue_to_rgb(p, q, h + 1/3) * 255)
    g = int(hue_to_rgb(p, q, h) * 255)
    b = int(hue_to_rgb(p, q, h - 1/3) * 255)
    
    return (r, g, b)
    
def hue_to_rgb(p, q, t):
    """
    Convert a hue to an rgb value
    """
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1/6:
        return p + (q-p) * 6 * t
    if t < 1/2:
        return q;
    if t < 2/3:
        return p + (q-p) * (2/3 - t) * 6
    return p
