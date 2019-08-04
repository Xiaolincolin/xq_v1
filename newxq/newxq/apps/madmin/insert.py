"""
author: Colin
@time: 2019-04-25 15:37
explain:

"""
# coding: utf-8
import csv
import math
from collections import defaultdict, OrderedDict     # OrderedDict,实现了对字典对象中元素的排序
from itertools import combinations
import time
import pymysql
import pandas as pd

conn = pymysql.connect(
                host="127.0.0.1",
                database="newxqs",
                user="root",
                password="xiaolin",
                port=3306,
                charset='utf8'
            )
def insert():
    with open('course.csv','r') as f:
        jg = csv.reader(f)
        for line in jg:
            data = line
            student_id = data[0]
            course_id = data[1]
            cur = conn.cursor()
            sql = ("insert into madmin_associatecourse(course_id,course_name)values('%s','%s')" % (student_id,course_id))
            try:
                cur.execute(sql)
                conn.commit()
            except:
                conn.rollback()


def getdata(file, minimum_score):
    """
    读取csv文件的数据，并根据给定的分数值筛选符合要求的数据，并以字典的形式返回
    :param file_path: 数据文件的存放路径
    :param minimum_score: 符合要求的最低分数值
    :return: 返回table，table的key是学生的学号，每个key对应的value是该学生符合要求的课程
    """
    # with open(file_path) as f:
    #     f_csv = csv.reader(f)
    table = defaultdict(list)  #defaultdict是指字典

    for line in file.values:   # 读取的是成绩的excel表
        # print(line)
        if int(line[3])>= minimum_score and line[2] not in table[line[1]]:
            table[line[1]].append(line[2])
    for key in table:
        table[key].sort()
    return table

def genl1(table, min_support):
    """
    产生频繁一项集
    :param table: 数据表
    :param min_support: 最小支持度
    :return: 返回频繁一项集:所有: c1; > min_support :l1
    """
    c1 = {}
    keys = []
    table2 = defaultdict(list)
    for stu in table:        #学号在Table表
        for course in table[stu]:          #课程在table表中
            if course in c1:
                c1[course] += 1
            else:
                keys.append(course)
                c1[course] = 1
    keys.sort()
    l1 = {}
    l = {} # TODO
    for key in keys:
        if c1[key] >= min_support:
            l1[key] = c1[key]
            l[(key,)] = c1[key] # TODO
    # 新table
    for stu in table:
        for course in table[stu]:
            if course in l1:
                table2[stu].append(course)
    return c1, l1, table2, l

# ## hash 二项频繁集

def combination2(t0):
    c2 =[]
    for  tti in range(len(t0)):
        c2.append(list(combinations(t0[tti], 2)))
    # print('c2',c2)     #相当于把所有的分解的数据库展开
    return c2

def hash_l2(table2, L, min_support):
    t = []
    for key, value in table2.items():
        t.append(value)
    t2 = combination2(t)
    hashr = [0 for i in range(997)]
    hashbit=[0 for i in range(997)]
    for t2t1 in t2:
        for X in t2t1:
            hash1 = 10*L.index(X[0])+ L.index(X[1])
            hash1 %=997
            hashr[hash1]+=1
            if hashr[hash1] > min_support:
                hashbit[hash1] = 1

    # hash 二项集生成
    L1L1=list(combinations(L, 2))
    C2 = []
    for y in L1L1:
        hash2 = 10*L.index(y[0])+ L.index(y[0])
        hash2 %=997
        if hashbit[hash2]>0:
            C2.append(y)
    # print('~~~~',len(C2))
    return C2

# ## 计算二项集支持度

def calc_supportX(C2, table2):
    C2s = {}
    for key in C2:            #在候选项集中找项集
        for stu in table2:           #table表中的学号
            if set(key).issubset(table2[stu]):        #set(key)是否包含在table[stu]中
                if key in C2s:
                    C2s[key] += 1
                else:
                    C2s[key]= 1
    return C2s

# ## 二项集mark计算

def gen_mark(C2s, L):
    mark=dict(zip(L,[0 for i in range(len(L))]))
    for key, value in C2s.items():
        if value >= min_support:
            for item in key:
                cnfd = value / all_ls[0][(item,)] # TODO
                if cnfd > 0.5:
                    mark[item] += 1
    return mark


# ## 循环生成多项集

def next_gen(l_next, mark, min_support):
    nd = {}
    for keys, v in l_next.items():
        if v > min_support:
            temp = list(set(keys))
            flag = 1
            for i in range(len(temp)):
                if mark[temp[i]] < 1:
                    flag = 0
                    break
            if flag:
                nd[keys] = v
    return nd

def combinationsX(l, t):
    C = []
    C_next = []
    for l in list(combinations(l, t)):
        if set(l) not in C:
            C.append(set(l))
            C_next.append(l)
    return C_next

# 更新 mark
def update_mark(mark):
    mark_s = {}
    for mk, v in mark.items():
        if v > 0:
            mark_s[mk] = v
    return mark_s

# ## 关联规则生成

def generate_rules(source,l, all_ls, support, min_confident):
    """
    关联规则生成算法
    :param l: 频繁项集
    :param all_ls: 所有的频繁项集，记录了每个频繁项集的支持度
    :param support: 频繁项集l的支持度
    :param min_confident: 最小置信度

    """
    course = {}
    # with open(source_path) as f:
    #     course_csv = csv.reader(f)
    for line in source.values:
        course[line[0]] = line[1]
    subsets = []
    length = len(l)
    # print('!!!!!!',length)
    for i in range(1, length):
        subsets.append(list(combinations(l, i)))
    result = []
    for subset in subsets:
        for item in subset:
            tmp = list(set(l) - set(item))
            tmp.sort()
            if item in all_ls[len(item) - 1]: # TODO
                cnfd = support / all_ls[len(item) - 1][item]
                if cnfd >= min_confident:
                    per_result = []
                    a = [course[i] for i in item]
                    b = [course[i] for i in tmp]
                    # print(a, '-->', b, ' 置信度:', cnfd, sep='')
                    per_result.append(a)
                    per_result.append(b)
                    per_result.append(cnfd)
                    result.append(per_result)
    return result


def has_infrequent_subset(c,l_pre):
    """
    根据Apriori算法的先验性质，进行剪枝处理
    :param c: 新生成的候选项K集中的某一项
    :param l_pre: 频繁(k-1)项集
    :return:
    """
    for item in c:     #item是频繁项集中的项
        tmpsubset = list(c - {item})        # tmpsnbset是指频繁项集中的课程代码项
        tmpsubset.sort()                      #l_pre.keys()频繁项集，如：odict_keys([('c0103810',), ('c1103001',), ('c1104001',), ('c1106001',)])
        if not {tuple(tmpsubset)}.issubset(set(l_pre.keys())):   #issubset() 方法用于判断集合的所有元素是否都包含在指定集合中，如果是则返回 True，否则返回 False
            return True                                           #tuple(tmpsubset)}是否包含在l_pre.keys()
    return False

def apriori_gen(l_pre):
    """
    生成候选K项集
    :param l_pre: 频繁K-1项集
    :return: 候选K项集c_next
    """
    keys = list()
    l_pre_key_list = list(l_pre.keys())
    l_pre_key_list.sort()                      #1频繁项集课程代码进行排序
    for idx, item1 in enumerate(l_pre_key_list):      #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中
        for i in range(idx + 1, len(l_pre_key_list)):   #在idx+1和1频繁集的长度之间
            item2 = l_pre_key_list[i]
            if item1[:-1] == item2[:-1] and\
                    not has_infrequent_subset(set(item1) | set(item2), l_pre):             # has_infrequent_subset调用进行了剪枝
                item = list(set(item1) | set(item2))
                item.sort()                #对项集进行排序
                keys.append(item)           #keys添加项集
    c_next = OrderedDict((tuple(key), 0) for key in keys)    #OrderedDict,实现了对字典对象中元素的排序，产生C2
    print('######', len(c_next))
    return c_next

if __name__ == '__main__':
    ts = time.time()
    file = pd.read_sql("select id,student_id,course_id,grade from madmin_associatecoursegrade",con=conn)
    source = pd.read_sql("select course_id,course_name from madmin_associatecourse", con=conn)
    score = 70
    score_table = getdata(file, score)
    min_support = math.ceil(len(score_table) * 0.4)  # 计算最小支持数，向上取整
    min_confident = 0.6
    print('Number of Student:', len(score_table))
    print('Min_Support:', min_support)
    print('Min_Confident:', min_confident)
    c1, L1, table2, l = genl1(score_table, min_support)
    all_ls = []  # 所有频繁项集是列表形式
    all_ls.append(l)  # 将1频繁项集添加到所有的频繁项集中 # TODO
    L = list(L1.keys()) # 部分， 用于生成hash
    C2 = hash_l2(table2, L, min_support)
    C2s = calc_supportX(C2, score_table)
    mark = gen_mark(C2s, L)
    l_next = C2s
    while (len(l_next)):
        for mk, v in mark.items():
            mark[mk] = v - 1
        nd = next_gen(l_next, mark, min_support)
        l_next = nd
        mark = update_mark(mark)
        if len(l_next) > 0:
            all_ls.append(l_next)
            print('l_%d length:' % len(all_ls), len(l_next))
            ## 生成k+1项集
            c_next = combinationsX(list(mark.keys()), len(all_ls) + 1)
            print('%%%%',len(c_next))
            l_next = calc_supportX(c_next, table2)
    l = all_ls[-1]
    result = []
    for item in l:
        r= generate_rules(source,list(item), all_ls, l[item], min_confident)
        result.append(r)
    print(time.time() - ts)
    for j in result:
        for k in j:
            print(k)
        print('-------------------------')