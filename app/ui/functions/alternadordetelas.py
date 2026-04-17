#app/ui/functions/alternadordetelas.py
from app.ui.config.registrotelas import RegistroTelas
from app.ui.widgets import Texto, Botão

class AlternadorDeTelas:
    def __init__(self, container, controller):
        self.container = container
        self.controller = controller
        self._histórico = []
        self._tela_atual = None

    def abrir(self, nome_tela: str, salvar_no_histórico: bool = True):
        if nome_tela not in RegistroTelas.REGISTRO:
            raise ValueError(f"Tela '{nome_tela}' não encontrada.")

        if salvar_no_histórico and self._tela_atual:
            self._histórico.append(self._tela_atual)

        self._tela_atual = nome_tela

        if self.container.winfo_children():
            for widget in self.container.winfo_children():
                if hasattr(widget, 'salvar_estado'):
                    widget.salvar_estado()
                widget.destroy()

        dados = RegistroTelas.REGISTRO[nome_tela]

        meta = dados['metadata']

        tela_instância = dados['class'](self.container, self.controller)

        self.controller.title(meta['título_janela'])

        self._criar_cabeçalho_automático(tela_instância, meta)

        if meta['mostrar_voltar'] and self._histórico:
            self._criar_botão_voltar(tela_instância)

    def _criar_cabeçalho_automático(self, tela, meta):


        tela.header_título = Texto(
            classe=tela,
            texto=meta['cabeçalho'],
            fonte=('times new roman', 30),
            # x='centro',
            y=0,
            altura=45,
            largura=self.controller.largura - 10
        )
        tela.header_desc = Texto(
            classe=tela,
            texto=meta['descrição'],
            fonte=('Arial', 17),
            y=40,
            altura=30,
            largura=self.controller.largura - 10
        )

    def voltar(self):
        if self._histórico:
            última_tela = self._histórico.pop()
            self.abrir(última_tela, salvar_no_histórico=False)

    def _criar_botão_voltar(self, tela):
        if not self._histórico:
            return


        tela.bt_back = Botão(
            tela,
            função=self.voltar,
            texto='←',
            fonte=('arial', 20),
            formato='bold',
            x=10, y=10,
            largura= 40, altura=40
        )
        tela.bt_back.lift()
