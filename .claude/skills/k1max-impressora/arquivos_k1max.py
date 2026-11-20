"""Lista ou apaga arquivos da lista de G-codes da K1 Max (firmware de fábrica, sem root).

Uso:
  python arquivos_k1max.py listar [--ip 192.168.0.69]
  python arquivos_k1max.py apagar "nome exato.gcode" ["outro.gcode" ...] [--ip ...]

Apagar só com pedido explícito de quem usa a impressora. Aceita apenas nomes exatos (sem curingas),
recusa o arquivo que está em uso e confere na lista, depois, se ele sumiu.
O comando é o mesmo do Creality Print: WebSocket 9999, {"method":"set","params":{"opGcodeFile":"deleteprt:<caminho>"}}.
"""
import argparse
import datetime
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k1max_status import IP_PADRAO, _ws_get  # noqa: E402


def lista(ip):
    d = _ws_get(ip, {"method": "get", "params": {"reqGcodeFile": 1}}, duracao=5)
    return {x["name"]: x for x in (d.get("retGcodeFileInfo2") or [])}


def listar(ip):
    arqs = sorted(lista(ip).values(), key=lambda x: -x.get("create_time", 0))
    print(f"{len(arqs)} arquivos na impressora:")
    for x in arqs:
        data = datetime.datetime.fromtimestamp(x.get("create_time", 0)).strftime("%d/%m/%Y %H:%M")
        print(f"  {data}  {x['file_size'] / 1e6:6.1f} MB  {x['name']}")


def apagar(ip, nomes):
    arqs = lista(ip)
    st = _ws_get(ip, {"method": "get", "params": {"ReqPrintObjects": 1}})
    em_uso = os.path.basename(st.get("printFileName") or "")
    ocupada = st.get("state") in (1, 5)
    for n in nomes:
        if n not in arqs:
            sys.exit(f"'{n}' não está na impressora. Nada apagado.")
        if ocupada and n == em_uso:
            sys.exit(f"'{n}' está em uso na impressão atual. Nada apagado.")
    for n in nomes:
        _ws_get(ip, {"method": "set", "params": {"opGcodeFile": "deleteprt:" + arqs[n]["path"]}}, duracao=2)
    time.sleep(1)
    restantes = lista(ip)
    falhou = [n for n in nomes if n in restantes]
    for n in nomes:
        print(f"{'NÃO apagado' if n in falhou else 'Apagado'}: {n}")
    if falhou:
        sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("acao", choices=["listar", "apagar"])
    ap.add_argument("nomes", nargs="*")
    ap.add_argument("--ip", default=IP_PADRAO)
    a = ap.parse_args()
    if a.acao == "listar":
        listar(a.ip)
    elif not a.nomes:
        sys.exit("Diga o nome exato de cada arquivo a apagar.")
    else:
        apagar(a.ip, a.nomes)
