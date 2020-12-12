#(c) 2020 nathan thimothe
"""
This module contains helper functions that help the flask backend work.
"""
from app import colors_cache, popups_cache
import folium as f
import base64

# HELPER FUNCTIONS (NO ROUTES)
def update_colors_cache(coordinates, original_color = ""):
    """
    Update colors_cache with average of two colors (`original_color` and color already present in cache) 
    """
    if colors_cache.get(coordinates) is not None:
        r1, g1, b1 = hex_to_rgb(original_color)
        r2, g2, b2 = hex_to_rgb(colors_cache.get(coordinates))
        # average RGB values
        res = ((r1+r2) // 2), ((g1+g2) // 2), ((b1+b2) // 2)
        colors_cache.delete(coordinates)
        colors_cache.add(coordinates,rgb_to_hex(res))
        check_success(coordinates, rgb_to_hex(res))
    else:
        colors_cache.add(coordinates, original_color)
        check_success(coordinates, original_color)

def update_popups_cache(coordinates, html_content):
    """
    Update popups_cache by mapping `coordinates` to correct `html_content`. In the case that `coordinates` already maps content, concatenate `html_content` to content that already exists within the cache.
    """
    # access dictionary at key None
    d = popups_cache.get(None)
    if d is None:
        return
    # if the coordinates exist within popups_cache[None] then 
    # add to html_content at that key, the new iframe + popup will be created out of this updated html content. Je souhaite que ca aille aller
    if d.get(coordinates,None) is not None:
        d[coordinates] += html_content
    # map coordinates to html content (at popup) if empty
    else:
        d[coordinates] = html_content if html_content is not None else None
    # remove k-v pair and re add
    popups_cache.delete(None)
    popups_cache.add(None, d)

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


def clear_caches():
    """
    Clear colors_cache and popups_cache of all cache relevant to their main functionality.
    """
    colors_cache.clear()
    popups_cache.delete(None)
    popups_cache.add(None, dict())

def increment_map_name():
    """
    Increment the name of map HTML file to reflect the latest update.
    """
    map_name = popups_cache.get('')
    map_name[1] = str(int(map_name[1]) + 1)
    popups_cache.delete('')
    popups_cache.add('', map_name)
    print(map_name)


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

def check_success(coordinates,color, newline=False):
    print("\n") if newline else None
    if colors_cache.get(coordinates) == color:
        print("Successfully added %s" % color) 
        print("{}: {}".format(coordinates,colors_cache.get(coordinates)))
    else:
        print("Unable to add %s" % color)

