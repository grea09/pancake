# Pancake
Using Tectonic + Pandoc + custom filters for scientific writing. 
This project is a docker image that contains various tools to write scientific papers in Markdown.
All this is made for [Pandoc v2.7](https://github.com/jgm/pandoc).

# General organisation

## Filters
### pandoc-science
Main component for scientific writing. It is an old personnal filter I recoded recently.
Strongly inspired by [pandoc-amsthm](https://github.com/ickc/pandoc-amsthm) it mainly add cref support.
Here is an example of its usage with the fenced divs of Pandoc 2 :

        ::: {.definition #def:resolver name="Resolvers"}
        A resolver is a potential causal link defined as a tuple $r = \langle a_s, a_t, f\rangle$
        ::::::::::::::::::::::::::::::::::::::::::::::::
        
Also, one can use code blocks to write pseudocode using

        ~~~ {.algorithm #alg:example name="A smart caption" startLine="1"}
        \Function{example}{Stuff $s$, Problem $\mathcal{P}$} \EndFunction
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### pandoc-crossref
Filter used to make smart cross references. Compiled version from latest version of this [github repository](https://github.com/lierdakil/pandoc-crossref)

### pandoc-table
Filter used to be able to use tables in two-column mode, adapted from [here](https://groups.google.com/forum/#!msg/pandoc-discuss/RUC-tuu_qf0/h-H3RRVt1coJ).

# Docker

The image will have most useful tools for writing scientific papers using markdown. It uses tectonic that downloads all dependancies as needed. You will need to mount your work directory in `/doc` and Pancake will scan for files in it to convert.
