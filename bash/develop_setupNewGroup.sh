#!/bin/bash

greengo remove 2>/dev/null 
rm -rf .gg/
rm -rf certs/
rm -rf config/
greengo create
aws s3 cp certs/ s3://gg-project-files-bf/certs --recursive
aws s3 cp config s3://gg-project-files-bf/config --recursive
aws s3 cp .gg s3://gg-project-files-bf/.gg --recursive