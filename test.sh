#!/bin/bash          
rm assets.db

# This is long running process
# Commenting for now
python3 idrive-tagging.py

# This is the iMac mini s3 bucket
# NickolaysMacmini
python3 idrive-tagging.py D01692572940000295373 //
python3 idrive-tagging.py D01692572940000295373 //Volumes
python3 idrive-tagging.py D01692572940000295373 //Volumes/Extreme\ Pro
python3 idrive-tagging.py D01692572940000295373 //Volumes/Extreme\ Pro/Photos\ Library

# TODO - All-Media.photoslibrary to be tagged
python3 idrive-tagging.py D01692572940000295373 //Volumes/Extreme\ Pro/Photos\ Library/All-Media.photoslibrary PhotosLibrary

# NickolaysMacBookPro
python3 idrive-tagging.py D01563711761000105006	//Users
python3 idrive-tagging.py D01563711761000105006	//Users/Shared
python3 idrive-tagging.py D01563711761000105006	//Users/nickolaycohen
python3 idrive-tagging.py D01563711761000105006	//Users/nickolaycohen/Pictures
# need to check this folder - maybe can delete from iDrive or extract of Mini, verify imported and then delete from service
# python3 idrive-tagging.py D01563711761000105006	//Users/nickolaycohen/Pictures/LightRoom\ Catalog\ and\ Data
python3 idrive-tagging.py D01563711761000105006	//Users/nickolaycohen/Pictures/Benny\ iPhone\ Download\ 05292017.photoslibrary PhotosLibrary
python3 idrive-tagging.py D01563711761000105006	//Users/nickolaycohen/Pictures/Backup\ of\ Photos\ from\ iPhoneSE\ 9May2021.photoslibrary PhotosLibrary
python3 idrive-tagging.py D01563711761000105006	//Users/nickolaycohen/Pictures/iPhone13ProMax.photoslibrary PhotosLibrary
python3 idrive-tagging.py D01563711761000105006	//Users/nickolaycohen/Pictures/Photos\ Library\ iPhone12\ 20230115.photoslibrary PhotosLibrary

# NickolaysiMac
python3 idrive-tagging.py D01563744743000489825 //Users
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures/Pipeline
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Pictures/LightRoom\ Catalog\ and\ Data
python3 idrive-tagging.py D01563744743000489825	//Users/nickolaycohen/Movies
python3 idrive-tagging.py D01563744743000489825	//Users/Shared
python3 idrive-tagging.py D01563744743000489825 //Archives
python3 idrive-tagging.py D01563744743000489825 //Pictures
python3 idrive-tagging.py D01563744743000489825	//Pictures/Photos\ Library.photoslibrary PhotosLibrary

# need to check this folder - maybe can delete from iDrive or extract of Mini, verify imported and then delete from service
# python3 idrive-tagging.py D01563744743000489825 //Pictures/iPhoneXI-Photos-Export 
python3 idrive-tagging.py D01563744743000489825 //Volumes
python3 idrive-tagging.py D01563744743000489825 //Volumes/OneTouch\ 4
python3 idrive-tagging.py D01563744743000489825 //Volumes/OneTouch\ 4/NAI\ Portable\ HDD\ temp

# ASUS
python3 idrive-tagging.py D01567232251000246054 //
python3 idrive-tagging.py D01567232251000246054 //C
python3 idrive-tagging.py D01567232251000246054 //C/DELL1TB02
python3 idrive-tagging.py D01567232251000246054 //C/RAID2
python3 idrive-tagging.py D01567232251000246054 //C/RAID2/RAID1

# iPhone (5)
python3 idrive-tagging.py R01563807439000950037 //Videos MediaSource
python3 idrive-tagging.py R01563807439000950037 //Photos MediaSource

# iPhone (3)
python3 idrive-tagging.py R01607197738000636951 //Videos MediaSource