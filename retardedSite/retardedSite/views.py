from django.shortcuts import render
from django.template import RequestContext, loader

from markov import Markov


def index(request):
    template = loader.get_template('index.html')
    markov = Markov(open("nyt_corpus_sports"), 3)
    context = RequestContext(request, {
        'text': markov.generate_markov_text(500),
    })
    return render(request, 'index.html', context)