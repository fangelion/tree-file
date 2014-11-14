#! /usr/bin/env python3

# tree.py
#
# author: Bugaevsky Igor
#
#


from os import listdir, sep
from os.path import abspath, basename, isdir
from sys import argv, platform

# Имя файла со стилем
css_style = "_styles.css"
# та же папка для иконок
icons_dir = "."
if platform == "win32":
    codepage = "CP-1251"
else:
    codepage = "UTF-8"
site_template = {
    "head": """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\"\
 \"http://www.w3.org/TR/html4/strict.dtd\">
<html lang=\"ru-RU\"><head><meta http-equiv=\"Content-Type\"\
 content=\"text/html;charset=""" + codepage + """\"><!--[if gte IE 9 ]>\
 <link rel=\"stylesheet\" type=\"text/css\" href=\"_styles.css\"\
  media=\"screen\"><![endif]-->
<!--[if !IE]>--><link rel=\"stylesheet\" type=\"text/css\"\
 href=\"""" + css_style + """\" media=\"screen\"><!--<![endif]-->\
</head>""",
    "title_begin": "<body><div id=\"titled\"><p>",
    "title_end": "</p></div>\n",
    "tree_begin": "<ol class=\"tree\">\n",
    "file": ["<li class=\"file\">", "</li>\n"],
    "dir_begin": "<li><label for=\"folder",
    "dir_in_1": "\">",
    "dir_in_2": "</label> <input type=\"checkbox\" checked id=\"folder",
    "dir_in_3": "\" /><ol>\n",
    "dir_end": "</ol></li>\n",
    "end": "</ol></body></html>"
}
num = 0
data = ""


def link(full_path):
    return("<a href=\"" + full_path + "\">" + basename(full_path) + "</a>")


def tree(dir):
    global num
    global data
    global dwalk
    path = dir + sep
    dirs = []
    files = []
    #data = ""
    for fl in listdir(dir):
        if isdir(path + fl):
            dirs.append(path + fl)
        else:
            files.append(path + fl)
    data += site_template["dir_begin"] + str(num) +\
        site_template["dir_in_1"] +\
        link(dir) + site_template["dir_in_2"] + str(num) +\
        site_template["dir_in_3"]
    num += 1
    dirs.sort()
    files.sort()
    if len(dirs) > 0:
        for sing in dirs:
            tree(sing)
    if len(files) > 0:
        for sing in files:
            data += site_template["file"][0] + link(sing) + site_template["file"][1]
    data += site_template["dir_end"]


def start(dir, dpath=""):
    global data
    data += site_template["head"]
    data += site_template["title_begin"] + dir + site_template["title_end"]
    data += site_template["tree_begin"]
    #dwalk = walk(dir)
    tree(dir)
    data += site_template["end"]
    with open(dpath + sep + "index.html", "w") as site_file:
        site_file.write(data)


def usage():
    return '''Usage: %s [-f] <PATH>
Print tree structure of path specified.
Options:
-f      Print files as well as directories
PATH    Path to process''' % basename(argv[0])


def main():
    if len(argv) == 1:
        print(usage())
    elif len(argv) == 2:
        # print just directories
        path = argv[1]
        if isdir(path):
            start(abspath(path))
        else:
            print('ERROR: \'' + path + '\' is not a directory')
    elif len(argv) == 3:
        # print directories and files
        path = argv[1]
        if isdir(path):
            start(abspath(path), argv[2])
        else:
            print('ERROR: \'' + path + '\' is not a directory')
    else:
        print(usage())

if __name__ == '__main__':
    main()
