import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    """
    expects a command line argument which will be the name of the directory
    to search through to compute PageRanks
    """
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
    # initalising the dict
    dict_probability = corpus.copy()
    for key in dict_probability:
        dict_probability[key] = 0

    if len(corpus[page]) != 0:
        # adding to all of them the residual value
        for key in dict_probability:
            dict_probability[key] += (1 - damping_factor) / len(corpus)
        # adding the additional value to exlcuding the pages
        for key in dict_probability:
            if key in list(corpus[page]):
                dict_probability[key] += damping_factor / len(corpus[page])
        return dict_probability
    if len(corpus[page]) == 0:
        # calculate the necessary values
        for key in dict_probability:
            dict_probability[key] += 1 / len(corpus)
        return dict_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    corpus is the dict
    damping factor is the value
    n is the number of samples that should be generated
    """
    rank = dict()

    # initialize rank of each page in the corpus to 0.0
    for key in corpus:
        rank[key] = 0.0

    # start with a random sample page and set its probability to 1/n
    # n = no. of samples
    sample = random.choices(list(corpus))[0]
    rank[sample] += (1 / n)

    # based on the transition model generated by this page, go to the next page
    # increment the rank of the next page by 1 / n
    for i in range(1, n):

        model = transition_model(corpus, sample, damping_factor)
        next_pages = []
        probabilities = []
        for key, value in model.items():
            next_pages.append(key)
            probabilities.append(value)
        
        sample = random.choices(next_pages, weights=probabilities)[0]
        rank[sample] += (1 / n)

    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # set threshold of convergence to be +/- 0.001
    threshold = 0.001
    # copy the corpus and reassigns the values
    # assign each page a rank of 1 / N N is the total number of pages in the corpus
    page_rank = dict()
    
    N = len(corpus)
    for key in corpus:
        page_rank[key] = 1/N
    copy_page_rank = page_rank.copy()
    
    # function should repeatedly calculate new rank values based on the curren rank value
        # a page that has no links should link to all pages 
        # repeat till the change of pagerank is less than 0.001

    # the dictionary that we are appending to has been called page_rank
    while True:
        # first condition
        first_condition = (1 - damping_factor) / len(corpus)
        # looping through all the pages one time
        for key in corpus:
            # holding value for the loop to add below
            summation_value = 0.0
            # iterate through every value obtaining the
            for page in corpus[key]:
                summation_value += page_rank[page] / len(corpus[page])
            # second condition
            second_condition = damping_factor * summation_value

            # append the sum of the two conditions into the new page_rank
            copy_page_rank[key] = (first_condition + second_condition)

        # compare the two dicts if the diff between the two is less than 0.001 return the copy 
        # if more than 0.001 copy the values of the copy_page_rank to page_rank and wipe page_rank and try again
        threshold_counter = 0
        for key in page_rank and copy_page_rank:
            if abs(page_rank[key] - copy_page_rank[key]) > threshold:
                threshold_counter += 1

        if threshold_counter == 0:
            return copy_page_rank
        if threshold_counter > 0:
            page_rank = copy_page_rank


if __name__ == "__main__":
    main()
