from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http.response import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import json
from datetime import datetime
import operator
import requests
import math

from django.contrib import auth
from .models import BasicInfo, AcademicInfo, PaperInfo, InfluenceInfo, InfluenceTime, \
    PapersTime, PaperRelation, OrganizationInfo, OpinionRaw, UserFav, User, \
    Hometown, HometownRelation, ThemeRelation, MyUser

universities_abbreviation = {
    '北大': '北京大学', '人大': '中国人民大学', '清华': '清华大学', '北航': '北京航空航天大学', '北理': '北京理工大学', '中国农大': '中国农业大学', '北师': '北京师范大学',
    '中央民大': '中央民族大学', '南开': '南开大学', '天大': '天津大学', '大工': '大连理工大学', '大连理工': '大连理工大学', '吉大': '吉林大学', '哈工大': '哈尔滨工业大学',
    '复旦': '复旦大学', '同济': '同济大学', '上海交大': '上海交通大学', '华东师大': '华东师范大学', '南大': '南京大学', '东大': '东南大学', '中国矿大': '中国矿业大学',
    '浙大': '浙江大学', '中国科大': '中国科学技术大学', '厦大': '厦门大学', '山大': '山东大学', '中国海大': '中国海洋大学', '武大': '武汉大学', '湖大': '湖南大学',
    '中大': '中山大学', '华南理工': '华南理工大学', '重大': '重庆大学', '电子科大': '电子科技大学', '西安交大': '西安交通大学', '西工大': '西北工业大学', '西北工大': '西北工业大学',
    '兰大': '兰州大学', '川大': '四川大学', '西农': '西北农林科技大学', '西北农大': '西北农林科技大学', '中南': '中南大学', '华中大': '华中科技大学', '北京交大': '北京交通大学',
    '北工大': '北京工业大学',
    '北科': '北京科技大学', '北化': '北京化工大学', '北邮': '北京邮电大学', '北林': '北京林业大学', '北中医': '北京中医药大学', '北外': '北京外国语大学',
    '中财': '中央财经大学', '央财': '中央财经大学', '外经贸': '对外经济贸易大学', '贸大': '对外经济贸易大学', '北体': '北京体育大学', '法大': '中国政法大学', '华电': '华北电力大学',
    '河北工大': '河北工业大学',
    '太原理工': '太原理工大学', '大连海大': '大连海事大学', '海大': '大连海事大学', '东北师大': '东北师范大学', '哈工程': '哈尔滨工程大学', '东北林大': '东北农业大学',
    '华理': '华东理工大学',
    '上外': '上海外国语大学', '上海财大': '上海财经大学', '上财': '上海财经大学', '苏大': '苏州大学', '南航': '南京航空航天大学', '南理工': '南京理工大学', '河海': '河海大学',
    '南农': '南京农业大学', '南京农大': '南京农业大学', '中国药大': '中国药科大学', '南京师大': '南京师范大学', '南师大': '南京师范大学', '南师': '南京师范大学', '安大': '安徽大学',
    '合肥工大': '合肥工业大学', '合工大': '合肥工业大学',
    '福大': '福州大学', '郑大': '郑州大学', '华中农大': '华中农业大学', '华农': '华中农业大学', '华中师大': '华中师范大学', '湖南师大': '湖南师范大学', '暨大': '暨南大学',
    '华南农大': '华南农业大学',
    '西南交大': '西南交通大学', '四川农大': '四川农业大学', '川农大': '四川农业大学', '西南财大': '西南财经大学', '西财': '西南财经大学', '贵大': '贵州大学', '云大': '云南大学',
    '西电': '西安电子科技大学',
    '陕西师大/陕师大': '陕西师范大学', '中国矿大（北京）': '中国矿业大学（北京）', '地大': '中国地质大学(北京)', '北京地大': '中国地质大学(北京)', '上大': '上海大学',
    '中南大': '中南财经政法大学',
    '武汉理工': '武汉理工大学', '中媒': '中国传媒大学', '地大': '中国地质大学', '中石大': '中国石油大学（北京）', '福师': '福建师范大学'
}


def basic_info_2_json(obj):
    return {
        'id': obj.id,
        'name': obj.name,
        'university': obj.university,
        'college': obj.college,
        'theme_list': obj.theme_list,
        'sub_list': obj.sub_list,
        'resume': obj.resume,
        'img_url': obj.img_url,
        'url1': obj.url1,
        'url2': obj.url2
    }


def to_dict(obj):
    # type(self._meta.fields).__name__
    return dict([(attr, getattr(obj, attr)) for attr in [f.name for f in obj._meta.fields]])


def sort_experts(all_experts):
    experts = []
    result = []
    # scores = []
    for expert in all_experts:
        influ_info = InfluenceInfo.objects.get(id=expert.id)
        score = influ_info.influ
        tup = (expert, score)
        experts.append(tup)

    tmp = sorted(experts, key=lambda expert: expert[1], reverse=True)
    for ele in tmp:
        dic = to_dict(ele[0])
        dic['score'] = str(ele[1])
        # print(dic)
        result.append(json.dumps(dic))
        # print('学者排名得分：' + str(ele[1]))

    return result


def sort_experts_solr(all_experts):
    # TODO 修改 solr 的 basic 核，加入影响力字段
    url_basic = 'http://127.0.0.1:8983/solr/influence_info/select?wt=json&rows=1&q='
    result = []

    for expert in all_experts:
        query_url = url_basic + 'id:' + expert['id']
        score = requests.get(query_url).json()['response']['docs'][0]['influ']
        expert['score'] = score

    all_experts.sort(key=lambda x: x['score'], reverse=True)
    for expert in all_experts:
        result.append(json.dumps(expert))
    return result


def sort_papers(papers):
    paper_list = []
    result = []
    for paper in papers:
        if paper.citation is None:
            paper.citation = 0
        paper_list.append(to_dict(paper))

    paper_list.sort(key=lambda x: x['citation'], reverse=True)
    for paper in paper_list:
        result.append(json.dumps(paper))
    return result


def sort_experts_by_field(field_experts):
    result = []
    # experts = []
    print(len(field_experts))
    for expert in field_experts:
        score = expert.influ
        # print(score)
        if score > 70:
            basic_info = BasicInfo.objects.get(id=expert.id)
            dic = to_dict(basic_info)
            dic['score'] = score
            result.append(json.dumps(dic))
        if len(result) >= 5:
            break
    # tmp = sorted(experts, key=lambda expert : expert[1], reverse=True)
    #
    # for ele in tmp:
    #     dic = toDict(ele[0])
    #     dic["score"] = str(ele[1])
    #     # print(dic)
    #     result.append(json.dumps(dic))

    return result


def sort_experts_by_field_solr(field_experts):
    # TODO 修改 solr 的 basic 核，加入影响力字段
    url_basic = 'http://127.0.0.1:8983/solr/influence_info/select?wt=json&rows=1&q='
    result = []
    experts = []

    for expert in field_experts:
        query_url = url_basic + 'id:' + expert.id
        expert_info = requests.get(query_url).json()['response']['docs'][0]
        experts.append(expert_info)

    experts.sort(key=lambda x: x['influ'], reverse=True)
    for expert in experts:
        result.append(json.dumps(expert))
    return result


def find_hometowm_experts(expert_id):
    try:
        hometown_id = HometownRelation.objects.get(id=expert_id).hometown_id
        # TODO 根据同乡分级进行显示,确定返回信息的粒度
        hometown_info = Hometown.objects.get(id=hometown_id)
        expert_list = hometown_info.list
        result = []
        if expert_list == "set()":
            return result

        for expert_id in expert_list[1:-1].replace(' ', '').split(','):
            result.append(json.dumps(to_dict(BasicInfo.objects.get(id=expert_id[1:-1]))))

        return result
    except:
        return []


def find_interest_experts(theme_list):
    try:
        result = []
        theme_infos = []
        for theme in theme_list.split('、'):
            theme_infos = ThemeRelation.objects.filter(theme=theme)
        if theme_infos is not None:
            for theme_info in theme_infos:
                result.append(json.dumps(to_dict(BasicInfo.objects.get(id=theme_info.expert_id))))

        return result
    except:
        return []


# 首页展示
def index(request):
    # Chinese classification number
    ccn_experts = [
        {'ccn_number': 'A', 'ccn_name': '马克思主义、列宁主义、毛泽东思想、邓小平理论', 'experts': []},
        {'ccn_number': 'B', 'ccn_name': '哲学、宗教', 'experts': []},
        {'ccn_number': 'C', 'ccn_name': '社会科学总论', 'experts': []},
        {'ccn_number': 'D', 'ccn_name': '政治、法律', 'experts': []},
        {'ccn_number': 'E', 'ccn_name': '军事', 'experts': []},
        {'ccn_number': 'F', 'ccn_name': '经济', 'experts': []},
        {'ccn_number': 'G', 'ccn_name': '文化、科学、教育、体育', 'experts': []},
        {'ccn_number': 'H', 'ccn_name': '语言、文字', 'experts': []},
        {'ccn_number': 'I', 'ccn_name': '文学', 'experts': []},
        {'ccn_number': 'J', 'ccn_name': '艺术', 'experts': []},
        {'ccn_number': 'K', 'ccn_name': '历史、地理', 'experts': []},
        {'ccn_number': 'N', 'ccn_name': '自然科学总论', 'experts': []},
        {'ccn_number': 'O', 'ccn_name': '数理科学和化学', 'experts': []},
        {'ccn_number': 'P', 'ccn_name': '天文学、地球科学', 'experts': []},
        {'ccn_number': 'Q', 'ccn_name': '生物科学', 'experts': []},
        {'ccn_number': 'R', 'ccn_name': '医药、卫生', 'experts': []},
        {'ccn_number': 'S', 'ccn_name': '农业科学', 'experts': []},
        {'ccn_number': 'T', 'ccn_name': '工业技术', 'experts': []},
        {'ccn_number': 'U', 'ccn_name': '交通运输', 'experts': []},
        {'ccn_number': 'V', 'ccn_name': '航空、航天', 'experts': []},
        {'ccn_number': 'X', 'ccn_name': '环境科学、安全科学', 'experts': []},
        {'ccn_number': 'Z', 'ccn_name': '综合性图书', 'experts': []}
    ]

    url_basic = 'http://127.0.0.1:8983/solr/influence_info/select?wt=json&rows=5&q='

    for ccn_expert in ccn_experts:
        # print(ccn_expert)
        # date1 = datetime.now()
        # field_experts = InfluenceInfo.objects.filter(field=ccn_expert['ccn_number'], influ__gt=70)
        query_url = url_basic + 'field:' + ccn_expert['ccn_number'] + '&fq=influ:[70 TO *]'

        result = requests.get(query_url)
        # print(result)

        # 取前五位专家的影响力分数，加在其 basicInfo 数据后面
        ccn_expert['experts'] = []
        hottest_five_result = result.json()['response']['docs'][:5]
        for expert in hottest_five_result:
            basic_info = BasicInfo.objects.get(id=expert['id'])
            dic = to_dict(basic_info)
            dic['score'] = expert['influ']
            ccn_expert['experts'].append(json.dumps(dic))

            # ccn_expert['experts'] = result.json()['response']['docs'][:5]

            # date2 = datetime.now()
            # print("time1:" + str((date2 - date1).seconds))
            # if len(field_experts) > 0:
            #     ccn_expert['experts'] = field_experts[:5]
            #     print("time2:" + str((datetime.now() - date1).seconds))

    # 暂时钦定
    hottest_five_organization_id = ['1', '2', '3', '4', '15']
    hottest_five_organizations = []
    for _id in hottest_five_organization_id:
        hottest_five_organizations.append(json.dumps(to_dict(OrganizationInfo.objects.get(index=_id))))

    hottest_five_experts_id = ['100000000463735', '100000004171913', '100000012865060', '100000012177090',
                               '100000010801473']
    hottest_five_experts = []
    for _id in hottest_five_experts_id:
        basic_info = BasicInfo.objects.get(id=_id)
        basic_dic = to_dict(basic_info)
        influ_info = InfluenceInfo.objects.get(id=_id)
        influ_dic = to_dict(influ_info)
        basic_dic['score'] = influ_dic['influ']
        hottest_five_experts.append(json.dumps(basic_dic))
        # hottest_five_experts.append(json.dumps(to_dict(BasicInfo.objects.get(id=_id))))

    result = {
        'ccn_experts': json.dumps(ccn_experts),
        'hottest_five_organizations': json.dumps(hottest_five_organizations),
        'hottest_five_experts': json.dumps(hottest_five_experts)
    }

    # print(type(result))
    # print(result)

    if request.is_ajax():
        print('AJAX 访问 index')
        return HttpResponse(json.dumps(result))
        # return render_to_response('index.html', result)
    else:
        print('非 AJAX 访问 index')
        # return HttpResponse(json.dumps(result))
        return render_to_response('index.html')
        # return render_to_response('index.html', result)


# 专家列表展示
def expert_list(request):
    # all_experts = BasicInfo.objects.all()[:10]
    # TODO 分页问题，由前端处理转到后端处理
    per_page_count = 10
    url_basic = 'http://127.0.0.1:8983/solr/basic_info/select?wt=json&rows=' + str(
        per_page_count) + '&sort=score desc,influ desc'

    query_type = request.GET.get('query_type', '')
    query_selection = request.GET.get('query_selection', '')
    query_input = request.GET.get('query_input', '')
    researcher = request.GET.get('researcher_input', '')
    field = request.GET.get('field_input', '')
    research_content = request.GET.get('research_content_input', '')
    organization = request.GET.get('organization_input', '')
    current_page = request.GET.get('current_page', 1)

    current_page_int = int(current_page)
    start = (current_page_int - 1) * per_page_count
    url_basic += '&start=' + str(start) + '&q='
    result_num = 0

    # print(query_type, query_input, query_selection)
    if query_type == 'normal':
        if query_selection == 'researcher':
            # all_experts = BasicInfo.objects.filter(name__icontains=query_input)
            # TODO 判定何时使用精确匹配，何时使用模糊匹配，以及模糊之后的排序问题
            query_url = url_basic + 'name:' + '\'' + query_input + '\''
            response = requests.get(query_url).json()['response']
            all_experts = response['docs']
            result_num = response['numFound']
        elif query_selection == 'field':
            # all_experts = BasicInfo.objects.filter(theme_list__icontains=query_input)
            query_url = 'http://127.0.0.1:8983/solr/basic_info/' + \
                        'select?wt=json&rows=10&bf=influ&defType=edismax&mm=2&qf=theme_list&start=' + str(start) + \
                        '&q=' + query_input
            response = requests.get(query_url).json()['response']
            all_experts = response['docs']
            result_num = response['numFound']
        elif query_selection == 'research-content':
            # all_experts = BasicInfo.objects.filter(sub_list__icontains=query_input)
            query_url = url_basic + 'sub_list:' + query_input
            response = requests.get(query_url).json()['response']
            all_experts = response['docs']
            result_num = response['numFound']
        elif query_selection == 'organization':
            # all_experts = BasicInfo.objects.filter(university__icontains=query_input)
            if query_input in universities_abbreviation:
                query_input = universities_abbreviation[query_input]
                query_url = url_basic + 'university:' + query_input
            else:
                query_url = url_basic + 'university:' + query_input + '~'
            response = requests.get(query_url).json()['response']
            all_experts = response['docs']
            result_num = response['numFound']
        else:
            raise Http404

    elif query_type == 'advanced':
        # TODO 改用 intersection 操作，避免 where 子句中用 and 操作，使用 qs1 = intersection(qs2, qs3)
        if len(researcher) != 0:
            experts1 = BasicInfo.objects.filter(name__icontains=researcher)
        else:
            experts1 = BasicInfo.objects.all()
        if len(field) != 0:
            experts2 = BasicInfo.objects.filter(theme_list__icontains=field)
        else:
            experts2 = BasicInfo.objects.all()
        if len(research_content) != 0:
            experts3 = BasicInfo.objects.filter(sub_list__icontains=research_content)
        else:
            experts3 = BasicInfo.objects.all()
        if len(organization) != 0:
            if organization in universities_abbreviation:
                organization = universities_abbreviation[organization]
            experts4 = BasicInfo.objects.filter(university__icontains=organization)
        else:
            experts4 = BasicInfo.objects.all()
        # experts2 = BasicInfo.objects.filter(name__icontains=field)
        # experts3 = BasicInfo.objects.filter(name__icontains=research_content)
        # experts4 = BasicInfo.objects.filter(name__icontains=organization)
        #
        all_experts = experts1 & experts2 & experts3 & experts4

    else:
        raise Http404

    # TODO 同时返回 result_num 用于计算页数
    # result = sort_experts_solr(all_experts)
    result = []

    if isinstance(all_experts, list):
        for expert in all_experts:
            expert['score'] = expert['influ']
            result.append(json.dumps(expert))
    else:
        result_num = len(all_experts)
        for expert in all_experts:
            dict = to_dict(expert)

            dict['score'] = InfluenceInfo.objects.get(id=expert.id).influ
            result.append(json.dumps(dict))
    result.append(result_num)
    # print(result)

    if request.is_ajax():
        print('AJAX 访问 expert_list', len(result))
        return HttpResponse(json.dumps(result))
    else:
        print('非 AJAX 访问 expert_list', len(result))
        # return HttpResponse(json.dumps(result))
        return render_to_response('index.html')


# 专家详情展示
def expert_detail(request):
    per_page_count = 10
    expert_id = request.GET.get('id', '')

    expert_basic = BasicInfo.objects.get(id=expert_id)
    opinion_raw = OpinionRaw.objects.get(expert_id=expert_id)

    expert_academic = AcademicInfo.objects.get(id=expert_id)
    expert_relation = PaperRelation.objects.get(id=expert_id)
    expert_influ = InfluenceInfo.objects.get(id=expert_id)
    expert_influ_time = InfluenceTime.objects.get(id=expert_id)
    expert_paper_time = PapersTime.objects.get(id=expert_id)
    current_page = request.GET.get('current_page', 1)

    current_page_int = int(current_page)
    start = (current_page_int - 1) * per_page_count
    result_num = 0
    url_paper = 'http://127.0.0.1:8983/solr/paper_info/select?wt=json&rows=10&sort=citation desc'
    url_paper += '&start=' + str(start) + '&q='

    query_url = url_paper + 'author1:' + expert_id + ' OR author2:' + expert_id + ' OR author3:' + \
                expert_id + ' OR author4:' + expert_id + ' OR author5:' + expert_id
    response = requests.get(query_url).json()['response']
    paper_row_list = response['docs']
    result_num = response['numFound']
    paper_list = []
    for paper in paper_row_list:
        paper_list.append(json.dumps(to_dict(PaperInfo.objects.get(paper_id=paper['id']))))

    co_experts_id = []
    co_years = []
    co_scores = []

    if expert_relation.coid_list is not None:
        for co_expert_id in expert_relation.coid_list[1:-1].replace(' ', '').split(','):
            co_experts_id.append(co_expert_id[1:-1])
        for co_year in expert_relation.year_list[1:-1].replace(' ', '').split(','):
            co_years.append(co_year[1:-1])
        for co_score in expert_relation.score_list[1:-1].replace(' ', '').split(','):
            co_scores.append(co_score)

    co_experts_info = []
    for i in range(len(co_experts_id)):
        co_expert_id = co_experts_id[i]
        co_year = co_years[i]
        co_score = co_scores[i]
        try:
            basic_info = BasicInfo.objects.get(id=co_expert_id)
            dicts = {
                'id': co_expert_id,
                'name': basic_info.name,
                'resume': basic_info.resume,
                'img_url': basic_info.img_url,
                'co_year': co_year,
                'co_score': co_score,
            }
            co_experts_info.append(json.dumps(dicts))
        except:
            print('数据库中无此学者id:' + co_expert_id + '对应的信息')
            pass

    # print(co_experts_info)
    same_hometown_experts = find_hometowm_experts(expert_id)
    similar_interest_experts = find_interest_experts(expert_basic.theme_list)

    result = {
        'expert_basic': json.dumps(to_dict(expert_basic)),
        'expert_academic': json.dumps(to_dict(expert_academic)),
        'papers': json.dumps(paper_list),
        'co_experts_info': json.dumps(co_experts_info),
        'influence_info': json.dumps(to_dict(expert_influ)),
        'influence_time': json.dumps(to_dict(expert_influ_time)),
        'paper_time': json.dumps(to_dict(expert_paper_time)),
        'opinion_raw': json.dumps(to_dict(opinion_raw)),
        'same_hometown_experts': json.dumps(same_hometown_experts),
        'similar_interest_experts': json.dumps(similar_interest_experts),
        'paper_num': result_num
    }

    # print(result)

    if request.is_ajax():
        print('AJAX 访问 expert_detail', len(result))
        return HttpResponse(json.dumps(result))
    else:
        print('非 AJAX 访问 expert_detail', len(result))
        return HttpResponse(json.dumps(result))
        # return render_to_response('index.html')
        # return render(request, 'detail.html', result)


def login(request):
    login_result = 'fail'

    if request.method == 'GET':
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user.id

            login_result = 'success'

        result = {
            'loginResult': login_result,
        }

        return HttpResponse(json.dumps(result))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user.id

            login_result = 'success'

        result = {
            'loginResult': login_result,
        }

        return HttpResponse(json.dumps(result))


def user_center(request):
    login_result = 'fail'
    if request.method == 'GET':
        if 'user_id' in request.session.keys():
            login_result = 'success'
            user_id = request.session['user_id']
            print(user_id)
            user = User.objects.get(id=user_id)
            # print(user)
            # print(type(user))
            # if hasattr(user, 'myuser'):
            #     print('myuser is in user')
            # else:
            #     print('myuser is NOT in user')

            myuser = user.myuser

            user_fav = UserFav.objects.filter(user=user.id)
            experts = []
            for userfav in user_fav:
                experts.append(json.dumps(to_dict(BasicInfo.objects.get(id=userfav.expert_id))))

            myuser_dict = {}
            myuser_dict_temp = to_dict(myuser)

            if 'id' in myuser_dict_temp:
                myuser_dict['id'] = myuser_dict_temp['id']
            if 'nickname' in myuser_dict_temp:
                myuser_dict['nickname'] = myuser_dict_temp['nickname']
            if 'interests' in myuser_dict_temp:
                myuser_dict['interests'] = myuser_dict_temp['interests']
            if 'user_id' in myuser_dict_temp:
                myuser_dict['user_id'] = myuser_dict_temp['user_id']
            if 'gender' in myuser_dict_temp:
                myuser_dict['gender'] = myuser_dict_temp['gender']
            if 'company' in myuser_dict_temp:
                myuser_dict['company'] = myuser_dict_temp['company']

            result = {
                'loginResult': login_result,
                'myuser': json.dumps(myuser_dict),
                'favExperts': json.dumps(experts),
            }

            return HttpResponse(json.dumps(result))

        else:
            result = {
                'loginResult': login_result,
            }

            return HttpResponse(json.dumps(result))


def edit_info(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        myuser = user.myuser

        username = request.GET.get('username', '')
        company = request.GET.get('company', '')
        interests = request.GET.get('interests', '')
        gender = request.GET.get('gender', '')

        myuser.nickname = username
        myuser.company = company
        myuser.interests = interests
        myuser.gender = gender
        myuser.save()

        myuser_dict = {}
        myuser_dict_temp = to_dict(myuser)

        if 'id' in myuser_dict_temp:
            myuser_dict['id'] = myuser_dict_temp['id']
        if 'nickname' in myuser_dict_temp:
            myuser_dict['nickname'] = myuser_dict_temp['nickname']
        if 'interests' in myuser_dict_temp:
            myuser_dict['interests'] = myuser_dict_temp['interests']
        if 'user_id' in myuser_dict_temp:
            myuser_dict['user_id'] = myuser_dict_temp['user_id']
        if 'gender' in myuser_dict_temp:
            myuser_dict['gender'] = myuser_dict_temp['gender']
        if 'company' in myuser_dict_temp:
            myuser_dict['company'] = myuser_dict_temp['company']

        # return HttpResponseRedirect(reverse('login'))
        result = {"myuser": json.dumps(myuser_dict)}
        return HttpResponse(json.dumps(result))

    if request.method == 'POST':
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        myuser = user.myuser

        username = request.POST.get('username', '')
        company = request.POST.get('company', '')
        interests = request.POST.get('interests', '')
        gender = request.POST.get('gender', '')

        myuser.nickname = username
        myuser.company = company
        myuser.interests = interests
        myuser.gender = gender
        myuser.save()

        myuser_dict = {}
        myuser_dict_temp = to_dict(myuser)

        if 'id' in myuser_dict_temp:
            myuser_dict['id'] = myuser_dict_temp['id']
        if 'nickname' in myuser_dict_temp:
            myuser_dict['nickname'] = myuser_dict_temp['nickname']
        if 'interests' in myuser_dict_temp:
            myuser_dict['interests'] = myuser_dict_temp['interests']
        if 'user_id' in myuser_dict_temp:
            myuser_dict['user_id'] = myuser_dict_temp['user_id']
        if 'gender' in myuser_dict_temp:
            myuser_dict['gender'] = myuser_dict_temp['gender']
        if 'company' in myuser_dict_temp:
            myuser_dict['company'] = myuser_dict_temp['company']
        # return HttpResponseRedirect(reverse('login'))
        result = {"myuser": json.dumps(to_dict(myuser))}
        return HttpResponse(json.dumps(result))


def change_pwd(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        # myuser = user.myuser

        pwd1 = request.GET.get('pwd1', '')
        pwd2 = request.GET.get('pwd2', '')

        if pwd1 == pwd2:
            user.set_password(pwd1)
            user.save()
            result = {
                'changePwdResult': '修改成功',
            }
            return HttpResponse(json.dumps(result))
        else:
            result = {
                'changePwdResult': '两次密码不一致',
            }
            return HttpResponse(json.dumps(result))

    if request.method == 'POST':
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        myuser = user.myuser

        pwd1 = request.POST.get('pwd1', '')
        pwd2 = request.POST.get('pwd2', '')

        if pwd1 == pwd2:
            user.set_password(pwd1)
            user.save()
            result = {
                'changePwdResult': '修改成功',
            }
            return HttpResponse(json.dumps(result))
        else:
            result = {
                'changePwdResult': '两次密码不一致',
            }
            return HttpResponse(json.dumps(result))


def add_fav(request):
    if request.method == 'GET':
        if 'user_id' in request.session.keys():
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)

            expert_id = request.GET.get('expert_id',)
            user_fav = UserFav.create(user, expert_id)
            user_fav.save()

            return HttpResponse("添加成功")
        else:
            #TODO 或者可以写一个登陆页面，直接跳转
            return HttpResponse("请先登陆")



def logout(request):
    try:
        del request.session['user_id']
        result = {
            'logoutResult': 'success'
        }
    except:
        result = {
            'logoutResult': 'fail'
        }

    # TODO 这里需要返回状态,还是跳转回主页
    return HttpResponse(json.dumps(result))
    # user_id = request.session['user_id']
    # user = User.objects.get(id=user_id)
    # auth.logout(request)
    # # 返回主页
    # return HttpResponseRedirect(reverse('index'))

# def login(request):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             # TODO 延迟后重定向到之前的界面
#             return HttpResponse("<p>您已登录" + request.user.username + "</p >")
#         return render(request, "login.html")
#     elif request.method == 'POST':
#         print("test")
#         context = {}
#         username = request.POST.get("username", "")
#         pwd = request.POST.get("password", "")
#         user = auth.authenticate(username=username, password=pwd)
#         print("————————————")
#         # context["fav_experts"] = UserFav.objects.filter(user=user)
#
#         # print(context)
#         if user is not None:
#             auth.login(request, user)
#             return render(request, "user1.html")
#         # TODO Group数据表
#         # expert_groups = ExpertGroup.objects.filter(user=user)
#         # new_dict = {}
#         # for expert_group in expert_groups:
#         #     if expert_group.name not in dict.keys():
#         #         new_list = [expert_group.expert_id]
#         #         new_dict[expert_group.name] = new_list
#         #     else:
#         #         new_dict[expert_group.name].append(expert_group.expert_id)
#         # # print(dict.keys())
#         # # print("对应的值：" + str(dict.get("第一个测试分组")))
#         # context["expert_groups"] = dict
#         # if user is not None:
#         #     auth.login(request, user)
#         #     return render(request, "success.html", context=context)
#         # else:
#         #     return render(request, "fail.html")
#     else:
#         print('login request type ERROR!!!')
#
#
# def register(request):
#     if request.method == 'GET':
#         return render(request, "register.html")
#     elif request.method == 'POST':
#         errors = []
#         username = request.POST.get("username", "")
#         pwd1 = request.POST.get("password1", "")
#         pwd2 = request.POST.get("password2", "")
#         # TODO 合法性检查
#         if (pwd1 != pwd2):
#             errors.append("两次输入密码不一致")
#         else:
#             user = User.objects.create_user(username=username, password=pwd1)
#             user.save()
#             user = auth.authenticate(username=username, password=pwd1)
#             auth.login(request, user)
#             return render(request, "success.html")  # HttpResponseRedirect('/')
#
#         return render_to_response("register.html", {'errors': errors})
#     else:
#         print('register request type ERROR!!!')
