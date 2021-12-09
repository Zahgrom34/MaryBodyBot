from peewee import MySQLDatabase
import configuration

Host = configuration.DATABASE['HOST']
Name = configuration.DATABASE['NAME']
User = configuration.DATABASE['USER']
Password = configuration.DATABASE['PASSWORD']
Port = configuration.DATABASE['PORT']

db = MySQLDatabase(Name, host=Host, port=Port, user=User, passwd=Password)