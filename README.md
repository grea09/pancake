# Dependencies

Packages to install on Ubuntu 14.04 (sudo apt-get install) :

<!--* texlive-science * texlive-fonts-recommended * texlive-latex-extra * texlive-generic-extra-->
* xzdec
* pandoc
* pandoc-citeproc
* inotify-tools
* git
* python
* python-pip
* python3-pip

Manual Latex install :

http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz

sudo ./install-tl

CTAN package (sudo tlmgr install ):

* xcolor-solarized

Python packages (pip install) :

* pandocfilters

Python 3 :

* pip3 install --upgrade git+https://github.com/msprev/panzer

# Install

Simply copy the script in `./bin/panzer-auto` to the system (somewhere like `/usr/local/bin/`)

# Usage

panzer-auto FORMAT FILE

* FORMAT : odt, tex, pdf (generate pdf file for each method)

