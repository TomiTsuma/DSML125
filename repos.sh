#!/bin/bash

DO_USERNAME=tom
DO_GITHUB_USERNAME=TomiTsuma
DO_GITHUB_TOKEN=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
DO_GITHUB_EMAIL=tommytsuma7@gmail.com


git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/DSML87
git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/QC_Model_Predictions
git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/DSML94
git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/EvaluationTool
git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/MSSC_DVC_V2.git MSSC_DVC
git clone https://${DO_GITHUB_TOKEN}@github.com/Cropnuts/deep-learning-optimizer.git dl
cd dl
git checkout default-args
cd ..