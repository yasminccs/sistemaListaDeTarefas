from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

def formatar_data(data):
    return datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

app = Flask(__name__)
app.secret_key = 'chave_secreta' 

DATABASE = 'tarefas.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                custo REAL NOT NULL,
                data_limite DATE NOT NULL,
                ordem INTEGER NOT NULL UNIQUE
            )
        ''')
        conn.commit()
        conn.close()

app.jinja_env.filters['moeda'] = formatar_moeda

def validar_data(data_limite):
    try:
        data_limite_dt = datetime.strptime(data_limite, '%Y-%m-%d').date()
        if data_limite_dt < datetime.now().date():
            return False, "A data limite não pode ser anterior à data atual."
        return True, "Data válida."
    except ValueError:
        return False, "Formato de data inválido. Use AAAA-MM-DD."
    
@app.route('/')
def lista_tarefas():
    conn = get_db_connection()
    tarefas = conn.execute('SELECT * FROM Tarefas ORDER BY ordem').fetchall()
    conn.close()
    tarefas_formatadas = [
        {**tarefa, 'data_limite': formatar_data(tarefa['data_limite'])} for tarefa in tarefas
    ]
    return render_template('lista_tarefas.html', tarefas=tarefas_formatadas)

@app.route('/incluir', methods=('GET', 'POST'))
def incluir_tarefa():
    mensagem = None
    if request.method == 'POST':
        nome = request.form['nome'].strip().lower()
        custo = float(request.form['custo'])
        data_limite = request.form['data_limite']
        
        data_valida, mensagem = validar_data(data_limite)
        if not data_valida:
            return render_template('incluir_tarefa.html', datetime=datetime, mensagem=mensagem)

        conn = get_db_connection()
        try:
            ordem_max = conn.execute('SELECT MAX(ordem) FROM Tarefas').fetchone()[0]
            ordem_max = ordem_max + 1 if ordem_max is not None else 1
            
            tarefa_existe = conn.execute('SELECT 1 FROM Tarefas WHERE LOWER(nome) = ?', (nome,)).fetchone()
            if tarefa_existe:
                mensagem = 'O nome da tarefa já existe!'
                return render_template('incluir_tarefa.html', datetime=datetime, mensagem=mensagem)

            conn.execute(
                'INSERT INTO Tarefas (nome, custo, data_limite, ordem) VALUES (?, ?, ?, ?)',
                (nome, custo, data_limite, ordem_max)
            )
            conn.commit()
            flash('Tarefa incluída com sucesso!', 'success')
            return redirect(url_for('lista_tarefas'))
        except sqlite3.IntegrityError:
            mensagem = 'Erro ao adicionar a tarefa.'
        finally:
            conn.close()

    return render_template('incluir_tarefa.html', datetime=datetime, mensagem=mensagem)

@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar_tarefa(id):
    conn = get_db_connection()
    tarefa = conn.execute('SELECT * FROM Tarefas WHERE id = ?', (id,)).fetchone()
    mensagem = None
    if request.method == 'POST':
        novo_nome = request.form['nome'].strip().lower()
        novo_custo = float(request.form['custo'])
        nova_data_limite = request.form['data_limite']
        nova_ordem = int(request.form['ordem'])

        data_valida, mensagem = validar_data(nova_data_limite)
        if not data_valida:
            return render_template('editar_tarefa.html', tarefa=tarefa, datetime=datetime, mensagem=mensagem)

        if novo_nome != tarefa['nome'].lower():
            tarefa_existe = conn.execute('SELECT 1 FROM Tarefas WHERE LOWER(nome) = ? AND id != ?', (novo_nome, id)).fetchone()
            if tarefa_existe:
                mensagem = 'O nome da tarefa já existe!'
                return render_template('editar_tarefa.html', tarefa=tarefa, datetime=datetime, mensagem=mensagem)

        conn.execute(
            'UPDATE Tarefas SET nome = ?, custo = ?, data_limite = ? WHERE id = ?',
            (novo_nome, novo_custo, nova_data_limite, id)
        )
        conn.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('lista_tarefas'))

    conn.close()
    return render_template('editar_tarefa.html', tarefa=tarefa, datetime=datetime, mensagem=mensagem)

@app.route('/excluir/<int:id>', methods=('POST',))
def excluir_tarefa(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Tarefa excluída com sucesso!', 'success')
    return redirect(url_for('lista_tarefas'))

@app.route('/reordenar', methods=['POST'])
def reordenar():
    data = request.get_json()
    ordem_nova = data['ordem_nova']

    conn = get_db_connection()
    for ordem, id in enumerate(ordem_nova, start=1):
        conn.execute('UPDATE Tarefas SET ordem = ? WHERE id = ?', (ordem, id))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/mover_tarefa', methods=['POST'])
def mover_tarefa():
    id = request.form['id']
    direcao = request.form['direcao']

    conn = get_db_connection()
    tarefa = conn.execute('SELECT id, ordem FROM Tarefas WHERE id = ?', (id,)).fetchone()

    if direcao == 'subir' and tarefa['ordem'] > 1:
        nova_ordem = tarefa['ordem'] - 1
    elif direcao == 'descer':
        nova_ordem = tarefa['ordem'] + 1
    else:
        return redirect(url_for('lista_tarefas'))

    tarefa_vizinha = conn.execute('SELECT id FROM Tarefas WHERE ordem = ?', (nova_ordem,)).fetchone()

    if tarefa_vizinha:
        conn.execute('UPDATE Tarefas SET ordem = ? WHERE id = ?', (tarefa['ordem'], tarefa_vizinha['id']))

    conn.execute('UPDATE Tarefas SET ordem = ? WHERE id = ?', (nova_ordem, tarefa['id']))
    conn.commit()
    conn.close()

    return redirect(url_for('lista_tarefas'))

init_db()

if __name__ == '__main__':
    app.run(debug=True)
