#-------------------------
#源码来自于公众号【谭某人】
#欢迎关注，一起学习和提升
#-------------------------

import requests,json,time,re,datetime
import pandas as pd

#请求评论api接口 
def requestApi(url):  
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }
 
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    
    except requests.HTTPError as e:
        print(e)        
    except requests.RequestException as e:
        print(e)
    except:
        print("出错了")

#解析接口返回数据        
def getData(html):    
    json_data = json.loads(html)['cmts']
    comments = []
    
    #解析数据并存入数组
    try:
        for item in json_data: 
            comment = []
            comment.append(item['nickName'])
            comment.append(item['cityName'] if 'cityName' in item else '')
            comment.append(item['content'].strip().replace('\n', ''))
            comment.append(item['score'])
            comment.append(item['startTime'])            
            comments.append(comment)
            
        return comments
    
    except Exception as e:
        print(comment)
        print(e)


#保存数据，写入excel        
def saveData(comments):

    filename = './movieComments.csv'
    
    dataObject = pd.DataFrame(comments)
    dataObject.to_csv(filename, mode='a', index=False, sep=',', header=False)
    

#爬虫主函数 
def main():   
    #当前时间
    start_time = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    # 电影上映时间
    end_time = '2019-02-05  00:00:00'  
    
    while start_time > end_time:
        url = 'http://m.maoyan.com/mmdb/comments/movie/248906.json?_v_=yes&offset=0&startTime=' + start_time.replace('  ', '%20')
        html = None
        print(url)
        try:
            html = requestApi(url)
        
        except Exception as e:#如果有异常,暂停一会再爬
            time.sleep(1)
            html = requestApi(url)
        
        # else: #开启慢速爬虫
            # time.sleep(0.5)
            
        comments = getData(html)
        #print(url)
        start_time = comments[14][4] #获取每页中最后一条评论时间,每页有15条评论
        # print(start_time)
        
        #最后一条评论时间减一秒，避免爬取重复数据
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d  %H:%M:%S') + datetime.timedelta(seconds=-1)
        start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d  %H:%M:%S')
        print(start_time)
        saveData(comments)
    
    
if __name__ == '__main__':
    main()    
