# Pancake
![Pancakes !](https://antoine.grea.me/wp-content/uploads/2016/11/pancake_inline-svg.png)

Using Panzer + Pandoc + custom filters for scientific writing. 
This project is a custom [Panzer](https://github.com/msprev/panzer) configuration folder that contains various tools to write scientific papers in Markdown.
All this is made for [Pandoc 2.0.1.1](https://github.com/jgm/pandoc).

# General organisation

## Filters
### pandoc-science
Main component for scientific writing. It is an old personnal filter I recoded recently.
Strongly inspired by [pandoc-amsthm](https://github.com/ickc/pandoc-amsthm) it mainly add cref support.
Here is an example of its usage with the fenced divs of Pandoc 2 :

        ::: {.definition #def:resolver name="Resolvers"}
        A resolver is a potential causal link defined as a tuple $r = \langle a_s, a_t, f\rangle$
        :::

### pandoc-crossref
Filter used to make smart cross references. Compiled version from latest version of this [github](https://github.com/lierdakil/pandoc-crossref) (Update 2017-11-10) Since it isn't compatible for now I am using the [latest beta](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.0.0-beta2a)

### pandoc-svg
Removed as it is now included in Pandoc.

### pandoc-table
Filter used to be able to use tables in two-column mode, adapted from [here](https://groups.google.com/forum/#!msg/pandoc-discuss/RUC-tuu_qf0/h-H3RRVt1coJ).

# Dependancies

## apt
Packages to install on Ubuntu 16.04 () :

`sudo apt install xzdec librsvg2-bin inotify-tools git python3-pip`

You can also install texlive and Pandoc from the default repositories but it is outdated and will limit the possibilities of modifications needed for Pancake:
* `sudo apt install texlive-science texlive-fonts-recommended texlive-latex-extra texlive-generic-extra`
* `sudo apt install pandoc pandoc-citeproc`

## pandoc

I use the latest version of Pandoc built directly from cabal :

        cabal update
        cabal install pandoc
        cabal install pandoc-citeproc
        cabal install pandoc-crossref

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

* `pip3 install --upgrade git+https://github.com/msprev/panzer pandocfilters`

## bin

Simply copy the script in `./bin/pancake` to the system (somewhere like `/usr/local/bin/`)

* Usage : pancake FILE [FORMAT]
* FORMAT : odt, tex, pdf (default)
