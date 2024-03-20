# What is PageRank?

  Search engines like Google use complex algorithms to determine the order of search results, with the goal of presenting users with the most relevant and high-quality pages. At the heart of this process lies an algorithm called PageRank, which plays a crucial role in assessing the importance and relevance of web pages.

# PageRank Algorithm Implementation

This Python script implements the PageRank algorithm for ranking web pages based on their importance. The script provides two methods for calculating PageRank: sampling and iteration.

## Getting Started

### Prerequisites

- Python 3.x
- The script uses standard libraries like `os`, `random`, `re`, and `sys`, so there's no need for additional installations.

### Usage

1. Clone this repository to your local machine.

```bash
git clone <https://github.com/shauryainks/PageRank>
```

2. Navigate to the directory containing the script.

```bash
cd <PageRank>
```

3. Prepare your corpus by placing HTML files in directories named `corpus0`, `corpus1`, and `corpus2`. These HTML files represent the web pages that you want to analyze.

4. Run the script with the following command:

```bash
python pagerank.py <corpus-directory>
```

Replace `<corpus-directory>` with the path to the directory containing your corpus.

## Functionality

### 1. Sampling PageRank

The script estimates PageRank values by sampling a fixed number of pages according to a transition model. This method is suitable for large corpora and provides a faster approximation of PageRank.

### 2. Iterative PageRank

The script calculates PageRank values iteratively by updating PageRank values until they converge. This method provides more accurate PageRank values but may be slower for larger corpora.

## File Structure

- `pagerank.py`: The main Python script containing the PageRank implementation.
- `corpus0`, `corpus1`, `corpus2`: Directories containing HTML files representing the web pages in different corpora.

## Parameters

- `DAMPING`: The damping factor used in the PageRank calculation. Default value is `0.85`.
- `SAMPLES`: The number of samples used in the sampling method. Default value is `10000`.

## Output

The script outputs the PageRank results obtained from both the sampling and iterative methods.

