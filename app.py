from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave-secreta-salao-2026'
DB = 'salao.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL, telefone TEXT, servico TEXT NOT NULL,
        data TEXT NOT NULL, hora TEXT NOT NULL, preco REAL NOT NULL,
        status TEXT DEFAULT 'pendente'
    );
    CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agendamento_id INTEGER, cliente TEXT NOT NULL, valor REAL NOT NULL,
        forma TEXT NOT NULL, data TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, categoria TEXT, quantidade INTEGER DEFAULT 0,
        qtd_minima INTEGER DEFAULT 1, preco REAL DEFAULT 0
    );
    ''')
    conn.commit()
    conn.close()

@app.template_filter('moeda')
def formatar_moeda(v):
    return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

@app.template_filter('data_br')
def formatar_data(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d').strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return s

@app.route('/')
def dashboard():
    conn = get_db()
    hoje = datetime.now().strftime('%Y-%m-%d')
    agendamentos_hoje = conn.execute(
        'SELECT * FROM agendamentos WHERE data = ? ORDER BY hora', (hoje,)).fetchall()
    total_mes = conn.execute(
        "SELECT COALESCE(SUM(valor),0) t FROM pagamentos WHERE strftime('%Y-%m',data)=strftime('%Y-%m','now')"
    ).fetchone()['t']
    estoque_baixo = conn.execute(
        'SELECT * FROM estoque WHERE quantidade <= qtd_minima').fetchall()
    total_agendamentos = conn.execute('SELECT COUNT(*) c FROM agendamentos').fetchone()['c']
    conn.close()
    return render_template('dashboard.html', agendamentos_hoje=agendamentos_hoje,
        total_mes=total_mes, estoque_baixo=estoque_baixo, total_agendamentos=total_agendamentos)

@app.route('/agendamentos')
def agendamentos():
    conn = get_db()
    lista = conn.execute('SELECT * FROM agendamentos ORDER BY data DESC, hora DESC').fetchall()
    conn.close()
    return render_template('agendamentos.html', agendamentos=lista)

@app.route('/agendamentos/novo', methods=['POST'])
def novo_agendamento():
    conn = get_db()
    conn.execute('INSERT INTO agendamentos (cliente,telefone,servico,data,hora,preco) VALUES (?,?,?,?,?,?)',
        (request.form['cliente'], request.form['telefone'], request.form['servico'],
         request.form['data'], request.form['hora'], float(request.form['preco'])))
    conn.commit(); conn.close()
    flash('Agendamento criado com sucesso!')
    return redirect(url_for('agendamentos'))

@app.route('/agendamentos/<int:id>/status', methods=['POST'])
def status_agendamento(id):
    conn = get_db()
    conn.execute('UPDATE agendamentos SET status=? WHERE id=?', (request.form['status'], id))
    conn.commit(); conn.close()
    return redirect(url_for('agendamentos'))

@app.route('/agendamentos/<int:id>/deletar', methods=['POST'])
def deletar_agendamento(id):
    conn = get_db()
    conn.execute('DELETE FROM agendamentos WHERE id=?', (id,))
    conn.commit(); conn.close()
    return redirect(url_for('agendamentos'))

@app.route('/pagamentos')
def pagamentos():
    conn = get_db()
    lista = conn.execute('SELECT * FROM pagamentos ORDER BY data DESC').fetchall()
    pendentes = conn.execute("""SELECT * FROM agendamentos WHERE status != 'cancelado'
        AND id NOT IN (SELECT agendamento_id FROM pagamentos WHERE agendamento_id IS NOT NULL)""").fetchall()
    conn.close()
    return render_template('pagamentos.html', pagamentos=lista, pendentes=pendentes)

@app.route('/pagamentos/novo', methods=['POST'])
def novo_pagamento():
    conn = get_db()
    agendamento_id = request.form.get('agendamento_id') or None
    conn.execute('INSERT INTO pagamentos (agendamento_id,cliente,valor,forma,data) VALUES (?,?,?,?,?)',
        (agendamento_id, request.form['cliente'], float(request.form['valor']),
         request.form['forma'], request.form['data']))
    if agendamento_id:
        conn.execute("UPDATE agendamentos SET status='concluido' WHERE id=?", (agendamento_id,))
    conn.commit(); conn.close()
    flash('Pagamento registrado!')
    return redirect(url_for('pagamentos'))

@app.route('/relatorios')
def relatorios():
    conn = get_db()
    hoje = datetime.now()
    
    total_hoje = conn.execute("SELECT COALESCE(SUM(valor),0) FROM pagamentos WHERE data=?",
        (hoje.strftime('%Y-%m-%d'),)).fetchone()[0]
        
    inicio_semana = (hoje - timedelta(days=hoje.weekday())).strftime('%Y-%m-%d')
    total_semana = conn.execute("SELECT COALESCE(SUM(valor),0) FROM pagamentos WHERE data>=?",
        (inicio_semana,)).fetchone()[0]
        
    total_mes = conn.execute(
        "SELECT COALESCE(SUM(valor),0) FROM pagamentos WHERE strftime('%Y-%m',data)=strftime('%Y-%m','now')"
    ).fetchone()[0]
    
    dias_com_venda = conn.execute(
        "SELECT COUNT(DISTINCT data) FROM pagamentos WHERE strftime('%Y-%m',data)=strftime('%Y-%m','now')"
    ).fetchone()[0]
    
    media_diaria = float(total_mes) / float(dias_com_venda) if dias_com_venda else 0.0
    
    servicos_populares = conn.execute(
        'SELECT servico, COUNT(*) as qtd, SUM(preco) as total FROM agendamentos GROUP BY servico ORDER BY qtd DESC LIMIT 5'
    ).fetchall()
    
    formas_pagamento = conn.execute(
        'SELECT forma, COUNT(*) as qtd, SUM(valor) as total FROM pagamentos GROUP BY forma').fetchall()
    
    rows_30_dias = conn.execute("""SELECT data, SUM(valor) as total FROM pagamentos
        WHERE data >= date('now','-30 days') GROUP BY data ORDER BY data""").fetchall()
    
    ultimos_30_dias = [{'data': r['data'], 'total': r['total']} for r in rows_30_dias]
    
    conn.close()
    return render_template('relatorios.html', total_hoje=total_hoje, total_semana=total_semana,
        total_mes=total_mes, media_diaria=media_diaria, servicos_populares=servicos_populares,
        formas_pagamento=formas_pagamento, ultimos_30_dias=ultimos_30_dias)

@app.route('/estoque')
def estoque():
    conn = get_db()
    lista = conn.execute('SELECT * FROM estoque ORDER BY nome').fetchall()
    total_financeiro = conn.execute('SELECT COALESCE(SUM(quantidade * preco), 0) FROM estoque').fetchone()[0]
    conn.close()
    return render_template('estoque.html', estoque=lista, total_financeiro=total_financeiro)

@app.route('/estoque/novo', methods=['POST'])
def novo_produto():
    conn = get_db()
    conn.execute('INSERT INTO estoque (nome,categoria,quantidade,qtd_minima,preco) VALUES (?,?,?,?,?)',
        (request.form['nome'], request.form['categoria'], int(request.form['quantidade']),
         int(request.form['qtd_minima']), float(request.form['preco'])))
    conn.commit(); conn.close()
    flash('Produto adicionado!')
    return redirect(url_for('estoque'))

@app.route('/estoque/<int:id>/ajustar', methods=['POST'])
def ajustar_estoque(id):
    conn = get_db()
    delta = int(request.form['delta'])
    conn.execute('UPDATE estoque SET quantidade = MAX(0, quantidade + ?) WHERE id=?', (delta, id))
    conn.commit(); conn.close()
    return redirect(url_for('estoque'))

@app.route('/estoque/<int:id>/deletar', methods=['POST'])
def deletar_produto(id):
    conn = get_db()
    conn.execute('DELETE FROM estoque WHERE id=?', (id,))
    conn.commit(); conn.close()
    return redirect(url_for('estoque'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
