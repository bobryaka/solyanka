from django.shortcuts import render, redirect

def main_page(request):
    return render(request, 'main/main.html')

def handshake(request):
    if request.method == 'POST':
        context = list()
        context.append(request.POST.get('firstman'))
        context.append(request.POST.get('secondman'))

        return render(request, 'main/handshake.html', {'context': context})
    return render(request, 'main/handshake.html')



