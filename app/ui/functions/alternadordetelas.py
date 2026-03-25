from app.ui.config.registrodetelas import RegistradorDeTelas
from app.ui.widgets import Texto, Botão

class AlternadorDeTelas:
    def __init__(self, container, controller):
        self.container = container
        self.controller = controller
        self.histórico = []
        self.tela_atual = None

    def abrir(self, nome_tela: str, salvar_no_histórico: bool = True):
        if nome_tela not in RegistradorDeTelas.REGISTRO_DE_TELAS:
            raise ValueError(f"Tela '{nome_tela}' não encontrada.")

        if salvar_no_histórico and self.tela_atual:
            self.histórico.append(self.tela_atual)

        self.tela_atual = nome_tela

        if self.container.winfo_children():
            for widget in self.container.winfo_children():
                if hasattr(widget, 'salvar_estado'):
                    widget.salvar_estado()
                widget.destroy()

        dados = RegistradorDeTelas.REGISTRO_DE_TELAS[nome_tela]

        meta = dados['metadata']

        tela_instância = dados['class'](self.container, self.controller)

        self.controller.title(meta['título_janela'])

        self._criar_cabeçalho_automático(tela_instância, meta)

        if meta['mostrar_voltar'] and self.histórico:
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
        if self.histórico:
            última_tela = self.histórico.pop()
            self.abrir(última_tela, salvar_no_histórico=False)

    def _criar_botão_voltar(self, tela):
        if not self.histórico:
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

