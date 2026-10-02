# from app.core.funcionalidades.matrícula.funções import render_html_template
# from rótulos import *
# import streamlit as st
# import streamlit.components.v1 as components
#
#
# # Configuração da página Streamlit
# st.set_page_config(page_title="Nova Matrícula", page_icon="📝", layout="wide")
#
# st.title("📝 Preenchimento da Ficha de Matrícula")
# st.write("Preencha os campos abaixo. A ficha HTML será atualizada e gerada automaticamente ao final.")
#
#
#
# # ---------------------------------------------------------
# # FORMULÁRIO STREAMLIT
# # ---------------------------------------------------------
# with st.form(key="form_matricula") :
#     # --- 1. DADOS PESSOAIS ---
#     st.subheader("1. Dados Pessoais")
#     c1, c2, c3 = st.columns([3, 1, 1])
#     nome_estudante = c1.text_input(NOME_ESTUDANTE)
#     data_nascimento = c2.text_input(DATA_NASCIMENTO)
#     genero = c3.selectbox(GÊNERO, ["", "Masculino", "Feminino"])
#
#     c4, c5, c6 = st.columns([2, 2, 1])
#     nome_social = c4.text_input(NOME_SOCIAL)
#     cpf_estudante = c5.text_input(CPF_ESTUDANTE)
#     uf_naturalidade = c6.text_input(UF_NATURALIDADE)
#
#     c7, c8, c9, c10 = st.columns([2, 1, 1, 1])
#     municipio_naturalidade = c7.text_input(MUNICÍPIO_NATURALIDADE)
#     termo_cert_nasc = c8.text_input(TERMO_CN)
#     livro = c9.text_input(LIVRO_CN)
#     folha = c10.text_input(FOLHA)
#
#     c11, c12, c13 = st.columns([1, 2, 2])
#     dt_emissao_cn = c11.text_input(DATA_EMISSÃO_CN)
#     cartorio_registro = c12.text_input(CARTÓRIO_REGISTRO)
#     municipio_registro = c13.text_input(MUNICÍPIO_REGISTRO)
#
#     col_cor, col_rel = st.columns(2)
#     cor_etnia = col_cor.selectbox(ETNIA, ["", "Branca", "Preta", "Parda", "Indígena", "Amarela", "Não declarada"])
#     religiao = col_rel.selectbox(RELIGIÃO,
#         ["", "Budismo", "Catolicismo", "Evangelismo", "Congregação", "Espírita", "Sem religião"])
#
#     st.markdown("**Tamanhos de Uniforme**")
#     u1, u2, u3, u4, u5 = st.columns(5)
#     tam_bermuda = u1.text_input(BERMUDA)
#     tam_camiseta = u2.text_input(CAMISETA)
#     tam_calca = u3.text_input(CALÇA)
#     tam_jaqueta = u4.text_input(JAQUETA)
#     tam_tenis = u5.text_input(TÊNIS)
#
#     st.divider()
#
#     # --- 2. DADOS FAMILIARES ---
#     st.subheader("2. Dados Familiares")
#
#     st.markdown("##### Filiação 1")
#     f1_col1, f1_col2, f1_col3 = st.columns([3, 1, 1])
#     filiacao1_nome = f1_col1.text_input(FILIAÇÃO1_NOME)
#     filiacao1_dn = f1_col2.text_input(FILIAÇÃO1_DN)
#     filiacao1_falecida = f1_col3.radio(FILIAÇÃO1_FALECIDA, ["Não", "Sim"], horizontal=True, key="f1_fal")
#
#     f1_c4, f1_c5, f1_c6, f1_c7, f1_c8 = st.columns([2, 2, 1, 1, 1])
#     filiacao1_cpf = f1_c4.text_input(FILIAÇÃO1_CPF)
#     filiacao1_titulo = f1_c5.text_input(FILIAÇÃO1_TÍTULO)
#     filiacao1_uf = f1_c6.text_input(FILIAÇÃO1_UF_ELEITORAL)
#     filiacao1_zona = f1_c7.text_input(FILIAÇÃO1_ZONA)
#     filiacao1_secao = f1_c8.text_input(FILIAÇÃO1_SEÇÃO)
#     filiacao1_profissao = st.text_input(FILIAÇÃO1_PROFISSÃO)
#
#     st.markdown("##### Filiação 2")
#     f2_col1, f2_col2, f2_col3 = st.columns([3, 1, 1])
#     filiacao2_nome = f2_col1.text_input(FILIAÇÃO2_NOME)
#     filiacao2_dn = f2_col2.text_input(FILIAÇÃO2_DN)
#     filiacao2_falecido = f2_col3.radio(FILIAÇÃO2_FALECIDA, ["Não", "Sim"], horizontal=True, key="f2_fal")
#
#     f2_c4, f2_c5, f2_c6, f2_c7, f2_c8 = st.columns([2, 2, 1, 1, 1])
#     filiacao2_cpf = f2_c4.text_input(FILIAÇÃO2_CPF)
#     filiacao2_titulo = f2_c5.text_input(FILIAÇÃO2_TÍTULO)
#     filiacao2_uf = f2_c6.text_input(FILIAÇÃO2_UF_ELEITORAL)
#     filiacao2_zona = f2_c7.text_input(FILIAÇÃO2_ZONA)
#     filiacao2_secao = f2_c8.text_input(FILIAÇÃO2_SEÇÃO)
#     filiacao2_profissao = st.text_input(FILIAÇÃO2_PROFISSÃO)
#
#     st.markdown("##### Responsável Legal")
#     resp_col1, resp_col2 = st.columns([3, 1])
#     responsavel_nome = resp_col1.text_input(RESPONSÁVEL_NOME)
#     responsavel_dn = resp_col2.text_input(RESPONSÁVEL_DN)
#
#     resp_c4, resp_c5, resp_c6, resp_c7, resp_c8 = st.columns([2, 2, 1, 1, 1])
#     responsavel_cpf = resp_c4.text_input(RESPONSÁVEL_CPF)
#     responsavel_titulo = resp_c5.text_input(RESPONSÁVEL_TÍTULO)
#     responsavel_uf = resp_c6.text_input(RESPONSÁVEL_UF)
#     responsavel_zona = resp_c7.text_input(RESPONSÁVEL_ZONA)
#     responsavel_secao = resp_c8.text_input(RESPONSÁVEL_SEÇÃO)
#
#     r_p, r_r = st.columns([2, 2])
#     responsavel_profissao = r_p.text_input(RESPONSÁVEL_PROFISSÃO)
#     responsavel_relacao = r_r.text_input(RESPONSÁVEL_VÍNCULO)
#
#     st.markdown("##### Núcleo Familiar")
#     nucleo_opcoes = st.multiselect(NÚCLEO_OPÇÕES,
#         ["Mãe", "Pai", "Irmãos", "Madrasta", "Tutor Legal", "Tios", "Avós", "Primos", "Padrasto", "Outros"])
#     nuc_outros_texto = ""
#     if NÚCLEO_OUTROS in nucleo_opcoes :
#         nuc_outros_texto = st.text_input(NÚCLEO_OUTROS_INPUT)
#
#     st.divider()
#
#     # --- 3. ENDEREÇO E CONTATO ---
#     st.subheader("3. Endereço e Contato")
#     e1, e2, e3, e4, e5 = st.columns([3, 1, 1, 1, 2])
#     logradouro = e1.text_input(LOGRADOURO)
#     quadra = e2.text_input(QUADRA)
#     lote = e3.text_input(LOTE)
#     numero = e4.text_input(NÚMERO)
#     cep = e5.text_input(CEP)
#
#     e6, e7, e8 = st.columns([2, 2, 2])
#     complemento = e6.text_input(COMPLEMENTO)
#     bairro = e7.text_input(BAIRRO)
#     municipio = e8.text_input(MUNICÍPIO)
#
#     ct1, ct2, ct3, ct4 = st.columns(4)
#     celular_mae = ct1.text_input(TELEFONE_MÃE)
#     celular_pai = ct2.text_input(TELEFONE_PAI)
#     fone_contato = ct3.text_input(TELEFONE_CONTATO)
#     telefone_fixo = ct4.text_input(TELEFONE_FIXO)
#
#     ct5, ct6, ct7 = st.columns([2, 2, 1])
#     email_contato = ct5.text_input(EMAIL_CONTATO)
#     uc_equatorial = ct6.text_input(UNIDADE_CONSUMIDORA)
#     cadunico = ct7.text_input(CAD_ÚNICO)
#     irmaos_ue = st.text_input(IRMÃOS)
#
#     st.divider()
#
#     # --- 4. NECESSIDADES EDUCACIONAIS ESPEICIAIS (NEE) ---
#     st.subheader("4. Necessidade Educacional Especial (NEE)")
#
#     possui_nee = st.radio("Possui Necessidade Educacional Especial?", ["Não", "Sim"], horizontal=True)
#
#     nee_opcoes = []
#     nee_outro_texto = ""
#     if possui_nee == "Sim" :
#         lista_nee = ["Dislexia", "Baixa Visão", "Deficiência Auditiva", "Transtorno do Espectro Autista",
#             "Surdo cegueira", "Dislalia", "Cegueira", "TDAH", "Altas Habilidades/Superdotação",
#             "Deficiência Intelectual", "Disgrafia", "Síndrome de Rett", "Surdez", "Distúrbios de Aprendizagem",
#             "Deficiência Física", "Discalculia", "Síndrome de Asperger", "Deficiência Múltipla",
#             "Transtorno Desintegrativo da Infância", "Outro"]
#         nee_opcoes = st.multiselect("Selecione as opções de NEE:", lista_nee)
#         if "Outro" in nee_opcoes :
#             nee_outro_texto = st.text_input("Especifique a NEE (Outro):")
#
#     restricao_alimentar = st.text_input("Restrição alimentar (se houver):")
#
#     st.divider()
#
#     # --- 5. DADOS ESCOLARES ---
#     st.subheader("5. Dados Escolares e Matrícula")
#
#     m1, m2, m3, m4 = st.columns([1, 2, 1, 1])
#     ano_letivo = m1.text_input(ANO_LETIVO, value="2026")
#     curso = m2.text_input(CURSO, value="Ensino Fundamental")
#     ano_serie = m3.text_input(ANO_SÉRIE)
#     turma = m4.text_input(TURMA)
#
#     m5, m6, m7 = st.columns([2, 1, 2])
#     num_matricula = m5.text_input(NUM_MATRÍCULA)
#     data_matricula = m6.text_input(DATA_MATRÍCULA)
#
#     resp_mat_opcao = m7.selectbox(RESPONSÁVEL_MATRÍCULA, ["Mãe", "Pai", "Outro"])
#     resp_mat_outro_texto = ""
#     if resp_mat_opcao == "Outro" :
#         resp_mat_outro_texto = st.text_input(RESPONSÁVEL_MATRÍCULA_OUTRO)
#
#     preenchido_por = st.text_input(PREENCHEDOR_MATRÍCULA, value="Secretaria Escolar")
#     logo_src = st.text_input("URL da Logo (opcional):", value="")
#
#     # Botão para submeter o formulário
#     btn_submit = st.form_submit_button(label=STR_BOTÃO_GERAR_FICHA)
#
# # ---------------------------------------------------------
# # PROCESSAMENTO DOS DADOS E RENDERIZAÇÃO
# # ---------------------------------------------------------
# if btn_submit :
#     # Montagem do dicionário mapeando os "X" para os checkboxes do Jinja
#     contexto = {
#         "logo_src" : logo_src,
#         "nome_estudante" : nome_estudante,
#         "data_nascimento" : data_nascimento,
#         "genero_m" : "X" if genero == "Masculino" else "",
#         "genero_f" : "X" if genero == "Feminino" else "",
#         "nome_social" : nome_social,
#         "cpf_estudante" : cpf_estudante,
#         "municipio_naturalidade" : municipio_naturalidade,
#         "uf_naturalidade" : uf_naturalidade,
#         "termo_cert_nasc" : termo_cert_nasc,
#         "livro" : livro,
#         "folha" : folha,
#         "dt_emissao_cn" : dt_emissao_cn,
#         "cartorio_registro" : cartorio_registro,
#         "municipio_registro" : municipio_registro,
#
#         # Cor / Etnia
#         "cor_branca" : "X" if cor_etnia == "Branca" else "", "cor_preta" : "X" if cor_etnia == "Preta" else "",
#         "cor_parda" : "X" if cor_etnia == "Parda" else "", "cor_indigena" : "X" if cor_etnia == "Indígena" else "",
#         "cor_amarela" : "X" if cor_etnia == "Amarela" else "",
#         "cor_nao_declarada" : "X" if cor_etnia == "Não declarada" else "",
#
#         # Religião
#         "rel_budismo" : "X" if religiao == "Budismo" else "",
#         "rel_catolicismo" : "X" if religiao == "Catolicismo" else "",
#         "rel_evangelismo" : "X" if religiao == "Evangelismo" else "",
#         "rel_congregacao" : "X" if religiao == "Congregação" else "",
#         "rel_espirita" : "X" if religiao == "Espírita" else "",
#         "rel_sem_religiao" : "X" if religiao == "Sem religião" else "",
#
#         # Tamanhos
#         "tam_bermuda" : tam_bermuda,
#         "tam_camiseta" : tam_camiseta,
#         "tam_calca" : tam_calca,
#         "tam_jaqueta" : tam_jaqueta,
#         "tam_tenis" : tam_tenis,
#
#         # Filiação 1
#         "filiacao1_nome" : filiacao1_nome,
#         "filiacao1_dn" : filiacao1_dn,
#         "filiacao1_cpf" : filiacao1_cpf,
#         "filiacao1_titulo" : filiacao1_titulo,
#         "filiacao1_uf" : filiacao1_uf,
#         "filiacao1_zona" : filiacao1_zona,
#         "filiacao1_secao" : filiacao1_secao,
#         "filiacao1_profissao" : filiacao1_profissao,
#         "filiacao1_falecida_sim" : "X" if filiacao1_falecida == "Sim" else "",
#         "filiacao1_falecida_nao" : "X" if filiacao1_falecida == "Não" else "",
#
#         # Filiação 2
#         "filiacao2_nome" : filiacao2_nome,
#         "filiacao2_dn" : filiacao2_dn,
#         "filiacao2_cpf" : filiacao2_cpf,
#         "filiacao2_titulo" : filiacao2_titulo,
#         "filiacao2_uf" : filiacao2_uf,
#         "filiacao2_zona" : filiacao2_zona,
#         "filiacao2_secao" : filiacao2_secao,
#         "filiacao2_profissao" : filiacao2_profissao,
#         "filiacao2_falecido_sim" : "X" if filiacao2_falecido == "Sim" else "",
#         "filiacao2_falecido_nao" : "X" if filiacao2_falecido == "Não" else "",
#
#         # Responsável
#         "responsavel_nome" : responsavel_nome,
#         "responsavel_dn" : responsavel_dn,
#         "responsavel_cpf" : responsavel_cpf,
#         "responsavel_titulo" : responsavel_titulo,
#         "responsavel_uf" : responsavel_uf,
#         "responsavel_zona" : responsavel_zona,
#         "responsavel_secao" : responsavel_secao,
#         "responsavel_profissao" : responsavel_profissao,
#         "responsavel_relacao" : responsavel_relacao,
#
#         # Núcleo Familiar
#         "nuc_mae" : "X" if "Mãe" in nucleo_opcoes else "",
#         "nuc_pai" : "X" if "Pai" in nucleo_opcoes else "",
#         "nuc_irmaos" : "X" if "Irmãos" in nucleo_opcoes else "",
#         "nuc_madrasta" : "X" if "Madrasta" in nucleo_opcoes else "",
#         "nuc_tutor_legal" : "X" if "Tutor Legal" in nucleo_opcoes else "",
#         "nuc_tios" : "X" if "Tios" in nucleo_opcoes else "", "nuc_avos" : "X" if "Avós" in nucleo_opcoes else "",
#         "nuc_primos" : "X" if "Primos" in nucleo_opcoes else "",
#         "nuc_padrasto" : "X" if "Padrasto" in nucleo_opcoes else "",
#         "nuc_outros" : "X" if "Outros" in nucleo_opcoes else "", "nuc_outros_texto" : nuc_outros_texto,
#
#         # Endereço e Contato
#         "logradouro" : logradouro,
#         "quadra" : quadra,
#         "lote" : lote,
#         "numero" : numero,
#         "cep" : cep,
#         "complemento" : complemento,
#         "bairro" : bairro,
#         "municipio" : municipio,
#         "uc_equatorial" : uc_equatorial,
#         "celular_mae" : celular_mae,
#         "fone_contato" : fone_contato,
#         "celular_pai" : celular_pai,
#         "telefone_fixo" : telefone_fixo,
#         "email_contato" : email_contato,
#         "irmaos_ue" : irmaos_ue,
#         "cadunico" : cadunico,
#
#         # NEE
#         "nee_sim" : "X" if possui_nee == "Sim" else "",
#         "nee_nao" : "X" if possui_nee == "Não" else "",
#         "nee_outro" : "X" if "Outro" in nee_opcoes else "",
#         "nee_outro_texto" : nee_outro_texto,
#         "nee_dislexia" : "X" if "Dislexia" in nee_opcoes else "",
#         "nee_baixa_visao" : "X" if "Baixa Visão" in nee_opcoes else "",
#         "nee_def_auditiva" : "X" if "Deficiência Auditiva" in nee_opcoes else "",
#         "nee_tea" : "X" if "Transtorno do Espectro Autista" in nee_opcoes else "",
#         "nee_surdo_cegueira" : "X" if "Surdo cegueira" in nee_opcoes else "",
#         "nee_dislalia" : "X" if "Dislalia" in nee_opcoes else "",
#         "nee_cegueira" : "X" if "Cegueira" in nee_opcoes else "",
#         "nee_tdah" : "X" if "TDAH" in nee_opcoes else "",
#         "nee_altas_habilidades" : "X" if "Altas Habilidades/Superdotação" in nee_opcoes else "",
#         "nee_def_intelectual" : "X" if "Deficiência Intelectual" in nee_opcoes else "",
#         "nee_disgrafia" : "X" if "Disgrafia" in nee_opcoes else "",
#         "nee_rett" : "X" if "Síndrome de Rett" in nee_opcoes else "",
#         "nee_surdez" : "X" if "Surdez" in nee_opcoes else "",
#         "nee_disturbios_aprendizagem" : "X" if "Distúrbios de Aprendizagem" in nee_opcoes else "",
#         "nee_def_fisica" : "X" if "Deficiência Física" in nee_opcoes else "",
#         "nee_discalculia" : "X" if "Discalculia" in nee_opcoes else "",
#         "nee_asperger" : "X" if "Síndrome de Asperger" in nee_opcoes else "",
#         "nee_def_multipla" : "X" if "Deficiência Múltipla" in nee_opcoes else "",
#         "nee_desintegrativo" : "X" if "Transtorno Desintegrativo da Infância" in nee_opcoes else "",
#         "restricao_alimentar" : restricao_alimentar,
#
#         # Dados Escolares
#         "ano_letivo" : ano_letivo,
#         "curso" : curso,
#         "ano_serie" : ano_serie,
#         "turma" : turma,
#         "num_matricula" : num_matricula,
#         "data_matricula" : data_matricula,
#         "resp_mat_mae" : "X" if resp_mat_opcao == "Mãe" else "",
#         "resp_mat_pai" : "X" if resp_mat_opcao == "Pai" else "",
#         "resp_mat_outro" : "X" if resp_mat_opcao == "Outro" else "",
#         "resp_mat_outro_texto" : resp_mat_outro_texto,
#         "preenchido_por" : preenchido_por,
#     }
#
#     # Renderiza o HTML com Jinja2
#     html_gerado = render_html_template(contexto)
#
#     st.success("Ficha gerada com sucesso!")
#
#     # Botão de Download do arquivo HTML gerado
#     st.download_button(label="📥 Baixar Ficha Preenchida (HTML)", data=html_gerado,
#         file_name=f"Ficha_Matricula_{nome_estudante if nome_estudante else 'Estudante'}.html", mime="text/html")
#
#     # Pré-visualização no próprio Streamlit
#     st.write("---")
#     st.subheader("Pré-visualização da Ficha Renderizada")
#     components.html(html_gerado, height=1200, scrolling=True)
