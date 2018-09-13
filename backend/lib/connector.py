# -*- coding: utf-8 -*-
import mysql.connector
import yaml

class MySQL:
    def __init__(self, conf):
        """
        conf: dictionary of config for connection
        """
        self.conf = conf
        self.conn = None

        if conf != None:
            self.connect()



    def connect(self, conf=None):
        """
        connect to mysql
        """
        if conf == None:
            conf = self.conf
        conn = mysql.connector.connect(**conf)

        self.conn = conn



    def close(self):
        self.conn.close()



    def connection(self):
        return self.conn



if __name__ == "__main__":
    f = open("../../settings.yml", "r+")
    conf = yaml.load(f)

    mysql = MySQL(conf)
    conn = mysql.connection()

    if conn.is_connected():
        print("Successed to connect.")
    else:
        print("Failed to connect.")
