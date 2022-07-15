# gamestop-nft-data

## Overview
This is a very ugly, quickly put together script that will scrape the gamestop nft api every hour and save the data to a csv, then push those changes to github

## How to use
The easiest thing to do is to just download the CSV file and open it with excel.

If you want to run the python script - I'll assume you are already somewhat familiar with python and know how to run a python file. The only thing you should need to change is the path of the log file and the path of the csv file inside `gs_nft_api.py`.

## Important Notes
1. All times are UTC
2. In the CSV file, if you see `Legacy` it means that data point was collected by [kowsheek](https://github.com/kowsheek). No idea if this data is accurate, but it's consistent with the later data I collected so it's probably good.
3. In the CSV file, f you see `EX`, that means it's extrapolated data. In other words, it's data I made up to fill gaps. In *other* words, it means it's almost certainly isn't reliable and should be deleted if you want to do any serious data analysis on this dataset.
4. Something really screwy going on between 2022-07-14 18:00 -- 2022-07-14 21:00:
   1. Around 2022-07-14 18:00. Metaboy just suddenly dropped off the API which accounted for approximately -550.68 eth, but...
   2. Around 2022-07-14 21:00, I was able to fix the script to pull data from the stats page (if the missing data is from one of the top 50 collections). Pulling from the stats page shows metaboy with +1058.90 eth. Since metaboy was the *only* collection missings from the API, this would suggest that metaboy had 508.22 eth in sales during that time period, but...
   3. According to metaboy's loopchain wallet, he earned 0.54569 eth during that timeframe. Even if we optimistically include transactions one hour before and after, it totals 0.738706 eth. Even if these transactions only account a certain percentage of sales (say, royalties), it's not even remotely close to the missing 508.22 eth. As in the metaboy loopring wallet optimistically accounts for 0.15% of the "missing" eth.
   4. I'm not sure what else to do, so I'm just leaving the CSV data as is. Just know that between 2022-07-14 18:00 -- 2022-07-14 21:00, the numbers are screwy.
