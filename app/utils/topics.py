import numpy as np
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app import models


def print_top_words(model, feature_names, n_top_words):
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topics.append(" ".join([feature_names[i]
                                for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return topics


def compute_nmf(data_samples):
    n_samples = 2000
    n_features = 1000
    n_topics = 3
    n_top_words = 20
    # Use tf-idf features for NMF.
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,  # max_features=n_features,
                                       stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(data_samples)
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                    stop_words='english')
    tf = tf_vectorizer.fit_transform(data_samples)

    nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)

    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    return print_top_words(nmf, tfidf_feature_names, n_top_words)


def compute_similarity(data_samples):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data_samples)
    score = cosine_similarity(X[0:1], X)[0]
    indexes = sorted(range(len(score)), key=lambda x: score[x]>0.7 and
                                                      score[x]<1)[-3:]
    employees = models.Employee.objects.filter(emp_id__in=indexes)
    #print employees.values()
    scores = [score[i] for i in indexes]
    return employees

def computex_similarity(data_samples):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data_samples)
    score = cosine_similarity(X[0:1], X)[0]
    indexes = sorted(range(len(score)), key=lambda x: score[x]>0.3 and
                                                      score[x]<.6)[-3:]
    employees = models.Employee.objects.filter(emp_id__in=indexes)
    #print employees.values()
    scores = [score[i] for i in indexes]
    return employees

def computey_similarity(data_samples):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data_samples)
    score = cosine_similarity(X[0:1], X)[0]
    indexes = sorted(range(len(score)), key=lambda x: score[x]>0.1 and
                                                      score[x]<0.3)[-3:]
    employees = models.Employee.objects.filter(emp_id__in=indexes)
    #print employees.values()
    scores = [score[i] for i in indexes]
    return employees