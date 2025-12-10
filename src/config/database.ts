import { DataSource } from "typeorm";
import { Livro } from "../entities/Livro";

export const AppDataSource = new DataSource({
  type: "sqlite",
  database: "biblioteca.sqlite",
  synchronize: true,
  logging: false,
  entities: [Livro],
  migrations: [],
  subscribers: [],
});

export const initializeDatabase = async () => {
  try {
    await AppDataSource.initialize();
    console.log("Conexão com o banco de dados estabelecida com sucesso!");
  } catch (error) {
    console.error("Erro durante a inicialização do banco de dados:", error);
    throw error;
  }
};
