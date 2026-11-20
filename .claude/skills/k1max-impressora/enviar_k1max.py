"""Envia um G-code para a lista de arquivos da K1 Max (firmware de fábrica, sem root). NÃO IMPRIME.

Faz o mesmo que o botão de enviar arquivo do Creality Print (POST http://IP/upload/<nome>).
A impressão só começa quando alguém, NA FRENTE DA IMPRESSORA, escolhe o arquivo na tela e
confere bico, filamento, mesa vazia e tampa. Este script não tem nenhum comando de iniciar.

Uso:
  python enviar_k1max.py arquivo.gcode [--ip 192.168.0.69] [--sobrescrever] [--mesmo-imprimindo]

Só biblioteca padrão do Python.
"""
import argparse
import os
import re
import sys
import urllib.parse
import urllib.request
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k1max_status import IP_PADRAO, _ws_get  # noqa: E402

ESTADOS = {0: "parada", 1: "imprimindo", 2: "concluída", 4: "erro/parada", 5: "pausada"}


def resumo_gcode(caminho):
    """Lê as configurações do rodapé do G-code (o Creality Print grava no fim do arquivo)."""
    tam = os.path.getsize(caminho)
    with open(caminho, "rb") as f:
        f.seek(max(0, tam - 400_000))
        fim = f.read().decode("utf-8", "ignore")
        f.seek(0)
        ini = f.read(300_000).decode("utf-8", "ignore")
    cfg = {}
    for m in re.finditer(r"^; ([\w \[\]()]+?) = (.*)$", ini + "\n" + fim, re.M):
        cfg.setdefault(m.group(1), m.group(2).strip().strip('"'))
    cfg["_miniatura"] = "thumbnail begin" in ini
    return cfg


def lista_arquivos(ip):
    d = _ws_get(ip, {"method": "get", "params": {"reqGcodeFile": 1}}, duracao=5)
    return {x["name"]: x for x in (d.get("retGcodeFileInfo2") or [])}


def enviar(ip, caminho, nome):
    limite = uuid.uuid4().hex
    with open(caminho, "rb") as f:
        dados = f.read()
    corpo = (f"--{limite}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{nome}\"\r\n"
             "Content-Type: application/octet-stream\r\n\r\n").encode() + dados + f"\r\n--{limite}--\r\n".encode()
    req = urllib.request.Request(f"http://{ip}/upload/{urllib.parse.quote(nome)}", data=corpo, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={limite}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.status, r.read().decode("utf-8", "ignore")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo")
    ap.add_argument("--ip", default=IP_PADRAO)
    ap.add_argument("--sobrescrever", action="store_true", help="substitui arquivo de mesmo nome na impressora")
    ap.add_argument("--mesmo-imprimindo", action="store_true", help="envia mesmo com a impressora ocupada")
    a = ap.parse_args()

    caminho = os.path.abspath(os.path.expanduser(a.arquivo))
    if not caminho.lower().endswith(".gcode"):
        sys.exit("Envie um .gcode fatiado (fatiar_3mf.py gera um).")
    nome = re.sub(r'[\\/:*?"\'<>|]', "", os.path.basename(caminho))
    cfg = resumo_gcode(caminho)
    if "nozzle_diameter" not in cfg:
        sys.exit("Esse arquivo não parece um G-code do Creality Print (sem configurações no rodapé).")

    st = _ws_get(a.ip, {"method": "get", "params": {"ReqPrintObjects": 1}})
    if not st:
        sys.exit(f"A impressora não respondeu em {a.ip}. Confira o IP na tela (Configurações → Rede).")
    estado = st.get("state")
    imprimindo = os.path.basename(st.get("printFileName") or "")
    if estado in (1, 5) and not a.mesmo_imprimindo:
        sys.exit(f"A impressora está {ESTADOS.get(estado)} ({imprimindo}). Nada enviado. "
                 "Use --mesmo-imprimindo se quiser só deixar o arquivo na lista.")
    if nome == imprimindo:
        sys.exit("Esse é o arquivo que está em uso na impressora. Nada enviado.")

    existentes = lista_arquivos(a.ip)
    if nome in existentes and not a.sobrescrever:
        sys.exit(f"Já existe '{nome}' na impressora. Nada enviado. Use --sobrescrever se for para substituir.")

    status, resp = enviar(a.ip, caminho, nome)
    if status != 200:
        sys.exit(f"Envio falhou: HTTP {status} {resp[:200]}")
    depois = lista_arquivos(a.ip).get(nome)
    tam = os.path.getsize(caminho)
    if not depois or int(depois.get("file_size", -1)) != tam:
        sys.exit(f"A impressora respondeu OK, mas o arquivo não apareceu na lista com {tam} bytes: {depois}")

    print(f"Enviado para a lista da impressora ({a.ip}): {nome}  ({tam / 1e6:.1f} MB). NÃO foi iniciado.")
    print(f"  Bico: {cfg.get('nozzle_diameter')}   Impressora: {cfg.get('printer_settings_id')}")
    print(f"  Filamento: {cfg.get('filament_settings_id')} [{cfg.get('filament_type')}]  "
          f"bico {cfg.get('nozzle_temperature')} °C / mesa {cfg.get('hot_plate_temp')} °C")
    print(f"  Tempo: {cfg.get('estimated printing time (normal mode)')}   "
          f"{cfg.get('filament used [g]')} g   miniatura: {'sim' if cfg['_miniatura'] else 'não'}")
    print("Para imprimir, na frente da impressora: confira o bico montado, o filamento carregado, "
          "a mesa vazia e limpa e a tampa (PLA: aberta). Depois escolha o arquivo na tela.")


if __name__ == "__main__":
    main()
