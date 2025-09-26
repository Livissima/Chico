import pandas as pd
from selenium.webdriver.common.by import By
from app.auto.data.sites.propriedades import Propriedades
from app.auto.functions.navegação import Navegação
from selenium.webdriver import Chrome


class GerenciadorDeFrequência :

    def __init__(self, navegador: Chrome, path, **kwargs) :
        self.path_xlsx = path
        self.master = navegador
        self.nv = Navegação(navegador, 'siap')
        self.pp = Propriedades(site='siap')
        print(f'{self.ausentes_do_dia = }')
        self.executar()
        self.master.quit()

    def executar(self) :
        self.master.get(self.pp.url)
        self.master.maximize_window()
        self._logon()
        self._acessar_painel_frequência()
        self._iterar_turmas()

    def _logon(self) :
        credenciais = self.pp.credenciais
        self.nv.digitar_xpath('input login', string=credenciais['id'])
        self.nv.digitar_xpath('input senha', string=credenciais['senha'])
        self._resolver_captcha()
        self.nv.clicar('xpath', 'botão login')
        self.nv.aguardar_página()

    def _resolver_captcha(self) :
        captcha = self.master.find_element(By.XPATH, self.pp.xpaths['captcha'])
        self.nv.digitar_xpath('input captcha', string=captcha.text)

    def _acessar_painel_frequência(self) :
        self.nv.clicar('xpath', 'menu sistema')
        self.nv.clicar('xpath', 'menu frequência')
        self.nv.aguardar_página()

    def _iterar_turmas(self) :
        turmas = self.nv.obter_turmas_siap()
        for turma in turmas :
            self.nv.clicar('xpath livre', turma)
            nome_turma = self.master.find_element(By.XPATH, turma).text
            self.nv.aguardar_página()
            print('página carregada')
            self._definir_faltas(nome_turma)

    def _definir_faltas(self, turma):
        matrículas_clicadas = self._executar_javascript('falta')
        self._executar_javascript('justificativa')
        for matrícula in matrículas_clicadas:
            estudante = self.ausentes_do_dia.get(matrícula, 'Não identificado')
            print(f'Falta lançada para: {estudante} - {matrícula}')
        print(f'Faltas lançadas na turma {turma}: {len(matrículas_clicadas)}')

        self.nv.clicar('xpath', 'salvar e próximo')

    @property
    def ausentes_do_dia(self) -> dict :
        df = pd.read_excel(self.path_xlsx, sheet_name='Compilado Faltas', dtype={'Matrícula' : str})
        df = df[['Turma Real', 'Estudante', 'Data Falta', 'Lançado', 'Matrícula']]
        df = df[df['Lançado'] == 'Lançado']
        df['Data Falta'] = df['Data Falta'].dt.strftime('%d/%m/%Y')
        df = df[df['Data Falta'] == self.pp.hoje]
        faltosos_de_hoje = dict(zip(df['Matrícula'], df['Estudante']))

        return faltosos_de_hoje

    @property
    def __script_js_faltas(self):
        return """
        const matriculasNecessarias = new Set(arguments[0]);
        const elementos = document.querySelectorAll('.listaDeFrequencias .itens div[data-matricula]');
        const matriculasClicadas = [];

        elementos.forEach(elemento => {
            const matricula = elemento.getAttribute('data-matricula');
            if (matriculasNecessarias.has(matricula)) {
                elemento.click();
                matriculasClicadas.push(matricula);
                }
            });
        return matriculasClicadas;
        """

    @property
    def __script_js_justificativas(self):
        return """
            const matriculasNecessarias = new Set(arguments[0]);
            const selects = document.querySelectorAll('.listaMotivoAusencia .itens select[data-matricula]');
            const resultados = [];

            selects.forEach(select => {
                const matricula = select.getAttribute('data-matricula');
                if (matriculasNecessarias.has(matricula)) {
                    const valorAntigo = select.value;
                    select.value = '1';
                    const valorNovo = select.value;

                    ['change', 'input', 'blur'].forEach(evento => {
                        select.dispatchEvent(new Event(evento, { bubbles: true }));
                    });
                    resultados.push({
                        matricula: matricula,
                        alterado: valorNovo === '1',
                        valorAntigo: valorAntigo,
                        valorNovo: valorNovo
                    });
                }
            });
            return resultados;
            """

    def _executar_javascript(self, tipo):
        scripts = {
            'falta' : self.__script_js_faltas,
            'justificativa' : self.__script_js_justificativas
        }
        argumento = list(self.ausentes_do_dia.keys())
        return self.master.execute_script(scripts[tipo], argumento)
