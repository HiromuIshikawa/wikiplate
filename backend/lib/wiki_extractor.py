# -*- coding: utf-8 -*-
from .connector import MySQL
import yaml
import pandas as pd
import os
import re

class WikiExtractor:
    def __init__(self, f_name):
        try:
            url = os.environ['JAWSDB_URL']
            m = re.match('mysql://(.*):(.*)@(.*):3306/(.*)', url)
            arg = m.groups()
            print(arg)
            conf = {'host':arg[2], 'user':arg[0], 'password':arg[1], 'database':arg[3], 'charset':'utf8'}
        except:
            f = open(f_name, "r+")
            conf = yaml.load(f)

        self.conf = conf

        mysql = MySQL(conf)
        self.conn = mysql.connection()
        if self.conn.is_connected() == False:
            print("Connection is down. Start reconnection...")
            self.conn.ping(reconnect=True)
            if self.conn.is_connected():
                print("Success reconnect")
            else:
                print("Failed reconnect")

    def categories(self, page_id):
        """
        Return categories(pandas DataFrame) from an Page object
        """

        sql = """
                SELECT
                  page_id, page_title
                FROM
                  page
                INNER JOIN
                  categorylinks
                ON
                  page_title = cl_to
                WHERE
                  cl_from = {} and page_namespace = 14

              """.format(page_id)

        df_read = pd.read_sql(sql, self.conn)
        # For convert bytearray to str
        decode = lambda x: x.decode()
        df_read["page_title"] = df_read["page_title"].map(decode)
        return df_read

    def infoboxed_pages(self, page_title):
        """
        Return all infoboxed pages by a infobox
        """

        sql = """
                SELECT
                  page_id, page_title
                FROM
                  templatelinks
                INNER JOIN
                  page
                ON
                  tl_from = page_id
                WHERE
                  tl_title = "{}" and page_namespace = 0
        """.format(page_title)

        df_read = pd.read_sql(sql, self.conn)
        decode = lambda x: x.decode()
        df_read["page_title"] = df_read["page_title"].map(decode)
        return df_read

    def page(self, page_id):
        """
        Get Wikipedia page from page_id
        """

        sql = """
                SELECT
                  page_id, page_title
                FROM
                  page
                WHERE
                  page_id = {}
        """.format(page_id)

        if self.conn.is_connected() == False:
            print("Connection is down. Start reconnection...")
            self.conn.ping(reconnect=True)
            if self.conn.is_connected():
                print("Success reconnect")
            else:
                print("Failed reconnect")
        df_read = pd.read_sql(sql, self.conn)
        decode = lambda x: x.decode()
        df_read["page_title"] = df_read["page_title"].map(decode)
        return df_read

    def insert_article(self, page_id, title, infobox, keywords):
        """
        Insert Article object into article table
        """
        if '"' in title:
            title = "'" + title + "'"
        else:
            title = '"' + title + '"'

        sql = """
                INSERT INTO article (page_id, title, infobox, keywords)
                VALUES ({}, {}, {}, '{}' );
        """.format(page_id, title, infobox, str(keywords).replace("'",'"').replace('""",', ''))
        cur = self.conn.cursor()

        try:
            cur.execute(sql)
            self.conn.commit()
        except:
            print(sql)
            self.conn.rollback()

    def add_sections(self, page_id, sections):
        """
        Add data into sectios column
        """

        sql = """
                UPDATE article SET sections='{}'
                WHERE page_id={};
        """.format(str(sections).replace("'",'"').replace('""",', ''), page_id)

        cur = self.conn.cursor()

        try:
            cur.execute(sql)
            self.conn.commit()
        except:
            print(sql)
            self.conn.rollback()

    def add_selected_keys(self, page_id, keys):
        """
        Add data into keywords column
        """

        sql = """
                UPDATE article SET selected_keys='{}'
                WHERE page_id={};
        """.format(str(keys).replace("'",'"').replace('""",', ''), page_id)

        cur = self.conn.cursor()

        try:
            cur.execute(sql)
            self.conn.commit()
        except:
            print(sql)
            self.conn.rollback()

    def articles(self):

        sql = """
                SELECT page_id FROM article
        """

        df_read = pd.read_sql(sql, self.conn)
        return df_read

    def articles_from_keys_or(self, keys):

        query = """JSON_CONTAINS(keywords, '"{}"')""".format(keys[0])
        for key in keys[1:]:
            query += """ OR JSON_CONTAINS(keywords, '"{}"')""".format(key)
        sql = """
                SELECT * FROM article
                WHERE {};
        """.format(query)

        df_read = pd.read_sql(sql, self.conn)

        return df_read

    def articles_from_keys(self, keys):

        query = "JSON_CONTAINS(selected_keys, *{}*)".format(keys)
        query = query.replace("'",'"').replace("*","'")
        print(query)
        sql = """
                SELECT * FROM article
                WHERE {};
        """.format(query)
        if self.conn.is_connected() == False:
            print("Connection is down. Start reconnection...")
            self.conn.ping(reconnect=True)
            if self.conn.is_connected():
                print("Success reconnect")
            else:
                print("Failed reconnect")
        df_read = pd.read_sql(sql, self.conn)

        return df_read

    def articles_from_ids(self, page_ids):
        query = ','.join(map(lambda x: str(x), page_ids))

        sql = """
                SELECT * FROM article
                WHERE page_id IN ({})
        """.format(query)

        try:
            df_read = pd.read_sql(sql, self.conn)
            return df_read
        except:
            print(sql)
            self.conn.rollback()

    def articles_from_titles(self, titles):
        query = ','.join(map(lambda x: "'" + x + "'", titles))

        sql = """
                SELECT * FROM article
                WHERE title IN ({})
        """.format(query)

        try:
            df_read = pd.read_sql(sql, self.conn)
            return df_read
        except:
            print(sql)
            self.conn.rollback()

    def close(self):
        self.conn.close()
