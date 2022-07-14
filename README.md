# gamestop-nft-data

This is a very ugly, quickly put together script that will scrape the gamestop nft api every hour and save the data to a csv, then push those changes to github

*NOTE*: On the CSV file, if you see "legacy" it means that data point was collected by [kowsheek](https://github.com/kowsheek). No idea if it's right or not, but it's consistent with the later data I collected, so it's probably good. Additionally, if you see "EX", that means it's extrapolated data. In other words, it's data I made up to fill the gaps. In *other* words, it means it's almost certainly isn't reliable and should be deleted if you want to do any serious data analysis on this dataset.

Something really screwy going on with the metaboy numbers around 2022-07-14 18:01:54.821433 -- 2022-07-14 21:02:48.967848. Metaboy just suddenly dropped off the API (about 550 eth were "missing" from the numbers), but then if you pull data from the stats page, it show +1,000 something eth. Very odd... 
