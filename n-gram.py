import math
import random
from collections import defaultdict, Counter
from nltk.util import ngrams
from tqdm import tqdm

def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().split() for line in f]

def generate_ngrams(corpus, n):
    ngram_counts = defaultdict(int)
    context_counts = defaultdict(int)
    
    for method in tqdm(corpus, desc=f"Generating {n}-grams"):
        method_ngrams = list(ngrams(method, n))
        for gram in method_ngrams:
            ngram_counts[gram] += 1
            context_counts[gram[:-1]] += 1
    
    return ngram_counts, context_counts

def kneser_ney_smoothing(ngram_counts, context_counts, vocab_size, d=0.75):
    probabilities = {}
    continuation_counts = defaultdict(set)
    
    for ngram in ngram_counts:
        continuation_counts[ngram[:-1]].add(ngram[-1])
    
    for ngram, count in ngram_counts.items():
        context = ngram[:-1]
        context_count = context_counts[context]
        continuation_count = len(continuation_counts[context])
        
        prob = max(count - d, 0) / context_count
        prob += (d * continuation_count / context_count) * (1 / vocab_size)
        
        probabilities[ngram] = prob
    
    return probabilities

def backoff_model(ngram_counts, context_counts, vocab, max_n=5):
    models = {}
    for n in range(1, max_n + 1):
        models[n] = kneser_ney_smoothing(ngram_counts[n], context_counts[n], len(vocab))
    
    def get_probability(ngram):
        for n in range(len(ngram), 0, -1):
            if ngram[-n:] in models[n]:
                return models[n][ngram[-n:]]
        return 1 / len(vocab)                     # uniform distribution for unseen ngrams
    
    return get_probability

def calculate_perplexity(corpus, get_probability, n):
    total_log_prob = 0
    total_tokens = 0
    for method in tqdm(corpus, desc="callculating perplexity"):
        method_ngrams = list(ngrams(method, n))
        for gram in method_ngrams:
            prob = get_probability(gram)
            total_log_prob += math.log(prob)
            total_tokens += 1
    perplexity = math.exp(-total_log_prob / total_tokens)
    return perplexity

def predict_next_token(context, get_probability, vocab, n):
    possible_next_tokens = []
    for token in vocab:
        ngram = context + (token,)
        prob = get_probability(ngram)
        possible_next_tokens.append((token, prob))
    return sorted(possible_next_tokens, key=lambda x: x[1], reverse=True)[:5]

def main():
    # loading the preprocessed data
    train_corpus = load_corpus('data/java_methods_train.txt')
    val_corpus = load_corpus('data/java_methods_val.txt')
    test_corpus = load_corpus('data/java_methods_test.txt')

    vocab = set(token for method in train_corpus for token in method)
    vocab_size = len(vocab)

    # generating the n-grams for different orders
    max_n = 6
    ngram_counts = {}
    context_counts = {}
    for n in range(1, max_n + 1):
        ngram_counts[n], context_counts[n] = generate_ngrams(train_corpus, n)

    # backoff model
    get_probability = backoff_model(ngram_counts, context_counts, vocab, max_n)

    # evaluation on the validation set
    val_perplexity = calculate_perplexity(val_corpus, get_probability, max_n)
    print(f"Validation Perplexity: {val_perplexity}")

    # evaluation on test set
    test_perplexity = calculate_perplexity(test_corpus, get_probability, max_n)
    print(f"Test Perplexity: {test_perplexity}")

    # sample sequences for code completion
    print("\nSampling code completions:")
    for _ in range(10):
        method = random.choice(test_corpus)
        if len(method) >= max_n:
            start_index = random.randint(0, len(method) - max_n)
            context = tuple(method[start_index:start_index + max_n - 1])
            completions = predict_next_token(context, get_probability, vocab, max_n)
            print(f"Context: {' '.join(context)}")
            print(f"Predicted next tokens: {completions}\n")

if __name__ == "__main__":
    main()
