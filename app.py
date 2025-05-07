import sqlite3, requests
from settings import url, account, password, db_path, id_community
from functools import reduce
from module import ApiClient, DataBase



id = '1725'


class Community:

    def __init__(self, apiclient, community_database):
        self.community_database = community_database
        self.apiclient = apiclient.get_full_dict()


community = Community(apiclient=ApiClient(url, account=account, password=password, id_community=id), community_database=DataBase(db_path, id_community=id))

community.community_database.create_table(id)

for info_device in community.apiclient:
    community.community_database.add_device(info_device)







print(community.apiclient)








