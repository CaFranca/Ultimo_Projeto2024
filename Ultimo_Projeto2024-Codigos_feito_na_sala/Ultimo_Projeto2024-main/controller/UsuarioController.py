from flask import Blueprint, request, redirect, url_for, render_template, flash
from repository import UsuarioRepository
from hashlib import sha256
from datetime import datetime

usuarioController = Blueprint('bp_usuario', __name__)
usuariosRepository = UsuarioRepository()


@usuarioController.route('/add', methods=['POST'])
def add_usuario():
    try:
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = sha256(request.form.get('senha').encode('utf-8')).hexdigest()
        tipo = request.form.get('tipo')
        data_criacao = datetime.now()

        if not all([nome, email, senha, tipo, data_criacao]):
            flash("Todos os campos são obrigatórios.", "error")
            return redirect(url_for('bp_usuario.view_usuarios'))

        response = usuariosRepository.novoUsuario(nome, email, senha, tipo, data_criacao)
        if isinstance(response, str):
            flash(response, "error")
        else:
            flash("Usuário criado com sucesso!", "success")

        return redirect(url_for('bp_usuario.view_usuarios'))
    except Exception as e:
        flash(f"Erro ao criar usuário: {e}", "error")
        return redirect(url_for('bp_usuario.view_usuarios'))


@usuarioController.route('/', methods=['GET'])
def view_usuarios():
    try:
        # Busca todos os usuários para exibição
        usuarios = usuariosRepository.listarTodosJSON()
        return render_template("Usuario/usuarios.html", usuarios=usuarios)
    except Exception as e:
        flash(f"Erro ao carregar os usuários: {e}", "error")
        return render_template("Usuario/usuarios.html", usuarios=[])


@usuarioController.route('/editar/<int:usuario_id>', methods=['GET', 'POST'])
def edit_usuario(usuario_id):
    try:
        if request.method == 'POST':
            # Atualização de dados do usuário
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            tipo = request.form.get('tipo')
            data_criacao = request.form.get('data_criacao')

            if not all([nome, email, senha, tipo, data_criacao]):
                flash("Todos os campos são obrigatórios para atualizar.", "error")
                return redirect(url_for('bp_usuario.edit_usuario', usuario_id=usuario_id))

            response = usuariosRepository.atualizar_usuario(usuario_id, nome, email, senha, tipo, data_criacao)
            if "Erro" in response:
                flash(response, "error")
            else:
                flash("Usuário atualizado com sucesso!", "success")

            return redirect(url_for('bp_usuario.view_usuarios'))

        # Recuperação do usuário para exibição no formulário
        usuario = usuariosRepository.buscarUsuarioPorId(usuario_id)
        if not usuario:
            flash("Usuário não encontrado.", "error")
            return redirect(url_for('bp_usuario.view_usuarios'))

        return render_template("Usuario/usuario_edit.html", usuario=usuario)
    except Exception as e:
        flash(f"Erro ao editar usuário: {e}", "error")
        return redirect(url_for('bp_usuario.view_usuarios'))


@usuarioController.route('/excluir/<int:usuario_id>', methods=['POST'])
def delete_usuario(usuario_id):
    try:
        response = usuariosRepository.deletar_usuario(usuario_id)
        if "Erro" in response:
            flash(response, "error")
        else:
            flash("Usuário excluído com sucesso!", "success")

        return redirect(url_for('bp_usuario.view_usuarios'))
    except Exception as e:
        flash(f"Erro ao excluir usuário: {e}", "error")
        return redirect(url_for('bp_usuario.view_usuarios'))
