import sys
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QTextEdit, QTableWidget, QTableWidgetItem  
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt

import pymysql
from datetime import datetime

def obter_cor_por_materia(materia):
    if materia == 'Robótica':
        return 'red'
    elif materia == 'Programação':
        return 'blue'
    elif materia == 'Português':
        return 'green'
    elif materia == 'Matemática':
        return 'orange'
    else:
        return 'black'  # Cor padrão para outras matérias


#Classe padronizando resultado de pesquisa
class ResultadosPesquisaDialog(QDialog):
    def __init__(self, resultados):
        super().__init__()
        self.setWindowTitle("Resultado da Pesquisa")
        # Defina a largura e altura desejadas para a janela de resultados
        self.setFixedSize(800, 400)  
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        table_widget = QTableWidget()
        table_widget.setColumnCount(5)
        table_widget.setHorizontalHeaderLabels(["Nome do Aluno", "Data", "Aula Efetuada", "Matéria", "Informações Adicionais"])
        table_widget.setRowCount(len(resultados))

        for i, resultado in enumerate(resultados):
            nome_aluno = QTableWidgetItem(resultado[1])
            data = QTableWidgetItem(str(resultado[2]))
            aula_efetuada = QTableWidgetItem(resultado[3])
            materia = QTableWidgetItem(resultado[4])
            informacoes_adicionais = QTableWidgetItem(resultado[5])

            table_widget.setItem(i, 0, nome_aluno)
            table_widget.setItem(i, 1, data)
            table_widget.setItem(i, 2, aula_efetuada)
            table_widget.setItem(i, 3, materia)
            table_widget.setItem(i, 4, informacoes_adicionais)
            
            # Obtenha a cor da linha com base na matéria
            cor_linha = obter_cor_por_materia(resultado[4])
            
            # Defina o estilo da linha
            for col in range(table_widget.columnCount()):
                item = table_widget.item(i, col)
                item.setForeground(QColor(cor_linha))

        self.layout.addWidget(table_widget)



# Função para converter a data de DD/MM/AAAA para AAAA-MM-DD
def converter_data(data):
    data_objeto = datetime.strptime(data, "%d/%m/%Y")
    data_convertida = data_objeto.strftime("%Y-%m-%d")
    return data_convertida


# Função para adicionar aula
def adicionar_aula():
    nome_aluno = entry_nome_aluno.text()
    data = converter_data(entry_data.text())
    aula_efetuada = entry_aula_efetuada.text()
    materia = combobox_materia.currentText()
    informacoes_adicionais = entry_informacoes_adicionais.text()

    if not nome_aluno or not data or not aula_efetuada or not materia:
        # Exibe a caixa de diálogo informando o campo que está faltando
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Preencha todos os campos antes de adicionar uma aula.")
        msg_box.setWindowTitle("Campos em branco")
        msg_box.exec_()


    else:
        query = "INSERT INTO teste_aluno (nome_aluno, data, aula_efetuada, materia, informacoes_adicionais) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome_aluno, data, aula_efetuada, materia, informacoes_adicionais)

        cursor.execute(query, valores)
        conexao.commit()

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Aula adicionada com sucesso!")
        msg_box.setWindowTitle("Sucesso")
        msg_box.exec_()

        # Obtém o valor atual do campo de entrada de data
        data_atual = entry_data.text()

        # Limpa os campos preenchidos
        entry_nome_aluno.clear()
        entry_data.clear()
        entry_aula_efetuada.clear()
        #entry_materia.clear()
        entry_informacoes_adicionais.clear()

        # Define o valor anterior da data atual no campo de entrada de data
        entry_data.setText(data_atual)




# Função para pesquisar aula por data
def pesquisar_por_data():

    data_input = entry_pesquisar_data.text()

    if not data_input:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Por favor, informe uma data para pesquisar.")
        msg_box.setWindowTitle("Alerta")
        msg_box.exec_()
        return

    data_pesquisa = converter_data(data_input)

    # Restante do código...


    query = "SELECT * FROM teste_aluno WHERE data = %s"
    valores = (data_pesquisa,)

    cursor.execute(query, valores)
    resultados = cursor.fetchall()

    if not resultados:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Nenhuma aula encontrada para a data informada.")
        msg_box.setWindowTitle("Alerta")
        msg_box.exec_()
    else:
        dialog = ResultadosPesquisaDialog(resultados)
        dialog.exec_()


# Função para pesquisar aula por nome de aluno
def pesquisar_por_nome_aluno():
    nome_aluno_pesquisa = entry_pesquisar_nome_aluno.text()

    query = "SELECT * FROM teste_aluno WHERE nome_aluno = %s"
    valores = (nome_aluno_pesquisa,)

    cursor.execute(query, valores)
    resultados = cursor.fetchall()

    if not resultados:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Sem Resultado! Digite um nome válido!")
        msg_box.setWindowTitle("Pesquisa")
        msg_box.exec_()
    else:
        dialog = ResultadosPesquisaDialog(resultados)
        dialog.exec_()


# Função para pesquisar aula por matéria
def pesquisar_por_materia():
    materia_pesquisa = entry_pesquisar_materia.text()
    query = "SELECT * FROM teste_aluno WHERE materia = %s"
    valores = (materia_pesquisa,)

    cursor.execute(query, valores)
    resultados = cursor.fetchall()

    if not resultados:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Sem resultado! Digite uma matéria válida!")
        msg_box.setWindowTitle("Pesquisa")
        msg_box.exec_()
        return
    else:
        dialog = ResultadosPesquisaDialog(resultados)
        dialog.exec_()


# Função para excluir aula
def excluir_aula():
    nome_aluno = entry_excluir_nome_aluno.text()
    data_input = entry_excluir_data.text()

    if not nome_aluno or not data_input:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Preencha todos os campos.")
        msg_box.setWindowTitle("Exclusão")
        msg_box.exec_()
        return

    data_pesquisa = converter_data(data_input)
    print(data_pesquisa)
    query = "DELETE FROM teste_aluno WHERE nome_aluno = %s AND data = %s"
    valores = (nome_aluno, data_pesquisa)

    cursor.execute(query, valores)
    conexao.commit()

    if cursor.rowcount > 0:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Aula removida com sucesso!")
        msg_box.setWindowTitle("Exclusão")
        msg_box.exec_()
    else:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Nenhuma aula encontrada para o nome do aluno e data informados.")
        msg_box.setWindowTitle("Exclusão")
        msg_box.exec_()


app = QApplication(sys.argv)
# Criação da janela principal
window = QWidget()
window.setWindowTitle("Controle de Aulas")
window.setGeometry(100, 100, 400, 300)
window.setStyleSheet("background-color: rgb(0, 184, 234);")

# Carregamento da logo
logo_icon = QIcon("C:/Users/Ensin/PycharmProjects/Projeto_RegistroAlunos/imagens/ensina-mais.png")

# Exibição da logo em um QLabel
logo_label = QLabel()
logo_label.setPixmap(logo_icon.pixmap(200, 200))
logo_label.setAlignment(Qt.AlignCenter)

# Layout da janela
layout = QVBoxLayout()
layout.addWidget(logo_label)
window.setLayout(layout)

# Adicionar aula
label_nome_aluno = QLabel("Nome do Aluno:")
label_nome_aluno.setStyleSheet("color: black; font-weight: bold;")
entry_nome_aluno = QLineEdit()
entry_nome_aluno.setStyleSheet("background-color: white")

label_data = QLabel("Data (DD/MM/AAAA):")
label_data.setStyleSheet("color: black; font-weight: bold;")
entry_data = QLineEdit()
entry_data.setStyleSheet("background-color: white")
entry_data.setText(datetime.now().strftime("%d/%m/%Y"))  # Define o campo Data com a data atual

label_aula_efetuada = QLabel("Aula Efetuada:")
label_aula_efetuada.setStyleSheet("color: black; font-weight: bold;")
entry_aula_efetuada = QLineEdit()
entry_aula_efetuada.setStyleSheet("background-color: white")

label_materia = QLabel("Matéria:")
label_materia.setStyleSheet("color: black; font-weight: bold;")

# Criação do combobox de matéria
combobox_materia = QComboBox()
combobox_materia.addItem("Robótica")
combobox_materia.addItem("Programação")
combobox_materia.addItem("Português")
combobox_materia.addItem("Matemática")
combobox_materia.setStyleSheet("background-color: white;")

label_informacoes_adicionais = QLabel("Informações Adicionais:")
label_informacoes_adicionais.setStyleSheet("color: black; font-weight: bold;")
entry_informacoes_adicionais = QLineEdit()
entry_informacoes_adicionais.setStyleSheet("background-color: white")

button_adicionar_aula = QPushButton("Adicionar Aula")
button_adicionar_aula.clicked.connect(adicionar_aula)
button_adicionar_aula.setStyleSheet("background-color: light gray; color: black; font-weight: bold;")

# Pesquisar por data
label_pesquisar_data = QLabel("Pesquisar por Data (DD/MM/AAAA):")
label_pesquisar_data.setStyleSheet("color: black; font-weight: bold;")
entry_pesquisar_data = QLineEdit()
entry_pesquisar_data.setStyleSheet("background-color: white")

button_pesquisar_data = QPushButton("Pesquisar por Data")
button_pesquisar_data.clicked.connect(pesquisar_por_data)
button_pesquisar_data.setStyleSheet("background-color: light gray; color: black; font-weight: bold;")

# Pesquisar por nome de aluno
label_pesquisar_nome_aluno = QLabel("Pesquisar por Nome do Aluno:")
label_pesquisar_nome_aluno.setStyleSheet("color: black; font-weight: bold;")
entry_pesquisar_nome_aluno = QLineEdit()
entry_pesquisar_nome_aluno.setStyleSheet("background-color: white")

button_pesquisar_nome_aluno = QPushButton("Pesquisar por Nome do Aluno")
button_pesquisar_nome_aluno.clicked.connect(pesquisar_por_nome_aluno)
button_pesquisar_nome_aluno.setStyleSheet("background-color: light gray; color: black; font-weight: bold;")

# Pesquisar por matéria
label_pesquisar_materia = QLabel("Pesquisar por Matéria:")
label_pesquisar_materia.setStyleSheet("color: black; font-weight: bold;")
entry_pesquisar_materia = QLineEdit()
entry_pesquisar_materia.setStyleSheet("background-color: white")

button_pesquisar_materia = QPushButton("Pesquisar por Matéria")
button_pesquisar_materia.clicked.connect(pesquisar_por_materia)
button_pesquisar_materia.setStyleSheet("background-color: light gray; color: black; font-weight: bold;")

# Excluir aula
label_excluir_nome_aluno = QLabel("Nome do Aluno:")
label_excluir_nome_aluno.setStyleSheet("color: black; font-weight: bold;")
entry_excluir_nome_aluno = QLineEdit()
entry_excluir_nome_aluno.setStyleSheet("background-color: white")

label_excluir_data = QLabel("Data (DD/MM/AAAA):")
label_excluir_data.setStyleSheet("color: black; font-weight: bold;")
entry_excluir_data = QLineEdit()
entry_excluir_data.setStyleSheet("background-color: white")

button_excluir_aula = QPushButton("Excluir Aula")
button_excluir_aula.clicked.connect(excluir_aula)
button_excluir_aula.setStyleSheet("background-color: light gray; color: black; font-weight: bold;")

# Adicionando widgets ao layout
layout.addWidget(logo_label)

layout.addWidget(label_nome_aluno)
layout.addWidget(entry_nome_aluno)

layout.addWidget(label_data)
layout.addWidget(entry_data)

layout.addWidget(label_aula_efetuada)
layout.addWidget(entry_aula_efetuada)

layout.addWidget(label_materia)
layout.addWidget(combobox_materia)  # Adicionando o combobox de matéria

layout.addWidget(label_informacoes_adicionais)
layout.addWidget(entry_informacoes_adicionais)

layout.addWidget(button_adicionar_aula)

layout.addWidget(label_pesquisar_data)
layout.addWidget(entry_pesquisar_data)

layout.addWidget(button_pesquisar_data)

layout.addWidget(label_pesquisar_nome_aluno)
layout.addWidget(entry_pesquisar_nome_aluno)

layout.addWidget(button_pesquisar_nome_aluno)

layout.addWidget(label_pesquisar_materia)
layout.addWidget(entry_pesquisar_materia)

layout.addWidget(button_pesquisar_materia)

layout.addWidget(label_excluir_nome_aluno)
layout.addWidget(entry_excluir_nome_aluno)

layout.addWidget(label_excluir_data)
layout.addWidget(entry_excluir_data)

layout.addWidget(button_excluir_aula)

# Conexão com o banco de dados MySQL
conexao = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="pedro"
)

cursor = conexao.cursor()

# Exibição da janela
window.show()
sys.exit(app.exec_())

# Fechar a conexão com o banco de dados
conexao.close()