from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
from allTeachers import models


def teachersShow(request):
    print('我是teachersShow页面')
    # 读取所有的字段数据，使用values_list可以读取期中的一个字段组成列表
    allTeachersInfo = models.teacherModel.objects.all()
    tEducation = [0] * 6
    tLevelJs = 0
    tLevelFjs = 0
    tLevelZjjs = 0
    tLevelZj = 0
    tLevelYjy = 0
    tLevelFyjy = 0
    tLevelZlyjy = 0
    tLevelYjsxy = 0
    tLevelQt = 0
    tSexM = 0
    tSexF = 0
    tTitle = [0] * 9
    tFrom = [0] * 6
    tProvince_sn = 0
    tProvince_sw = 0
    for one in allTeachersInfo:
        # 计算学历的个数
        if one.t_education == '博士研究生':
            tEducation[0] += 1
        elif one.t_education == '硕士研究生':
            tEducation[1] += 1
        elif one.t_education == '本科':
            tEducation[2] += 1
        elif one.t_education == '大专':
            tEducation[3] += 1
        elif one.t_education == '专科':
            tEducation[4] += 1
        else:
            tEducation[5] += 1

        # 计算职称的个数
        if one.t_level == '教授':
            tLevelJs = tLevelJs + 1
        elif one.t_level == '副教授':
            tLevelFjs = tLevelFjs + 1
        elif one.t_level == '讲师':
            tLevelZjjs = tLevelZjjs + 1
        elif one.t_level == '助教':
            tLevelZj = tLevelZj + 1
        elif one.t_level == '研究员':
            tLevelYjy = tLevelYjy + 1
        elif one.t_level == '副研究员':
            tLevelFyjy = tLevelFyjy + 1
        elif one.t_level == '助理研究员':
            tLevelZlyjy = tLevelZlyjy + 1
        elif one.t_level == '研究实习员':
            tLevelYjsxy = tLevelYjsxy + 1
        else:
            tLevelQt = tLevelQt + 1

        # 计算男女的个数
        if one.t_sex == '男':
            tSexM = tSexM + 1
        else:
            tSexF = tSexF + 1

        # 计算职级的个数
        print(tTitle[1])
        if one.t_title == '省部级':
            tTitle[0] += 1
        elif one.t_title == '正厅':
            tTitle[1] += 1
        elif one.t_title == '副厅':
            tTitle[2] += 1
        elif one.t_title == '正处':
            tTitle[3] += 1
        elif one.t_title == '副处':
            tTitle[4] += 1
        elif one.t_title == '正科':
            tTitle[5] += 1
        elif one.t_title == '副科':
            tTitle[6] += 1
        elif one.t_title == '科员':
            tTitle[7] += 1
        else:
            tTitle[8] += 1

        # 计算行业的个数
        if one.t_from == '政府机关':
            tFrom[1] += 1
        elif one.t_from == '党校':
            tFrom[2] += 1
        elif one.t_from == '高校':
            tFrom[3] += 1
        elif one.t_from == '企业':
            tFrom[4] += 1
        else:
            tFrom[5] += 1

        # 计算省内外的个数
        if one.t_province == '省内':
            tProvince_sn += 1
        else:
            tProvince_sw += 1

    tFrom[0] = tFrom[1] + tFrom[2] + tFrom[3] + tFrom[4] + tFrom[5]
    # ztbcPeople = ztbcPeople + int(float(i.c_people))

    return render(request, 'teachersShowHtml.html', locals())
