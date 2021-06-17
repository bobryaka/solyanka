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

        user1 = services.defender(request.POST.get('firstman'), keys[0], services.Contact.api)
        user2 = services.defender(request.POST.get('secondman'), keys[0], services.Contact.api)
        err_rep = dict()
        err_rep['photo'] = "https://sun1.beeline-kz.userapi.com/s/v1/if1/Z8oRq-BszSyVfkSzkoGp78_rz704GcLTnu3FutEM7Rc-" \
                           "7kamFR-Gy-0F_wC_a2t4nwkQ1Z_9.jpg?size=200x0&quality=96&crop=312,112,712,712&ava=1"
        err_rep['id'] = "https://vk.com/id223627530"
        for user_index, user in enumerate((user1, user2)):
            if user == 'closed':
                err_rep['name'] = 'Страница %s пользователя закрыта, можете попробовать с другим, а ' \
                                  'можете перейти на мою страничку нажав на фотографию и лайкнуть аву ' \
                                  % ('первого' if user_index == 0 else 'второго')
                err_rep['smile'] = 'https://www.meme-arsenal.com/memes/5036975aac221f9edae77eec70138723.jpg'
                return render(request, 'main/handshake.html', {'context': [err_rep, ]})

            elif user == 'deactivated':
                err_rep['name'] = 'Страница %s пользователя удалена (либо не существует), можете попробовать с другим' \
                                  ', а можнете перейти на мою страничку нажав на фотографию и лайкнуть' \
                                  ' аву' % ('первого' if user_index == 0 else 'второго')
                err_rep['smile'] = 'https://www.meme-arsenal.com/memes/5036975aac221f9edae77eec70138723.jpg'
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



