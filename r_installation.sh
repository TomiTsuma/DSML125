#!/bin/bash



wget https://cran.r-project.org/src/contrib/clhs_0.9.0.tar.gz
wget https://cran.r-project.org/src/contrib/Archive/terra/terra_1.7-28.tar.gz
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
sudo apt update
sudo apt install r-base
sudo apt-get install r-base
R --version
sudo apt install libudunits2-dev
sudo apt install libgdal-dev
sudo apt install r-base-core

Rscript -e 'install.packages("prospectr")'
Rscript -e 'install.packages("sp")'
Rscript -e 'install.packages("sf")'
Rscript -e 'install.packages("raster")'
Rscript -e 'install.packages("reshape2")'
Rscript -e 'install.packages("plyr")'
Rscript -e 'install.packages("ggplot2")'
Rscript -e 'install.packages("stringr")'
Rscript -e 'install.packages("data.table", dependencies=TRUE)'
sudo R CMD INSTALL clhs_0.9.0.tar.gz
sudo R CMD INSTALL terra_1.7-28.tar.gz