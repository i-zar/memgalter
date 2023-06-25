#!/bin/bash

rm telethon-lambda-package.zip
cd lib/python3.10/site-packages
zip -r ../../../telethon-lambda-package.zip .
cd ../../../
zip -r telethon-lambda-package.zip lambda_function.py