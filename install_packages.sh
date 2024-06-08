#!/bin/bash

# Navigate to the directory where requirements.txt is located
cd ./backend/python
mv requirements.ignore.txt requirements.txt

# Install dependencies
pip install -r requirements.txt -t lambdas/packages

mv requirements.txt requirements.ignore.txt
