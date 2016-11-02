\def\PackageName{jdt}
\def\PackageVersion{0.4}
\def\firstversion{07/05/2009}
\def\filedate{10/07/2015}
\def\docdate{10/07/2015}

\NeedsTeXFormat{LaTeX2e}

\def\fileversion{\PackageVersion}
\ProvidesClass{\PackageName}[
  \filedate \space Version:\space \PackageVersion]
\typeout{Style pour la JdT LIRIS}
\ProvidesFile{\PackageName.cls}[
  \filedate \space Version:\space \PackageVersion]


\ExecuteOptions{a4paper,twocolumn,10pt}


\LoadClass{article}

\RequirePackage{ifpdf}

\RequirePackage[english,frenchb]{babel}
\RequirePackage[utf8]{inputenc}    % pour les accents 8 bits dans le source
\RequirePackage[T1]{fontenc}       % pour les accents dans le DVI
\RequirePackage{lmodern}
\RequirePackage{fancyhdr}
\RequirePackage{url}

\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage[]{graphicx}
\RequirePackage[dvipsnames,usenames]{color}

\setlength{\textwidth}{17.5cm}
\setlength{\textheight}{25cm}


\setlength{\hoffset}{-0.75cm}       % à ajuster par dvips selon imprimante
\setlength{\oddsidemargin}{0mm}     % pour que la marge de gauche
\setlength{\evensidemargin}{0mm}    % soit exactement de 45mm
\setlength{\marginparsep}{0mm}      % soit exactement de 45mm

\setlength{\voffset}{-2cm}

%\settoheight{\headheight}{26pt}

\definecolor{topcolor}{rgb}{0.01,0.29,0.48}
\newcommand{\resume}[1]{
  \twocolumn[
    \begin{@twocolumnfalse}
      \maketitle
      \begin{abstract}
      \textbf{#1\\~\\}
      \end{abstract}
    \end{@twocolumnfalse}
  ]
  \thispagestyle{fancy}
  \lhead{\includegraphics[width=1.5cm]{graphics/liris.pdf}}
  \chead{}
  \rhead{\textcolor{topcolor}{\textbf{$9^{\text{\`eme}}$ Journée des Thèses du LIRIS, 10 novembre 2016, Villeurbanne}}}
}

\addto\captionsfrench{%
  \renewcommand{\abstractname}%
  {Résumé de la thèse}%
}
\renewcommand\familydefault{\sfdefault}

\newcommand{\auteur}[1]{\def\Vauteur{#1}}
\newcommand{\encadrants}[1]{\def\Vencadrants{#1}}
\newcommand{\anneethese}[1]{\def\Vanneethese{#1}}
\newcommand{\financement}[1]{\def\Vfinancement{#1}}
\newcommand{\equipe}[1]{\def\Vequipe{#1}}
\newcommand{\email}[1]{\def\Vemail{\url{#1}}}
\newcommand{\siteweb}[1]{\def\Vsiteweb{\url{#1}}}
\newcommand{\titre}[1]{\title{\vspace{-1cm}\textbf{#1}}}

\newcommand{\makeauthor}{\author
  {\Vauteur,~\Vencadrants\\
    ~\\ 
    {\normalsize \Vanneethese année de thèse, Financement \Vfinancement, \'Equipe \Vequipe}\\ 
    {\normalsize \Vemail~--~\normalsize\Vsiteweb}
  }
}


%\renewcommand{\subsection}{\subsection}

% Infos qui apparaissent dans les propriétés du pdf final. Reprendre les variables du .tex
\ifpdf
  \pdfinfo{
    /Title ()
    /Author ()
    /CreationDate ()
    /Subject ()
    /Keywords ()
  }
\fi
