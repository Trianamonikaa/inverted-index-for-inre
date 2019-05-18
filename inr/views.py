from django.shortcuts import render
from inr import main


# Create your views here.

def index(request):
    if request.method == 'POST':
        text = request.POST['input']
        mydict, judul = main.main(text)
        isi ={'mydict':mydict, 'judul': judul}
        return render(request, 'hasil.html', isi)
    return render(request, 'index.html')

def hasil(lala):
    return render(lala,'hasil.html')