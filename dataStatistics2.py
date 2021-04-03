import json

rest_id = []
stream_id = []
rest_amount = 0
rest_retweet = 0
rest_geo = 0
rest_quote = 0
rest_video = 0
rest_photo = 0
rest_place = 0
rest_gif = 0
rest_verified = 0
with open('./data/DataRest.json', 'r', encoding='utf-8')as f:
    try:
        while True:
            line = f.readline()
            if line:
                d = json.loads(line)
                rest_id.append(d['uid'])
                rest_amount += 1
                if d['retweet'] == True:
                    # print(d['retweet'])
                    rest_retweet += 1

                if d['geoenabled'] == True:
                    rest_geo += 1
                if d['location']:
                    rest_place += 1
                if d['verified'] == True:
                    rest_verified += 1
                if d['quote'] == True:
                    rest_quote += 1
            else:
                break
    except Exception as e:
        print(e)





stream_amount = 0
stream_retweet = 0
stream_geo = 0
stream_quote = 0
stream_video = 0
stream_photo = 0
stream_place = 0
stream_gif = 0
stream_verified = 0
with open('./data/DataStream.json', 'r', encoding='utf-8')as f:
    while True:
        line = f.readline()
        # print(line)
        if line:
            d = json.loads(line)
            stream_id.append(d['_id'])
            stream_amount += 1
            media = d['media']
            # print(media)
            if d['retweet'] == True:
                # print(d['retweet'])
                stream_retweet += 1
            if d['geoenabled'] == True:
                stream_geo += 1
            if d['location']:
                stream_place += 1
            if media == ['photo']:
                stream_photo += 1
            if d['videoLinks']:
                stream_video += 1
            if media == 'animated_gif':
                stream_gif += 1
            if d['verified'] == True:
                stream_verified += 1
            if d['quote'] == True:
                stream_quote += 1
        else:
            break
count = 0
print(len(rest_id))
print(len(stream_id))
for i in stream_id:
    for j in rest_id:
        if i == j:
            count = count + 1
print('redundant data', count)
print("total amounts of streaming:", stream_amount)
print("total amounts of rest:", rest_amount)
print("tweets with geo-tag :", rest_geo + stream_geo)
print("tweets with locations/Place Object:", rest_place + stream_place)
print("Tweets with images:", stream_photo)
print("Tweets with videos:", stream_video)
print("tweets verified:", rest_verified + stream_verified)
print("tweets animated_gif:", stream_gif)
print("Tweets with retweets:", rest_retweet + stream_retweet)
print("Tweets with quotes:", rest_quote + stream_quote)
