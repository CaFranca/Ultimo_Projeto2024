from database import database

class Emprestimos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey("usuarios.id"), nullable=False)
    livro_id = database.Column(database.Integer, database.ForeignKey("livros.id"), nullable=False)
    data_emprestimo = database.Column(database.DateTime, nullable=False)
    data_devolucao_prevista = database.Column(database.DateTime, nullable=False)
    data_devolucao_real = database.Column(database.DateTime, nullable=True)

    usuario = database.relationship("Usuarios", back_populates="emprestimos")
    livro = database.relationship("Livros", back_populates="emprestimos")

    def JSonificar(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "livro_id": self.livro_id,
            "data_emprestimo": self.data_emprestimo.isoformat(),
            "data_devolucao_prevista": self.data_devolucao_prevista.isoformat(),
            "data_devolucao_real": self.data_devolucao_real.isoformat() if self.data_devolucao_real else None
        }