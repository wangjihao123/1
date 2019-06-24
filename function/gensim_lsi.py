import jieba
from gensim import corpora
from gensim import models
from gensim import similarities
from function.database import read_question, read_answer


sim_degree = 0.6

# raw_docs = ["你的名字是什么", "你今年几岁了", "你会敲代码吗", '你会干什么',]


def get_index_matrix():

    global dictionary, lsi, raw_docs

    print('正在查询问题。。。')
    raw_docs = read_question()
    print(raw_docs)

    # 如果已经训练过，且自定义的问题未更改，可以直接加载模型、返回index
    # if 'Lsi_matrix.index' in os.listdir('.'):
    #     index = similarities.SparseMatrixSimilarity.load('Lsi_matrix.index')
    #     return index

    # 没有模型，或者自定义问题更改，开始重新训练。
    all_doc_list = [list(jieba.cut(doc)) for doc in raw_docs]
    # 制作词袋
    dictionary = corpora.Dictionary(all_doc_list)
    # 语料库:
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
    # 将corpus语料库(初识语料库) 使用Lsi模型进行训练
    lsi = models.LsiModel(corpus)
    # 文本相似度
    # 稀疏矩阵
    index = similarities.SparseMatrixSimilarity(
        lsi[corpus], num_features=len(dictionary.keys()))
    # 保存矩阵模型
    index.save('Lsi_matrix.index')
    return index


def get_high_sim(doc):

    doc_test_list = list(jieba.cut(doc))
    # 将需要寻找相似度的分词列表 做成 语料库 doc_test_vec
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    sim = index[lsi[doc_test_vec]]

    # 对下标和相似度结果进行一个排序,拿出相似度最高的结果
    cc = sorted(enumerate(sim), key=lambda item: -item[1])
    print(cc)

    high_score = cc[0]
    text = raw_docs[high_score[0]]

    print(doc, '-------', text)
    print('相似度：', high_score[1])
    if high_score[1] > sim_degree:
        return cc[0][0]


index = get_index_matrix()


if __name__ == '__main__':
    doc = '你今年多大了'
    index = get_high_sim(doc)
    print(read_answer(index))
