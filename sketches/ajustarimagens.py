import cv2
import numpy as np
import os

DIRETORIO_ORIGEM = r'C:\Users\meren\OneDrive - Secretaria de Estado da Educação\SIGE\fonte\fotos'
DIRETORIO_DESTINO = r'C:\Users\meren\Desktop\Fotos mexidas'


def imread_utf8(caminho) :
    with open(caminho, "rb") as f :
        chunk = f.read()
    array = np.frombuffer(chunk, dtype=np.uint8)
    return cv2.imdecode(array, cv2.IMREAD_COLOR)


def imwrite_utf8(caminho, imagem) :
    extensao = os.path.splitext(caminho)[1].lower()
    # Se for JPG, salvamos com alta qualidade (95)
    params = [cv2.IMWRITE_JPEG_QUALITY, 95] if extensao in ['.jpg', '.jpeg'] else []
    is_success, im_buf_arr = cv2.imencode(extensao, imagem, params)
    if is_success :
        im_buf_arr.tofile(caminho)
        return True
    return False


def ajustar_foto(imagem) :
    # Reduzi para 1.4 para evitar o efeito "estourado" no fundo branco
    gama = 1.6
    inv_gama = 1.0 / gama
    tabela = np.array([((i / 255.0) ** inv_gama) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(imagem, tabela)


def processar_recursivo() :
    if not os.path.exists(DIRETORIO_ORIGEM) :
        print(f"Erro: Pasta não encontrada: {DIRETORIO_ORIGEM}")
        return

    contador = 0
    # Extensões permitidas em uma TUPLA
    extensoes_permitidas = ('.png', '.jpg', '.jpeg', '.bmp')

    for root, dirs, files in os.walk(DIRETORIO_ORIGEM) :
        for file in files :
            # Converte para minúsculo para não ignorar .JPG ou .PNG
            nome_minusculo = file.lower()

            if nome_minusculo.endswith(extensoes_permitidas) :
                caminho_full_origem = os.path.join(root, file)

                rel_path = os.path.relpath(root, DIRETORIO_ORIGEM)
                pasta_destino_atual = os.path.join(DIRETORIO_DESTINO, rel_path)
                os.makedirs(pasta_destino_atual, exist_ok=True)

                caminho_full_destino = os.path.join(pasta_destino_atual, file)

                img = imread_utf8(caminho_full_origem)
                if img is not None :
                    img_corrigida = ajustar_foto(img)
                    if imwrite_utf8(caminho_full_destino, img_corrigida) :
                        contador += 1
                        print(f"[{contador}] Processado ({nome_minusculo.split('.')[-1]}): {file}")
                else :
                    print(f"Falha ao ler: {file}")

    print(f"\n--- Processo concluído! {contador} imagens salvas em '{DIRETORIO_DESTINO}' ---")


if __name__ == "__main__" :
    processar_recursivo()