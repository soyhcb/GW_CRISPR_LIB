from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Report(models.Model):
    class ReportCategory(models.IntegerChoices):
        GENERAL = 0, _("General")
        GW_CRISPR_LIB = 1, _('Genome-wide Crispr Library')
    name = models.CharField(max_length=50, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    problem = models.CharField(max_length=500, verbose_name="Problem Title")
    detail = models.TextField(verbose_name="Problem Details")
    time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created Time")
    category = models.IntegerField(
        choices=ReportCategory.choices,
        default=ReportCategory.GW_CRISPR_LIB,
        verbose_name="Category"
        )
    solved = models.BooleanField(default=False, verbose_name="Solved")
    marked = models.BooleanField(default=False, verbose_name="Marked")

    def __str__(self):
        return "Problem:{prob} at {time} about {cat}".format(
            prob=self.problem, time=self.time, cat=self.category
            )
