import re
import requests
from bs4 import BeautifulSoup
from path import path

def get_author(image_id):
    html = requests.get("http://en.fotolia.com/id/" + str(image_id)).content
    print "http://en.fotolia.com/id/" + str(image_id)
    html_td = BeautifulSoup(html, "html.parser").find("div", class_="content-preview")
    return html_td.find_next('a').string

def get_category_for_id(image_id):
    html = requests.get("http://en.fotolia.com/id/" + str(image_id)).content
    html_td = BeautifulSoup(html, "html.parser").find("ol", class_="breadcrumb")
    return [x.string for x in html_td.find_all("a")]

def clean_author(author):
    return author.lower().replace(" ", "_")

def clean_category(category_list):
    def clean(category):
        return category.lower().replace("&", "and").replace(" / ", ",").replace(" ", "_").replace("__", "_")

    return "/".join([clean(x) for x in category_list])

def get_id_from_filename(filename):
    return int(FOTOLIA_REGEX.match(filename).group("id"))

SOURCE_DIR = "./Fotolia downloads/"
DESTINATION_DIR = path(SOURCE_DIR) / "_sorted"
FOTOLIA_REGEX = re.compile("^Fotolia_(?P<id>[0-9]+)_(?P<type>[^.]+).(?P<ext>.*)")

for f in path(SOURCE_DIR).files("Fotolia_*"):
    try:
        image_id = get_id_from_filename(f.name)
        author = clean_author(get_author(image_id))
    except:
        print "ERROR: " + f.name
        continue

    category = clean_category(get_category_for_id(image_id))
    print f.name + " (" + str(image_id) + ") from " + author + " in " + category

    dest = path(DESTINATION_DIR) / author / category / f.name
    if not dest.parent.exists():
        dest.parent.makedirs()
    f.move(dest)
    print dest
