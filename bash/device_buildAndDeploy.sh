#!/bin/bash

#clone project
echo '========= Git Clone ========='
git clone https://github.com/tibernardinelli/plant-watering.git
cd plant-watering
#Get state from S3
echo '========= Get state from S3 ========='
aws s3 cp s3://gg-project-files-bf/.gg/gg_state.json .gg/gg_state.json
cat .gg/gg_state.json
#sync with greengrass
echo '========= Greengrass Sync ========='
greengo update
#deploy
echo '========= Greengrass Deploy ========='
greengo deploy
#update state
echo '========= Update State ========='
aws s3 cp .gg/gg_state.json s3://gg-project-files-bf/.gg/gg_state.json  