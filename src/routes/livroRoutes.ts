import { Router } from "express";
import { livroControllerInstance } from "../controllers/LivroController";

const router = Router();
const controller = livroControllerInstance;

router.post("/", (req, res) => controller.criar(req, res));
router.get("/", (req, res) => controller.buscarTodos(req, res));
router.get("/:id", (req, res) => controller.buscarPorId(req, res));
router.put("/:id", (req, res) => controller.atualizar(req, res));
router.delete("/:id", (req, res) => controller.excluir(req, res));

export default router;
