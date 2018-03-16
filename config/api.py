#!/usr/bin/env python3

from collections import  namedtuple

import os
import configparser
import logging




dic = {"DEBUG": logging.DEBUG,
       "WARNING": logging.WARNING,
       "INFO": logging.INFO,
       "CRITICAL": logging.CRITICAL,
       "ERROR": logging.ERROR,
       }






class Config(object):
    config = configparser.ConfigParser()
    rawconfig = configparser.RawConfigParser()
    config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "conf" + os.sep + "config.ini"


    @staticmethod
    def conf():
        result=dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            result["log_path"] = Config.config.get('config', 'log_path')
            result["log_level"] = Config.config.get('config', 'log_level')
        return result

    @staticmethod
    def db():
        result = dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            result["engine"] = Config.config.get('db', 'engine')
            result["host"] = Config.config.get('db', 'host')
            result["port"] = Config.config.get('db', 'port')
            result["user"] = Config.config.get('db', 'user')
            result["password"] = Config.config.get('db', 'password')
            result["database"] = Config.config.get('db', 'database')
        return result

    @staticmethod
    def redis():
        result=dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            result["host"] = Config.config.get('redis', 'host')
            result["port"] = Config.config.get('redis', 'port')
            result["user"] = Config.config.get('redis', 'user')
            result["password"] = Config.config.get('redis', 'password')
        return result

    @staticmethod
    def jenkins():
        result = dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            result["url"] = Config.config.get('jenkins', 'url')
            result["user"] = Config.config.get('jenkins', 'user')
            result["password"] = Config.config.get("jenkins","password")
        return  result


    @staticmethod
    def mongodb():
        result = dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            result["host"] = Config.config.get('mongodb', 'host')
            result["port"] = Config.config.get('mongodb', 'port')
            result["user"] = Config.config.get('mongodb', 'user')
            result["password"] = Config.config.get('mongodb', 'password')
            result["collection"] = Config.config.get('mongodb', 'collection')
        return  result

    @staticmethod
    def webssh():
        result = dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            result["webssh_domain"] = Config.config.get('webssh', 'domain')
            result["token"] = Config.config.get('webssh', 'token')
            result["password"] = Config.config.get('webssh', 'password')
        return  result

    @staticmethod
    def svn():
        result = dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            result["user"] = Config.config.get("svn", "user")
            result["password"] = Config.config.get("svn", "password")
        return result

    @staticmethod
    def email():
        result = dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            # result["tls"] = Config.config.get("email", "tls")
            # result["host"] = Config.config.get("email", "host")
            # result["port"] = Config.config.get("email", "port")
            result["email"] = Config.config.get("email", "email")
            result["password"] = Config.config.get("email", "password")
            #result["from_email"] = Config.config.get("email", "from_email")
        return result

    @staticmethod
    def ftp():
        result = dict()
        with open(Config.config_path) as cfgfile:
            Config.rawconfig.read_file(cfgfile)
            result["host"] = Config.rawconfig.get("ftp", "host")
            result["port"] = Config.rawconfig.get("ftp", "port")
            result["user"] = Config.rawconfig.get("ftp", "user")
            result["password"] = Config.rawconfig.get("ftp", "password")
            result["ftppath"] = Config.rawconfig.get("ftp","ftppath")

        return result

    @staticmethod
    def gateone():
        result = dict()
        with open(Config.config_path) as cfgfile:
            Config.config.read_file(cfgfile)
            result["api_key"] = Config.config.get("gateone", "api_key")
            result["gateone_server"] = Config.config.get("gateone", "gateone_server")
        return result

    @staticmethod
    def conf_all():
        result=dict()
        result["conf"]=Config.conf()
        result["db"] = Config.db()
        result["redis"] = Config.redis()
        result["mongodb"] = Config.mongodb()
        result["jenkins"] = Config.jenkins()
        result["gateone"] = Config.gateone()
        result["webssh"] = Config.webssh()
        result["svn"] = Config.svn()
        result["email"] = Config.email()
        result["ftp"] = Config.ftp()

        return result

    @staticmethod
    def save(*args,**kwargs):
        #config
        try:
            log_path = args[0].get('log_path')
            log_level = args[0].get('log_level')
            # db
            engine = args[0].get('engine')
            host =args[0].get('host')
            port = args[0].get('port')
            user = args[0].get('user')
            password = args[0].get('password')
            database = args[0].get('database')
            #redis
            redis_host = args[0].get('redis_host')
            redis_port = args[0].get('redis_port')
            redis_user = args[0].get('redis_user')
            redis_password =args[0].get('redis_password')
            # mongodb
            mongodb_host = args[0].get('mongodb_host')
            mongodb_port = args[0].get('mongodb_port')
            mongodb_user = args[0].get('mongodb_user')
            mongodb_password = args[0].get('mongodb_password')
            mongodb_collection = args[0].get('mongodb_collection')
            #jenkins
            jenkins_url = args[0].get("jenkins_url")
            jenkins_user = args[0].get("jenkins_user")
            jenkins_password = args[0].get("jenkins_password")
            #gateone
            api_key = args[0].get("api_key")
            gateone_server = args[0].get("gateone_server")
            #svn
            svn_user=args[0].get("svn_user")
            svn_password = args[0].get("svn_password")

            #email
            # tls=args[0].get("tls")
            # email_host = args[0].get("email_host")
            # email_port = args[0].get("email_port")
            email = args[0].get("email")
            email_password = args[0].get("email_password")
            #from_email = args[0].get("from_email")

            #ftp
            ftp_host = args[0].get("ftp_host")
            ftp_port = args[0].get("ftp_port")
            ftp_user = args[0].get("ftp_user")
            ftp_password = args[0].get("ftp_password")
            ftppath = args[0].get("ftppath")


            # webssh
            token = args[0].get('token')
            ssh_password = args[0].get('token')
            webssh_domain = args[0].get('webssh_domain')

            config=configparser.RawConfigParser()
            #config
            config.add_section('config')
            config.set('config', 'log_path', log_path)
            config.set('config', 'log_level', log_level)
            #db
            config.add_section('db')
            config.set('db', 'engine', engine)
            config.set('db', 'host', host)
            config.set('db', 'port', port)
            config.set('db', 'user', user)
            config.set('db', 'password', password)
            config.set('db', 'database', database)
            #redis
            config.add_section('redis')
            config.set('redis', 'host', redis_host)
            config.set('redis', 'port', redis_port)
            config.set('redis', 'user', redis_user)
            config.set('redis', 'password', redis_password)
            #mongodb
            config.add_section('mongodb')
            config.set('mongodb', 'host', mongodb_host)
            config.set('mongodb', 'port', mongodb_port)
            config.set('mongodb', 'user', mongodb_user)
            config.set('mongodb', 'password', mongodb_password)
            config.set('mongodb', 'collection', mongodb_collection)
            #jenkins
            config.add_section('jenkins')
            config.set('jenkins', 'url', jenkins_url)
            config.set('jenkins', 'user', jenkins_user)
            config.set('jenkins', 'password', jenkins_password)
            #gateone
            config.add_section('gateone')
            config.set("gateone", "api_key", api_key)
            config.set("gateone", "gateone_server", gateone_server)
            #svn
            config.add_section("svn")
            config.set("svn", "user", svn_user)
            config.set("svn", "password", svn_password)
            #email
            config.add_section("email")
            # config.set("email", "tls", tls)
            # config.set("email", "host", email_host)
            # config.set("email", "port", email_port)
            config.set("email", "email", email)
            config.set("email", "password", email_password)
            #config.set("email", "from_email", from_email)

            #ftp
            config.add_section("ftp")
            config.set("ftp","host", ftp_host)
            config.set("ftp", "port", ftp_port)
            config.set("ftp", "user", ftp_user)
            config.set("ftp", "password", ftp_password)
            config.set("ftp", "ftppath", ftppath)

            #webssh
            config.add_section('webssh')
            config.set('webssh', 'token', token)
            config.set('webssh', 'password', ssh_password)
            config.set('webssh', 'domain', webssh_domain)
            with open(Config.config_path, 'w') as cfgfile:
                config.write(cfgfile)
        except Exception as e:
            print(str(e))
            return False
        else:
            return True


if __name__ == '__main__':
    print(Config.ftp())
    print(Config.db)
