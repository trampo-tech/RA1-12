def exibirResultados(resultados: list) -> None:
    print("RESULTADOS")
 
    if not resultados:
        print("Nenhum resultado para exibir.")
        return
 
    for i, valor in enumerate(resultados):
        if valor == int(valor):
            valor_fmt = f"{int(valor)}"
        else:
            valor_fmt = f"{valor:.6f}"
        print(f"Linha {i + 1:>3}: {valor_fmt}")
 
    print(f"Total de expressoes avaliadas: {len(resultados)}")

# Falta:
# Alertar se o arquivo tiver linhas malformadas ou exceder limites.
# Implementar e gerenciar a interface no main, incluindo leitura do argumento de linha de comando;
# Corrigir problemas de entrada
# Criar funcoes de teste para validar a saida e o comportamento do programa completo