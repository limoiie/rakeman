import time

import jieba
import jieba.posseg
import redis

from rake.core.constants import *
from rake.core.dbhelper import db_helper
from rake.core.serialize import *
from rake.core.utils import LRUCache


class QueryMsgQueue:

    def __init__(self, redis_db: redis.StrictRedis):
        self.redis_db = redis_db
        self.task_id = 0

    def __generate_task_id(self):
        return self.redis_db.incr(KEY_TASK_ID, 1)

    def publish_query_task(self, sentence) -> list:
        serialized_task = bytearray()
        # step 1: append task type, 2 for query
        serialized_task.append(2)

        task_id = self.__generate_task_id()
        # step 2: append task id
        serialized_task.extend(serialize_integer(task_id))
        # step 3: append query sentence
        serialized_task.extend(serialize_string(sentence))

        self.redis_db.rpush(KEY_TASK_QUEUE, bytes(serialized_task))

        print('query: wait for response...')
        while True:
            response_bytes = self.redis_db.hget(KEY_RESPONSE_QUERY_HASH, str(task_id))
            if response_bytes is not None and len(response_bytes) > 0:
                print('query: response: ')
                if chr(response_bytes[0]) == '0':
                    doc_ids = list()

                    offset = 1
                    num_docs, offset = deserialize_integer(response_bytes, offset)
                    for ii in range(0, num_docs):
                        doc_id, offset = deserialize_integer(response_bytes, offset)
                        doc_ids.append(doc_id)
                    return doc_ids
                else:
                    raise Exception('Fuck, query failed.')

            time.sleep(0.01)


cache = LRUCache(100)

msg_queue = QueryMsgQueue(redis.StrictRedis(host='192.168.128.129'))


def generate_digest_by_terms(doc: Doc, keywords: set):
    keywords = sorted(keywords, key=len)

    if len(doc.content) > 240:
        for keyword in keywords:
            ind = doc.content.find(keyword)
            if ind != -1:
                start = ind - 120 if ind > 120 else 0
                content_size = len(doc.content)

                if ind + 120 > content_size:
                    doc.content = ('...' if start != 0 else '') + doc.content[start:content_size]
                else:
                    doc.content = ('...' if start != 0 else '') + doc.content[start:ind + 120] + '...'
                break

    for keyword in keywords:
        doc.title = doc.title.replace(keyword, '<code>' + keyword + '</code>')
        doc.content = doc.content.replace(keyword, '<code>' + keyword + '</code>')

    return doc


def express_query(query_sentence: str, page: int, page_size: int) -> list():
    doc_id_list = cache.get(query_sentence)
    hit_in_history = doc_id_list is not None
    if not hit_in_history:
        doc_id_list = msg_queue.publish_query_task(query_sentence)

    terms = jieba.posseg.cut(query_sentence)
    keywords = {word for word, flag in terms if flag != 'x' and flag != 'uj'}

    doc_list = []
    offset = page * page_size
    doc_id_page = doc_id_list[offset:offset + page_size]
    for doc_id in doc_id_page:
        doc = db_helper.get_doc_by_id(doc_id)
        doc_list.append(generate_digest_by_terms(doc, keywords))

    if not hit_in_history:
        cache.set(query_sentence, doc_id_list)
    return doc_list, len(doc_id_list)


if __name__ == '__main__':
    for i in express_query('微风习习 透漏', 10, 5):
        print(i)
