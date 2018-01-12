import sqlite3


class Doc:
    def __init__(self, doc_id=-1, url='', title='', source='', content='', time=''):
        self.doc_id = doc_id
        self.url = url
        self.title = title
        self.source = source
        self.content = content
        self.time = time


class DocDbHelper:
    @staticmethod
    def get_doc_by_id(doc_id):
        sqlite_db = sqlite3.connect('D://Project//local//pycharm//scrapy_news//web.db')
        news = sqlite_db.execute('SELECT * FROM finalnews WHERE id=?', (doc_id,))
        news = news.fetchall()[0]
        source = '%s~%s' % (news[5], news[4])
        return Doc(doc_id=news[0],
                   url=news[1],
                   title=news[2],
                   source=source,
                   content=news[6],
                   time=news[8]
                   )

    @staticmethod
    def get_titles(page_size, page_num):
        sqlite_db = sqlite3.connect('D://Project//local//pycharm//scrapy_news//web.db')
        page_offset = page_size*page_num
        cursor = sqlite_db.execute(
            'SELECT title FROM finalnews limit ?, ?', (page_offset, page_size))
        return cursor.fetchall()


db_helper = DocDbHelper()
