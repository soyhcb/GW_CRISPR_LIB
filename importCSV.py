import os
import pandas as pd
from crispr_lib.models import Crispr

tb = pd.read_csv("./files/LibraryA_Simple.csv")

numofrows = len(tb.index)
ct = 0
for index, row in tb.iterrows():
    newcp = Crispr(
        gene = row['Gene'],
        ccds_id =  row['CCDS ID'],
        gsrna_ccds =  row['gsRNA(not shown)'],
        gsrna_seq =  row['gsRNA'],
        genome_position =  row['Genome Position'],
        offtarget_score = row['Off-target Score'],
        ontarget_score = row['On-target Score'],
        surface_protein = True if row['SurfaceProtein'] == "YES" else False,
        grna_number = row['gRNA_Number'],
        gene_id = row['Gene_id'],
        extended_sequence = row['extendedSequence'],
        grna_efficacy = row['gRNAefficacy'],
        grna_s_plus_pam = row['gRNAsPlusPAM'],
        top5_offtarget_total_score = row['top5OfftargetTotalScore'],
        top1Hit_onTarget_MMdistance2PAM = row['top1Hit.onTarget.MMdistance2PAM'],
        topOfftarget1MMdistance2PAM = row['topOfftarget1MMdistance2PAM'],
        topOfftarget2MMdistance2PAM = row['topOfftarget2MMdistance2PAM'],
        topOfftarget3MMdistance2PAM = row['topOfftarget3MMdistance2PAM'],
        topOfftarget4MMdistance2PAM = row['topOfftarget4MMdistance2PAM'],
        topOfftarget5MMdistance2PAM = row['topOfftarget5MMdistance2PAM'],
        topOfftarget6MMdistance2PAM = row['topOfftarget6MMdistance2PAM'],
        topOfftarget7MMdistance2PAM = row['topOfftarget7MMdistance2PAM'],
        topOfftarget8MMdistance2PAM = row['topOfftarget8MMdistance2PAM'],
        topOfftarget9MMdistance2PAM = row['topOfftarget9MMdistance2PAM'],
        topOfftarget10MMdistance2PAM = row['topOfftarget10MMdistance2PAM'] 
    )
    newcp.save()
    ct += 1
    print("\rNo.{}/{} added".format(ct,numofrows),end='')

print()
print("Done")
