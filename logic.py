from flask import Flask, render_template, request
from markupsafe import escape
from constants import *
import folium as f
from cache import colors_cache, popups_cache
import base64

app = Flask(__name__)

# maps lat,lon tuples to hex colors
colors_cache.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 0})
# maps None to dict of lat,lon tuples to appropriate pop up messages
popups_cache.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 0})
popups_cache.add('',['map','0'])
popups_cache.add(None,dict())

@app.route('/', methods=['GET', 'POST'])
def root():
    cc_color = "#3186cc"
    av_color = "#ff2600"
    vdg_color = "#00ff48"
    # if colors are being submitted, redefine color vars
    if request.method == 'POST':
        clear_caches()
        print('POST_REQUEST')
        cc_color = request.form['cc_color']
        av_color = request.form['av_color']
        vdg_color = request.form['vdg_color']
        # update map_name
        increment_map_name()
    print("cc_color: %s" % cc_color)
    print("av_color: %s" % av_color)
    print("vdg_color: %s" % vdg_color)
    map(cc_color,av_color,vdg_color, name=''.join(popups_cache.get('')))
    # update the html so the default value is what the user last entered
    return render_template(
        FORMATTED_MAP,
        value1=cc_color,
        value2=av_color,
        value3=vdg_color,
        )

@app.route('/about')
def about():
    about = ""
    with open('templates/data/text/about.txt') as x:
        about = x.read()
    return render_template(
        ABOUT,
        about=about
    )

@app.route('/citations')
def citations():
    citations = ""
    with open('templates/data/text/citations.txt') as x:
        citations = x.read()
    citations = citations.splitlines()
    print(citations)
    return render_template(
        CITATIONS,
        citations=citations
    )

def map(cc_color,av_color,vdg_color, name="map"):
    """
    Creates a new map using appropriate color parameter for each explorer.
    cc_color : Color for Christopher Columbus's departure locations.
    av_color : Color for Amerigo Vespucci's departure locations.
    vdg_color : Color for Vasco da Gama's departure locations.
    """
    map = f.Map(
        location=['48.8566', '2.3522'], 
        zoom_start = 12, 
        min_zoom = 3, 
        tiles = 'CartoDB positron')
    cc = add_cc(map, cc_color)
    av = add_av(map, av_color)
    vdg = add_vdg(map, vdg_color)
    # add all circles and circle markers to the map
    for each in [cc, av, vdg]:
        for item in each:
            item.add_to(map)
    map.save("templates/" + name + '.html')

@app.route('/map_render')
def map_render():
    name = ''.join(popups_cache.get(''))
    return render_template(name + '.html')

def add_cc(map, cc_color):
    """
    Add Christopher Columbus's departure points to map.
    """
    # user color (originally some shade of blue)
    CC_COLOR = cc_color

    # first voyage
    PALOS_COORDINATES = (37.2289, -6.8954)
    # update caches -- if a coordinate is already mapped to a color, average colors, else map coordinates to color
    update_colors_cache(PALOS_COORDINATES, original_color=CC_COLOR)
    update_popups_cache(PALOS_COORDINATES, load_popup_content('templates/data/photos/colomb.jpeg','templates/cc.html', 'templates/data/text/palos_cc.txt'))

    c1 = f.Circle(
        radius=INNER_RADIUS,
        location=PALOS_COORDINATES,
        popup='',
        color=CRIMSON,
        fill=False,
        )

    cm1 = f.CircleMarker(
        radius=OUTER_RADIUS,
        location=PALOS_COORDINATES,
        popup=make_popup(popups_cache.get(None)[PALOS_COORDINATES]), # make popup out of most up-to-date HTML content
        color=CC_COLOR,
        fill=True,
        fill_color=CC_COLOR
        )


    # second, fourth voyages
    CADIZ_COORDINATES = (36.5271,-6.2886)
    # update caches
    update_colors_cache(CADIZ_COORDINATES, CC_COLOR)
    # update cache with html_content from colombus's second and fourth voyages
    update_popups_cache(CADIZ_COORDINATES, load_popup_content('templates/data/photos/colomb.jpeg','templates/cc.html', 'templates/data/text/cadiz_cc_1.txt'))
    update_popups_cache(CADIZ_COORDINATES, load_popup_content('templates/data/photos/colomb.jpeg','templates/cc.html', 'templates/data/text/cadiz_cc_2.txt'))

    c2 = f.Circle(
        radius=INNER_RADIUS,
        location=CADIZ_COORDINATES,
        popup='',
        color=CRIMSON,
        fill=False
        )

    cm2 = f.CircleMarker(
        radius=OUTER_RADIUS,
        location=CADIZ_COORDINATES,
        popup=make_popup(popups_cache.get(None)[CADIZ_COORDINATES]),
        color=CC_COLOR,
        fill=True,
        fill_color=CC_COLOR
        )


    # third voyage
    SAN_LUC_COORDINATES = (36.7726,-6.3530)
    # update caches
    update_colors_cache(SAN_LUC_COORDINATES, CC_COLOR)
    update_popups_cache(SAN_LUC_COORDINATES, load_popup_content('templates/data/photos/colomb.jpeg','templates/cc.html', 'templates/data/text/sanlucar_cc.txt'))

    c3 = f.Circle(
        radius=INNER_RADIUS,
        location=SAN_LUC_COORDINATES,
        popup='',
        color=CRIMSON,
        fill=False
        )

    cm3 = f.CircleMarker(
        radius=OUTER_RADIUS,
        location=SAN_LUC_COORDINATES,
        popup=make_popup(popups_cache.get(None)[SAN_LUC_COORDINATES]),
        color=CC_COLOR,
        fill=True,
        fill_color=CC_COLOR
        )        
    return [c1,cm1,c2,cm2,c3,cm3]



def add_av(map, av_color):
    """
    Add Amerigo Vespucci's 2 verified departure points to map.
    """
    # user color (originally some shade of red)
    ORIG_AV_COLOR = av_color


    # first voyage (under the service of Spain)
    CADIZ_COORDINATES = (36.5271,-6.2886)
    # update caches
    update_colors_cache(CADIZ_COORDINATES, ORIG_AV_COLOR)
    update_popups_cache(CADIZ_COORDINATES, load_popup_content('templates/data/photos/vespucci.jpg','templates/av.html', 'templates/data/text/cadiz_av.txt'))

    c1 = f.Circle(
        radius=INNER_RADIUS,
        location=CADIZ_COORDINATES,
        popup='',
        color=CRIMSON,
        fill=False
        )

    cm1 = f.CircleMarker(
        radius=OUTER_RADIUS,
        location=CADIZ_COORDINATES,
        popup=make_popup(popups_cache.get(None)[CADIZ_COORDINATES]),
        color=colors_cache.get(CADIZ_COORDINATES),
        fill=True,
        fill_color=colors_cache.get(CADIZ_COORDINATES)
        )


    # second voyage under the service of Portugal
    LISBON_COORDINATES = (38.7223, -9.1393)
    # update caches
    update_colors_cache(LISBON_COORDINATES, ORIG_AV_COLOR)
    update_popups_cache(LISBON_COORDINATES, load_popup_content('templates/data/photos/vespucci.jpg','templates/av.html', 'templates/data/text/lisbon_av.txt'))

    c2 = f.Circle(
        radius=INNER_RADIUS,
        location=LISBON_COORDINATES,
        popup='',
        color=CRIMSON,
        fill=False,
        )

    cm2 = f.CircleMarker(
        radius=OUTER_RADIUS,
        location=LISBON_COORDINATES,
        popup=make_popup(popups_cache.get(None)[LISBON_COORDINATES]),
        color=colors_cache.get(LISBON_COORDINATES),
        fill=True,
        fill_color=colors_cache.get(LISBON_COORDINATES)
        )

    return [c1,cm1,c2,cm2]

def add_vdg(map, vdg_color):
    """
    Add Vasco da Gama's departure locations to map.
    """
    ORIG_VDG_COLOR = vdg_color


    # first + second? voyages under the service of Portugal
    LISBON_COORDINATES = (38.7223, -9.1393)
    # update caches
    update_colors_cache(LISBON_COORDINATES, ORIG_VDG_COLOR)
    update_popups_cache(LISBON_COORDINATES, load_popup_content('templates/data/photos/daGama.jpg','templates/vdg.html', 'templates/data/text/lisbon_vdg.txt'))

    c1 = f.Circle(
        radius=INNER_RADIUS,
        location=LISBON_COORDINATES,
        popup='',
        color=CRIMSON,
        fill=False,
        )

    cm1 = f.CircleMarker(
        radius=OUTER_RADIUS,
        location=LISBON_COORDINATES,
        popup=make_popup(popups_cache.get(None)[LISBON_COORDINATES]),
        color=colors_cache.get(LISBON_COORDINATES),
        fill=True,
        fill_color=colors_cache.get(LISBON_COORDINATES)
        )

    return [c1,cm1]

def add_pb(map):
    """
    Add Pierre Belon's departure locations to map.
    """
    pass
    """
    
    ORIG_PB_COLOR = ''

    # ????
    ??????_COORDINATES = []
    if ??????_COORDINATES in LOCATIONS:
        r1, g1, b1 = hex_to_rgb(ORIG_PB_COLOR)
        r2, g2, b2 = hex_to_rgb(LOCATIONS[??????_COORDINATES])
        # average RGB values
        res = ((r1+r2) // 2), ((g1+g2) // 2), ((b1+b2) // 2)
        # convert back to hex and ensure proper formatting (pad w/ 0s)
        for i in range(len(res)):
            if len(res[i]) < 2:
                res[i] = '0' * (2-len(res[i])) + res[i]

        PB_COLOR = '#' + ''.join(res)
        LOCATIONS[???_COORDINATES] = PB_COLOR
    else:
        VDG_COLOR = PB_VDG_COLOR

    f.Circle(
        radius=INNER_RADIUS,
        location=None,
        popup='',
        color=CRIMSON,
        fill=False,
        ).add_to(map)

    f.CircleMarker(
        radius=OUTER_RADIUS,
        location=None,
        popup='',
        color=PB_COLOR,
        fill=True,
        fill_color=PB_COLOR
        ).add_to(map)
        """

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

