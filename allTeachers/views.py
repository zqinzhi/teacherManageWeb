from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json

from allTeachers import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.serializers import Serializer
from django.core import serializers


# Create your views here.
# 获取所有教师的数据
@xframe_options_exempt
@login_required(login_url='/user/user.html')
def teachers(request, page):
    # 读取所有的字段数据，使用values_list可以读取期中的一个字段组成列表
    t_sex = models.sex.objects.values_list("t_sex", flat=True)
    t_education = models.education.objects.values_list("t_education", flat=True)
    t_level = models.level.objects.values_list("t_level", flat=True)
    t_title = models.title.objects.values_list("t_title", flat=True)
    t_province = models.province.objects.values_list("t_province", flat=True)
    t_school = models.school.objects.values_list("t_school", flat=True)
    t_from = models.fromWhere.objects.values_list("t_from", flat=True)
    # 性别是1，级别是2，职称是4，学历是3，省份是5，校内外是6，行业是7.data[{title:,id:}]
    # 下面重复的是声明字典和列表
    oneSex = {'title': '', 'id': ''}
    allSex = []
    oneEducation = {'title': '', 'id': ''}
    allEducation = []
    oneLevel = {'title': '', 'id': ''}
    allLevel = []
    oneTitle = {'title': '', 'id': ''}
    allTitle = []
    oneProvince = {'title': '', 'id': ''}
    allProvince = []
    oneSchool = {'title': '', 'id': ''}
    allSchool = []
    oneFrom = {'title': '', 'id': ''}
    allFrom = []
    # 下面这些是为了组成特定的数据类型，传到前端的js中应用，主要是下拉列表应用
    i = 101
    for sex in t_sex:
        oneSex['title'] = sex
        oneSex['id'] = i
        i = i + 1
        allSex.append(oneSex)
        oneSex = {'title': '', 'id': ''}
    oneSex['title'] = '全部'
    oneSex['id'] = i
    allSex.append(oneSex)
    print(allSex)
    # 下面这些是为了组成特点的数据类型，传到前端的js中应用，主要是下拉列表应用
    i = 301
    for education in t_education:
        oneEducation['title'] = education
        oneEducation['id'] = i
        i = i + 1
        allEducation.append(oneEducation)
        oneEducation = {'title': '', 'id': ''}
    oneEducation['title'] = '全部'
    oneEducation['id'] = i
    allEducation.append(oneEducation)
    print(allEducation)
    # 下面这些是为了组成特点的数据类型，传到前端的js中应用，主要是下拉列表应用
    i = 401
    for level in t_level:
        oneLevel['title'] = level
        oneLevel['id'] = i
        i = i + 1
        allLevel.append(oneLevel)
        oneLevel = {'title': '', 'id': ''}
    oneLevel['title'] = '全部'
    oneLevel['id'] = i
    allLevel.append(oneLevel)
    print(allLevel)
    # 下面这些是为了组成特点的数据类型，传到前端的js中应用，主要是下拉列表应用
    i = 201
    for title in t_title:
        oneTitle['title'] = title
        oneTitle['id'] = i
        i = i + 1
        allTitle.append(oneTitle)
        oneTitle = {'title': '', 'id': ''}
    oneTitle['title'] = '全部'
    oneTitle['id'] = i
    allTitle.append(oneTitle)
    print(allTitle)
    # 下面这些是为了组成特点的数据类型，传到前端的js中应用，主要是下拉列表应用
    i = 501
    for province in t_province:
        oneProvince['title'] = province
        oneProvince['id'] = i
        i = i + 1
        allProvince.append(oneProvince)
        oneProvince = {'title': '', 'id': ''}
    oneProvince['title'] = '全部'
    oneProvince['id'] = i
    allProvince.append(oneProvince)
    print(allProvince)
    # 下面这些是为了组成特点的数据类型，传到前端的js中应用，主要是下拉列表应用
    i = 601
    for school in t_school:
        oneSchool['title'] = school
        oneSchool['id'] = i
        i = i + 1
        allSchool.append(oneSchool)
        oneSchool = {'title': '', 'id': ''}
    oneSchool['title'] = '全部'
    oneSchool['id'] = i
    allSchool.append(oneSchool)
    print(allSchool)
    # 下面这些是为了组成特点的数据类型，传到前端的js中应用，主要是下拉列表应用
    i = 701
    for fromWhere in t_from:
        oneFrom['title'] = fromWhere
        oneFrom['id'] = i
        i = i + 1
        allFrom.append(oneFrom)
        oneFrom = {'title': '', 'id': ''}
    oneFrom['title'] = '全部'
    oneFrom['id'] = i
    allFrom.append(oneFrom)
    print(allFrom)

    # 获取全部数据然后返回页面
    teachers = models.teacherModel.objects.all()
    teacherList = []
    for i in teachers:
        teacherList.append(i)
    paginator = Paginator(teacherList, len(teacherList))
    if page == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        page = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(page)

    page = paginator.page(page)  # 传递当前页的实例对象到前端
    # 为了前端能正常显示，要全部转为json数据
    allSex = json.dumps(allSex)
    allEducation = json.dumps(allEducation)
    allLevel = json.dumps(allLevel)
    allTitle = json.dumps(allTitle)
    allProvince = json.dumps(allProvince)
    allSchool = json.dumps(allSchool)
    allFrom = json.dumps(allFrom)
    # 将制作好的各选项的json数据写入数据库对应的表中
    options = models.allOptions.objects.all()
    if options:
        print('allOptions已经存在，我什么都不干')
    else:
        allOptions = models.allOptions(t_from=allFrom, t_school=allSchool, t_province=allProvince, t_title=allTitle,
                                       t_level=allLevel, t_sex=allSex, t_education=allEducation)
        allOptions.save()
    return render(request, 'teachersManage.html',
                  {'page': page, 'allSex': allSex, 'allEducation': allEducation, 'allLevel': allLevel,
                   'allTitle': allTitle,
                   'allProvince': allProvince, 'allSchool': allSchool, 'allFrom': allFrom})


# 定义一个全局变量，用来存储多项筛选
screenDic = {'cate1': '', 'cate2': '', 'year': ''}

# mangeOneYearInfo是培训班管理页面中显示一年的详细数据
def allInfo(request):
    print('我获取所有数据：')
    # 这个if和else是用来进行筛选的
    oneYearInfo = models.courseCategoryModel.objects.all()

    # 读取出各个下拉菜单的选项——开始
    coursecategory = models.courseCategory.objects.values_list("category", flat=True)
    coursecategory2 = models.courseCategory2.objects.values_list("category2", flat=True)
    allyears = models.allyears.objects.values_list("year", flat=True)
    print(coursecategory)
    print(coursecategory2)
    oneCategory = {'title': '', 'id': ''}
    allCategory = []
    i = 101
    for category in coursecategory:
        oneCategory['title'] = category
        oneCategory['id'] = i
        i = i + 1
        allCategory.append(oneCategory)
        oneCategory = {'title': '', 'id': ''}
    oneCategory['title'] = '全部'
    oneCategory['id'] = i
    allCategory.append(oneCategory)
    print(allCategory)

    oneCategory2 = {'title': '', 'id': ''}
    allCategory2 = []
    i = 201
    for category2 in coursecategory2:
        oneCategory2['title'] = category2
        oneCategory2['id'] = i
        i = i + 1
        allCategory2.append(oneCategory2)
        oneCategory2 = {'title': '', 'id': ''}
    oneCategory2['title'] = '全部'
    oneCategory2['id'] = i
    allCategory2.append(oneCategory2)
    print(allCategory)

    oneYear = {'title': '', 'id': ''}
    yearList = []
    i = 301
    for year in allyears:
        oneYear['title'] = year
        oneYear['id'] = i
        i = i + 1
        yearList.append(oneYear)
        oneYear = {'title': '', 'id': ''}
    oneYear['title'] = '全部'
    oneYear['id'] = i
    yearList.append(oneYear)
    print(yearList)
    # 读取出各个下拉菜单的选项——结束

    return render(request, 'courseManage.html',
                  {'page': oneYearInfo, 'allCategory': allCategory, 'allCategory2': allCategory2, 'allYears': yearList})


@csrf_exempt
def selectInfo(request):
    print('我是ajax数据：')
    print(request.POST)
    # 这个if和else是用来进行筛选的
    if 'screenInfo[]' in request.POST:
        print('我不是None')
        data = request.POST.copy()
        screenInfo = data.pop('screenInfo[]')  # 此时就可以用删除方法删除querydict中的数据了
        print(screenInfo)
        #screenInfo = getInfo.split(",")  # 字符串转为列表，[0]是序号，[1]是筛选的值
        sid = screenInfo[0]
        value = screenInfo[1]
        print('我是sid:')
        print(sid)
        print('我是value')
        print(value)
        # sid第一位是1代表类型1,2代表类型2,3代表年份
        if sid[0:1] == '1':
            print('我是类型1')
            screenDic['cate1'] = value
            if screenDic['cate1'] == '全部':
                if screenDic['cate2'] == '' and screenDic['year'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter()
                elif screenDic['cate2'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_year=screenDic['year'])
                elif screenDic['year'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate2'])
            elif screenDic['cate2'] == '' and screenDic['year'] == '':
                oneYearInfo = models.courseCategoryModel.objects.filter(c_outORin=screenDic['cate1'])
            elif screenDic['cate2'] == '':
                oneYearInfo = models.courseCategoryModel.objects.filter(c_outORin=screenDic['cate1'],
                                                                        c_year=screenDic['year'])
            elif screenDic['year'] == '':
                oneYearInfo = models.courseCategoryModel.objects.filter(c_outORin=screenDic['cate1'],
                                                                        c_category=screenDic['cate2'])
            else:
                oneYearInfo = models.courseCategoryModel.objects.filter(c_outORin=screenDic['cate1'],
                                                                        c_category=screenDic['cate2'],
                                                                        c_year=screenDic['year'])

        if sid[0:1] == '2':
            print('我是类型2')
            screenDic['cate2'] = value
            if screenDic['cate2'] == '全部':
                if screenDic['cate1'] == '' and screenDic['year'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter()
                elif screenDic['cate1'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_year=screenDic['year'])
                elif screenDic['year'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate1'])
            elif screenDic['cate1'] == '' and screenDic['year'] == '':
                oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate2'])
            elif screenDic['cate1'] == '':
                oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate2'],
                                                                        c_year=screenDic['year'])
            elif screenDic['year'] == '':
                oneYearInfo = models.courseCategoryModel.objects.filter(c_outORin=screenDic['cate1'],
                                                                        c_category=screenDic['cate2'])
            else:
                oneYearInfo = models.courseCategoryModel.objects.filter(c_outORin=screenDic['cate1'],
                                                                        c_category=screenDic['cate2'],
                                                                        c_year=screenDic['year'])
        if sid[0:1] == '3':
            print('我是年份')
            screenDic['year'] = value
            if screenDic['year'] == '全部':
                if screenDic['cate1'] == '' and screenDic['cate2'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter()
                elif screenDic['cate1'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_year=screenDic['cate2'])
                elif screenDic['cate2'] == '':
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate1'])
            elif screenDic['cate1'] == '' and screenDic['cate2'] == '':
                if screenDic['year'] == '全部':
                    oneYearInfo = models.courseCategoryModel.objects.filter()
                else:
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_year=screenDic['year'])
            elif screenDic['cate1'] == '':
                if screenDic['year'] == '全部':
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate2'])
                else:
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate2'],
                                                                            c_year=screenDic['year'])
            elif screenDic['cate2'] == '':
                if screenDic['year'] == '全部':
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate1'])
                else:
                    oneYearInfo = models.courseCategoryModel.objects.filter(c_category=screenDic['cate1'],
                                                                            c_year=screenDic['year'])
            else:
                oneYearInfo = models.courseCategoryModel.objects.filter(c_outORin=screenDic['cate1'],
                                                                        c_category=screenDic['cate2'],
                                                                        c_year=screenDic['year'])
        print('我是screenDic:')
        print(screenDic)
    else:
        print(request.POST)
        oneYearInfo = models.courseCategoryModel.objects.all()
        print('错啦！我是None')

    # 读取出各个下拉菜单的选项——开始
    coursecategory = models.courseCategory.objects.values_list("category", flat=True)
    coursecategory2 = models.courseCategory2.objects.values_list("category2", flat=True)
    allyears = models.allyears.objects.values_list("year", flat=True)
    print(coursecategory)
    print(coursecategory2)
    oneCategory = {'title': '', 'id': ''}
    allCategory = []
    i = 101
    for category in coursecategory:
        oneCategory['title'] = category
        oneCategory['id'] = i
        i = i + 1
        allCategory.append(oneCategory)
        oneCategory = {'title': '', 'id': ''}
    oneCategory['title'] = '全部'
    oneCategory['id'] = i
    allCategory.append(oneCategory)
    print(allCategory)

    oneCategory2 = {'title': '', 'id': ''}
    allCategory2 = []
    i = 201
    for category2 in coursecategory2:
        oneCategory2['title'] = category2
        oneCategory2['id'] = i
        i = i + 1
        allCategory2.append(oneCategory2)
        oneCategory2 = {'title': '', 'id': ''}
    oneCategory2['title'] = '全部'
    oneCategory2['id'] = i
    allCategory2.append(oneCategory2)
    print(allCategory)

    oneYear = {'title': '', 'id': ''}
    yearList = []
    i = 301
    for year in allyears:
        oneYear['title'] = year
        oneYear['id'] = i
        i = i + 1
        yearList.append(oneYear)
        oneYear = {'title': '', 'id': ''}
    oneYear['title'] = '全部'
    oneYear['id'] = i
    yearList.append(oneYear)
    print(yearList)
    print(list(oneYearInfo.values()))
    oneYearInfo = list(oneYearInfo.values())# 将QuerySet转为List数据，就是将从数据库中读取的数据转为list
    data = {"pageInfo": oneYearInfo, "allCategory": allCategory, "allCategory2": allCategory2, "yearList": yearList}
    return JsonResponse(data)
