### Purpose and Scope
This is a tool to narrow search results within subscriptions, as this option only appears in the searcch tool when youtube feels like it.
Another alternative tool is PocketTube, which takes too long.


### Usage
#### List down the youtube channels
For this one, use Google's takeout option. For further instruction, refer to newpipe's tutorial on how to get a google takeout of youtube subscriptions. The same type of file is used here.
#### Preparation
Install sqlite, yt-dlp. It is also recommended to use an application to navigate the output.

First, run db.py to initialize the database. This is where the videos will be listed.
Then, run searcher.py and wait for a while. After it has finished parsing everything, it will place them in the DB.
Enjoy!

Note: You will have to reset the DB every time you wish to run this program (Append and update is WIP as the main owner of the repo is busy these days. Help would be nice on making things easier.)

#### WIP
Append new videos without duplicating things
Handle the DB in a better way
