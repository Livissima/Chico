# app/auto/tasks/siap/frequenciador/prof/constantes.py
from selenium.webdriver.common.by import By

MÊS = 'Maio'
BIMESTRE = '2'

# Seletores da Tabela de Disciplinas
SELETOR_TABELA_UPDATE = (By.ID, 'cphFuncionalidade_UpdatePanel1')
SELETOR_CORPO_TABELA = (By.TAG_NAME, 'tbody')
SELETOR_LINHAS_GERAIS = (By.TAG_NAME, 'tr')

# Seletores do Calendário
SELETOR_CALENDÁRIO_ITERÁVEIS = (By.ID, 'cphFuncionalidade_cphCampos_CalendarioMensal')
SELETOR_TABELA = (By.TAG_NAME, 'table')
SELETOR_TD = (By.TAG_NAME, 'td')

