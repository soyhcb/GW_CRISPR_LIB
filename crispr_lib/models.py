from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
import json
# Create your models here.

class Crispr(models.Model):
    gene = models.CharField(max_length=50, verbose_name="Gene")
    ccds_id = models.CharField(max_length=50, verbose_name="CCDS ID")
    gsrna_ccds = models.CharField(max_length=50, verbose_name="gsRNA(name)")
    gsrna_seq = models.CharField(max_length=50, verbose_name="gsRNA")
    genome_position = models.CharField(max_length=100, verbose_name="Genome Position")
    offtarget_score = models.FloatField(verbose_name="Off-target Score")
    ontarget_score = models.FloatField(verbose_name="On-target Score")
    surface_protein = models.BooleanField(verbose_name="Surface Protein")
    grna_number = models.IntegerField(verbose_name="gRNA Number")
    gene_id = models.IntegerField(verbose_name="Gene ID")
    extended_sequence = models.CharField(max_length=100, verbose_name="Extended Sequence")
    grna_efficacy = models.FloatField(verbose_name="gRNA Efficacy")
    grna_s_plus_pam = models.CharField(max_length=50, verbose_name="gRNAs+PAM")
    top5_offtarget_total_score = models.FloatField(verbose_name="Top 5 Off-target Total Score")
    top1Hit_onTarget_MMdistance2PAM = models.CharField(max_length=50, verbose_name="top1Hit.onTarget.MMdistance2PAM")
    # use ArrayField if use PostgreSQL as database, which is better. 
    topOfftarget1MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget2MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget3MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget4MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget5MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget6MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget7MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget8MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget9MMdistance2PAM = models.CharField(max_length=200)
    topOfftarget10MMdistance2PAM = models.CharField(max_length=200)

    gene_search = SearchVectorField(null=True)
    ccds_search = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=["gene_search", 'ccds_search'])]
    def __str__(self):
        return self.gsrna_ccds
