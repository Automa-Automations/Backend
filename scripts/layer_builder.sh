#!/bin/bash
# script to build the backend main layer

cd backend/
pip install -r python/requirements.dev.txt -t temp_requirements
zip -r backend_layer.zip temp_requirements

DIR="./layers"

if [ -d "$DIR" ]; then
  echo "Directory $DIR already exists."
else
  echo "Directory $DIR does not exist. Creating now."
  mkdir -p "$DIR"
  echo "Directory $DIR created successfully."
fi

mv backend_layer.zip "$DIR"
rm -rf temp_requirements
