from django.db import models
from django.contrib.auth.models import AbstractUser as DefUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


class User(DefUser):
    is_active = models.BooleanField(
        _('active'),
        default=True,

    )

    email = models.EmailField(
        _("email address"),
        unique=True,

    )



    rank = models.PositiveSmallIntegerField('Rütbe', default=1)

    score = models.PositiveSmallIntegerField('Puan', default=0)




    def give_score(self, score):
        self.score += score

        if self.score < 25:
            self.rank = 1
        elif self.score < 50:
            self.rank = 2
        elif self.score < 75:
            self.rank = 3
        elif self.score < 100:
            self.rank = 4
        elif self.score < 125:
            self.rank = 5
        elif self.score < 150:
            self.rank = 6
        elif self.score > 150:
            self.rank = 7

        
        self.save()

    
    def get_rank(self):
        if self.rank == 1:
            return "Üyecik"
        elif self.rank == 2:
            return "Üye"
        elif self.rank == 3:
            return "Değerli Üye"
        elif self.rank == 4:
            return "Altın Üye"
        elif self.rank == 5:
            return "Anketör"
        elif self.rank == 6:
            return "Anket Kralı"
        elif self.rank == 7:
            return "EFSANE"
    
    def get_rank_formatted(self):
        if self.rank == 1:
            return "Üyecik"
        elif self.rank == 2:
            return "Üye"
        elif self.rank == 3:
            return """<div class="text-green">Değerli Üye</div>"""
        elif self.rank == 4:
            return """<div class="text-yellow"><strong>Altın Üye</strong></div>"""
        elif self.rank == 5:
            return """<div class="text-blue"><strong>Anketör</strong></div>"""
        elif self.rank == 6:
            return """<div class="text-purple"><strong>ANKET KRALI</strong></div>"""
        elif self.rank == 7:
            return """<div class="text-red"><strong>EFSANE</strong></div>"""
