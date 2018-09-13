# -*- coding: utf-8 -*-
from .connector import MySQL
import yaml
import pandas as pd

class WikiExtractor:
    def __init__(self, f_name):
        f = open(f_name, "r+")
        conf = yaml.load(f)

        mysql = MySQL(conf)
        self.conn = mysql.connection()

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
        """.format(page_id, title, infobox, str(keywords).replace("'",'"'))
        cur = self.conn.cursor()

        try:
            cur.execute(sql)
            self.conn.commit()
        except:
            print(sql)
            self.conn.rollback()
            raise

    def articles_from_keys(self, keys):

        query = """JSON_CONTAINS(keywords, '"{}"')""".format(keys[0])
        for key in keys[1:]:
            query += """ OR JSON_CONTAINS(keywords, '"{}"')""".format(key)
        sql = """
                SELECT * FROM article
                WHERE {};
        """.format(query)

        df_read = pd.read_sql(sql, self.conn)

        return df_read

    def close(self):
        self.conn.close()
