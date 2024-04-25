#!/bin/bash

sudo apt update
sudo apt install r-base

wget https://cran.r-project.org/src/contrib/clhs_0.9.0.tar.gz
wget https://cran.r-project.org/src/contrib/Archive/terra/terra_1.7-28.tar.gz
sudo apt install libudunits2-dev
sudo apt install libgdal-dev

