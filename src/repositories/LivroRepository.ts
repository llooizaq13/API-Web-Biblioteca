import { AppDataSource } from "../config/database";
import { Livro } from "../entities/Livro";
import { Repository } from "typeorm";

const livroRepository: Repository<Livro> = AppDataSource.getRepository(Livro);

export class LivroRepository {
  async criar(livro: Partial<Livro>): Promise<Livro> {
    return livroRepository.save(livro as Livro);
  }

  async buscarTodos(): Promise<Livro[]> {
    return livroRepository.find();
  }

  async buscarPorId(id: number): Promise<Livro | null> {
    return livroRepository.findOneBy({ id });
  }

  async atualizar(id: number, dadosAtualizados: Partial<Livro>): Promise<Livro | null> {
    const livro = await this.buscarPorId(id);
    if (!livro) {
      return null;
    }

    const livroAtualizado = livroRepository.merge(livro, dadosAtualizados);
    return livroRepository.save(livroAtualizado);
  }

  async excluir(id: number): Promise<boolean> {
    const resultado = await livroRepository.delete(id);
    return resultado.affected! > 0;
  }
}

export const livroRepositoryInstance = new LivroRepository();
