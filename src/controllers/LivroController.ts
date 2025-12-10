import { Request, Response } from "express";
import { LivroRepository, livroRepositoryInstance } from "../repositories/LivroRepository";
import { Livro } from "../entities/Livro";

const repository: LivroRepository = livroRepositoryInstance;

export class LivroController {
  async criar(req: Request, res: Response): Promise<Response> {
    const { titulo, autor, isbn, anoPublicacao, disponivel } = req.body;

    if (!titulo || !autor || !isbn || !anoPublicacao) {
      return res.status(400).json({
        mensagem: "Todos os campos obrigatórios (titulo, autor, isbn, anoPublicacao) devem ser fornecidos.",
      });
    }

    try {
      const novoLivro: Partial<Livro> = {
        titulo,
        autor,
        isbn,
        anoPublicacao: Number(anoPublicacao),
        disponivel: disponivel ?? true,
      };

      const livroSalvo = await repository.criar(novoLivro);
      return res.status(201).json(livroSalvo);
    } catch (error: any) {
      if (error.code === "SQLITE_CONSTRAINT") {
        return res.status(409).json({ mensagem: "ISBN já cadastrado.", erro: error.message });
      }
      return res.status(500).json({ mensagem: "Erro ao cadastrar o livro.", erro: error.message });
    }
  }

  async buscarTodos(req: Request, res: Response): Promise<Response> {
    try {
      const livros = await repository.buscarTodos();
      return res.status(200).json(livros);
    } catch (error: any) {
      return res.status(500).json({ mensagem: "Erro ao buscar a lista de livros.", erro: error.message });
    }
  }

  async buscarPorId(req: Request, res: Response): Promise<Response> {
    const id = Number(req.params.id);

    if (isNaN(id)) {
      return res.status(400).json({ mensagem: "O ID deve ser um número válido." });
    }

    try {
      const livro = await repository.buscarPorId(id);

      if (!livro) {
        return res.status(404).json({ mensagem: "Livro não encontrado." });
      }

      return res.status(200).json(livro);
    } catch (error: any) {
      return res.status(500).json({ mensagem: "Erro ao buscar o livro.", erro: error.message });
    }
  }

  async atualizar(req: Request, res: Response): Promise<Response> {
    const id = Number(req.params.id);
    const dadosAtualizados: Partial<Livro> = req.body;

    if (isNaN(id)) {
      return res.status(400).json({ mensagem: "O ID deve ser um número válido." });
    }

    if (dadosAtualizados.anoPublicacao !== undefined) {
      dadosAtualizados.anoPublicacao = Number(dadosAtualizados.anoPublicacao);
      if (isNaN(dadosAtualizados.anoPublicacao)) {
        return res.status(400).json({ mensagem: "O anoPublicacao deve ser um número válido." });
      }
    }

    try {
      const livroAtualizado = await repository.atualizar(id, dadosAtualizados);

      if (!livroAtualizado) {
        return res.status(404).json({ mensagem: "Livro não encontrado para atualização." });
      }

      return res.status(200).json(livroAtualizado);
    } catch (error: any) {
      if (error.code === "SQLITE_CONSTRAINT") {
        return res.status(409).json({ mensagem: "ISBN já cadastrado.", erro: error.message });
      }
      return res.status(500).json({ mensagem: "Erro ao atualizar o livro.", erro: error.message });
    }
  }

  async excluir(req: Request, res: Response): Promise<Response> {
    const id = Number(req.params.id);

    if (isNaN(id)) {
      return res.status(400).json({ mensagem: "O ID deve ser um número válido." });
    }

    try {
      const foiExcluido = await repository.excluir(id);

      if (!foiExcluido) {
        return res.status(404).json({ mensagem: "Livro não encontrado para exclusão." });
      }

      return res.status(204).send();
    } catch (error: any) {
      return res.status(500).json({ mensagem: "Erro ao excluir o livro.", erro: error.message });
    }
  }
}

export const livroControllerInstance = new LivroController();
