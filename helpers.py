# (c) 2020 nathan thimothe
"""
This module contains helper functions that help the flask backend work.
"""
from app import session
import folium as f
import base64
import uuid

# HELPER FUNCTIONS 
def update_colors_cache(coordinates, original_color = ""):
    """
    Update colors_cache with average of two colors (`original_color` and color already present in cache) 
    """
    assert 'colors_cache' in session, "colors cache must be in session"
    cache = session['colors_cache']
    if cache.get(str(coordinates), None) is not None:
        r1, g1, b1 = hex_to_rgb(original_color)
        r2, g2, b2 = hex_to_rgb(cache.get(str(coordinates)))
        # average RGB values
        res = ((r1+r2) // 2), ((g1+g2) // 2), ((b1+b2) // 2)
        #cache.delete(coordinates)
        cache[str(coordinates)] = rgb_to_hex(res)
    else:
        cache[str(coordinates)] = original_color # since keys must be str, int, float, bool or None
    # overwrite the cache at key colors_cache with updated cache
    session['colors_cache'] = cache

def rgb_to_hex(rgb):
    """
    Convert rgb value to hex and ensure proper formatting (pad w/ 0s).
    """
    vals = []
    for i in range(len(rgb)):
        col = hex(rgb[i])[2:]
        if len(col) < 2:
            col = '0' * (2-len(col)) + col
        vals.append(col)
    return '#' + ''.join(vals)
    

def hex_to_rgb(hex_val):
    """
    Convert a hex color value to RGB values as a list
    """
    hex_val = hex_val[1:]
    return list((int(hex_val[:2],16), int(hex_val[2:4],16), int(hex_val[4:], 16)))


def clear_colors_cache():
    """
    Clear colors_cache. 
    """
    session['colors_cache'].clear()

def load_popup_content(img_path, html_file_path, text_file_path):
    """ 
    Given a valid `img_path`, `html_file_path`, and `text_file_path`, this function 
    returns a string of popup content.
    Parameters
    ----------
    img_path : str
        path of the image to be loaded into popup content
    html_file_path: str
        path of the HTML file that wraps image and text
    text_file_path: str
        path of the text to be loaded
    """
    html = None
    txt = None
    encoded = base64.b64encode(open(img_path, 'rb').read())
    with open(html_file_path, 'r') as x:
        html = x.read()
    with open(text_file_path, 'r') as x:
        txt = x.read()
    return html.format(encoded.decode('UTF-8'), txt)


def make_popup(html_content):
    frame = f.IFrame(html_content, figsize=(6,5))
    return f.Popup(frame)


def make_dir(dir_name):
    """
    If a given `dir_name` does not exist with the templates directory, create the directory.
    """
    import os
    path = os.path.join('templates', dir_name)
    if not os.path.exists(path):
        os.mkdir(path)

def get_dir_id():
    if 'visited' not in session:
        session['visited'] = True
        unique_dir_id = str(uuid.uuid1())
        session['dir'] = unique_dir_id
    else:
        unique_dir_id = session['dir']
    return unique_dir_id


def set_colors_cache():
    """
    If a session does not have a colors_cache (lat,long tuples mapped to colors), set it equal to an empty dictionary
    """
    if 'colors_cache' not in session:
        session['colors_cache'] = dict()

