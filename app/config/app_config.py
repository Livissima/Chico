import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
# from app.config.env_config import
from pathlib import Path
from platformdirs import user_documents_dir



DIRETÓRIO_BASE_PADRÃO = str(os.path.join(Path(user_documents_dir()), 'SIGE'))




# class ConfigManager:
#     def __init__(self):
#         self.config_dir = Path(__file__).parent.parent.parent / 'data' / 'config'
#         self.config_file = self.config_dir / 'app_settings.json'
#         self._ensure_config_directory()
#         self.settings = self._load_settings()
#
#     def _ensure_config_directory(self) -> None:
#         self.config_dir.mkdir(parents=True, exist_ok=True)
#
#     def _load_settings(self) -> Dict[str, Any]:
#         if not self.config_file.exists():
#             return {}
#
#         try:
#             with open(self.config_file, 'r', encoding='utf-8') as file:
#                 return json.load(file)
#         except (json.JSONDecodeError, FileNotFoundError):
#             return {}
#
#     def _save_settings(self) -> None:
#         with open(self.config_file, 'w', encoding='utf-8') as file:
#             json.dump(self.config_file, 'f', indent=2, ensure_ascii=False)
#
#     def get_user_settings(self, turmas: list[str], usuário: Optional[str] = None) -> Dict[str, Any]:
#         #todo: aqui eu devo inserir variáveis que representam o valor coletado nos inputs
#         # que serão criados
#         #usuário = usuário or ID
#         turmas = [turmas]
#         #
#         #
#         #
#         #
#         ############################# PAREI AQUI
#
#     def save_user_setting(self, key: str, value: Any, user_id: Optional[str] = None) -> None :
#         """Salva uma configuração específica do usuário"""
#         user_id = user_id or ID
#
#         if user_id not in self.settings :
#             self.settings[user_id] = {}
#
#         self.settings[user_id][key] = value
#         self._save_settings()
#
#     def get_last_used(self, key: str, default: Any = None, user_id: Optional[str] = None) -> Any :
#         """Obtém o último valor usado para uma chave específica"""
#         user_settings = self.get_user_settings(user_id)
#         return user_settings.get(key, default)
#
#     def save_last_used(self, **kwargs) -> None :
#         """Salva múltiplos parâmetros de uma vez"""
#         for key, value in kwargs.items() :
#             self.save_user_setting(key, value)
#
#     def clear_user_settings(self, user_id: Optional[str] = None) -> None :
#         """Limpa todas as configurações do usuário"""
#         user_id = user_id or ID
#         if user_id in self.settings :
#             del self.settings[user_id]
#             self._save_settings()
#
#
# # Instância global para uso em toda a aplicação
# config_manager = ConfigManager()
