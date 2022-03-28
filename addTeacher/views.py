import os

from dist.manage.django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse
from allTeachers import models
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
import xlrd
import logging
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.
def addHtml(request):
    # 读取所有的字段数据
    t_sex = models.sex.objects.all()
    t_education = models.education.objects.all()
    t_level = models.level.objects.all()
    t_title = models.title.objects.all()
    t_province = models.province.objects.all()
    t_school = models.school.objects.all()
    t_from = models.fromWhere.objects.all()
    return render(request, 'addOneT.html', locals())


def addOne(request):
    if request.method == 'POST':
        data = models.teacherModel.objects.all().values_list("id")  # 获取所有的id
        maxId = max(data)  # 去除最大的id
        maxId = list(maxId)  # 将quryset转为list
        id = int(maxId[0]) + 1  # 因为maxId是数组，[0]就是最大的id值，然后强制转为int，再+1
        addInfo = request.POST
        insetInfo = models.teacherModel(id=id, t_Name=addInfo['name'], t_sex=addInfo['sex'], t_work=addInfo['work'],
                                        t_education=addInfo['education'], t_level=addInfo['level'],
                                        t_title=addInfo['title'],
                                        t_ID_card=addInfo['ID_card'], t_age=addInfo['age'], t_from=addInfo['from'],
                                        t_school=addInfo['school'], t_province=addInfo['province'],
                                        t_introduction=addInfo['introduction'])
        if insetInfo:
            insetInfo.save()
            messages.success(request, "保存成功")
        else:
            messages.success(request, "保存失败")

    else:
        print('我是真的服气2')

    return render(request, 'addOneT.html', locals())


# 我是删除选中项。。。。。终于成功了
def delete(request):
    print('我是delete')
    # print(request.POST['choiceID'])
    deleteID = request.POST['choiceID'].split(",")
    print(deleteID)
    deleteID = [k for k in deleteID if k != '']  # 删除列表中的空值
    print(deleteID)
    for j in deleteID:
        obj = models.teacherModel.objects.get(id=j)
        obj.delete()
    teachers = models.teacherModel.objects.all()
    teacherList = []
    for i in teachers:
        teacherList.append(i)
    paginator = Paginator(teacherList, len(teacherList))
    page = paginator.page(1)  # 传递当前页的实例对象到前端
    # 从数据库中读取制作好的各选项的json数据，想到将这些数据直接写入数据库然后读出来我还是牛逼的
    allOptions = models.allOptions.objects.all()
    print(allOptions[0].t_education)
    allSex = allOptions[0].t_sex
    allEducation = allOptions[0].t_education
    allLevel = allOptions[0].t_level
    allTitle = allOptions[0].t_title
    allProvince = allOptions[0].t_province
    allSchool = allOptions[0].t_school
    allFrom = allOptions[0].t_from
    return render(request, 'teachersManage.html',
                  {'page': page, 'allSex': allSex, 'allEducation': allEducation, 'allLevel': allLevel,
                   'allTitle': allTitle,
                   'allProvince': allProvince, 'allSchool': allSchool, 'allFrom': allFrom})


# 导入名单文件
def inputFile(request):
    if request.method == "POST":
        result = []
        myFile = request.FILES.get("inputFile", None)
        if not myFile:
            return HttpResponse("no files for upload!")
        # 后面两句很关键啊，inputFile是从前端使用input-file打开的文件，不能直接xlrd.open_workbook，得需要使用后面两句代码才能打开excel文件
        f = myFile.read()
        data = xlrd.open_workbook(file_contents=f)
        names = data.sheet_names()  # 返回表格中所有工作表的名字
        for sheet_name in names:
            status = data.sheet_loaded(sheet_name)  # 检查sheet1是否导入完毕
            if status is True:
                table = data.sheet_by_name(sheet_name)
                try:
                    keys = table.row_values(0)  # 第一行作为key值
                except Exception as e:
                    logging.error(e)  # 表格中存在空sheet，或者第一行没数据
                    continue
                if keys:
                    rowNum = table.nrows  # 获取该sheet中的有效行数
                    colNum = table.ncols  # 获取该sheet中的有效列数
                    if rowNum == 0 or colNum == 0:
                        continue
                    else:
                        result = []  # 列表L存放取出的数据
                        for i in range(1, rowNum):  # 从第二行（数据行）开始取数据
                            sheet_data = {}  # 定义一个字典用来存放对应数据
                            for j in range(colNum):  # j对应列值
                                if j == 0:  # 因为从excel读取的纯数字会有小数点和一位小数位，所有要用2个If删掉
                                    str1 = str(table.row_values(i)[j])[:-1]
                                    str2 = str1[:-1]
                                    sheet_data[keys[j]] = str2
                                elif j == 8:
                                    str1 = str(table.row_values(i)[j])[:-1]
                                    str2 = str1[:-1]
                                    sheet_data[keys[j]] = str2
                                else:
                                    sheet_data[keys[j]] = table.row_values(i)[j]  # 把第i行第j列的值取出赋给第j列的键值，构成字典
                            result.append(sheet_data)  # 一行值取完之后（一个字典），追加到L列表中
        # result就是最后搞出来的数据了，而且是字典类的
        print(result[0])
        # 将数据写入数据库
        for one in result:
            insetInfo = models.teacherModel(id=one['id'], t_Name=one['t_Name'], t_sex=one['t_sex'],
                                            t_work=one['t_work'],
                                            t_education=one['t_education'], t_level=one['t_level'],
                                            t_title=one['t_title'],
                                            t_ID_card=one['t_ID_card'], t_age=one['t_age'], t_from=one['t_from'],
                                            t_province=one['t_province'], t_school=one['t_school'],
                                            t_introduction=one['t_introduction'])
            if insetInfo:
                insetInfo.save()
    # 读取数据返回页面
    teachers = models.teacherModel.objects.all()
    teacherList = []
    for i in teachers:
        teacherList.append(i)
    paginator = Paginator(teacherList, len(teacherList))
    page = paginator.page(1)  # 传递当前页的实例对象到前端
    # 从数据库中读取制作好的各选项的json数据，想到将这些数据直接写入数据库然后读出来我还是牛逼的
    allOptions = models.allOptions.objects.all()
    print(allOptions[0].t_education)
    allSex = allOptions[0].t_sex
    allEducation = allOptions[0].t_education
    allLevel = allOptions[0].t_level
    allTitle = allOptions[0].t_title
    allProvince = allOptions[0].t_province
    allSchool = allOptions[0].t_school
    allFrom = allOptions[0].t_from
    return render(request, 'teachersManage.html',
                  {'page': page, 'allSex': allSex, 'allEducation': allEducation, 'allLevel': allLevel,
                   'allTitle': allTitle,
                   'allProvince': allProvince, 'allSchool': allSchool, 'allFrom': allFrom})


# 打开修改教师信息页面
# 下面这个黄色是解决现在的浏览器不支持ifram嵌套页面的问题
updateT_id = ''


@xframe_options_exempt
def updateT(request):
    # global是外面声明了一个updateT_id变量作为全局变量，然后使用global声明一下里面的就是外面的
    global updateT_id
    updateT_id = request.GET['ID']
    updateInfo = models.teacherModel.objects.get(id=updateT_id)
    print(updateT_id)
    # 读取所有的字段数据
    t_sex = models.sex.objects.all()
    t_education = models.education.objects.all()
    t_level = models.level.objects.all()
    t_title = models.title.objects.all()
    t_province = models.province.objects.all()
    t_school = models.school.objects.all()
    t_from = models.fromWhere.objects.all()
    return render(request, 'updateOneT.html', locals())


# 更新修改制定教师信息
@xframe_options_exempt
def updateOne(request):
    print("i am updateOne")
    addInfo = request.POST['choiceID']  # 经过teachersManage.html页面获取到的弹出ifram(updateOneT.html)数据
    addInfo = addInfo.split(",")  # 因为获取的数据是逗号分割的字符串，这个操作转成列表
    print(addInfo)
    # 将数据修改写入数据库
    updateInfo = models.teacherModel.objects.get(id=updateT_id)
    updateInfo.t_Name = addInfo[0]
    updateInfo.t_sex = addInfo[1]
    updateInfo.t_work = addInfo[2]
    updateInfo.t_level = addInfo[3]
    updateInfo.t_title = addInfo[4]
    updateInfo.t_education = addInfo[5]
    updateInfo.t_ID_card = addInfo[6]
    updateInfo.t_age = addInfo[7]
    updateInfo.t_province = addInfo[8]
    updateInfo.t_school = addInfo[9]
    updateInfo.t_from = addInfo[10]
    updateInfo.t_introduction = addInfo[11]

    updateInfo.save()
    # 读取数据返回页面
    teachers = models.teacherModel.objects.all()
    teacherList = []
    for i in teachers:
        teacherList.append(i)
    paginator = Paginator(teacherList, len(teacherList))
    page = paginator.page(1)  # 传递当前页的实例对象到前端
    # 从数据库中读取制作好的各选项的json数据，想到将这些数据直接写入数据库然后读出来我还是牛逼的
    allOptions = models.allOptions.objects.all()
    print(allOptions[0].t_education)
    allSex = allOptions[0].t_sex
    allEducation = allOptions[0].t_education
    allLevel = allOptions[0].t_level
    allTitle = allOptions[0].t_title
    allProvince = allOptions[0].t_province
    allSchool = allOptions[0].t_school
    allFrom = allOptions[0].t_from
    # return render(request, 'teachersManage.html', locals())
    return render(request, 'teachersManage.html',
                  {'page': page, 'allSex': allSex, 'allEducation': allEducation, 'allLevel': allLevel,
                   'allTitle': allTitle,
                   'allProvince': allProvince, 'allSchool': allSchool, 'allFrom': allFrom})


# 删除指定的一个教师信息
def deleteOne(request):
    print('我是deleteOne')
    # print(request.POST['deleteID'])
    deleteID = request.POST['deleteID']
    obj = models.teacherModel.objects.get(id=deleteID)
    obj.delete()
    # 读取数据返回页面
    teachers = models.teacherModel.objects.all()
    teacherList = []
    for i in teachers:
        teacherList.append(i)
    paginator = Paginator(teacherList, len(teacherList))
    page = paginator.page(1)  # 传递当前页的实例对象到前端
    # 从数据库中读取制作好的各选项的json数据，想到将这些数据直接写入数据库然后读出来我还是牛逼的
    allOptions = models.allOptions.objects.all()
    print(allOptions[0].t_education)
    allSex = allOptions[0].t_sex
    allEducation = allOptions[0].t_education
    allLevel = allOptions[0].t_level
    allTitle = allOptions[0].t_title
    allProvince = allOptions[0].t_province
    allSchool = allOptions[0].t_school
    allFrom = allOptions[0].t_from
    # return render(request, 'teachersManage.html', locals())
    return render(request, 'teachersManage.html',
                  {'page': page, 'allSex': allSex, 'allEducation': allEducation, 'allLevel': allLevel,
                   'allTitle': allTitle,
                   'allProvince': allProvince, 'allSchool': allSchool, 'allFrom': allFrom})


@csrf_exempt
def screen(request):
    print('我是screen')
    print(request.POST)
    screenInfo = request.POST['screenInfo'].split(",")  # 字符串转为列表，[0]是序号，[1]是筛选的值
    sid = screenInfo[0]
    value = screenInfo[1]
    print(value)
    print(sid[0])
    # 序号[0]是筛选的区分，字符串第一位1性别，2是职级，4是职称，3是学历
    # 根据序号来判断筛选哪个值
    field = ''
    if (sid[0] == '1'):
        field = 't_sex'
    elif (sid[0] == '2'):
        field = 't_title'
    elif (sid[0] == '3'):
        field = 't_education'
    elif (sid[0] == '4'):
        field = 't_level'
    elif (sid[0] == '5'):
        field = 't_province'
    elif (sid[0] == '6'):
        field = 't_school'
    elif (sid[0] == '7'):
        field = 't_from'

    if value == '全部':
        teachers = models.teacherModel.objects.all()
    else:
        teachers = models.teacherModel.objects.filter(**{field: value})
    teacherList = []
    for i in teachers:
        teacherList.append(i)
    paginator = Paginator(teacherList, len(teacherList))
    page = paginator.page(1)  # 传递当前页的实例对象到前端
    print(page)
    # 从数据库中读取制作好的各选项的json数据，想到将这些数据直接写入数据库然后读出来我还是牛逼的
    allOptions = models.allOptions.objects.all()
    print(allOptions[0].t_education)
    allSex = allOptions[0].t_sex
    allEducation = allOptions[0].t_education
    allLevel = allOptions[0].t_level
    allTitle = allOptions[0].t_title
    allProvince = allOptions[0].t_province
    allSchool = allOptions[0].t_school
    allFrom = allOptions[0].t_from
    return render(request, 'teachersManage.html',
                  {'page': page, 'allSex': allSex, 'allEducation': allEducation, 'allLevel': allLevel,
                   'allTitle': allTitle,
                   'allProvince': allProvince, 'allSchool': allSchool, 'allFrom': allFrom})