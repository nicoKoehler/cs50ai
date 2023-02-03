from pagerank import *

corpus_test = {
    "1.html":{"2.html", "3.html"},
    "2.html": {},
    "3.html": {"2.html","4.html", "1.html"},
    "4.html": {"1.html"}

}

corpus_test2 = {
    "1.html":{"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"}

}

tm = transition_model(corpus_test2, "1.html",0.85)
spr = sample_pagerank(corpus_test, 0.85, 10000)
print(spr)
print(iterate_pagerank(corpus_test, 0.85))