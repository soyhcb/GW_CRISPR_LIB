from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse, QueryDict
from django.db.models import Q
import json

from django_pandas.io import read_frame
# import django_tables2 as tables

from crispr_lib.models import Crispr
# Create your views here.

#==================set table view=====================
# class CrisprTable(tables.Table):
#     class Meta:
#         model = Crispr
#         attrs = {"id": "result_table", 'style':"margin-bottom: 5vh;"}
FIELD_LIST = (
    'id',
    'gene',
    'ccds_id',
    'gsrna_ccds',
    'gsrna_seq',
    'genome_position',
    'offtarget_score',
    'ontarget_score',
    'surface_protein',
    'grna_number',
    'gene_id',
    'extended_sequence',
    'grna_efficacy',
    'grna_s_plus_pam',
    'top5_offtarget_total_score',
    'top1Hit_onTarget_MMdistance2PAM',
    'topOfftarget1MMdistance2PAM',
    'topOfftarget2MMdistance2PAM',
    'topOfftarget3MMdistance2PAM',
    'topOfftarget4MMdistance2PAM',
    'topOfftarget5MMdistance2PAM',
    'topOfftarget6MMdistance2PAM',
    'topOfftarget7MMdistance2PAM',
    'topOfftarget8MMdistance2PAM',
    'topOfftarget9MMdistance2PAM',
    'topOfftarget10MMdistance2PAM',
)
INCLUDE_LIST = (
    # 'id',
    'gene',
    'ccds_id',
    'gsrna_ccds',
    'gsrna_seq',
    'genome_position',
    'offtarget_score',
    'ontarget_score',
    # 'surface_protein',
    # 'grna_number',
    # 'gene_id',
    # 'extended_sequence',
    # 'grna_efficacy',
    # 'grna_s_plus_pam',
    # 'top5_offtarget_total_score',
    # 'top1Hit_onTarget_MMdistance2PAM',
    # 'topOfftarget1MMdistance2PAM',
    # 'topOfftarget2MMdistance2PAM',
    # 'topOfftarget3MMdistance2PAM',
    # 'topOfftarget4MMdistance2PAM',
    # 'topOfftarget5MMdistance2PAM',
    # 'topOfftarget6MMdistance2PAM',
    # 'topOfftarget7MMdistance2PAM',
    # 'topOfftarget8MMdistance2PAM',
    # 'topOfftarget9MMdistance2PAM',
    # 'topOfftarget10MMdistance2PAM',
)
#=====================================================

def get_crispr(request):
    assert(request.method == "POST")
    keywords_raw = request.POST.get('search_keywords')
    keywords = keywords_raw.replace('\n', ',').replace(' ', ',').replace('\r', '')
    keywords = keywords.split(',')
    keywords = list(filter(None, keywords))
    keywords_CCDS = set([x for x in keywords if x[:4].upper() == "CCDS"])
    keywords_GS = list(set(keywords) - keywords_CCDS)
    keywords_CCDS = list(keywords_CCDS)
    results = Crispr.objects.filter(Q(ccds_id__in=keywords_CCDS) | Q(gene__in=keywords_GS))
    found_info = {"hit":[], "miss":[]}
    df = read_frame(results, fieldnames=INCLUDE_LIST)
    got_keywords = set(df["gene"])
    for kw in keywords_GS:
        if kw in got_keywords:
            found_info['hit'].append(kw)
            continue
        found_info['miss'].append(kw)
    got_keywords = set(df["ccds_id"])
    for kw in keywords_CCDS:
        if kw in got_keywords:
            found_info['hit'].append(kw)
            continue
        found_info['miss'].append(kw)
    
    
    df['gene'] = df.apply(lambda row: '<a target="_blank" href="/crispr/{name}">{gene}<a>'.format(name=row.gsrna_ccds, gene=row.gene), axis = 1) 
    df = df.drop(columns=['gsrna_ccds'])

    rename_rule = {}
    for field_name in INCLUDE_LIST:
        rename_rule[field_name] = verbose(field_name)
    df = df.rename(rename_rule, axis=1)
    table = df.to_html(table_id="result_table", escape=False)
    table = table.replace("""<table border="1" class="dataframe" id="result_table">""","""<table id="result_table" class="table table-striped table-bordered" style="width:100%">""").replace("></th>", ">&nbsp;</th>")
    return render(request, "pages/dynamic/crispr_lib.html", {"have_search" : True, "search_keywords" : keywords_raw, "table" : table, "found_info" : found_info})

@login_required(login_url="/login/")
def crispr_lib_page(request):
    if request.method == "POST":
        return get_crispr(request)
    else:
        return render(request, "pages/dynamic/crispr_lib.html", {"have_search" : False, "search_keywords" : ''})

@login_required(login_url="/login/")
def check_gsrna(request, fullname):
    assert(request.method == "GET")
    element = Crispr.objects.get(gsrna_ccds=fullname)
    crispr_info=[]
    for field_name in FIELD_LIST:
        crispr_info.append({'n':verbose(field_name), 'v':getattr(element, field_name)})
    return render(request, "pages/dynamic/crispr_element.html", {"info" : crispr_info})

def verbose(field_name):
    return Crispr._meta.get_field(field_name).verbose_name