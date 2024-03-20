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
    page = crawl(sys.argv[1])
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
    linked to by the current page. With probability `1 - damping_factor`,
    choose a link at random chosen from all pages in the corpus.
    """

    N = len(corpus)  # Total number of pages in the corpus
    probability_distribution = {}  # Initialize the probability distribution dictionary

    # Iterate over each page in the corpus
    for page_corpus in corpus:
        # If the current page links to the iterated page, calculate probability accordingly
        if page_corpus in corpus[page]:
            probability_distribution[page_corpus] = (
                damping_factor / len(corpus[page])) + ((1 - damping_factor) / N)
        # If the current page does not link to the iterated page, assign equal probability to all pages
        else:
            probability_distribution[page_corpus] = (1 - damping_factor) / N

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to the transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize a dictionary to store estimated PageRank values
    estimated_pageranks = {}

    # Start at a random page
    current_page = random.choice(list(corpus.keys()))

    # Initialize counter for the current page
    estimated_pageranks[current_page] = 1

    # Perform sampling 'n' times
    for _ in range(n - 1):
        # Generate the transition model for the current page
        trans_model = transition_model(corpus, current_page, damping_factor)

        # Select a new page based on the transition model
        current_page = random.choices(
            list(trans_model.keys()),
            weights=list(trans_model.values()))[0]

        # Update the counter for the new page
        if current_page not in estimated_pageranks:
            estimated_pageranks[current_page] = 1
        else:
            estimated_pageranks[current_page] += 1

    # Normalize the counters to get estimated PageRank values
    for page in estimated_pageranks:
        estimated_pageranks[page] /= n

    return estimated_pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    def are_dicts_approx_equal(dict1, dict2, tolerance=0.001):
        """
        returns True if the values of both dictionaries are in the tolerance radius
        """
        if len(dict1) != len(dict2):  # If the dictionaries have different lengths, they can't be equal
            return False

        for key in dict1:  # Iterate through keys in the first dictionary
            if key not in dict2:  # If a key is missing in the second dictionary, they are not equal
                return False
            value1 = dict1[key]  # Get value from the first dictionary
            value2 = dict2[key]  # Get value from the second dictionary
            # Check if the difference between values exceeds tolerance
            if abs(value1 - value2) > tolerance:
                return False
        return True

    # Initialize variables
    # Create a deep copy of the corpus to avoid modifying the original
    corpus_copy = corpus.copy()
    num_pages = len(corpus_copy)  # Number of pages in the corpus
    # Initialize PageRank values for each page
    pagerank_values = {page: 1 / num_pages for page in corpus_copy.keys()}
    # Create a copy of the initial PageRank values
    old_pagerank_values = pagerank_values.copy()
    continue_loop = True  # Variable to control the iteration loop

    # Ensure that dangling nodes (pages with no outgoing links) point to all pages
    for page in corpus_copy:
        if not corpus_copy[page]:
            corpus_copy[page] = list(corpus_copy.keys())

    # Iteratively update PageRank values until convergence
    while continue_loop:
        for page in corpus_copy:
            linking_pages = []  # List to store pages linking to the current page

            # Initialize the new PageRank value for the current page
            new_pagerank = (1 - damping_factor) / num_pages

            # Find pages linking to the current page
            for linking_page in corpus_copy:
                if page in corpus_copy[linking_page]:
                    linking_pages.append(linking_page)

            # Update PageRank value using the PageRank values of linking pages
            for linking_page in linking_pages:
                if len(corpus_copy[linking_page]) != 0:
                    new_pagerank += damping_factor * \
                        pagerank_values[linking_page] / \
                        len(corpus_copy[linking_page])

            # Store the old PageRank value before updating
            old_pagerank_values[page] = pagerank_values[page]
            # Update the PageRank value for the current page
            pagerank_values[page] = new_pagerank

        # Check for convergence by comparing old and new PageRank values
        if are_dicts_approx_equal(old_pagerank_values, pagerank_values, 0.001):
            continue_loop = False  # If converged, exit the loop

    return pagerank_values


if __name__ == "__main__":
    main()
