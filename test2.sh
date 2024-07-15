#!/bin/bash          
rm assets.db

# This is long running process
# Commenting for now
python3 idrive-tagging.py

# NickolaysiMac
python3 idrive-tagging.py D01563744743000489825 //Users
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures/Pipeline
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures/LightRoom\ Catalog\ and\ Data