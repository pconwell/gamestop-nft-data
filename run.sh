#!/bin/bash

/usr/bin/python3 /root/gamestop-nft-data/gs_nft_api.py

git add .
git commit -m "updated csv"
git push origin main
