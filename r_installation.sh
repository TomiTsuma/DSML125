#!/bin/bash

wget https://cran.r-project.org/src/contrib/clhs_0.9.0.tar.gz
wget https://cran.r-project.org/src/contrib/Archive/terra/terra_1.7-28.tar.gz
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
sudo apt update --assume-yes
sudo apt install r-base --assume-yes
sudo apt-get install r-base --assume-yes
R --version
sudo apt install libudunits2-dev --assume-yes
sudo apt install libgdal-dev --assume-yes
sudo apt install r-base-core --assume-yes

Rscript -e 'install.packages("prospectr")' --assume-yes
Rscript -e 'install.packages("sp")' --assume-yes
Rscript -e 'install.packages("sf")' --assume-yes
Rscript -e 'install.packages("raster")' --assume-yes
Rscript -e 'install.packages("reshape2")' --assume-yes
Rscript -e 'install.packages("plyr")' --assume-yes
Rscript -e 'install.packages("ggplot2")' --assume-yes
Rscript -e 'install.packages("stringr")' --assume-yes
Rscript -e 'install.packages("data.table", dependencies=TRUE)' --assume-yes
sudo R CMD INSTALL clhs_0.9.0.tar.gz --assume-yes
sudo R CMD INSTALL terra_1.7-28.tar.gz --assume-yes