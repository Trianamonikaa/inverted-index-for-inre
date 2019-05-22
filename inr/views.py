from django.shortcuts import render
from inr import main


# Create your views here.

def index(request):
    if request.method == 'POST':
        text = request.POST['input']
        dic,prepros = main.main(text)
        # print(prepros)
        if len(dic) == 0:
            isi = {}
            return render(request, 'notfound.html', isi)
        else:
            isi = {'dic':dic, 'prepros' : prepros}
            return render(request, 'hasil.html', isi)
    return render(request, 'index.html')



def hasil(lala):
    return render(lala,'hasil.html')

def notfound(ll):
    return render(ll, 'notfound.html')