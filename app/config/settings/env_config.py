import os
import logging
from dataclasses import dataclass
from typing import Optional, Dict, List
from pathlib import Path

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class CredencialSIAP :
    usuario: str
    id_siap: str
    senha: str
    tipo: str

    def validar(self) -> bool :
        return all([self.usuario, self.id_siap, self.senha, self.tipo])

    def __repr__(self) -> str :
        return f"CredencialSIAP(usuario='{self.usuario}', tipo='{self.tipo}')"


@dataclass
class Configuracao :
    id_sige: str
    senha_sige: str
    credenciais_siap: Dict[str, CredencialSIAP]

    def validar(self) -> bool :
        if not self.id_sige or not self.senha_sige :
            logger.warning("Credenciais SIGE não configuradas")
            return False

        if not self.credenciais_siap :
            logger.warning("Nenhuma credencial SIAP foi carregada")
            return False

        return True


class ConfiguradorAmbiente :
    MAX_CREDENCIAIS = 20
    VARIÁVEIS_OBRIGATÓRIAS_SIGE = ['ID_SIGE', 'SENHA_SIGE']

    def __init__(self, caminho_env: Optional[Path] = None) :
        self._carregar_dotenv(caminho_env)
        self._config: Optional[Configuracao] = None
        self._erros: List[str] = []

    @staticmethod
    def _carregar_dotenv(caminho: Optional[Path] = None) -> None :
        if caminho :
            caminho = Path(caminho)
            if not caminho.exists() :
                logger.warning(f"Arquivo .env não encontrado em: {caminho}")
            else :
                logger.info(f"Carregando .env de: {caminho}")

        load_dotenv(dotenv_path=caminho)

    def obter(self, chave: str, padrao: Optional[str] = None) -> Optional[str] :
        valor = os.getenv(chave, padrao)

        if valor is None :
            mensagem = f"Variável de ambiente '{chave}' não encontrada"
            logger.warning(mensagem)
            self._erros.append(mensagem)

        return valor

    def _carregar_credenciais_sige(self) -> tuple[str, str] :
        valores = {}

        for var in self.VARIÁVEIS_OBRIGATÓRIAS_SIGE :
            valor = self.obter(var)
            if not valor :
                mensagem = f"Variável obrigatória '{var}' não foi configurada"
                logger.error(mensagem)
                self._erros.append(mensagem)
                raise ValueError(mensagem)
            valores[var] = valor

        logger.info("Credenciais SIGE carregadas com sucesso")
        return valores['ID_SIGE'], valores['SENHA_SIGE']

    def _carregar_credenciais_siap(self) -> Dict[str, CredencialSIAP] :

        credenciais: Dict[str, CredencialSIAP] = {}

        for i in range(self.MAX_CREDENCIAIS) :
            usuario = self.obter(f'USUARIO{i}')
            id_siap = self.obter(f'ID_SIAP{i}')
            senha = self.obter(f'SENHA_SIAP{i}')
            tipo = self.obter(f'TIPO{i}')


            if not any([usuario, id_siap, senha, tipo]) :
                continue

            if not all([usuario, id_siap, senha, tipo]) :
                mensagem = (f"Credencial SIAP incompleta no índice {i}: "
                            f"usuario={bool(usuario)}, id={bool(id_siap)}, "
                            f"senha={bool(senha)}, tipo={bool(tipo)}")
                logger.warning(mensagem)
                self._erros.append(mensagem)
                continue

            cred = CredencialSIAP(usuario=usuario, id_siap=id_siap, senha=senha, tipo=tipo)

            if not cred.validar() :
                mensagem = f"Credencial SIAP inválida para usuário {usuario}"
                logger.warning(mensagem)
                self._erros.append(mensagem)
                continue

            credenciais[usuario] = cred
            logger.debug(f"Credencial SIAP carregada: {cred}")

        quantidade = len(credenciais)
        logger.info(f"{quantidade} credencial(is) SIAP carregada(s)")

        return credenciais

    def carregar(self) -> Configuracao :

        try :
            id_sige, senha_sige = self._carregar_credenciais_sige()
            credenciais_siap = self._carregar_credenciais_siap()

            self._config = Configuracao(id_sige=id_sige, senha_sige=senha_sige, credenciais_siap=credenciais_siap)

            if not self._config.validar() :
                raise ValueError("Configuração inválida após carregamento")

            logger.info("Configuração carregada e validada com sucesso")
            return self._config

        except ValueError as e :
            logger.error(f"Erro ao carregar configuração: {e}")
            raise

    @property
    def config(self) -> Optional[Configuracao] :
        return self._config

    @property
    def erros(self) -> List[str] :
        return self._erros.copy()

    def exibir_relatorio(self) -> None :
        print("\n" + "=" * 60)
        print("RELATÓRIO DE CONFIGURAÇÃO")
        print("=" * 60)

        if self._config :
            print(f"\n✓ SIGE configurado")
            print(f"  ID: {self._config.id_sige}")

            print(f"\n✓ SIAP - {len(self._config.credenciais_siap)} usuário(s)")
            for usuario, cred in self._config.credenciais_siap.items() :
                print(f"  - {usuario} (Tipo: {cred.tipo})")
        else :
            print("\n✗ Nenhuma configuração carregada")

        if self._erros :
            print(f"\n⚠ AVISOS E ERROS ({len(self._erros)}):")
            for erro in self._erros :
                print(f"  - {erro}")
        else :
            print("\n✓ Nenhum erro detectado")

        print("=" * 60 + "\n")


# ============================================================================


_configurador: Optional[ConfiguradorAmbiente] = None
_config: Optional[Configuracao] = None


def inicializar(caminho_env: Optional[Path] = None) -> Configuracao :
    global _configurador, _config

    _configurador = ConfiguradorAmbiente(caminho_env)
    _config = _configurador.carregar()

    return _config


def obter_config() -> Configuracao :

    if _config is None :
        raise RuntimeError("Configuração não inicializada. "
                           "Chame inicializar() primeiro.")
    return _config


def obter_erros() -> List[str] :
    if _configurador is None :
        return []
    return _configurador.erros


def exibir_relatorio() -> None :
    if _configurador :
        _configurador.exibir_relatorio()


try :
    _config_inicial = inicializar()
    ID_SIGE = _config_inicial.id_sige
    SENHA_SIGE = _config_inicial.senha_sige
    CREDENCIAIS_SIAP = _config_inicial.credenciais_siap

except (ValueError, RuntimeError) as e :
    logger.error(f"Falha ao inicializar configuração automaticamente: {e}")
    ID_SIGE = None
    SENHA_SIGE = None
    CREDENCIAIS_SIAP = {}
    