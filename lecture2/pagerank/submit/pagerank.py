import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    out_prob = {}
    if not corpus[page]: return {k: 1/len(corpus) for k in corpus.keys()}

    for k,p in corpus.items():
        if k not in out_prob: out_prob[k] = 0.0
        out_prob[k] += (1-damping_factor)/len(corpus)
        
        if page == k:
            for l in p:
                if l not in out_prob: out_prob[l] = 0.0
                out_prob[l] += damping_factor / len(p)


    return dict(sorted(out_prob.items(), key=lambda x: x[1]))


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_key = random.choice(list(corpus.keys()))

    SPR = {k:0 for k in corpus.keys()}
    SPR[page_key] += 1


    #exclude first random sample
    for s in range(n-1):
        choice_options = []
        rand = random.random()
        transModel = transition_model(corpus, page_key, damping_factor)
  
        choice_weights = []
        [(choice_options.append(k), choice_weights.append(v)) for k,v in transModel.items()]
        
        page_key = random.choices(choice_options, choice_weights)[0]
        SPR[page_key] += 1


    for k in SPR.keys():

        SPR[k] = SPR[k] /n

    return SPR



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """


    IPR = {k: 1/len(corpus) for k in corpus.keys()}
    change_detected = 1

 
    while change_detected > 0: 
        change_detected = 0

        for current_page, current_value in IPR.items():
            old_value = current_value
            new_value_prefix = (1-damping_factor)/len(corpus)
            new_value_suffix = 0

            for page,links in corpus.items():
                if current_page in links:
                    new_value_suffix += IPR[page]/len(links)
                
                elif not links: new_value_suffix += IPR[page] / len(corpus)
            
            new_value = new_value_prefix + damping_factor * new_value_suffix

            IPR[current_page] = new_value

            if abs(old_value - new_value) > 0.001: change_detected += 1



    return IPR




if __name__ == "__main__":
    main()
