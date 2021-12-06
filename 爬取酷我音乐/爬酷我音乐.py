'''
作者：叉叉L
日期：2021年8月4日 
功能：爬取酷我音乐
'''

#encoding = utf-8
import requests
import os

# 判断文件是否存在
def isFileExists(path):
    if os.path.exists(path=path):
        return True
    else:
        return False

# 获取音乐对应网址返回的json数据
def getMusciJson():
    # 目标网址
    url = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={key}&pn={page_numOfMusic}&rn=30&httpsStatus=1&reqId=3adbfc80-f462-11eb-9392-275a4ac7520f'
    response = requests.get(url=url, headers=headers).json()  # 将请求以json数据格式返回
    return response

# 获取mp3的网址
def getAudioUrl():
    # 这是能得到mp3网站的url
    music_url = f'http://www.kuwo.cn/url?format=mp3&rid={music_rid}&response=url&type=convert_url3&br=128kmp3&from=web&t=1627999255296&httpsStatus=1&reqId=38921711-f463-11eb-9503-d91362e4fe3d'

    # 得到url返回的json数据
    audio_url = requests.get(url=music_url, headers=headers).json()
    return audio_url

# 将爬取到的文件保存
# @ fileName: 文件路径
# @ music_name: 音乐名称
# @ music_artist: 音乐作者
def saveFile(fileName, music_name, music_artist):
     # 利用with open保存文件（图片/视频/音频 一般以二进制流在网站传输）
        with open(fileName + music_artist + ' 《' + music_name + '》' + '.mp3', mode='wb')as f:

            # 利用.content得到mp3的二进制流，写入文件
            f.write(requests.get(url=getAudioUrl()['url'], headers=headers).content)

# 如果没有music文件夹，则创建，用来保存下载的mp3文件
fileName = './music/'
if not isFileExists(fileName):
    os.mkdir(fileName)

key = '周杰伦'# key是搜索关键词
numOfMusic = 0 # 统计下载歌曲数量

#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Referer': f'http://www.kuwo.cn',  # 防盗---意味着只能从网页首页点进搜索栏
    'csrf': 'KEK74YPXT4',  # 跨域
    'cookie': '_ga=GA1.2.1908815202.1627995039; _gid=GA1.2.1559305376.1627995039; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1627996710,1627998825,1627999104,1627999256; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1627999256; kw_token=KEK74YPXT4'
}

for page_numOfMusic in range(1,2): # page_numOfMusic 页数
    print(f'========第{page_numOfMusic}页========')

    for music in getMusciJson()['data']['list']:       
        numOfMusic += 1 # 每下载一首歌，numOfMusic + 1

        music_name = music['name']     # 获取音乐的名称
        music_artist = music['artist'] # 获取歌曲作者
        music_rid = music['rid']       # 获取音乐的唯一标识符 rid     
        
        # 如果文件已经存在，则跳过下载
        if isFileExists(fileName + music_artist + ' 《' + music_name + '》' + '.mp3'):
            print(f"\t\t：{music_artist} 《{music_name}》已存在，跳过下载")
            continue

        # 如果返回状态代码为200 且 信息为success 说明访问成功 
        if getAudioUrl()['code'] == 200 and getAudioUrl()['msg'] == 'success':         

            # 打印信息：第几首歌 + 歌曲作者 + 歌曲名字                
            print(f"\t\t正在下载第{numOfMusic}首歌：{music_artist} 《{music_name}》")

             # 保存文件
            saveFile(fileName, music_name, music_artist)

# 下载完成，则打印完成的信息：numOfMusic-下载歌曲的数量
print(f'\n========下载完成，一共下载了{numOfMusic}首歌========\n')

