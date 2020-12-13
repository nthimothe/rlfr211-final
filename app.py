# (c) 2020 nt
from flask import Flask, render_template, request, session
from markupsafe import escape
from constants import *
import folium as f
from helpers import *
import uuid 
import os
import config

"""
Flask app hosted at https://explorateurs.herokuapp.com/
Valid paths include:
    - `\`
    - `\about`
    - `\citations`
    - `map_render`
"""

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG
app.config['TEMPLATES_AUTO_RELOAD'] = config.TEMPLATES_AUTO_RELOAD

@app.before_request
def set_session():
    session.permanent = True

@app.route('/', methods=['GET', 'POST'])
def root():
    cc_color = ORIG_AV
    av_color = ORIG_CC
    vdg_color = ORIG_VDG
    # if colors are being submitted, redefine color vars
    if request.method == 'POST':
        clear_colors_cache()
        cc_color = request.form['cc_color']
        av_color = request.form['av_color']
        vdg_color = request.form['vdg_color']
    # if the user has already visited the site, set visited key + create a unique_dir_id for them, else access existing unique_dir_id
    unique_dir_id = get_dir_id()
    make_dir(unique_dir_id)
    # set colors cache, if it does not yet exist
    set_colors_cache()

    map(cc_color,av_color,vdg_color, os.path.join(unique_dir_id, 'map.html'))

    # update the html so the default value is what the user last entered
    return render_template(
        FORMATTED_MAP,
        value1=cc_color,
        value2=av_color,
        value3=vdg_color,
        )

@app.route('/map_render')
def map_render():
    assert 'visited' in session, "'visited' must be in session dict"
    return render_template(os.path.join(session['dir'], 'map.html'))
    
@app.route('/about')
def about():
    return render_template(ABOUT)

@app.route('/about_text')
def about_text():
    """
    Post ABOUT_TEXT as '/about_text' so JS can load the HTML into elementID id.
    """
    return render_template(
        'data/text/jinja_about_template.txt',
        lines=ABOUT_TEXT
    )

@app.route('/citations_text')
def citation_text():
    """
    Post CITATION_TEXT at '/citation_text' so JS can load the HTML into elementID id.
    """
    return render_template(
        'data/text/jinja_about_template.txt',
        lines=CITATION_TEXT
    )

@app.route('/citations')
def citations():
    return render_template(CITATIONS)

def map(cc_color,av_color,vdg_color, name="map.html"):
    """
    Creates a new map using appropriate color parameter for each explorer.
    cc_color : Color for Christopher Columbus's departure locations.
    av_color : Color for Amerigo Vespucci's departure locations.
    vdg_color : Color for Vasco da Gama's departure locations.
    """
    import os
    import random
    coordinates = [PALOS_COORDINATES, CADIZ_COORDINATES, LISBON_COORDINATES, SAN_LUC_COORDINATES]

    map = f.Map(
        location=coordinates[random.randrange(len(coordinates))],
        zoom_start = 12, 
        min_zoom = 2, 
        tiles = 'CartoDB positron',
        max_bounds=True
        )
    cc = add_cc(map, cc_color)
    av = add_av(map, av_color)
    vdg = add_vdg(map, vdg_color)

    # add all circles and circle markers to the map
    for each in [cc, av, vdg]:
        for item in each:
            item.add_to(map)
    map.save(os.path.join('templates', name))


def add_cc(map, cc_color):
    """
    Add Christopher Columbus's departure points to map.
    """
    # user color (originally some shade of blue)
    CC_COLOR = cc_color

    # first voyage
    # update cache -- if a coordinate is already mapped to a color, average colors, else map coordinates to color
    update_colors_cache(PALOS_COORDINATES, original_color=CC_COLOR)

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
        popup=make_popup(PALOS_HTML),
        color=CC_COLOR,
        fill=True,
        fill_color=CC_COLOR
        )


    # second, fourth voyages
    # update colors cache
    update_colors_cache(CADIZ_COORDINATES, CC_COLOR)

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
        popup='',
        color=CC_COLOR,
        fill=True,
        fill_color=CC_COLOR
        )


    # third voyage
    # update colors cache
    update_colors_cache(SAN_LUC_COORDINATES, CC_COLOR)
   
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
        popup=make_popup(SANLUCAR_HTML),
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
    # update colors cache
    update_colors_cache(CADIZ_COORDINATES, ORIG_AV_COLOR)

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
        popup=make_popup(CADIZ_HTML),
        color=session['colors_cache'][str(CADIZ_COORDINATES)],
        fill=True,
        fill_color=session['colors_cache'][str(CADIZ_COORDINATES)]
        )


    # second voyage under the service of Portugal
    # update caches
    update_colors_cache(LISBON_COORDINATES, ORIG_AV_COLOR)

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
        popup='',
        color=session['colors_cache'][str(LISBON_COORDINATES)],
        fill=True,
        fill_color=session['colors_cache'][str(LISBON_COORDINATES)]
        )

    return [c1,cm1,c2,cm2]

def add_vdg(map, vdg_color):
    """
    Add Vasco da Gama's departure locations to map.
    """
    ORIG_VDG_COLOR = vdg_color

    # first + second? voyages under the service of Portugal
    # update caches
    update_colors_cache(LISBON_COORDINATES, ORIG_VDG_COLOR)
   
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
        popup=make_popup(LISBON_HTML),
        color=session['colors_cache'][str(LISBON_COORDINATES)],
        fill=True,
        fill_color=session['colors_cache'][str(LISBON_COORDINATES)]
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
