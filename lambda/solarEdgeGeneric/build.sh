#! /bin/bash -xe
#pigar
rm -rf my-deployment-package.zip package
pip3 install --target ./package -r requirements.txt  --upgrade
cd package
zip -q -r ../my-deployment-package.zip .
cd ..
zip -q -g my-deployment-package.zip lambda_function.py
