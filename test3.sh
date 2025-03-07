#!/bin/bash          
# rm assets.db

# This is long running process
# Commenting for now
python3 src/idrive-tagging.py

# NickolaysiMac
python3 src/idrive-tagging.py D01563744743000489825	//
python3 src/idrive-tagging.py D01563744743000489825 //Users
python3 src/idrive-tagging.py D01563744743000489825	//Users/nickolaycohen
python3 src/idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures
python3 src/idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures/Pipeline
python3 src/idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures/LightRoom\ Catalog\ and\ Data
python3 src/idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures/LightRoom\ Catalog\ and\ Data/LightRoom\ Imported\ Media
# python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Movies
# python3 idrive-tagging.py D01563744743000489825	//Users/Shared
python3 src/idrive-tagging.py D01563744743000489825 //Archives
python3 src/idrive-tagging.py D01563744743000489825 //Archives/Pictures
python3 src/idrive-tagging.py D01563744743000489825 //Pictures
# python3 idrive-tagging.py D01563744743000489825	//Pictures/Photos\ Library.photoslibrary PhotosLibrary

# need to check this folder - maybe can delete from iDrive or extract of Mini, verify imported and then delete from service
# python3 idrive-tagging.py D01563744743000489825 //Pictures/iPhoneXI-Photos-Export 

python3 src/idrive-tagging.py D01563744743000489825 //Volumes
python3 src/idrive-tagging.py D01563744743000489825 //Volumes/OneTouch\ 4
python3 src/idrive-tagging.py D01563744743000489825 //Volumes/OneTouch\ 4/NAI\ Portable\ HDD\ temp

