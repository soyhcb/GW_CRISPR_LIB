from django.contrib import admin
from crispr_lib.models import Crispr


# Register your models here.

class CrisprAdmin(admin.ModelAdmin):
    list_filter = ('surface_protein', 'gene')
    list_display = ('gene',"gene_id" , 'gsrna_ccds', "offtarget_score", "ontarget_score")
    fieldsets = [
        ('Gene Info', {'fields': ['gene', 'ccds_id', 'gsrna_ccds', 'gsrna_seq', 'genome_position',
        'offtarget_score', 'ontarget_score', 'surface_protein', 'grna_number', 'gene_id', 'extended_sequence', 
        'grna_efficacy', 'grna_s_plus_pam', 'top5_offtarget_total_score', 'top1Hit_onTarget_MMdistance2PAM']}),
        ('Other Info', {'fields': ['topOfftarget{}MMdistance2PAM'.format(i+1) for i in range(10)]}),
    ]

admin.site.register(Crispr, CrisprAdmin)
