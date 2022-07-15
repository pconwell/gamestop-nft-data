#!/bin/bash

cd /root/gamestop-nft-data/

git pull origin main

/usr/bin/python3 /root/gamestop-nft-data/gs_nft_api.py

git add .
git commit -m "update csv and rotate logs"
git push origin main
