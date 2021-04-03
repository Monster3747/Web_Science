import requests
import re
import json


def download(address):
    root = './medias/'
    for i in range(0,5):
        file_name = address[i].split('/')[-1]
        file_name = re.sub(r'\?.*', '', file_name)
        print("download process: %s" % file_name)
        r = requests.get(address[i], stream=True).iter_content(chunk_size=1024 * 1024)
        with open(root + file_name, 'wb') as f:
            for chunk in r:
                if chunk:
                    f.write(chunk)
        print("%s complete!\n" % file_name)
    print("all finish!")
    return

if __name__ == "__main__":
    photoLinks= []
    videoLinks = []
    gifLinks = []

    with open('./data/StreamData.json', 'r', encoding='utf-8') as data:
        Data = json.load(data)
        for i in range(0, len(Data)):
            if Data[i]['media_type'] == "photo":
                    photoLinks.append(Data[i]['media_url'])
            elif Data[i]['media_type'] == "video":
                    videoLinks.append(Data[i]['media_url'])
            elif Data[i]['media_type'] == "animated_gif":
                    gifLinks.append(Data[i]['media_url'])
        download(photoLinks)
        download(videoLinks)
        download(gifLinks)