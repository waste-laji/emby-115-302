import flask,requests,hashlib
from flask import request, redirect
from flask_cors import CORS
#仅适用 emby 4.8.0.39 版本及以下版本
#emby信息
emby_url = "http://127.0.0.1:8096"
emby_key = ""

#alist地址
alist_local=""
alist_Global=""
#alist-管理-设置-其他-令牌
alist_token=""

app = flask.Flask(__name__)



def alist(local):
    url = alist_local+"/api/fs/get"
    h = {
    "authorization":""+alist_token
    }

    '''
    将视频路径替换为alist直链地址
    emby视频路径: /home/gdrive/国产剧/123/123.MP4
    alist路径:  /drive/gdrive/gd/国产剧/123/123.MP4
    '''
    if "/home/gdrive" in local:
        local=""+str(local).replace("/home/gdrive","")
    elif "/home/remux" in local:
        local="/drive/gdrive/REMUX"+str(local).replace("/home/remux","")

    data={
      "path": local,
      "password": "",
      "page": 1,
      "per_page": 0,
      "refresh": False
    }
    
    res = requests.post(url,json=data,headers=h).json()
    print(res)
    raw_url = alist_Global+"/d"+local+"?sign="+res['data']['sign']
    

    return raw_url




@app.route('/emby/videos/<item_Id>/stream.<type>',methods=["GET"])
def handle_request(item_Id,type):
    MediaSourceId = request.args.get("MediaSourceId")
    api_key = request.args.get("api_key")
    

    if api_key:
        # 非Infuse
        itemInfoUri = f"{emby_url}/Items/{item_Id}/PlaybackInfo?MediaSourceId={MediaSourceId}&api_key={api_key}"
        print(itemInfoUri)
        emby_path = fetchEmbyFilePath(itemInfoUri,MediaSourceId)

        raw_url = alist(emby_path)

        return redirect(raw_url)
    else:
        # Infuse
        itemInfoUri = f"{emby_url}/Items/{item_Id}/PlaybackInfo?MediaSourceId={MediaSourceId}&api_key={emby_key}"
        emby_path = fetchEmbyFilePath(itemInfoUri,MediaSourceId)

        raw_url = alist(emby_path)

        return redirect(raw_url)

@app.route('/Videos/<item_Id>/stream',methods=["GET"])
def handle_request2(item_Id):
    MediaSourceId = request.args.get("MediaSourceId")
    api_key = request.args.get("api_key")

    if api_key:
        # 非Infuse
        itemInfoUri = f"{emby_url}/Items/{item_Id}/PlaybackInfo?MediaSourceId={MediaSourceId}&api_key={api_key}"
        emby_path = fetchEmbyFilePath(itemInfoUri,MediaSourceId)

        raw_url = alist(emby_path)

        return redirect(raw_url)
    else:
        # Infuse
        itemInfoUri = f"{emby_url}/Items/{item_Id}/PlaybackInfo?MediaSourceId={MediaSourceId}&api_key={emby_key}"
        emby_path = fetchEmbyFilePath(itemInfoUri,MediaSourceId)

        raw_url = alist(emby_path)

        return redirect(raw_url)


#yamby
@app.route('/videos/<item_Id>/stream.<type>',methods=["GET"])
def handle_request3(item_Id,type):
    MediaSourceId = request.args.get("MediaSourceId")
    api_key = request.args.get("api_key")
    
    if api_key:
        # 非Infuse
        itemInfoUri = f"{emby_url}/Items/{item_Id}/PlaybackInfo?MediaSourceId={MediaSourceId}&api_key={api_key}"
        print(itemInfoUri)
        emby_path = fetchEmbyFilePath(itemInfoUri,MediaSourceId)

        raw_url = alist(emby_path)

        return redirect(raw_url)
    else:
        # Infuse
        itemInfoUri = f"{emby_url}/Items/{item_Id}/PlaybackInfo?MediaSourceId={MediaSourceId}&api_key={emby_key}"
        emby_path = fetchEmbyFilePath(itemInfoUri,MediaSourceId)

        raw_url = alist(emby_path)

        return redirect(raw_url)





def fetchEmbyFilePath(itemInfoUri,MediaSourceId):
    # 获取Emby内文件路径
    req = requests.get(itemInfoUri)
    resjson = req.json()
    for i in resjson['MediaSources']:
        if i['Id'] == MediaSourceId:
            mount_path = i['Path']
    return mount_path


# 在Flask应用中启用CORS
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(port=60000,debug=True,host='0.0.0.0',threaded=True) 