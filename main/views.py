from django.shortcuts import render, redirect
from . import services
from .tokens import keys
import requests


def index(request):
    return render(request, 'main/index.html')


def handshake(request):
    if request.method == 'POST':
        if not request.POST.get('firstman') or not request.POST.get('secondman'):
            return render(request, 'main/handshake.html')

        data = list()
        data.append(request.POST.get('firstman'))
        data.append(request.POST.get('secondman'))

        user1 = services.defender(data[0], keys[0], services.Contact.api)
        err_rep = dict()
        err_rep['photo'] = "https://vk.com/images/camera_200.png"
        err_rep['id'] = "https://vk.com/id223627530"
        if user1[0] != 'ok':
            err_rep['name'] = 'Хозяин первой страницы удалил её или што такое с ней еще приключилось'
            return render(request, 'main/handshake.html', {'context': [err_rep, ]})

        user2 = services.defender(data[1], keys[0], services.Contact.api)
        if user2[0] != 'ok':
            err_rep['name'] = 'Хозяин второй страницы удалил её или што такое с ней еще приключилось'
            return render(request, 'main/handshake.html', {'context': [err_rep, ]})

        all_ids = services.Contact(user1[1]['id'], user2[1]['id'], keys).handshake()
        if all_ids == 'not found':
            err_rep['name'] = 'Вы друг от друга слишком далеки'
            return render(request, 'main/handshake.html', {'context': [err_rep, ]})

        context = list()
        context.append({'name': user1[1]['last_name'] + ' ' + user1[1]['first_name'],
                        'photo': user1[1]['photo_200'],
                        'id': "https://vk.com/id" + str(user1[1]['id'])
                        })

        for id in all_ids[1:-1]:
            temp_dict = dict()
            user = \
            requests.get("https://api.vk.com/method/users.get?user_ids=%s&fields=photo_200&access_token=%s&v=%s" % (
                id, keys[0], services.Contact.api)).json()['response'][0]
            temp_dict['name'] = user['last_name'] + ' ' + user['first_name']
            temp_dict['photo'] = user['photo_200']
            temp_dict['id'] = "https://vk.com/id" + str(user['id'])
            context.append(temp_dict)

        context.append({'name': user2[1]['last_name'] + ' ' + user2[1]['first_name'],
                        'photo': user2[1]['photo_200'],
                        'id': "https://vk.com/id" + str(user2[1]['id'])
                        } )

        return render(request, 'main/handshake.html', {'context': context})
    return render(request, 'main/handshake.html')



