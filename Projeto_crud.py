import mysql.connector

configuracoes = {
    "host": "localhost",
    "user": "root",
    "password": "Mysql102030",
    "database": "loja"
}

def atualizar(comando):
    conexao = mysql.connector.connect(**configuracoes)
    janelinha = conexao.cursor()
    janelinha.execute(comando)
    conexao.commit()
    janelinha.close()
    conexao.close()
    return "Banco atualizado com sucesso"

def visualizar(comando):
    conexao = mysql.connector.connect(**configuracoes)
    janelinha = conexao.cursor()
    janelinha.execute(comando)
    todos_dos_dados = janelinha.fetchall()
    janelinha.close()
    conexao.close()
    return todos_dos_dados

while True:
    menu = int(input("""
    Escolha uma opção:
    1 - Cadastrar novo produto
    2 - Ver todos os produtos
    3 - Editar um produto
    4 - Excluir um produto
    5 - Cadastrar venda
    6 - Ver todas as vendas
    7 - Editar uma venda
    8 - Excluir uma venda
    0 - Sair
"""))

    match menu:
        case 1:
            nome = input("Digite o nome do produto: ")
            descricao = input("Digite a descrição do produto: ")
            qntd_disponivel = int(input("Digite a quantidade disponível do produto: "))
            preco = float(input("Digite o preço do produto: "))
            print(atualizar(f"""
                INSERT INTO produto (nome, descricao, qntd_disponivel, preco) VALUES
                ('{nome}', '{descricao}', {qntd_disponivel}, {preco});
            """))

        case 2:
            todos_produtos = visualizar("SELECT * FROM produto")
            for produto in todos_produtos:
                print(f"""
                ID: {produto[0]}
                Nome: {produto[1]}
                Descrição: {produto[2]}
                Quantidade disponível: {produto[3]}
                Preço: {produto[4]}
                """)

        case 3:
            todos_produtos = visualizar("SELECT * FROM produto")
            for produto in todos_produtos:
                print(f"""
                ID: {produto[0]}
                Nome: {produto[1]}
                Descrição: {produto[2]}
                Quantidade disponível: {produto[3]}
                Preço: {produto[4]}
                """)

            id_editado = int(input("Digite o ID do produto que deseja editar: "))
            produto_selecionado = visualizar(f"SELECT * FROM produto WHERE id = {id_editado};")

            if not produto_selecionado:
                print("Produto não encontrado!")
                continue

            while True:
                submenu = int(input(
                    """Escolha uma opção:
                    1 - Alterar descrição
                    2 - Alterar quantidade disponível
                    3 - Alterar preço
                    4 - Voltar ao menu principal
                    """
                ))
                match submenu:
                    case 1:
                        descricao = input("Digite a nova descrição: ")
                        print(atualizar(f"""
                            UPDATE produto SET descricao = '{descricao}' WHERE id = {id_editado};
                        """))
                    case 2:
                        qntd_disponivel = int(input("Digite a nova quantidade disponível: "))
                        print(atualizar(f"""
                            UPDATE produto SET qntd_disponivel = {qntd_disponivel} WHERE id = {id_editado};
                        """))
                    case 3:
                        preco = float(input("Digite o novo preço: "))
                        print(atualizar(f"""
                            UPDATE produto SET preco = {preco} WHERE id = {id_editado};
                        """))
                break

        case 4:
            todos_os_produtos = visualizar("SELECT * FROM produto")
            produtos_disponiveis = []
            for produto in todos_os_produtos:
                produtos_disponiveis.append(produto[0])
                print(f"""
                ID: {produto[0]}
                Nome: {produto[1]}
                Descrição: {produto[2]}
                """)

            id_excluido = int(input("Digite o ID do produto que você deseja deletar: "))
            if id_excluido in produtos_disponiveis:
                print(atualizar(f"""
                    DELETE FROM produto WHERE id = {id_excluido};
                """))
            else:
                print("Produto não encontrado!")

        case 5:
            todos_produtos = visualizar("SELECT * FROM produto")
            produtos_disponiveis = []
            for produto in todos_produtos:
                produtos_disponiveis.append(produto[0])
                print(f"""
                ID: {produto[0]}
                Nome: {produto[1]}
                Quantidade disponível: {produto[3]}
                """)

            id_produto = int(input("Digite o ID do produto que você deseja vender: "))
            if id_produto in produtos_disponiveis:
                qntd_vendida = float(input("Digite a quantidade vendida: "))
                data_venda = input("Digite a data da venda (YYYY-MM-DD): ")
                qntd_disponivel = visualizar(f"SELECT qntd_disponivel FROM produto WHERE id = {id_produto};")[0][0]
                if qntd_vendida > qntd_disponivel:
                    print("Quantidade vendida excede a disponível!")
                else:
                    print(atualizar(f"""
                        INSERT INTO venda (id_produto, qntd_vendida, data_venda) VALUES ({id_produto}, {qntd_vendida}, '{data_venda}');
                    """))
                    nova_qntd_disponivel = qntd_disponivel - qntd_vendida
                    print(atualizar(f"""
                        UPDATE produto SET qntd_disponivel = {nova_qntd_disponivel} WHERE id = {id_produto};
                    """))
            else:
                print("Produto não encontrado!")

        case 6:
            todas_vendas = visualizar("""
                SELECT venda.id, produto.nome, venda.qntd_vendida, venda.data_venda
                FROM venda
                JOIN produto ON venda.id_produto = produto.id
            """)
            for venda in todas_vendas:
                print(f"""
                ID da Venda: {venda[0]}
                Nome do Produto: {venda[1]}
                Quantidade Vendida: {venda[2]}
                Data da Venda: {venda[3]}
                """)

        case 7:
            todas_vendas = visualizar("""
                SELECT venda.id, produto.nome, venda.qntd_vendida, venda.data_venda
                FROM venda
                JOIN produto ON venda.id_produto = produto.id
            """)
            for venda in todas_vendas:
                print(f"""
                ID da Venda: {venda[0]}
                Nome do Produto: {venda[1]}
                Quantidade Vendida: {venda[2]}
                Data da Venda: {venda[3]}
                """)

            id_venda = int(input("Digite o ID da venda que deseja editar: "))
            venda_selecionada = visualizar(f"SELECT * FROM venda WHERE id = {id_venda};")

            if not venda_selecionada:
                print("Venda não encontrada!")
                continue

            while True:
                submenu = int(input("""
            Escolha o que deseja editar:
            1 - Alterar quantidade vendida
            2 - Alterar data da venda
            0 - Voltar ao menu principal
            """))

                match submenu:
                    case 1:
                        nova_qntd_vendida = float(input("Digite a nova quantidade vendida: "))
                        print(atualizar(f"""
                            UPDATE venda SET qntd_vendida = {nova_qntd_vendida} WHERE id = {id_venda};
                        """))
                    case 2:
                        nova_data_venda = input("Digite a nova data da venda (YYYY-MM-DD): ")
                        print(atualizar(f"""
                            UPDATE venda SET data_venda = '{nova_data_venda}' WHERE id = {id_venda};
                        """))
                    case 0:
                        break
                    case _:
                        print("Opção inválida!")

        case 8:
            todas_vendas = visualizar("""
                SELECT venda.id, produto.nome, venda.qntd_vendida, venda.data_venda
                FROM venda
                JOIN produto ON venda.id_produto = produto.id
            """)
            for venda in todas_vendas:
                print(f"""
                ID da Venda: {venda[0]}
                Nome do Produto: {venda[1]}
                Quantidade Vendida: {venda[2]}
                Data da Venda: {venda[3]}
                """)

            id_venda = int(input("Digite o ID da venda que deseja excluir: "))
            venda_selecionada = visualizar(f"SELECT * FROM venda WHERE id = {id_venda};")

            if not venda_selecionada:
                print("Venda não encontrada!")
                continue

            confirmacao = input("Tem certeza que deseja excluir esta venda? (S/N): ").upper()

            match confirmacao:
                case "S":
                    print(atualizar(f"DELETE FROM venda WHERE id = {id_venda};"))
                    print("Venda excluída com sucesso!")
                case "N":
                    print("Operação de exclusão cancelada.")
                case _:
                    print("Opção inválida!")

        case 0:
            print('Fim do programa')
            break

        case _:
            print('Opção inválida')



