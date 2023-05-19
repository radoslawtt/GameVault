import pymysql
import csv

#CHANGE HOST, USER, PASSWORD BEFORE RUNNING PROGRAM

def conect_db():
           db_connection = pymysql.connect(
                host='host',
                user='user',
                password='password',
                db='game_platform',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
           cursor = db_connection.cursor()
           return db_connection, cursor


def disconnect_db(cursor, db):
    cursor.close()
    db.close()


def create_database():
    db_connection = pymysql.connect(
        host='host',
        user='user',
        password='password',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with db_connection.cursor() as my_cursor:
            sql = "CREATE DATABASE IF NOT EXISTS game_platform"
            my_cursor.execute(sql)

        db_connection.commit()
    finally:
        db_connection.close()


def create_users_data_table():
    my_db, my_cursor = conect_db()
    sql = """
                    CREATE TABLE IF NOT EXISTS `users_data` (
                      `id` INT(11) NOT NULL AUTO_INCREMENT,
                      `username` VARCHAR(50) NOT NULL,
                      `password` VARCHAR(50) NOT NULL,
                      `question` VARCHAR(100) NOT NULL,
                      `answer` VARCHAR(50) NOT NULL,
                      PRIMARY KEY (`id`),
                      UNIQUE KEY (`username`)
                    ) 
                    """
    my_cursor.execute(sql)
    my_db.commit()
    disconnect_db(my_cursor, my_db)


def create_users_scores_table():

    my_db, my_cursor = conect_db()
    sql = """
                CREATE TABLE IF NOT EXISTS `users_scores` (
                  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
                  `tetris_points` INT(11) NOT NULL,
                  `tetris_best_score` INT(11) NOT NULL,
                  `snake_points` INT(11) NOT NULL,
                  `snake_best_score` INT(11) NOT NULL,
                  `sudoku_points` INT(11) NOT NULL,
                  `sudoku_best_time` VARCHAR(15) NOT NULL,
                  `hangman_points` INT(11) NOT NULL,
                  `hangman_best_score` INT(11) NOT NULL,
                  UNIQUE KEY (`user_id`)
                ) 
                """
    my_cursor.execute(sql)
    my_db.commit()
    disconnect_db(my_cursor, my_db)


def create_games_tracking_table():

    my_db, my_cursor = conect_db()
    sql = """
                CREATE TABLE IF NOT EXISTS `games_tracking` (
                  `id` INT(11) NOT NULL AUTO_INCREMENT,
                  `game_name` VARCHAR(15) NOT NULL,
                  `user_id` INT(11) NOT NULL,
                  `user_score` INT(11) NOT NULL,
                  PRIMARY KEY (`id`)
                ) 
                """
    my_cursor.execute(sql)
    my_db.commit()
    disconnect_db(my_cursor, my_db)


def create_sudoku_puzzle_table():
    my_db, my_cursor = conect_db()
    sql_1 = """
                CREATE TABLE IF NOT EXISTS`sudoku_puzzles` (
                  `id` INT(11) NOT NULL AUTO_INCREMENT,
                  `puzzles` VARCHAR(100) NOT NULL,
                  `solutions` VARCHAR(100) NOT NULL,
                  PRIMARY KEY (`id`)
                ) 
                """
    my_cursor.execute(sql_1)
    my_db.commit()

    with open('sudoku_puzzles.csv', 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)
        for row in csv_data:
            my_cursor.execute('INSERT INTO sudoku_puzzles (puzzles, solutions) VALUES (%s, %s)', (row[0], row[1]))
    my_db.commit()
    disconnect_db(my_cursor, my_db)


def create_words_table():
    my_db, my_cursor = conect_db()
    sql_1 = """
        CREATE TABLE IF NOT EXISTS `english_words` (
          `words` VARCHAR(100) NOT NULL
        ) 
    """
    my_cursor.execute(sql_1)
    my_db.commit()

    with open('words.csv', 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)
        for row in csv_data:
            my_cursor.execute('INSERT INTO english_words (words) VALUES (%s)', (row[0],))
    my_db.commit()
    disconnect_db(my_cursor, my_db)


def register_user(username, password, question, answer):
    my_db, my_cursor = conect_db()
    sql_1 = "INSERT INTO users_data (username, password, question, answer) VALUES (%s, %s, %s, %s)"
    values = (username, password, question, answer)
    my_cursor.execute(sql_1, values)
    my_db.commit()

    user_id = my_cursor.lastrowid
    sql_2 = "INSERT INTO users_scores (user_id, tetris_points, tetris_best_score, snake_points, snake_best_score, sudoku_points, sudoku_best_time, hangman_points, hangman_best_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (user_id, 0, 0, 0, 0, 0, "00:00", 0, 0)
    my_cursor.execute(sql_2, values)
    my_db.commit()

    disconnect_db(my_cursor, my_db)


def login_user(username, password):
    my_db, my_cursor = conect_db()
    sql = "SELECT * FROM users_data WHERE BINARY username=%s AND BINARY password=%s"
    values = (username, password)
    my_cursor.execute(sql, values)
    result = my_cursor.fetchone()
    my_db.commit()
    disconnect_db(my_cursor, my_db)
    return result


def username_exist(username):
    my_db, my_cursor = conect_db()
    sql = "SELECT * FROM users_data WHERE BINARY username=%s"
    values = (username,)
    my_cursor.execute(sql, values)
    result = my_cursor.fetchone()
    my_db.commit()
    disconnect_db(my_cursor, my_db)
    if result:
        security_question = result["question"]
        return security_question


def answer_verification(username, answer):
    my_db, my_cursor = conect_db()
    sql = "SELECT * FROM users_data WHERE BINARY username=%s"
    values = (username,)
    my_cursor.execute(sql, values)
    result = my_cursor.fetchone()
    my_db.commit()
    disconnect_db(my_cursor, my_db)
    if result["answer"] == answer:
        return True
    else:
        return False


def replace_password(username, password):
    my_db, my_cursor = conect_db()
    sql = "UPDATE users_data SET password=%s WHERE BINARY username=%s"
    values = (password, username)
    my_cursor.execute(sql, values)
    my_db.commit()
    disconnect_db(my_cursor, my_db)


def replace_username(old_username, new_username):
    my_db, my_cursor = conect_db()
    sql_1 = "SELECT username FROM users_data WHERE username = %s"
    values = (new_username,)
    my_cursor.execute(sql_1, values)
    result = my_cursor.fetchone()
    if result is not None:
        disconnect_db(my_cursor, my_db)
        return False
    else:
        sql_2 = "UPDATE users_data SET username=%s WHERE BINARY username=%s"
        values = (new_username, old_username)
        my_cursor.execute(sql_2, values)
        my_db.commit()
        disconnect_db(my_cursor, my_db)
        return True


def replace_security(username, question, answer):
    my_db, my_cursor = conect_db()
    sql = "UPDATE users_data SET question=%s, answer=%s WHERE BINARY username=%s"
    values = (question, answer, username)
    my_cursor.execute(sql, values)
    my_db.commit()
    disconnect_db(my_cursor, my_db)


def delete_account(username):
    my_db, my_cursor = conect_db()
    sql = "DELETE FROM users_data WHERE BINARY username = %s"
    values = username
    my_cursor.execute(sql, values)
    my_db.commit()
    disconnect_db(my_cursor, my_db)


def load_user_best_score(username, game_name):
        best_score = 0
        sql_2 = ""
        my_db, my_cursor = conect_db()
        sql_1 = "SELECT id FROM users_data WHERE BINARY username = %s"
        values = username
        my_cursor.execute(sql_1, values)
        user_id = my_cursor.fetchone()

        if game_name == "sudoku":
            sql_2 = "SELECT sudoku_best_time FROM users_scores WHERE user_id = %s"
            values = (user_id["id"],)
            my_cursor.execute(sql_2, values)
            result = my_cursor.fetchone()
            best_score = result[f"sudoku_best_time"] if result else None
        else:
            sql_2 = f"SELECT {game_name}_best_score FROM users_scores WHERE user_id = %s"
            values = (user_id["id"],)
            my_cursor.execute(sql_2, values)
            result = my_cursor.fetchone()
            best_score = result[f"{game_name}_best_score"] if result else None

        disconnect_db(my_cursor, my_db)

        return best_score


def change_user_scores(username, game_name, user_score):
    my_db, my_cursor = conect_db()
    sql_1 = "SELECT id FROM users_data WHERE BINARY username = %s"
    values = username
    my_cursor.execute(sql_1, values)

    user_id = my_cursor.fetchone()
    sql_2 = f"UPDATE users_scores SET {game_name}_points = {game_name}_points + %s WHERE user_id = %s"
    values = (user_score, user_id["id"],)
    my_cursor.execute(sql_2, values)
    my_db.commit()

    disconnect_db(my_cursor, my_db)


def change_user_best_score(username, game_name, user_score):
    my_db, my_cursor = conect_db()
    sql_1 = "SELECT id FROM users_data WHERE BINARY username = %s"
    values = username
    my_cursor.execute(sql_1, values)
    user_id = my_cursor.fetchone()

    if game_name == "sudoku":
        sql_2 = "UPDATE users_scores SET sudoku_best_time = %s WHERE user_id = %s"
        values = (user_score, user_id["id"],)
        my_cursor.execute(sql_2, values)

    else:
        sql_2 = f"UPDATE users_scores SET {game_name}_best_score = %s WHERE user_id = %s"
        values = (user_score, user_id["id"],)
        my_cursor.execute(sql_2, values)

    my_db.commit()
    disconnect_db(my_cursor, my_db)


def save_game_data(username, game_name, user_score):
    my_db, my_cursor = conect_db()
    sql_1 = "SELECT id FROM users_data WHERE BINARY username = %s"
    values = username
    my_cursor.execute(sql_1, values)

    user_id = my_cursor.fetchone()
    sql_2 = "INSERT INTO games_tracking (game_name, user_id, user_score) VALUES (%s, %s, %s)"
    values = (game_name, user_id["id"], user_score)
    my_cursor.execute(sql_2, values)
    my_db.commit()

    disconnect_db(my_cursor, my_db)


def load_sudoku(id):
    my_db, my_cursor = conect_db()
    sql_1 = "SELECT puzzles, solutions FROM sudoku_puzzles WHERE id = %s"
    values = id
    my_cursor.execute(sql_1, values)
    result = my_cursor.fetchone()
    disconnect_db(my_cursor, my_db)

    return result["puzzles"], result["solutions"]


def load_word():
    my_db, my_cursor = conect_db()
    sql = "SELECT * FROM english_words ORDER BY RAND() LIMIT 1"
    my_cursor.execute(sql)
    result = my_cursor.fetchone()
    disconnect_db(my_cursor, my_db)

    return result["words"]


def load_ranking(game_name, places):
    my_db, my_cursor = conect_db()
    sql = f"SELECT * FROM users_scores ORDER BY {game_name}_points DESC LIMIT 10"
    my_cursor.execute(sql)
    results = my_cursor.fetchall()

    ranked_results = []

    for result in results:
        user_id = result['id']
        user_name = get_user_name_by_id(user_id)
        result['username'] = user_name
        ranked_results.append(result)

    disconnect_db(my_cursor, my_db)

    return ranked_results


def get_user_name_by_id(user_id):

    my_db, my_cursor = conect_db()
    sql = "SELECT username FROM users_data WHERE id = %s"
    my_cursor.execute(sql, user_id)
    result = my_cursor.fetchone()
    disconnect_db(my_cursor, my_db)
    return result["username"]