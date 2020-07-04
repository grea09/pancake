# Pancake
Using Tectonic + Pandoc + custom filters for scientific writing.
This project is a docker image that contains various tools to write scientific papers in Markdown.
All this is made for [Pandoc v2.10](https://github.com/jgm/pandoc).

# Usage

This project is a [Docker container](https://www.docker.com/). This means that Pancake runs in a containerized machine based on Alpine linux. Inside that container, tools needed to use Pandoc and Tectonic are installed. In order to launch Pancake on a project, you first need to [install docker](https://docs.docker.com/get-docker/). Then to run the converter use the following command:

        docker run -d -v $PWD:/data -e PANDOC_OPTIONS="--listings --top-level-division=chapter --number-sections" -e PANDOC_OUTPUT="thesis.pdf" -e PANDOC_INPUT="*.md" --name pancake grea09/pancake

The following options may be of use:

* `-v`: volume mount. Use `/data` as the working directory.
* `PANDOC_OPTIONS`: options to give to `pandoc`
* `PANDOC_INPUT`: input files to be converted
* `PANDOC_OUTPUT`: output file
* `PANDOC_TYPE`: output type, if unspecified it is inferred from output's extension.
* `PANCAKE_ONCE`: if defined, will end the container after the first conversion attempt. Otherwise, `pandoc` will be invoked on every file change until the container is manually stopped.

# Configuration

Pancake will search for `.yaml` files in the working directory. For convenience, you may put them in a `style` folder. All style files will be read in the alphabetical order. The YAML files can contain any Pandoc metadata variables (except for font specification).

## Font specification

To specify a font you need to define it either using Pandoc's `fontfamily` variable or using the following:

        fonts:
          my-font:
            font: latexMacroName
            regular: Arial
            italic: Arial Italic
            bold: Arial Black
            bold-italic: Arial Bold Italic
            slanted: Verdana
            bold-slanted: Verdana Bold
            smallcaps: Times New Roman
            scale: 1.2
            color: magenta
            options: #fontspec options as a string list

To define default fonts, name your font one of the following:

        main:
        sans:
        mono:
        math:
        cjk:

## List options



# Filters

### pancake_blocks
Main component for scientific writing. It is an old personal filter that evolved a lot with time.
Strongly inspired by [pandoc-amsthm](https://github.com/ickc/pandoc-amsthm) it mainly adds cref support.
Here is an example of its usage with the fenced divs of Pandoc 2:

        ::: {.definition #def:resolver name="Resolvers"}
        A resolver is a potential causal link defined as a tuple $r = \langle a_s, a_t, f\rangle$
        ::::::::::::::::::::::::::::::::::::::::::::::::

## pancake_algorithm
Also, one can use code blocks to write pseudocode using

        ~~~ {.algorithm #alg:example name="A smart caption" startLine="1"}
        \Function{example}{Stuff $s$, Problem $\mathcal{P}$} \EndFunction
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
