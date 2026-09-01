\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mybraintrainer}[2025/07/19 Custom beamer class for brain training]

\LoadClass{beamer}

\setbeamertemplate{navigation symbols}{
  \hyperlink{toc}{\beamerbutton{Spis Treści}}\quad
  \insertslidenavigationsymbol
}

\setbeamertemplate{footline}{
  \leavevmode%
  \hbox{%
    \begin{beamercolorbox}[wd=\paperwidth,ht=2.5ex,dp=1ex,leftskip=1em,rightskip=1em]{author in head/foot}
      \scriptsize
      \href{https://github.com/konradcinkusz/brain-train}{\faGithub\;brain-train}
    \end{beamercolorbox}%
  }
}

\RequirePackage{geometry}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{xcolor}
\RequirePackage{multicol}
\RequirePackage{pgffor}
\RequirePackage{xparse}
\RequirePackage{tikz}
\usetikzlibrary{positioning,calc}
\RequirePackage{fontawesome5}
\RequirePackage{etoolbox}
\RequirePackage{amsmath}
\RequirePackage{amssymb}

% Category colors
\definecolor{ArithColor}{HTML}{6BAED6}
\definecolor{OpsColor}{HTML}{FD8D3C}
\definecolor{LogicColor}{HTML}{9C27B0}
\definecolor{SeqColor}{HTML}{388E3C}
\definecolor{MixColor}{HTML}{D81B60}

% Section button colors
\definecolor{sec1bg}{HTML}{6BAED6}
\definecolor{sec2bg}{HTML}{FD8D3C}
\definecolor{sec3bg}{HTML}{9C27B0}
\definecolor{sec4bg}{HTML}{388E3C}
\definecolor{sec5bg}{HTML}{D81B60}

\setbeamercolor{sec1}{fg=white,bg=sec1bg}
\setbeamercolor{sec2}{fg=white,bg=sec2bg}
\setbeamercolor{sec3}{fg=white,bg=sec3bg}
\setbeamercolor{sec4}{fg=white,bg=sec4bg}
\setbeamercolor{sec5}{fg=white,bg=sec5bg}

\AtBeginSection[]{
  \begin{frame}[allowframebreaks]{Spis treści}
    \small
    \tableofcontents[currentsection,hideothersubsections]
  \end{frame}
}
