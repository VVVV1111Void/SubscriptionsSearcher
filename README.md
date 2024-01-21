### Purpose and Scope
When searching on youtube for videos, we are not able to search within channels or groups of channels. There are other solutions, such as using extensions (PocketTube). However, I saw that they were quite slow.

The purpose of this tool is to allow users to search for videos only within their subscription list.

### Usage
#### Setup the input data
Using this tool requires the use of the Takeout option for youtube subscriptions. For further instruction, refer to newpipe's tutorial on how to get a google takeout of youtube subscriptions. The same type of file used to import subscriptions can be used here.

The takeout should be a csv file. It should be placed in the directory and be named "input.csv"

#### Preparation
Install sqlite and yt-dlp. The output will be an sqlite database.

First, run db.py to initialize the database to create the file.

```
python3 ./db.py
```

Afterwards, run the searcher.py to perform the scraping.

```
python3 ./searcher.py
```

Note: If broken, please delete the cache and db as incremental updates are still WIP.


### WIP
auto-open takeout in the browser and allow users to point to the file