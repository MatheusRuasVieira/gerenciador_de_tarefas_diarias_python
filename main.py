import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

class GerenciadorDeTarefa:
    def __init__(self, nome_arquivo='tarefas.json'):
        self.tarefas = []
        self.path_tarefas = Path(nome_arquivo)
        print(f"-------INICIANDO GERENCIADOR DE TAREFAS-------")

    def salvar(self):
        print(f"Salvando arquivos...")
        with open(self.path_tarefas, 'w', encoding='utf-8') as f:
            json.dump(self.tarefas, f, indent=4)
        print(f"{len(self.tarefas)} tarefas salvas com sucesso!")

    def resetar_tarefas(self):
        self.tarefas = []
        self.salvar()
        print(f"Todas as tarefas foram apagadas com sucesso!")

    def carregar_tarefas(self):
        if self.path_tarefas.exists():
            print(f"Arquivo encontrado! Carregando tarefas...")
            with open(self.path_tarefas, 'r', encoding='utf-8') as f:
                self.tarefas = json.load(f)
        else:
            print(f"Nenhum arquivo foi encontrado")
            self.salvar()

    def adicionar_tarefas(self, descricao_tarefa):
        for tarefa in self.tarefas:
            if tarefa["descricao"].strip().lower() == descricao_tarefa.strip().lower():
                messagebox.showwarning("Aviso", "Essa tarefa já existe!")
                return False

        nova_tarefa = {"descricao": descricao_tarefa, "concluida": False}
        self.tarefas.append(nova_tarefa)
        self.salvar()
        return True

    def concluir_tarefa(self, descricao):
        for tarefa in self.tarefas:
            if tarefa["descricao"] == descricao:
                tarefa["concluida"] = True
                self.salvar()
                return True
        return False

    def excluir_tarefa(self, descricao):
        self.tarefas = [t for t in self.tarefas if t["descricao"] != descricao]
        self.salvar()

# --- Inicialização ---
gerenciador = GerenciadorDeTarefa()
gerenciador.carregar_tarefas()

# --- Funções da Interface ---
def adicionar_tarefa_gui():
    descricao = text_descricao.get()
    if descricao:
        if gerenciador.adicionar_tarefas(descricao):  # agora retorna True/False
            atualizar_lista_tarefas()
            text_descricao.delete(0, tk.END)
            print(f"Tarefa '{descricao}' adicionada com sucesso!")

def atualizar_lista_tarefas():
    for item in lista_tarefas.get_children():
        lista_tarefas.delete(item)

    for tarefa in gerenciador.tarefas:
        status = "Concluída" if tarefa['concluida'] else "Pendente"
        tag = "concluida" if tarefa['concluida'] else "pendente"  # <-- ADICIONADO tags
        lista_tarefas.insert('', tk.END, values=(tarefa['descricao'], status), tags=(tag,))

# --- ADICIONADO: Função para concluir tarefa selecionada
def concluir_tarefa_gui():
    item_selecionado = lista_tarefas.selection()
    if item_selecionado:
        descricao = lista_tarefas.item(item_selecionado, "values")[0]
        if gerenciador.concluir_tarefa(descricao):
            atualizar_lista_tarefas()

# --- ADICIONADO: Função para excluir tarefa selecionada
def excluir_tarefa_gui():
    item_selecionado = lista_tarefas.selection()
    if item_selecionado:
        descricao = lista_tarefas.item(item_selecionado, "values")[0]
        gerenciador.excluir_tarefa(descricao)
        atualizar_lista_tarefas()

# --- Configuração da Janela ---
janela = tk.Tk()
janela.title("Gerenciador de Tarefas Diárias")
janela.geometry("600x800")
janela.resizable(False, False)

# --- Entrada ---
frame_entrada = tk.Frame(janela)
frame_entrada.pack(pady=10)

text_descricao = tk.Entry(frame_entrada, font=("Arial", 12), width=30)
text_descricao.pack(side='left', pady=5)

add_button = tk.Button(frame_entrada, text='ADICIONAR', command=adicionar_tarefa_gui)
add_button.pack(side='left', padx=5)

# --- Botões de Concluir e Excluir (ADICIONADOS) ---
btn_concluir = tk.Button(frame_entrada, text='CONCLUIR', command=concluir_tarefa_gui)
btn_concluir.pack(side='left', padx=5)

btn_excluir = tk.Button(frame_entrada, text='EXCLUIR', command=excluir_tarefa_gui)
btn_excluir.pack(side='left', padx=5)

# --- Lista ---
frame_lista_tarefas = tk.Frame(janela)
frame_lista_tarefas.pack(pady=5, padx=10, fill='both', expand=True)

colunas = ('descricao', 'status')
lista_tarefas = ttk.Treeview(frame_lista_tarefas, columns=colunas, show='headings')

lista_tarefas.heading('descricao', text='Descrição da tarefa')
lista_tarefas.heading('status', text='Status')
lista_tarefas.column('descricao', width=250, anchor='w')
lista_tarefas.column('status', width=250, anchor='center')

# --- ADICIONADO: Cores para indicar status ---
lista_tarefas.tag_configure("concluida", background="#c6f7d0")  # verde claro
lista_tarefas.tag_configure("pendente", background="#f7d0d0")   # vermelho claro

lista_tarefas.pack(side='left', fill='both', expand=True)

# Barra de Rolagem
scrollbar = ttk.Scrollbar(frame_lista_tarefas, orient='vertical', command=lista_tarefas.yview)
lista_tarefas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')

# --- Inicializa a lista ---
atualizar_lista_tarefas()
janela.mainloop()
