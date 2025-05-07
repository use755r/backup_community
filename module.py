import requests, sqlite3
class ApiClient:
    """передаем url, логинб пароль, id сообщества"""
    def __init__(self, url, account, password, id_community):
        self.row = 40
        self.url = url
        self.account = account
        self.password = password
        self.id_community = id_community
        self.token = self.get_token()

    def get_token(self):
        """получить токен авторизации"""
        response = requests.post(f'{self.url}/property/login', json={"Account": self.account, "passwd": self.password})
        response = response.json()
        return response["token"]

    def get_device_list(self, page):
        """получить список устройств на текущей странице №page"""
        response = requests.get(f'{self.url}/property/selectdevice?token={self.token}&row={self.row}&page={page}',headers={'x-community-id': f'{self.id_community}'})
        response = response.json()
        return response['data']

    def get_full_dict(self):
        """Получить полный список устройств со всех страниц"""
        full_dict = []
        count_device = self.get_device_list(page=0)['total']
        count_page = (count_device + self.row - 1) // self.row
        for i in range(1, count_page + 1):
            result = self.get_device_list(page=i)['detail']
            full_dict.extend(result)
        return full_dict


class DataBase:
    def __init__(self, db_path, id_community):
        self.db_path = db_path
        self.id_community = id_community
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def get_device_status(self, device_id):
        """Получить статус устройства из базы данных."""
        status = self.cursor.execute(f'SELECT Status FROM "{self.id_community}" WHERE ID=?', (device_id,)).fetchone()
        return status[0] if status else None

    def update_device_status(self, device_id, status):
        """Обновить статус устройства в базе данных."""
        self.cursor.execute(f'UPDATE "{self.id_community}" SET Status=? WHERE ID=?', (status, device_id))
        self.connection.commit()

    def close(self):
        """Закрыть соединение с базой данных."""
        self.connection.close()

    def add_device(self, info_device):
        """добавить устройство в базу в случае отсутствия"""
        self.cursor.execute(f'INSERT INTO "{self.id_community}" (ID, Location, MAC, LastConnection, Status, Firmware, Name, UnitName) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (int(info_device['ID']), info_device['Location'], info_device['MAC'], info_device['LastConnection'], int(info_device['Status']), info_device['Firmware'],
                     info_device['Name'], info_device['UnitName']))
        self.connection.commit()

    def create_table(self, id_community):
        """создать таблицу в базе"""
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS "{id_community}" (ID INTEGER PRIMARY KEY, Location TEXT, MAC TEXT, LastConnection TEXT, Status INTEGER, Firmware TEXT, Name TEXT, UnitName TEXT)')
        self.connection.commit()




