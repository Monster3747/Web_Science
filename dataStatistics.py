import json

dataCount = []
retweetsCount = []
quotesCount = []
photoesCount = []
videosCount = []
animated_gifCount = []
verifiedCount = []
geotagged = []
localtions = []
places = []

def statisticsData(database):

    # obtain the data
    with open('./data/'+database+'.json', 'r', encoding='utf-8') as data:
        Data = json.load(data)

    for i in range(0, len(Data)):
        if Data[i]['_id']:
            dataCount.append(Data[i]['_id'])
        if Data[i]['retweet']:
            retweetsCount.append(Data[i]['retweet'])
        if Data[i]['quote']:
            quotesCount.append(Data[i]['quote'])
        if Data[i]['media_type'] == "photo":
            photoesCount.append(Data[i]['media_type'])
        elif Data[i]['media_type'] == "video":
            videosCount.append(Data[i]['media_type'])
        elif Data[i]['media_type'] == "animated_gif":
            animated_gifCount.append(Data[i]['media_type'])
        if Data[i]['verified']:
            verifiedCount.append(Data[i]['verified'])
        if Data[i]['geo_enabled']:
            geotagged.append(Data[i]['geo_enabled'])
        if Data[i]['location']:
            localtions.append(Data[i]['location'])
        if Data[i]['city']:
            places.append(Data[i]['city'])

    return dataCount,retweetsCount,quotesCount,geotagged,localtions,photoesCount,videosCount,animated_gifCount,verifiedCount



dc,rc,qc,geo,local,pc,vc,ac,verc = statisticsData('streamData')

print("--------------------------Streaming API--------------------------------")
print("total amounts of streaming:", len(dc))
print("Tweets with retweets:", len(rc))
print("Tweets with quotes:", len(qc))
print("tweets with geo-tag :", len(geo))
print("tweets with locations Object:", len(local))
print("Tweets with images:", len(pc))
print("Tweets with videos:", len(vc))
print("tweets animated_gif:", len(ac))
print("tweets verified:", len(verc))

