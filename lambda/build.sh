#! /bin/bash
pigar -i package -c requirements.txt
pip install --target ./package -r requirements.txt  --upgrade
rm -f my-deployment-package.zip
cd package
zip -q -r ../my-deployment-package.zip .
cd ..
zip -q -g my-deployment-package.zip lambda.py

