from scipy.misc import  imread

import codecs

from os import  path

import jieba

from wordcloud import WordCloud


#暂时没有用到
def get_all_keywords(file_name):
    word_lists=[]  #关键词列表
    with codecs.open(file_name,'r',encoding='utf-8') as f:
        Lists=f.readlines()
        for li in Lists:
            cut_list=list(jieba.cut(li))
            for word in cut_list:
                word_lists.append(word)

    word_lists_set=set(word_lists)  #去除相同的元素
    sort_count=[]
    word_lists_set=list(word_lists_set)

    length=len(word_lists_set)
    print(u'共有%d个关键词'%length)
    k = 1
    for w in word_lists_set:
        sort_count.append(w + u':' + str(word_lists.count(w)) + u"次\n")
        print(u"%d---" % k + w + u":" + str(word_lists.count(w)) + u"次")
        k += 1
    with codecs.open('count_word.txt', 'w', encoding='utf-8') as f:
        f.writelines(sort_count)


def save_jieba_result(file_name):
    #设置多线程切割
    #jieba.enable_parallel(4)
    dirs=path.join(path.dirname(__file__),file_name)
    print(dirs)
    with codecs.open(dirs,encoding='utf-8') as f:
        comment_text=f.read()
    cut_text=" ".join(jieba.cut(comment_text))
    with codecs.open('pjl_jieba.txt','w',encoding='utf-8') as f:
        f.write(cut_text)


def draw_wordcloud(file_name):
    with codecs.open(file_name,encoding='utf-8') as f:
        comment_text=f.read()
    color_mask=imread('template.png') #读取背景图片
    stopwords = ['png','douban','com','href','https','img','img3','class','source','icon','shire',u'有点',u'真的',u'觉得',u'还是',u'一个',u'就是', u'电影', u'你们', u'这么', u'不过', u'但是', u'什么', u'没有', u'这个', u'那个', u'大家', u'比较', u'看到', u'真是',
                 u'除了', u'时候', u'已经', u'可以']
    font = r'C:\Windows\Fonts\simfang.ttf'
    cloud=WordCloud(font_path=font,background_color='white',max_words=20000,max_font_size=200,min_font_size=4,mask=color_mask,stopwords=stopwords)
    word_cloud=cloud.generate(comment_text)  #产生词云
    word_cloud.to_file('pjl_cloud.jpg')
