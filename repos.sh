#!/bin/bash

echo starting
DO_USERNAME=tom
DO_GITHUB_USERNAME=TomiTsuma
DO_GITHUB_TOKEN=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
DO_GITHUB_EMAIL=tommytsuma7@gmail.com


git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/DSML87
git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/QC_Model_Predictions
git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/DSML94
git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/MSSC_DVC_V2.git MSSC_DVC
git clone https://${DO_GITHUB_TOKEN}@github.com/Cropnuts/deep-learning-optimizer.git dl