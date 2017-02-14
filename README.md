# Pancake
![Pancakes !](pancake_inline.svg)

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

# Dependencies

Instructions writen mainly for Ubuntu 16.04.

## apt
###Packages to install :

`sudo apt install xzdec pandoc pandoc-citeproc inotify-tools python python-pip python3-pip`

###LaTeX [not compatible with tlmgr]:

* `sudo apt install texlive-latex-base texlive-fonts-recommended texlive-science`
* [optional] `sudo apt install texlive-latex-extra texlive-generic-extra`

## latex
###Automatic LaTeX install [ubuntu] :

`cd /tmp && wget https://github.com/scottkosty/install-tl-ubuntu/raw/master/install-tl-ubuntu && chmod +x ./install-tl-ubuntu && sudo -H ./install-tl-ubuntu`

###Manual Latex install [generic]:

```
cd /tmp
wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
tar -xzvf install-tl-unx.tar.gz #or use dtrx
cd install-tl-unx
sudo -H ./install-tl #customize what you need
sudo echo "PATH=PATH=/usr/local/texlive/2016/bin/:$PATH" >> /etc/environement
PATH=PATH=/usr/local/texlive/2016/bin/:$PATH
```

###CTAN package :
`sudo tlmgr install xcolor-solarized`

## python
###Python packages :

* `pip install pandocfilters`
* `pip3 install --upgrade git+https://github.com/msprev/panzer`

# Installation

## git

clone the repository in `~/.panzer` (backup the previous folder if needed)
`git clone https://github.com/grea09/pancake.git ~/.panzer`

## bin

Simply copy the script in `./bin/pancake` to the system (somewhere like `/usr/local/bin/`)
`sudo cp ~/.panzer/bin/pancake /usr/local/bin/`

### Usage

`pancake FILE FORMAT`
* FORMAT : odt, tex, pdf (generate pdf file for each method)

To manage styles please refer to [Panzer](https://github.com/msprev/panzer).
For more syntax information please refer to [Pandoc 1.18](https://github.com/jgm/pandoc).
