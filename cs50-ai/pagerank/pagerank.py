import os
import random
import re
import sys

DMP = 0.85
SMP = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corp")
    corp = crawl(sys.argv[1])
    ranks = sample_pagerank(corp, DMP, SMP)
    print(f"PageRank Results from Sampling (n = {SMP})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corp, DMP)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    pages = dict()
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    return pages

def transition_model(corp, page, DMP_factor):
    prob_dist = {page_name : 0 for page_name in corp}
    if len(corp[page]) == 0:
        for page_name in prob_dist:
            prob_dist[page_name] = 1 / len(corp)
        return prob_dist
    random_prob = (1 - DMP_factor) / len(corp)
    link_prob = DMP_factor / len(corp[page])
    for page_name in prob_dist:
        prob_dist[page_name] += random_prob
        if page_name in corp[page]:
            prob_dist[page_name] += link_prob
    return prob_dist

def sample_pagerank(corp, DMP_factor, n):
    visits = {page_name: 0 for page_name in corp}
    curr_page = random.choice(list(visits))
    visits[curr_page] += 1
    for i in range(0, n-1):
        trans_model = transition_model(corp, curr_page, DMP_factor)
        rand_val = random.random()
        total_prob = 0
        for page_name, probability in trans_model.items():
            total_prob += probability
            if rand_val <= total_prob:
                curr_page = page_name
                break
        visits[curr_page] += 1
    prs = {page_name: (visit_num/n) for page_name, visit_num in visits.items()}
    print('Sum of sample page ranks: ', round(sum(prs.values()), 4))
    return prs

def iterate_pagerank(corp, DMP_factor):
    num_pages = len(corp)
    init_rank = 1 / num_pages
    random_choice_prob = (1 - DMP_factor) / len(corp)
    iterations = 0
    prs = {page_name: init_rank for page_name in corp}
    nrs = {page_name: None for page_name in corp}
    mrc = init_rank
    while mrc > 0.001:
        iterations += 1
        mrc = 0
        for page_name in corp:
            surf_choice_prob = 0
            for other_page in corp:
                if len(corp[other_page]) == 0:
                    surf_choice_prob += prs[other_page] * init_rank
                elif page_name in corp[other_page]:
                    surf_choice_prob += prs[other_page] / len(corp[other_page])
            nr = random_choice_prob + (DMP_factor * surf_choice_prob)
            nrs[page_name] = nr
        normf = sum(nrs.values())
        nrs = {page: (rank / normf) for page, rank in nrs.items()}
        for page_name in corp:
            rc = abs(prs[page_name] - nrs[page_name])
            if rc > mrc:
                mrc = rc
        prs = nrs.copy()
    print('Iteration took', iterations, 'iterations to converge')
    print('Sum of iteration page ranks: ', round(sum(prs.values()), 4))
    return prs

if __name__ == "__main__":
    main()
