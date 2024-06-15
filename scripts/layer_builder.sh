#!/bin/bash
# script to build the backend main layer

pip install -r backend/python/requirements.dev.txt -t temp_requirements
zip -r backend/backend_layer.zip temp_requirements
rm -rf temp_requirements
