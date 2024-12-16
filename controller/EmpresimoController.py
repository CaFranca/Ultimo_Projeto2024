from flask import Blueprint, request, redirect, url_for, render_template, flash
from repository import EmprestimosRepository
from datetime import datetime

emprestimoController = Blueprint('bp_loan', __name__)
emprestimosRepository = EmprestimosRepository()


@emprestimoController.route('/add', methods=['POST'])
def add_emprestimo():
    try:
        # Coleta de dados do formulário
        usuario_id = request.form.get('usuario_id')
        livro_id = request.form.get('livro_id')
        data_emprestimo = datetime.now().replace(second=0, microsecond=0)
        data_devolucao_prevista_bruta = request.form.get('data_devolucao_prevista')
        data_devolucao_prevista = datetime.strptime(data_devolucao_prevista_bruta, '%Y-%m-%d')

        # Validação dos campos obrigatórios
        if not all([usuario_id, livro_id, data_emprestimo, data_devolucao_prevista]):
            flash("Todos os campos são obrigatórios.", "error")
            return redirect(url_for('bp_loan.view_emprestimos'))

        # Tentativa de criar o empréstimo
        response = emprestimosRepository.criarEmprestimo(
            usuario_id, livro_id, data_emprestimo, data_devolucao_prevista
        )
        if isinstance(response, str):
            flash(response, "error")
        else:
            flash("Empréstimo criado com sucesso!", "success")

        return redirect(url_for('bp_loan.view_emprestimos'))
    except Exception as e:
        flash(f"Erro ao criar empréstimo: {e}", "error")
        return redirect(url_for('bp_loan.view_emprestimos'))


@emprestimoController.route('/', methods=['GET'])
def view_emprestimos():
    try:
        # Busca todos os empréstimos para exibição
        emprestimos = emprestimosRepository.listarTodosJSON()
        usuarios=emprestimosRepository.getUsuarios()
        livros=emprestimosRepository.getLivros()
        return render_template("Emprestimo/emprestimos.html", emprestimos=emprestimos,livros=livros,usuarios=usuarios)
    except Exception as e:
        flash(f"Erro ao carregar os empréstimos: {e}", "error")
        print(f"Erro ao carregar os empréstimos: {e}", "error")
        return render_template("Emprestimo/emprestimos.html", emprestimos=[])


@emprestimoController.route('/editar/<int:emprestimo_id>', methods=['GET', 'POST'])
def edit_emprestimo(emprestimo_id):
    try:
        if request.method == 'POST':
            usuario_id = request.form.get('usuario_id')
            livro_id = request.form.get('livro_id')
            data_emprestimo = datetime.now().replace(second=0, microsecond=0)
            data_devolucao_prevista_bruta = request.form.get('data_devolucao_prevista')
            data_devolucao_prevista = datetime.strptime(data_devolucao_prevista_bruta, '%Y-%m-%d').date()
            print(type(data_devolucao_prevista_bruta),type(data_devolucao_prevista))
            
            if not all([usuario_id, livro_id, data_emprestimo, data_devolucao_prevista]):
                flash("Todos os campos são obrigatórios.", "error")
                print("Todos os campos são obrigatórios.", "error")
                return redirect(url_for('bp_loan.edit_emprestimo', emprestimo_id=emprestimo_id))

            response = emprestimosRepository.atualizar_devolucao(emprestimo_id,usuario_id, livro_id, data_emprestimo, data_devolucao_prevista)
            if "Erro" in response:
                flash(response, "error")
                print(response, "error")
            else:
                flash("Devolução atualizada com sucesso!", "success")
                print("Devolução atualizada com sucesso!", "success")

            return redirect(url_for('bp_loan.view_emprestimos'))

        # Recuperação do empréstimo para exibição no formulário
        emprestimo = emprestimosRepository.buscarEmprestimoPorId(emprestimo_id)
        usuarios=emprestimosRepository.getUsuarios()
        livros=emprestimosRepository.getLivros()
        if not emprestimo:
            flash("Empréstimo não encontrado.", "error")
            print("Empréstimo não encontrado.", "error")
            return redirect(url_for('bp_loan.view_emprestimos'))

        return render_template("Emprestimo/EmprestimosEdit.html", emprestimo=emprestimo,usuarios=usuarios,livros=livros)
    except Exception as e:
        flash(f"Erro ao editar empréstimo: {e}", "error")
        print(f"Erro ao editar empréstimo: {e}", "error")
        return redirect(url_for('bp_loan.view_emprestimos'))


@emprestimoController.route('/excluir/<int:emprestimo_id>', methods=['GET','POST'])
def deletar_emprestimo(emprestimo_id):
    try:
        response = emprestimosRepository.deletarEmprestimo(emprestimo_id)
        if "Erro" in response:
            flash(response, "error")
        else:
            flash("Empréstimo excluído com sucesso!", "success")

        return redirect(url_for('bp_loan.view_emprestimos'))
    except Exception as e:
        flash(f"Erro ao excluir empréstimo: {e}", "error")
        return redirect(url_for('bp_loan.view_emprestimos'))


@emprestimoController.route('/usuario/<int:usuario_id>', methods=['GET'])
def listar_por_usuario(usuario_id):
    try:
        emprestimos = emprestimosRepository.listarPorUsuarioJSON(usuario_id)
        return render_template("Emprestimo/emprestimos_por_usuario.html", emprestimos=emprestimos)
    except Exception as e:
        flash(f"Erro ao listar empréstimos por usuário: {e}", "error")
        return render_template("Emprestimo/emprestimos_por_usuario.html", emprestimos=[])


@emprestimoController.route('/livro/<int:livro_id>', methods=['GET'])
def listar_por_livro(livro_id):
    try:
        emprestimos = emprestimosRepository.listarPorLivroJSON(livro_id)
        return render_template("Emprestimo/emprestimos_por_livro.html", emprestimos=emprestimos)
    except Exception as e:
        flash(f"Erro ao listar empréstimos por livro: {e}", "error")
        return render_template("Emprestimo/emprestimos_por_livro.html", emprestimos=[])


@emprestimoController.route('/marcar_devolvido/<int:emprestimo_id>', methods=['GET'])
def marcar_devolvido(emprestimo_id):
    try:
        # Atualiza a data de devolução real
        data_devolucao_real = datetime.now().replace(second=0, microsecond=0)
        response = emprestimosRepository.marcarDevolvido(emprestimo_id, data_devolucao_real)

        if "Erro" in response:
            flash(response, "error")
        else:
            flash("Empréstimo marcado como devolvido com sucesso!", "success")

        return redirect(url_for('bp_loan.view_emprestimos'))
    except Exception as e:
        flash(f"Erro ao marcar devolução: {e}", "error")
        return redirect(url_for('bp_loan.view_emprestimos'))