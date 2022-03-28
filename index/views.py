from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from allTeachers import models


def index(request):
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
    tFromZfjg = 0
    tFromDx = 0
    tFromGx = 0
    tFromQy = 0
    tFromQt = 0
    tTitleSbj = 0
    tTitleZt = 0
    tTitleFt = 0
    tTitleZc = 0
    tTitleFc = 0
    tTitleZk = 0
    tTitleFk = 0
    tTitleKy = 0
    tTitleQt = 0

    for one in allTeachersInfo:
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

        # 计算职级的个数
        if one.t_title == '省部级':
            tTitleSbj += 1
        elif one.t_title == '正厅':
            tTitleZt += 1
        elif one.t_title == '副厅':
            tTitleFt += 1
        elif one.t_title == '正处':
            tTitleZc += 1
        elif one.t_title == '副处':
            tTitleFc += 1
        elif one.t_title == '正科':
            tTitleZk += 1
        elif one.t_title == '副科':
            tTitleFk += 1
        elif one.t_title == '科员':
            tTitleKy += 1
        else:
            tTitleQt += 1

        # 计算C行业的个数
        if one.t_from == '政府机关':
            tFromZfjg += 1
        elif one.t_from == '党校':
            tFromDx += 1
        elif one.t_from == '高校':
            tFromGx += 1
        elif one.t_from == '企业':
            tFromQy += 1
        else:
            tFromQt += 1

    tTitleTj = tTitleZt + tTitleFt
    tTitleCj = tTitleZc + tTitleFc
    tTitleKj = tTitleZk + tTitleFk
    # ztbcPeople = ztbcPeople + int(float(i.c_people))
    return render(request, 'index.html', locals())