from django.db import models

# Create your models here.


class Game(models.Model):
    gameID = models.CharField(max_length=30, default='')
    objects = models.Manager


class Board(models.Model):
    appID = models.CharField(max_length=30, default='')
    data = models.CharField(max_length=500, default='{}')
    ships = models.CharField(max_length=500, default='{}')
    shipsLeft = models.IntegerField(default=6)
    turn = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=1)
    objects = models.Manager


class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    sessionId = models.CharField(max_length=30)
    appID = models.CharField(max_length=30, default='')
    gamesPlayed = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    objects = models.Manager


class Queue(models.Model):
    appID = models.CharField(max_length=30, default='')
    gameID = models.CharField(max_length=30, default='')
    opponent = models.CharField(max_length=30, default='')
    objects = models.Manager
