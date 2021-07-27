import colorsys

def clamp_coordinate(x):
    """
    Clamp function for color value (between 0 and 255)
    """
    return max(0, min(int(round(x)), 255))

def hex_to_rgb(hex):
    """
    Convert a hex string to rgb tupple (coordinates from 0 to 1)
    """
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """
    Convert a rgb tupple (coordinates from 0 to 1) to hex string
    """
    r, g, b = (clamp_coordinate(x * 255) for x in rgb)
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

def hex_scale_brightness(hex, scale = 0):
    """
    Set a hex string by a given factor.

    To darken the color, use a float value between -1 and 0.
    To brighten the color, use a float value between 0 and 1.
    """
    r, g, b = hex_to_rgb(hex)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    rgb = colorsys.hls_to_rgb(h, min(1, l * scale), s = s)
    return rgb_to_hex(rgb)
