MANIFEST:
========
This scipt generates first level bucket report for all devices attached to a iDrive user account.
For each of the devices generates a csv output where directories are sorted by their size.

SETUP:
=====
- update system python3 to 3.12.3   
https://www.python.org/downloads/release/python-3123/
- install requests
> pip3 install requests

- for debugging with VS Code:
set VS default Interpreter to system Python:
    - Ex: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3  

- check if terraform is installed
  >terraform -version

- if not installed download binary from:
  https://developer.hashicorp.com/terraform/install
  for MacOS:
  https://developer.hashicorp.com/terraform/install#darwin
  https://releases.hashicorp.com/terraform/1.11.0/terraform_1.11.0_darwin_arm64.zip
  
  > mv Downloads/terraform_*_darwin_amd64/terraform /Users/nickolaycohen/bin/
  >terraform -version

- AWS CLI:
  https://aws.amazon.com/cli/
  
- aws sso temporary credentials
  https://www.youtube.com/watch?v=_KhrGFV_Npw&t=151s
  https://www.youtube.com/watch?v=YzNX_YZHPXk&ab_channel=RichDevelops

- AWS Login
  https://d-9067eed1af.awsapps.com/start/#
  - https://d-9067eed1af.awsapps.com/start/#/?tab=accounts
  - get env credential from AccessKeys link in AWS access portal page
  - add to the .aws/credential file
  
- aws commands:
  Login using existing profile
  > aws sso login --profile test

  List lambdas
  > aws lambda list-functions --region us-east-1 --query 'Functions[].FunctionName' --output text

- create deployment package
> cd src
> pip install --target . requests

RUN:
===
- login to iDrive account from web interface
- get the token from the API call
- enter the token in the constant.py file
- program has 2 parameters: first is the device index - defults to 0 if not passed
- run:> python3 idrive-web-scrape.py 2 

RUN THE TAGGING SCRIPT:
======================
- > python3 idrive-tagging.py D01692572940000295373 //Volumes
- > python3 idrive-tagging.py D01692572940000295373 //Volumes/Extreme Pro
python3 idrive-tagging.py D01692572940000295373 //Volumes/Extreme Pro/Photos Library
python3 idrive-tagging.py D01692572940000295373 //Volumes/Extreme Pro/Photos Library/All-Media.photoslibrary/database

python3 idrive-tagging.py D01692572940000295373 //Volumes/Extreme Pro/Photos Library/All-Media.photoslibrary/originals

      "args": [
        "D01692572940000295373",
        "//Volumes/Extreme Pro/Photos Library/All-Media.photoslibrary"
      ]
