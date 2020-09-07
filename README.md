# Pancake
Using Tectonic + Pandoc + custom filters for scientific writing.
This project is a docker image that contains various tools to write scientific papers in Markdown.
All this is made for [Pandoc v2.9](https://github.com/jgm/pandoc).

# Usage

This project is a [Docker container](https://www.docker.com/). This means that Pancake runs in a containerized machine based on Alpine linux. Inside that container, tools needed to use Pandoc and Tectonic are installed. In order to launch Pancake on a project, you first need to [install docker](https://docs.docker.com/get-docker/). Then to run the converter use the following command:

        docker run -d -v $PWD:/data -e PANDOC_OPTIONS="--listings --top-level-division=chapter --number-sections" -e PANDOC_OUTPUT="thesis.pdf" -e PANDOC_INPUT="*.md" --name pancake grea09/pancake

The following options may be of use:

* `-v`: volume mount. Use `/data` as the working directory.
* `PANDOC_OPTIONS`: options to give to `pandoc`
* `PANDOC_INPUT`: input files to be converted
* `PANDOC_OUTPUT`: output file
* `PANDOC_FROM`: input format, if unspecified it is inferred from input's extension.
* `PANDOC_EXTENSIONS`: additional pandoc extensions to add to the format (e.g. `markdown+hard_line_breaks`).
* `PANDOC_TO`: output format, if unspecified it is inferred from output's extension.
* `PANCAKE_ONCE`: if defined, will end the container after the first conversion attempt. Otherwise, `pandoc` will be invoked on every file change until the container is manually stopped.

# Configuration

Pancake will search for `.yaml` files in the working directory. For convenience, you may put them in a `styles` folder. All style files will be read in the alphabetical order. The YAML files can contain any Pandoc metadata variables (except for font specification).

## Font specification

To specify a font you need to define it either using Pandoc's `fontfamily` variable or using the following:

        fonts:
          timesnew: Times New Roman
          foo:
            font: Arial # Main font
            regular: Arial
            italic: Arial Italic
            bold: Arial Black
            bold-italic: Arial Bold Italic
            slanted: Verdana
            bold-slanted: Verdana Bold
            smallcaps: Times New Roman
            scale: 1.2
            options: #fontspec options as a string list

The name of the font will be the key suffixed with `font` (here `\timesnewfont` & `\foofont` respectively). To define default fonts, name your font one of the following:

        main:
        sans:
        mono:
        math:
        cjk:

Additional fonts will be loaded from the `/data/fonts` folder. To list the available fonts, execute the `fc-list` inside the container using `docker exec` while it is running.

## Element style

In order to change the appearance of the different elements in the document one must use the following:

        elements:
          my-element:
            theorem: #or
            block: true
            koma: true #Koma element
            prefix:
             - singularForm
             - pluralForm
            ref: shortcode for refs
            preposition: of #Between prefix and name
            font: macroFontName
            color: Blue
            title:
              font: \anotherMacro
              background: Grey
            style:
            border:
            background:
            options: #latex options as a string list
            number: section

The following elements can be styled:

        quote: # Title is lettrine
        code: #verbatim code
        algorithm: #Enables algorithmx
        document: #Title is main title, number is page number and only box.background change the page color. Style is pagestyle.
        chapter:
        section:
        figure:
        table:
        equation:

### Document

For the document element, here is the list of handled options:

* `style`: documet class
* `color`: text color
* `background`: page color
* `options`: class options like `a4paper` and such.

### Theorems

This part will use `tcolorbox` to generate theorem like blocks. Please refer to the (package documentation)[http://www.texdoc.net/texmf-dist/doc/latex/tcolorbox/tcolorbox.pdf].

### Blocks

Will generate classical block LaTeX code using `begin` and `end`.

### Koma

This setting allows to style default KOMA class elements like `section` or `chapter`. The style is applied as part of the `\addtokomafont` command. Don't forget the `font` prefix added when defining fonts in Pancake. The `style` element is passed as a latex command.

## List options

Several lists of elements can be used in each document. Lists are tables that enumerates elements of a certain type and some of their properties. For example list of figures with their caption or various table of content or glossary. To change their display, use the following:

        lists:
          my-list: #Enables the list
            title: Super List
            depth: 4
            level: chapter #Heading of the list
            columns: 3 #Requires multicol
            linkcolor: solarized-base1

Here is the list of lists:

        glossary:
        figures:
        content:
        tables:

## Links color

In order to change the default link colors, one must use the following:

        colorlinks:
          link: solarized-blue
          file: solarized-magenta
          cite: solarized-green
          url: solarized-cyan

## Latex Commands

For convenience, a new latex command parameter has been added to define custom LaTeX command:

        macro:
          - name: raw LaTeX definition
          - bb: \mathbb
          …

# Filters

## Glossary

Glossaries are used in two steps: definition and usage. The glossary is defined in a `.yaml` configuration file. It can be put in a separate file or defined in the main configuration file as follows :

        glossary:
          acronyms:
            - FOO: First On Observation
          symbols:
            - label: bar
              symbol: _
              description: An example symbol
          entries:
            - name: trivial
              description: Complicated word to say simple.

Once defined, you may use the following notation to reference a word/acronym/symbol in your text:

        A few <+trivialS> ways to express examples can be done when <+foo> using the <-bar> notation.

The behavior can be modified in a few ways:

* +/- at the start of the `<>` notation is used for the entry type:
  + + for linked reference
  - - for text only reference
* Capitalisation of the first letter of the reference to use the capitalized form
* Adding a upper case `S` at the end of the reference for plural form.

## Pseudocode

Also, one can use code blocks to write pseudocode using `algpseudocode`:

        ~~~ {.algorithm #alg:example name="A smart caption" startLine="1"}
        \Function{example}{Stuff $s$, Problem $\mathcal{P}$} \EndFunction
        ~~~
