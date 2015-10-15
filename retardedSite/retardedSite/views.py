from django.shortcuts import render
from django.template import RequestContext, loader

from .markov import Markov

def index(request):
    template = loader.get_template('index.html')
    markov = Markov("nyt_corpus_business_tagged", 4)
    markov_head = Markov("nyt_corpus_business_tagged", 4)
    context = RequestContext(request, {
        'text': markov.generate_markov_text(markov.lidstone_smoothing, 500),
        'head': markov_head.generate_markov_text(markov.lidstone_smoothing, 10, True).title(),
    })
    return render(request, 'index.html', context)