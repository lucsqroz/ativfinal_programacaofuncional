import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# Quantidade de água recomendada por dia
QUANTIDADE_DIARIA = 2000

# Função para gerenciar o consumo de água (closure para manter o estado dos registros)
def criar_gerenciador_agua():
    consumo_diario = []  # Armazena os consumos do dia, com ml e horário

    # Função para adicionar um registro de consumo
    def registrar_consumo(quantidade_ml):
        hora_atual = datetime.now()
        consumo_diario.append({'quantidade': quantidade_ml, 'hora': hora_atual})
        return sum([registro['quantidade'] for registro in consumo_diario])

    # Função para listar todos os registros de consumo
    def obter_registros():
        return consumo_diario

    # Função para gerar um resumo diário do consumo
    def gerar_resumo():
        total_consumido = sum([registro['quantidade'] for registro in consumo_diario])
        restante = QUANTIDADE_DIARIA - total_consumido
        return {"total_consumido": total_consumido, "restante": max(restante, 0)}

    return registrar_consumo, obter_registros, gerar_resumo

# Função lambda para filtrar os consumos das últimas 24 horas
filtrar_consumo_24h = lambda registros: [registro for registro in registros if registro['hora'] >= datetime.now() - timedelta(hours=24)]

# Função para exibir a quantidade e horário de consumo
def exibir_registros(registros):
    return [f"{registro['quantidade']}ml | {registro['hora'].strftime('%H:%M:%S')}" for registro in registros]

# Criando o gerenciador de água
registrar, listar_registros, resumo_diario = criar_gerenciador_agua()

# Variável global para controlar a exibição dos consumos
mostrar_consumos = False

# Funções para a interface gráfica
def atualizar_interface():
    total_atual = registrar(int(entrada_ml.get()))
    percentual_progresso = (total_atual / QUANTIDADE_DIARIA) * 100
    percentual_progresso = min(percentual_progresso, 100)  # Limita a barra em 100%
    barra_progresso['value'] = percentual_progresso
    rotulo_resumo.config(text=f"Total consumido: {total_atual} ml\nRestante: {QUANTIDADE_DIARIA - total_atual} ml")
    entrada_ml.delete(0, tk.END)  # Limpa o campo de entrada

def alternar_visibilidade_consumos():
    global mostrar_consumos
    mostrar_consumos = not mostrar_consumos  # Alterna entre exibir e ocultar

    if mostrar_consumos:
        registros = listar_registros()
        registros_recentes = filtrar_consumo_24h(registros)  # Usando o lambda para filtrar as últimas 24h
        exibir_recentes = exibir_registros(registros_recentes)
        rotulo_registros.config(text="Consumo recente (ml | hora):\n" + "\n".join(exibir_recentes))
        botao_ver_consumos.config(text="Ocultar últimos consumos")
    else:
        rotulo_registros.config(text="")
        botao_ver_consumos.config(text="Ver últimos consumos")

# Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Controle de Consumo de Água")
janela.geometry("300x400")

# Instrução ao usuário
rotulo_instrucoes = tk.Label(janela, text="Informe o consumo de água (ml):")
rotulo_instrucoes.pack(pady=5)

# Entrada para o consumo de água
entrada_ml = tk.Entry(janela)
entrada_ml.pack(pady=5)

# Botão para adicionar o consumo
botao_registrar = tk.Button(janela, text="Registrar", command=atualizar_interface)
botao_registrar.pack(pady=5)

# Barra de progresso para visualizar o consumo de água
barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=200, mode="determinate")
barra_progresso.pack(pady=10)

# Exibição do resumo do consumo
rotulo_resumo = tk.Label(janela, text="Total consumido: 0 ml\nRestante: 2000 ml")
rotulo_resumo.pack(pady=5)

# Botão para alternar visibilidade dos consumos recentes
botao_ver_consumos = tk.Button(janela, text="Ver últimos consumos", command=alternar_visibilidade_consumos)
botao_ver_consumos.pack(pady=5)

# Exibição dos horários de consumo (inicialmente oculto)
rotulo_registros = tk.Label(janela, text="")
rotulo_registros.pack(pady=5)

# Configurações da barra de progresso (em azul)
estilo = ttk.Style()
estilo.theme_use('default')
estilo.configure("TProgressbar", thickness=20, troughcolor='white', background='blue')

# Loop principal da interface gráfica
janela.mainloop()
