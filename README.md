-------------------

Codes to analyze Gaotu json data, mainly analyze free classes and summer/autumn classes.

## 1. extract json data to csv
python extract_json_data.py

## 2. make statistics for different class types.
python make_statistics_summer_autumn_classes.py
python make_statistics_spring_classes.py
python make_statistics_free_classes.py



Use matplotlib to draw images, steps to resolve chinese display gibberish.
1. download microsoft SimHei font file, or directly use project directory "SimHei.ttf".

2. copy "SimHei.ttf" file to your matplotlib font directory.
for my ubuntu, the location is "/home/ubuntu/.local/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/".

3. modify configuration file matplotlibrc
for my ubuntu, the location is "/home/ubuntu/.local/lib/python3.6/site-packages/matplotlib/mpl-data/matplotlibrc".
add the following text:
font.family         : sans-serif
font.sans-serif     : SimHei
axes.unicode_minus  : False

4. restart/reload python
-------------------


Uncover GSX Fraud
===========================

## Gaotu Enrollment Data

File `gaotu100-enrollment-2020-05-09-17:00:44.json` is an actual 
snapshot captured at 2020-05-09-17:00:44 UTC. You can inspect it to find the field called `enrolled_count` for each courses.

Running `get_enrollment_counts.py` would generate a new snapshot with a new timestamp, if the API is still usable by the time you run it.


## Fake User Profile Creation on Genshuixue.com

You need to find a file called `SequenceNumber.py` from certain code hosting website (did I just say Github?) and put it in this directory. Here is the magic keyword for your search `374154408`. I cannot redistribute that file.

Script `get_gsx_user_count.py` will probe and find the last
user id so far. Along the way, it will output some profile URLs
you can see for yourself whether they are fake (99.99% of the cases they are). Notice all these profiles are female.

It also prints out a list of profile URLs that are going to be created. Due to bot speed, server-side caching, distributed id generation and other factors, they may or may not have been created by the time you click them.

If you run this script periodically, you can track the user growth. The script will keep a log for you in a file named `gsx_user_count.txt`.

-------------------

A message to engineers working for GSX: it is not worth it, and you know it.