import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import LSHForest

from rake.core.dbhelper import *

if __name__ == '__main__':
    titles = [t[0] for t in db_helper.get_titles(10000, 0)]

    tfidf_vectorizer = TfidfVectorizer(min_df=1,
                                       max_features=None,
                                       ngram_range=(1, 2),
                                       use_idf=1,
                                       smooth_idf=1,
                                       sublinear_tf=1)

    terms = []
    for title in titles:
        terms.append(' '.join(list(jieba.cut(title))))

    train_vec = tfidf_vectorizer.fit_transform(terms)

    query = "习近平强调高质量发展 带领中国经济再上新台阶"
    str_terms = list(jieba.cut(query))
    str_vec = tfidf_vectorizer.transform([' '.join(str_terms)])

    lshf = LSHForest(random_state=42)
    lshf.fit(train_vec.toarray())

    dis, ind = lshf.kneighbors(str_vec.toarray(), n_neighbors=4)

    print(dis)
    print(ind)

    for i in ind[0]:
        print(titles[i])
