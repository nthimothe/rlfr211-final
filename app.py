from flask import Flask, render_template, request
from markupsafe import escape
from constants import *
import folium as f
from cache import colors_cache, popups_cache
from helpers import *
"""
Flask app hosted at [________]
Valid paths include:
    - `\`
    - `\about`
    - `\citations`
    - `map_render`
"""

app = Flask(__name__)

# maps lat,lon tuples to hex colors
colors_cache.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 0})
# maps None to dict of lat,lon tuples to appropriate pop up messages
popups_cache.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 0})
popups_cache.add('',['map','0'])
popups_cache.add(None,dict())

@app.route('/', methods=['GET', 'POST'])
def root():
    cc_color = ORIG_AV
    av_color = ORIG_CC
    vdg_color = ORIG_VDG
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

@app.route('/map_render')
def map_render():
    name = ''.join(popups_cache.get(''))
    return render_template(name + '.html')
    
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

if __name__ == "__main__":
    app.run()
