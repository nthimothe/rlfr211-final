from helpers import load_popup_content
# filename constants
ROOT='root.html'
ABOUT='about.html'
FORMATTED_MAP='map_formatted.html'
CITATIONS='citations.html'

# size constants
INNER_RADIUS = 25
OUTER_RADIUS = 50

#color constant
CRIMSON = 'crimson'
ORIG_CC = '#3186cc'
ORIG_AV = '#ff2600'
ORIG_VDG = '#00ff48'

# data constants
PALOS_COORDINATES = (37.2289, -6.8954)
CADIZ_COORDINATES = (36.5271,-6.2886)
SAN_LUC_COORDINATES = (36.7726,-6.3530)
LISBON_COORDINATES = (38.7223, -9.1393)

# store text file for duration of session
ABOUT_TEXT = ""
with open('templates/data/text/about.txt', 'r') as x:
    ABOUT_TEXT = x.read()
ABOUT_TEXT = ABOUT_TEXT.splitlines()

CITATION_TEXT = ""
with open('templates/data/text/citations.txt', 'r') as x:
    CITATION_TEXT = x.read()
CITATION_TEXT = CITATION_TEXT.splitlines()


PALOS_HTML = []
_palos_files = ['templates/data/text/palos_cc.txt']
_palos_img_files = ['templates/data/photos/colomb.jpeg']
_palos_html_files = ['templates/cc.html']
for i in range(len(_palos_files)):
    text_file_path = _palos_files[i]
    img_path = _palos_img_files[i]
    html_file_path = _palos_html_files[i]
    PALOS_HTML.append(load_popup_content(img_path, html_file_path, text_file_path))
PALOS_HTML = ''.join(PALOS_HTML)

CADIZ_HTML = []
_cadiz_files = ['templates/data/text/cadiz_cc_1.txt', 'templates/data/text/cadiz_cc_2.txt', 'templates/data/text/cadiz_av.txt']
_cadiz_img_files = ['templates/data/photos/colomb.jpeg', 'templates/data/photos/colomb.jpeg', 'templates/data/photos/vespucci.jpg']
_cadiz_html_files = ['templates/cc.html', 'templates/cc.html', 'templates/av.html']
for i in range(len(_cadiz_files)):
    text_file_path = _cadiz_files[i]
    img_path = _cadiz_img_files[i]
    html_file_path = _cadiz_html_files[i]
    CADIZ_HTML.append(load_popup_content(img_path, html_file_path, text_file_path)) 
CADIZ_HTML = ''.join(CADIZ_HTML)

SANLUCAR_HTML = []
_sanlucar_files = ['templates/data/text/sanlucar_cc.txt']
_sanlucar_img_files = ['templates/data/photos/colomb.jpeg']
_sanlucar_html_files = ['templates/cc.html']
for i in range(len(_sanlucar_files)):
    text_file_path = _sanlucar_files[i]
    img_path = _sanlucar_img_files[i]
    html_file_path = _sanlucar_html_files[i]
    SANLUCAR_HTML.append(load_popup_content(img_path, html_file_path, text_file_path)) 
SANLUCAR_HTML = ''.join(SANLUCAR_HTML)

LISBON_HTML = []
_lisbon_files = ['templates/data/text/lisbon_av.txt', 'templates/data/text/lisbon_vdg.txt']
_lisbon_img_files = ['templates/data/photos/vespucci.jpg', 'templates/data/photos/daGama.jpg']
_lisbon_html_files = ['templates/av.html', 'templates/vdg.html']
for i in range(len(_lisbon_files)):
    text_file_path = _lisbon_files[i]
    img_path = _lisbon_img_files[i]
    html_file_path = _lisbon_html_files[i]
    LISBON_HTML.append(load_popup_content(img_path, html_file_path, text_file_path)) 
LISBON_HTML = ''.join(LISBON_HTML)