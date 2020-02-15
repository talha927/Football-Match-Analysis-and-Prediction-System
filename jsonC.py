
import json

def convert_json_format(data):
    imglst=[]
    titlelst=[]
    desclst=[]
    authorlst=[]
    contentlst=[]
    urllst=[]
    # print(json.dumps(data, indent=4, sort_keys=True))
    # print(data['status'])
    # print("Author: ",data['articles'][0]['author'])
    # print("Content: ",data['articles'][0]['content'])
    for d in data['articles']:
        authorlst.append(d['author'])
        titlelst.append(d['title'])
        desclst.append(d['description'])
        urllst.append(d['url'])
        imglst.append(d['urlToImage'])
        contentlst.append(d['content'])
        
    return authorlst,titlelst,desclst,contentlst,imglst,urllst

def convert_json_format1(data):
    imglst=[]
    titlelst=[]
    desclst=[]
    authorlst=[]
    contentlst=[]
    urllst=[]
    # print(json.dumps(data, indent=4, sort_keys=True))
    # print(data['status'])
    # print("Author: ",data['articles'][0]['author'])
    # print("Content: ",data['articles'][0]['content'])
    for d in data['articles']:
        authorlst.append(d['author'])
        titlelst.append(d['title'])
        desclst.append(d['description'])
        urllst.append(d['url'])
        imglst.append(d['urlToImage'])
        contentlst.append(d['content'])
        
    return authorlst,titlelst,desclst,contentlst,imglst,urllst


