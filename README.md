# Dependencies

Packages to install on Ubuntu 14.04 (sudo apt-get install) :

* texlive-science
* texlive-fonts-recommended
* texlive-latex-extra
* xzdec
* pandoc
* pandoc-citeproc
* inotify-tools
* python
* python3-pip

CTAN package (tlmgr init-usertree && tlmgr install ):

* xcolor-solarized

Python packages (pip install) :

* pandocfilters

Python 3 :

* pip3 install --upgrade git+https://github.com/msprev/panzer

# Install

Simply copy the script in `./bin/paanzer-auto` to the system (somewhere like `/usr/local/bin/`)

# Usage

panzer-auto FORMAT FILE

* FORMAT : odt, tex, pdf (generate pdf file for each method)

