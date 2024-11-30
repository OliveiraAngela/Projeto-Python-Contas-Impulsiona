# Gerenciador de Contas

Um sistema simples para gerenciar contas financeiras, permitindo criação, listagem, atualização, exclusão, geração de relatórios e busca de contas. O projeto utiliza o módulo `csv` para armazenamento local dos dados e `reportlab` para geração de relatórios em PDF.

## Funcionalidades

- **Criar Conta**: Adicione uma nova conta ao sistema.
- **Listar Contas**: Exiba todas as contas cadastradas.
- **Atualizar Conta**: Atualize os detalhes de uma conta existente.
- **Deletar Conta**: Remova uma conta específica.
- **Gerar Relatório em PDF**: Crie um relatório financeiro mensal em PDF.
- **Buscar Contas**: Filtre contas por critérios como tipo, categoria e status.
- **Resumo por Categoria**: Visualize totais de débitos e créditos agrupados por categoria.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **CSV**: Armazenamento local das contas.
- **ReportLab**: Geração de relatórios em PDF.

## Estrutura do Projeto

```plaintext
gerenciador_de_contas/
├── contas.csv                # Arquivo de armazenamento das contas
├── main.py                   # Arquivo principal com a lógica do sistema