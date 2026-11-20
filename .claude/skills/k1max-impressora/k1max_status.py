"""Lê status e histórico da Creality K1 Max (firmware de fábrica) pelo WebSocket da porta 9999.

Só leitura: não envia comandos de impressão, temperatura ou movimento.
Só biblioteca padrão do Python.

Uso:
  python k1max_status.py status [--ip 192.168.0.69]
  python k1max_status.py historico [--ip 192.168.0.69] [--n 10]
  python k1max_status.py bruto [--ip ...]          # JSON completo do status
"""
import argparse
import base64
import datetime
import json
import os
import socket
import time

IP_PADRAO = "192.168.0.69"


def _ws_get(ip, pedido=None, duracao=5.0):
    s = socket.create_connection((ip, 9999), timeout=5)
    chave = base64.b64encode(os.urandom(16)).decode()
    s.send((f"GET / HTTP/1.1\r\nHost: {ip}:9999\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {chave}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n").encode())
    buf = b""
    while b"\r\n\r\n" not in buf:
        buf += s.recv(4096)
    buf = buf.split(b"\r\n\r\n", 1)[1]

    if pedido is not None:
        dados = json.dumps(pedido).encode()
        mascara = os.urandom(4)
        cab = bytearray([0x81])
        if len(dados) < 126:
            cab.append(0x80 | len(dados))
        else:
            cab.append(0x80 | 126)
            cab += len(dados).to_bytes(2, "big")
        s.send(bytes(cab) + mascara + bytes(b ^ mascara[i % 4] for i, b in enumerate(dados)))

    s.settimeout(1)
    fim = time.time() + duracao

    def ler(n):
        nonlocal buf
        while len(buf) < n:
            try:
                pedaco = s.recv(65536)
            except socket.timeout:
                if time.time() > fim:
                    raise TimeoutError
                continue
            if not pedaco:
                raise EOFError
            buf += pedaco
        r, buf = buf[:n], buf[n:]
        return r

    juntado = {}
    try:
        while time.time() < fim:
            b0, b1 = ler(2)
            n = b1 & 0x7F
            if n == 126:
                n = int.from_bytes(ler(2), "big")
            elif n == 127:
                n = int.from_bytes(ler(8), "big")
            carga = ler(n)
            if b0 & 0x0F == 1:
                try:
                    juntado.update(json.loads(carga.decode("utf-8", "replace"), strict=False))
                except json.JSONDecodeError:
                    pass
    except (TimeoutError, EOFError, OSError):
        pass
    s.close()
    return juntado


def status(ip):
    d = _ws_get(ip, {"method": "get", "params": {"ReqPrintObjects": 1}})
    estados = {0: "parada", 1: "imprimindo", 2: "concluída", 4: "erro/parada", 5: "pausada"}
    print(f"Impressora: {d.get('model')} ({d.get('hostname')}) em {ip}")
    print(f"Estado: {estados.get(d.get('state'), d.get('state'))}")
    print(f"Bico: {float(d.get('nozzleTemp', 0)):.1f} °C (alvo {d.get('targetNozzleTemp')})")
    print(f"Mesa: {float(d.get('bedTemp0', 0)):.1f} °C (alvo {d.get('targetBedTemp0')})")
    print(f"Câmara: {d.get('boxTemp')} °C")
    print(f"Pressure advance no Klipper agora: {d.get('pressureAdvance')}")
    if d.get("printFileName"):
        print(f"Arquivo: {os.path.basename(d['printFileName'])} – {d.get('printProgress')}% "
              f"(camada {d.get('layer')}/{d.get('TotalLayer')}, faltam {d.get('printLeftTime', 0) // 60} min)")
    err = d.get("err") or {}
    if err.get("errcode"):
        print(f"ERRO: {err}")
    return d


def historico(ip, n):
    d = _ws_get(ip, {"method": "get", "params": {"reqHistory": 1}}, duracao=6)
    lista = sorted(d.get("historyList") or [], key=lambda x: -x.get("starttime", 0))
    print(f"{len(lista)} trabalhos no histórico; os {min(n, len(lista))} mais recentes:")
    for h in lista[:n]:
        inicio = datetime.datetime.fromtimestamp(h["starttime"]).strftime("%d/%m/%Y %H:%M")
        dur = h.get("usagetime", 0)
        fim = "concluída" if h.get("printfinish") else "interrompida"
        print(f"  {inicio}  {os.path.basename(h['filename'])}  "
              f"{dur // 3600}h{dur % 3600 // 60:02d}  {h.get('usagematerial', 0) / 1000:.2f} m  {fim}")
    return lista


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("acao", choices=["status", "historico", "bruto"])
    ap.add_argument("--ip", default=IP_PADRAO)
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()
    if a.acao == "status":
        status(a.ip)
    elif a.acao == "historico":
        historico(a.ip, a.n)
    else:
        print(json.dumps(_ws_get(a.ip, {"method": "get", "params": {"ReqPrintObjects": 1}}),
                         ensure_ascii=False, indent=1))
