#!/bin/bash

sudo apt update
sudo apt install r-base

wget https://cran.r-project.org/src/contrib/clhs_0.9.0.tar.gz
wget https://cran.r-project.org/src/contrib/Archive/terra/terra_1.7-28.tar.gz
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