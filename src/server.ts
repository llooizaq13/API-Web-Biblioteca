import "reflect-metadata";
import express from "express";
import { initializeDatabase } from "./config/database";
import livroRoutes from "./routes/livroRoutes";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.use("/api/livros", livroRoutes);

initializeDatabase()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`🚀 Servidor Express rodando na porta ${PORT}`);
      console.log(`Acesse: http://localhost:${PORT}/api/livros`);
    });
  })
  .catch((error) => {
    console.error("Falha ao iniciar a aplicação devido a erro no BD:", error);
  });
