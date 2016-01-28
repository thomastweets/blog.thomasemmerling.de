Title: Automatic LaTeX CV publishing on GitHub Pages via TravisCI
Date: 2016-01-28
Category: Tech
Tags: devops, Travis CI, GitHub Pages, git, continuous integration, LaTeX, CV

Recently, I wanted to update my CV and as I had good experiences with *LaTeX* for writing my [diploma thesis](http://dx.doi.org/10.13140/RG.2.1.1129.0644) I thought to give it a try for typesetting my CV, too. I started to remember that keeping the full LaTeX stack up-to-date and, more importantly, all package dependencies for compilation was a bit of a hassle (although there are great projects like [MacTeX](http://tug.org/mactex/) of course!). It certainly did not appeal to my desire to keep things versionized and automated. And as I had [good experiences]({filename}/automatic-pelican-publishing.md) with [Travis CI](https://travis-ci.org/) and [GitHub Pages](https://pages.github.com) I thought to give it a try for my CV, too. So, here we go.

We will use TravisCI to run a docker container that uses an image with an updated [TeX Live distribution](http://tug.org/texlive/). This docker container will then compile the file 'cv.tex' into a nice PDF file on every commit (and push) to the GitHub repository. This PDF file, in turn, is then pushed to the ```gh-pages``` branch of the repository accompanied with an index.html that displays this very PDF and (if configured) a CNAME to customize the (sub-)domain under which this beautiful CV is available. Voila!
You can see an example at [cv.thomasemmerling.de](http://cv.thomasemmerling.de).

I that was a little too fast just head over to my GitHub repository [cv-on-ghpages](https://github.com/thomastweets/cv-on-ghpages) and let me walk you through setting it up over there. It should be pretty straightforward - if not, please send me a comment, mail, tweet, issue, you name it.
And good luck with this job application!
