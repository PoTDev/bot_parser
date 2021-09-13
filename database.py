import mariadb
import sys

class database:
    

    
    def check_connection(self, check):
        try:
            # Подключение к существующей базе данных
            self.connection = mariadb.connect(user="root",
                                        password="",
                                        host="localhost",
                                        port=3306,
                                        database="bottelegram")
            #self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            # Курсор для выполнения операций с базой данных
            cursor = self.connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        user_id INT,
                        chat_id INT,
                        userfirstname VARCHAR(255),
                        usersurname VARCHAR(255),
                        username VARCHAR(255),
                        last_activity timestamp);
                        """)
            self.connection.commit()
            check = True
            

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

            self.connection.close()

            check = False

        return check
 
         


    #проверка пользователя в бд.
    #если нет - добавить, если есть - записать время последнего действия

    
    def user_identity(self, user_id, chat_id, user_name, user_surname, username):
        
        db = database()
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE chat_id=?", (chat_id, ))
        print('ЧАТ АЙДИ:', chat_id)
        # Получить результат
        record = cursor.fetchone()
        #print("Вы подключены к - ", record, "\n")


        if record:
            cursor.execute("UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE chat_id=?",(chat_id, ))
            self.connection.commit()
            print('Время пользователя обновлено')

        else:
            cursor = self.connection.cursor()
            try:
                cursor.execute("INSERT INTO users (user_id, chat_id, userfirstname, usersurname, username, last_activity) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (user_id, chat_id, user_name, user_surname, username))
                self.connection.commit()
                print('NONE')
            except mariadb.Error as e: 
                print(f"Error: {e}")

        self.connection.close()
        print('СОЕДИНЕНИЕ ЗАКРЫТО')

