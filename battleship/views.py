from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os, zipfile, uuid, traceback
from io import BytesIO
import json
from .models import User, Board, Queue, Game
from django.core.exceptions import ObjectDoesNotExist
import re
# Create your views here.

MESSAGE = "\nMultiplayer is still in development.  Please report any crashes or bugs.\n"


def logged_in(request):
    if 'session_id' in request.COOKIES.keys() and User.objects.filter(sessionId=request.COOKIES['session_id']).exists():
        return True
    else:
        return False


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return HttpResponse(render(request, 'login.html', {'valid': True}))

    elif request.method == 'POST':

        try:
            username = request.POST['username']
            password = request.POST['password']
            try:
                if User.objects.get(username=username) and User.objects.get(username=username).password == password:
                    print("Logged In User: " + username)
                    session = uuid.uuid4().hex
                    user = User.objects.get(username=username)
                    user.sessionId = session
                    user.save()
                    response = HttpResponseRedirect("/battleship/")
                    response.set_cookie(key="session_id", value=session, max_age=86400, httponly=True)
                    return response

                else:
                    return HttpResponse(render(request, 'login.html', {'valid': False}))

            except ObjectDoesNotExist:
                return HttpResponse(render(request, 'login.html', {'valid': False}))
        except KeyError:
            return HttpResponse('bad post')


def logout(request):
    response = HttpResponseRedirect('/battleship/')
    response.delete_cookie('session_id')
    return response


@csrf_exempt
def createAccount(request):

    if request.method == 'GET':
        return HttpResponse(render(request, 'createAccount.html', {'valid': True}))

    elif request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']

            if User.objects.filter(username=username).exists() or not re.match('[a-zA-Z0-9]+', username) or not len(password) > 4:
                return HttpResponse(render(request, 'createAccount.html', {'valid': False}))

            else:
                session = uuid.uuid4().hex
                newUser = User(username=username, password=password, sessionId=session)
                newUser.save()
                response = HttpResponseRedirect("/battleship/")
                response.set_cookie(key="session_id", value=session, max_age=86400, httponly=True)
                return response

        except KeyError:
            return HttpResponse('bad post')


def app_logged_in(request):
    if request.method == 'GET':
        if User.objects.filter(appID=request.GET['appID']).exists():
            return True
        else:
            return False

    elif request.method == 'POST':
        for key in request.POST.keys():
            print("\n" + key + "\n")
        appID = request.POST["appID"]
        print("\n\n" + appID + "\n\n")
        if User.objects.filter(appID=appID).exists():
            return True
        else:
            return False


def home(request):
    if logged_in(request):
        return HttpResponse(render(request, 'hello.html', {'loggedIn': logged_in(request), 'user': User.objects.get(sessionId=request.COOKIES['session_id']).username}))
    else:
        return HttpResponse(render(request, 'hello.html'))


def profile(request):
    if logged_in(request):
        user = User.objects.get(sessionId=request.COOKIES['session_id'])
        return HttpResponse(render(request, 'profile.html', {'user': user.username, 'wins': user.wins, 'losses': user.gamesPlayed - user.wins}))
    else:
        return HttpResponseRedirect('/battleship/')


def leaderboard(request):
    players = {}  # {username: user, wins: wins,  'total': gamesPlayed}
    leaders = []
    done = []
    wins = []
    users = User.objects.all()
    for user in users:

        if user.username != 'admin' and user.username != 'test':

            new = {user.username: [user.wins, user.gamesPlayed]}
            if new[user.username][1] == 0:
                new[user.username].append(0)
            else:
                new[user.username].append(user.wins / user.gamesPlayed)

            players.update(new)
            wins.append(new[user.username][2])

    i = 0

    test = sorted(wins)

    test.reverse()

    for value in test:
        for player in players:
            if players[player][2] == value and player not in done and i < 10:
                leaders.append({'user': player, 'rank': i + 1, 'wins': players[player][0], 'losses': players[player][1] - players[player][0]})
                done.append(player)

                i += 1

            elif i == 10:
                return HttpResponse(render(request, 'leaderboard.html', {'leaderboard': leaders}))

    while i < 10:
        leaders.append({'user': "---", 'rank': i + 1, 'wins': '--', 'losses': '--'})
        i += 1

    return HttpResponse(render(request, 'leaderboard.html', {'leaderboard': leaders}))



def admin(request):
    return HttpResponse(render(request, 'admin.html'))


def download(request):
    if request.GET['os'] == 'mac':
        zip_dir = settings.BASE_DIR + "/battleship/Battleship_mac"
        filenames = [zip_dir + "/Battleship", zip_dir + "/Battleship.jar", zip_dir + '/preferences.txt']

    elif request.GET['os'] == 'win':
        zip_dir = settings.BASE_DIR + "/battleship/Battleship_win"
        filenames = [zip_dir + "/Battleship.bat", zip_dir + "/Battleship.jar", zip_dir + '/preferences.txt']

    zip_subdir = "Battleship"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp


def message(request):
    return HttpResponse(MESSAGE)


@csrf_exempt
def appLogin(request):

    if request.method == 'GET':
        return HttpResponse('login')

    elif request.method == 'POST':
        for key in request.POST.keys():
            print(key)
        try:
            username = request.POST['username']
            password = request.POST['password']

            if request.META['HTTP_X_REQUESTED_WITH'] == 'java_app' and User.objects.filter(username=username).exists() and User.objects.get(username=username).password == password:
                print("\nLogged In App for User: " + username + '\n')
                user = User.objects.get(username=username)
                if user.appID == '':
                    appID = uuid.uuid4().hex
                    user.appID = appID
                    user.save()
                return JsonResponse({'status': 'success', 'appID': user.appID})

            else:
                return JsonResponse({'status': 'incorrect credentials'})

        except KeyError:

            return JsonResponse({'status': 'bad post'})


@csrf_exempt
def game(request):
    try:
        if request.META['HTTP_X_REQUESTED_WITH'] == 'java_app':
            if app_logged_in(request):
                if request.method == 'GET':
                    appID = request.GET['appID']
                    if 'gameID' in request.GET.keys():
                        try:
                            gameID = request.GET['gameID']
                            try:
                                currentGame = Game.objects.get(gameID=gameID)
                            except ObjectDoesNotExist:
                                return JsonResponse({'end': True})

                            if request.GET['method'] == 'getOpponentData':
                                opponentBoard = Board.objects.filter(game=currentGame).exclude(appID=appID)[0]
                                data = json.loads(opponentBoard.data)
                                ships = json.loads(opponentBoard.ships)
                                return JsonResponse(data)

                            elif request.GET['method'] == 'getPlayerData':


                                board = Board.objects.get(game=currentGame, appID=appID)
                                data = json.loads(board.data)
                                ships = json.loads(board.ships)
                                return JsonResponse(data)





                        except KeyError:
                            return JsonResponse({'status': 'failed', 'message': 'bad request'})


                    else:

                        if 'leaveQueue' in request.GET.keys():
                            if Queue.objects.filter(appID=appID).exists():
                                q = Queue.objects.get(appID=appID)
                                q.delete()
                                return JsonResponse({'status': 'success', 'message': 'removed from queue'})
                            else:
                                return JsonResponse({'status': 'failed', 'message': 'not in queue'})

                        if Queue.objects.filter(appID=appID).exists():  # if user is already in queue
                            player = Queue.objects.get(appID=appID)

                            if player.opponent != '':
                                ID = player.gameID
                                opponent = player.opponent
                                turn = Board.objects.get(appID=appID, game=Game.objects.get(gameID=ID)).turn
                                player.delete()
                                return JsonResponse({'status': 'success', 'gameID': ID, 'opponent': User.objects.get(appID=opponent).username, 'turn': turn})
                            else:

                                if len(Queue.objects.all()) > 1:
                                        try:
                                            opponent = Queue.objects.filter(opponent='').exclude(appID=appID)[0]

                                            gameID = uuid.uuid4().hex
                                            g = Game(gameID=gameID)
                                            g.save()
                                            b1 = Board(appID=appID, game=g, turn=0)
                                            b2 = Board(appID=opponent.appID, game=g, turn=1)
                                            b1.save()
                                            b2.save()

                                            player.opponent = opponent.appID
                                            player.gameID = gameID

                                            opponent.opponent = player.appID
                                            opponent.gameID = gameID

                                            player.save()
                                            opponent.save()

                                        except IndexError:
                                            print("index")

                                        return JsonResponse({'status': 'success', 'message': 'waiting for match'})

                                else:
                                    return JsonResponse({'status': 'success', 'message': 'waiting for match'})

                        else:
                            q = Queue(appID=appID)
                            q.save()
                            return JsonResponse({'status': 'success', 'message': 'placed in queue'})

                elif request.method == 'POST':

                    appID = request.POST['appID']
                    try:
                        gameID = request.POST['gameID']
                        currentGame = Game.objects.get(gameID=gameID)
                        if request.POST['method'] == 'sendPlayerData':
                            board = Board.objects.get(game=currentGame, appID=appID)
                            data = request.POST['data']
                            board.data = data
                            board.save()
                            return JsonResponse({'status': 'success'})

                        elif request.POST['method'] == 'sendOpponentData':
                            board = Board.objects.filter(game=currentGame).exclude(appID=appID)[0]
                            if 'sunk' in request.POST.keys():
                                board.shipsLeft = board.shipsLeft - request.POST['sunk']
                            data = request.POST['data']
                            board.data = data
                            board.save()
                            return JsonResponse({'status': 'success'})

                        elif request.POST['method'] == 'endGame':
                            user = User.objects.get(appID=appID)
                            opponent = User.objects.get(appID=Board.objects.filter(game=currentGame).exclude(appID=appID)[0].appID)
                            if request.POST['won'] == 'true':
                                user.wins += 1

                            else:
                                opponent.wins += 1

                            user.gamesPlayed += 1
                            opponent.gamesPlayed += 1

                            user.save()
                            opponent.save()

                            currentGame.delete()
                            return JsonResponse({'status': 'success'})

                    except KeyError:
                        return JsonResponse({'status': 'failed', 'message': 'bad request'})


            else:
                return JsonResponse({'status': 'failed', 'message': 'not logged in'})
        else:
            return HttpResponse('this is an app-only endpoint')
    except KeyError:
        print(traceback.format_exc())
        return JsonResponse({'status': 'failed', 'message': 'bad request'})


def clearQueue(request):
    Queue.objects.all().delete()
    Game.objects.all().delete()
    return HttpResponse('queue cleared')

def clearStats(request):
    if logged_in(request) and User.objects.get(sessionId=request.COOKIES['session_id']).username == 'admin':
        if User.objects.filter(username=request.GET['user']).exists():
            user = User.objects.get(username=request.GET['user'])
            user.wins = 0
            user.gamesPlayed = 0
            user.save()

    return HttpResponseRedirect('/battleship/')
