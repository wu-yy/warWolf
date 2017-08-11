import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
import json
from bs4 import BeautifulSoup
try:
    from PIL import Image
except:
    pass

from mywordCloud import save_jieba_result
from mywordCloud import draw_wordcloud

import codecs
# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
headers = {
    "Host": "www.douban.com",
    "Referer": "https://www.douban.com/",
    'User-Agent': agent,
}

#使用cookie登录信息
session=requests.session()
session.cookies=cookielib.LWPCookieJar(filename='cookies')

try:
    session.cookies.load(ignore_discard=True)
    print('成功加载cookie')
except:
    print("cookie 未能加载")

# 获取验证码
def get_captcha(url):
    #获取验证码
    print('获取验证码',url)
    captcha_url = url
    r = session.get(captcha_url, headers=headers)
    print('test')
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha

def isLogin():
    #登录个人主页，查看是否登录成功
    url='https://www.douban.com/people/151607908/'
    login_code=session.get(url,headers=headers,allow_redirects=False).status_code
    if login_code==200:
        return True
    else:
        return False


def login(acount,secret):
    douban="https://www.douban.com/"
    htmlcha=session.get(douban,headers=headers).text
    patterncha=r'id="captcha_image" src="(.*?)" alt="captcha"'
    httpcha=re.findall(patterncha,htmlcha)
    pattern2=r'type="hidden" name="captcha-id" value="(.*?)"'
    hidden_value=re.findall(pattern2,htmlcha)
    print(hidden_value)

    post_data = {
        "source": "index_nav",
        'form_email': acount,
        'form_password': secret
    }
    if len(httpcha)>0:
        print('验证码连接',httpcha)
        capcha=get_captcha(httpcha[0])
        post_data['captcha-solution']=capcha
        post_data['captcha-id']=hidden_value[0]

    print (post_data)
    post_url='https://www.douban.com/accounts/login'
    login_page=session.post(post_url,data=post_data,headers=headers)
    #保存cookies
    session.cookies.save()

    if isLogin():
        print('登录成功')
    else:
        print('登录失败')


def get_movie_sort():
    time.sleep(1)
    movie_url='https://movie.douban.com/chart'
    html=session.get(movie_url,headers=headers)
    soup=BeautifulSoup(html.text,'html.parser')
    result=soup.find_all('a',{'class':'nbg'})
    print(result)

#爬取短评论
def get_comment(filename):  #filename为爬取得内容保存的文件
    begin=1
    next_url='?start=20&limit=20&sort=new_score&status=P'
    f=open(filename,'w+',encoding='utf-8')
    while(True):
        time.sleep(2)
        comment_url='https://movie.douban.com/subject/26363254/comments'
        data={
            'start':'27',
            'limit':'-20',
            'sort':'new_score',
            'status':'P'
        }
        headers2 = {
            "Host": "movie.douban.com",
            "Referer": "https://www.douban.com/",
            'User-Agent': agent,
            'Connection': 'keep-alive',
        }

        html=session.get(url='https://movie.douban.com/subject/26363254/comments'+next_url,headers=headers2)
        soup=BeautifulSoup(html.text,'html.parser')

        #爬取当前页面的所有评论
        result=soup.find_all('div',{'class':'comment'}) #爬取得所有的短评
        pattern4 = r'<p class=""> (.*?)' \
                   r'</p>'
        for item in result:
            s=str(item)
            count2=s.find('<p class="">')
            count3=s.find('</p>')
            s2=s[count2+12:count3]  #抽取字符串中的评论
            f.write(s2)

        #获取下一页的链接
        next_url=soup.find_all('div',{'id':'paginator'})
        pattern3=r'href="(.*?)">后页'
        if(len(next_url)==0):
            break
        next_url=re.findall(pattern3,str(next_url[0]))  #得到后页的链接
        if(len(next_url)==0): #如果没有后页的链接跳出循环
            break
        next_url=next_url[0]
        print('%d爬取下一页评论...'%begin)
        begin=begin+1
        #如果爬取了6次则多休息2秒
        if(begin%6==0):
            time.sleep(2)
            print('休息...')
        print(next_url)
    f.close()


if __name__=='__main__':
    if isLogin():
        print('您已经登录')
    else:
        login('ehuwcsw@qq.com','3ewfw642')
    get_comment('key.txt')
    #get_movie_sort()
    save_jieba_result('key.txt')
    draw_wordcloud('pjl_jieba.txt')

