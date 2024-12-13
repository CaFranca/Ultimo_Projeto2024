from DAO import LivroDAO
from datetime import datetime

class LivroRepository:
    def __init__(self):
        self.livroDAO = LivroDAO()

    def searchBooksJSON(self):
        try:
            livros = self.livroDAO.searchBooks()
            return [livro.JSonificar() for livro in livros]
        except Exception as e:
            return {"error": f"Erro ao buscar livros: {e}"}

    def addBook(self, titulo, isbn, data_publicacao, autor_id, categoria_id):
        try:
            data_publicacao_formatada = datetime.strptime(data_publicacao, "%Y-%m-%d").date()
            sucesso = self.livroDAO.addBook(
                titulo, isbn, data_publicacao_formatada,autor_id, categoria_id
            )
            return {"success": sucesso}
        except ValueError as e:
            return {"error": f"Data de publicação inválida ({e})"}
        except Exception as e:
            return {"error": f"Erro ao adicionar livro: {e}"}

    def updateBook(self, id, titulo, isbn, data_publicacao, autor_id, categoria_id):
        try:
            data_publicacao_formatada = datetime.strptime(data_publicacao, "%Y-%m-%d").date()
            sucesso = self.livroDAO.updateBook(
                id, titulo, isbn, data_publicacao_formatada, autor_id, categoria_id
            )
            return {"success": sucesso}
        except ValueError as e:
            return {"error": f"Data de publicação inválida ({e})"}
        except Exception as e:
            return {"error": f"Erro ao atualizar livro: {e}"}

    def getBookById(self, id):
        try:
            return self.livroDAO.getBookById(id)
        except Exception as e:
            return {"error": f"Erro ao buscar livro por ID: {e}"}

    def getAutores(self):
        try:
            return self.livroDAO.getAutores()
        except Exception as e:
            return {"error": f"Erro ao buscar autores: {e}"}

    def getCategorias(self):
        try:
            return self.livroDAO.getCategorias()
        except Exception as e:
            return {"error": f"Erro ao buscar categorias: {e}"}

    def deleteBook(self, id):
        try:
            sucesso = self.livroDAO.deleteBook(id)
            return {"success": sucesso}
        except Exception as e:
            return {"error": f"Erro ao excluir livro: {e}"}

    def searchBooksCustom(self, titulo=None, autor_id=None, categoria_id=None, data_inicio=None, isbn=None):
        try:
            livros = self.livroDAO.searchBooksCustom(titulo, autor_id, categoria_id, data_inicio, isbn)
            return [livro.JSonificar() for livro in livros]
        except Exception as e:
            return {"error": f"Erro ao realizar consulta personalizada: {e}"}