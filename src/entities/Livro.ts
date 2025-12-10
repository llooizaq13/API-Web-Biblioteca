import { Entity, PrimaryGeneratedColumn, Column } from "typeorm";

@Entity("livros")
export class Livro {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ type: "varchar", length: 255 })
  titulo!: string;

  @Column({ type: "varchar", length: 150 })
  autor!: string;

  @Column({ type: "varchar", length: 20, unique: true })
  isbn!: string;

  @Column({ type: "int" })
  anoPublicacao!: number;

  @Column({ type: "boolean", default: true })
  disponivel!: boolean;
}
