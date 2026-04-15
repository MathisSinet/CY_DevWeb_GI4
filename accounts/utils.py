from django.db import models
from django.contrib.auth.models import User

levels_requirements = {"beginner":0, "intermediate": 5, "advanced": 20, "expert": 35}
levels_order = ["beginner", "intermediate", "advanced", "expert"]

def addPoints(user, nb):
    user.points += nb
    user.save()

def upgradeLevel(user):

    #if levels_order.index(user.current_level) >= levels_order.index(id_level):
    #    return #on l'autorise pas d'upgrade à un niveau inférieur ou égale

    #if user.points < levels_requirements[id_level]:
    #    return #pas assez de points

    #if user.points >= levels_requirements[id_level]:
    #    user.current_level = id_level
    #    removePoints(user, levels_requirements[id_level])
    #    user.save()

    if user.points >= 0:
        user.current_level = 'beginner'
    if user.points >= 5:
        user.current_level = 'intermediate'
    if user.points >= 20:
        user.current_level = 'advanced'
    if user.points >= 35:
        user.current_level = 'expert'
