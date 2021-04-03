# Web_Science

**Program running environment:**

`Python version:3.8.3 (default, Jul  2 2020, 17:30:36)  [MSC v.1916 64 bit (AMD64)]`
`tweepy version:3.10.0`
`pymongo version:3.11.2`
`emoji version:0.6.0`
`requests version:2.25.1`
`numpy version:1.19.2`
`nltk version:3.4.5`


##### **<u>`dataCrawl.py`</u>**

------

**What it does: Data can be crawled through the Streaming API and rest API and stored in the MongoDB database. **

`./data/StreamData.json` : The first Streaming API crawls data stored in this file.
`./data/DataStream.json` : The second Streaming API crawls data stored in this file.
`./data/DataRest.json`:REST API crawls data stored in this file.

------

##### **<u>`dataStatistics.py`</u>**

------

**What it does: Count the data that has been crawled through the Streaming API. **

`./data/StreamData.json`: Data crawled in this file

------

##### **<u>`dataStatistics2.py`</u>**

------

**What it does: Count the data that has been crawled through the hybrid architecture of Streaming & REST APIs. **

`./data/DataStream.json` : The data stored in this file.
`./data/DataRest.json`:The data stored in this file.

------

##### **<u>`dataGrouping.py`</u>**

------

**What it does: local sensitive hash algorithm is used for Twitter text clustering **

`./data/StreamData.json`: Read the raw data from this folder and cluster it.

------

##### **<u>`dataDowload.py`:</u>**

------

**What it does: Download the media from the crawled data locally. **

`./data/StreamData.json`: Obtaining the data from this folder.

------

