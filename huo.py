from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import subprocess

app = Flask(__name__)


# Обновленная функция для добавления имени игрока в базу данных
def add_player_to_db(name):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE name=?", (name,))
    existing_player = cursor.fetchone()

    if existing_player:
        # Если игрок уже существует в базе данных, обновляем его результат
        cursor.execute("UPDATE players SET score=0 WHERE name=?", (name,))
    else:
        # Если игрок не существует, создаем новую запись
        cursor.execute("INSERT INTO players (name, score) VALUES (?, 0)", (name,))

    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game', methods=['POST'])
def start_game():
    player_name = request.form['name']
    add_player_to_db(player_name)  # Добавление или обновление игрока в базе данных
    return redirect(url_for('play_game'))


@app.route('/game', methods=['GET'])
def play_game():
    return render_template('play_game.html')


@app.route('/play_pygame')
def play_pygame():
    # Запускаем игру в Pygame с помощью subprocess.Popen
    subprocess.Popen(['python', 'Apelson.py'])
    # После запуска игры, делаем редирект обратно на главную страницу или на любую другую страницу
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
