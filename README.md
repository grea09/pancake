# Pancake
![](https://raw.githubusercontent.com/grea09/pancake/master/graphics/pancake_inline.svg)
Using Panzer + Pandoc + custom filters for scientific writing. 
This project is a custom [Panzer](https://github.com/msprev/panzer) configuration folder that contains various tools to write scientific papers in Markdown.
All this is made for [Pandoc 1.18](https://github.com/jgm/pandoc).

# General organisation

## Filters
### pandoc-science
Main component for scientific writing. It is an old personnal filter I recoded recently. 
Strongly inspired by [pandoc-amsthm](https://github.com/ickc/pandoc-amsthm) it mainly add cref support.

### pandoc-crossref
Filter used to make smart cross references. Compiled version from latest version of this [github](https://github.com/lierdakil/pandoc-crossref) (2016-11-04) 

### pandoc-svg
Filter to handle SVG format in Pandoc adapted from source code found [here](https://github.com/jgm/pandoc/issues/265#issuecomment-27317316). 
I corrected some bugs and ignored Gtk warnings from Inkscape.

### pandoc-table
Filter used to be able to use tables in two-column mode, adapted from [here](https://groups.google.com/forum/#!msg/pandoc-discuss/RUC-tuu_qf0/h-H3RRVt1coJ).

# Dependancies

## apt
Packages to install on Ubuntu 16.04 (`sudo apt install`) :

<!--* texlive-science * texlive-fonts-recommended * texlive-latex-extra * texlive-generic-extra-->
* `xzdec`
* `pandoc`
* `pandoc-citeproc`
* `inotify-tools`
* `git`
* `python`
* `python-pip`
* `python3-pip`

## latex
Manual Latex install [optional]:

```
wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
dtrx install-tl-unx.tar.gz
cd install-tl-unx
sudo ./install-tl
```

CTAN package (`sudo tlmgr install`):

* `xcolor-solarized`

## python
Python packages (`pip install`) :

* `pandocfilters`

Python 3 :

* `pip3 install --upgrade git+https://github.com/msprev/panzer`

## bin

Simply copy the script in `./bin/pancake` to the system (somewhere like `/usr/local/bin/`)

* Usage : pancake FILE FORMAT
* FORMAT : odt, tex, pdf (generate pdf file for each method)
