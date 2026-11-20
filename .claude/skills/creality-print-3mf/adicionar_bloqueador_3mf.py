#!/usr/bin/env python3
"""
Adiciona caixas de BLOQUEIO (ou REFORCO) de suporte a um objeto de um projeto .3mf do Creality Print 7,
sem abrir o programa. Estrutura copiada de um projeto real do Creality (partes extras = type="other"
no object_N.model + component no 3dmodel.model + <part subtype=...> no model_settings.config).

Uso:
  python3 adicionar_bloqueador_3mf.py ENTRADA.3mf SAIDA.3mf CAIXAS_JSON [--tipo support_blocker|support_enforcer] [--objeto 1]

  CAIXAS_JSON: lista de caixas em coordenadas da MESA (mm, como no fatiador; mesa 0..300):
    '[{"nome":"Bloqueador bico frontal","min":[145,173,0],"max":[162,181,3.6]}]'

Confira depois no Creality: os itens aparecem dentro do objeto na lista; ao fatiar, nao ha suporte na caixa.
"""
import json, re, sys, zipfile

import numpy as np


def caixa_xml(oid, uuid, mn, mx, tipo_obj="other"):
    x0, y0, z0 = mn
    x1, y1, z1 = mx
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    vs = "".join(f'<vertex x="{a:.6f}" y="{b:.6f}" z="{c:.6f}"/>' for a, b, c in v)
    ts = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f)
    return f'<object id="{oid}" p:UUID="{uuid}" type="{tipo_obj}"><mesh><vertices>{vs}</vertices><triangles>{ts}</triangles></mesh></object>'


def main():
    src, dst, caixas = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
    tipo = sys.argv[sys.argv.index("--tipo") + 1] if "--tipo" in sys.argv else "support_blocker"
    n_obj = sys.argv[sys.argv.index("--objeto") + 1] if "--objeto" in sys.argv else "1"
    path = f"3D/Objects/object_{n_obj}.model"
    z = zipfile.ZipFile(src)
    obj = z.read(path).decode()
    m3 = z.read("3D/3dmodel.model").decode()
    ms = z.read("Metadata/model_settings.config").decode()

    comp = re.search(rf'<component p:path="/{re.escape(path)}"[^>]*/>', m3).group(0)
    comp_t = np.array(list(map(float, re.search(r'transform="([^"]+)"', comp).group(1).split())))
    wrapper = re.search(r'<object id="(\d+)"[^>]*>\s*<components>\s*' + re.escape(comp), m3).group(1)
    item_t = np.array(list(map(float, re.search(rf'<item objectid="{wrapper}"[^>]*transform="([^"]+)"', m3).group(1).split())))
    # transform 3MF: 12 numeros (3x3 por linhas de vetores + translacao). Converter mesa -> local do objeto
    def mat(t):
        M = np.eye(4); M[:3, :3] = t[:9].reshape(3, 3).T; M[:3, 3] = t[9:]; return M
    inv = np.linalg.inv(mat(item_t) @ mat(comp_t))

    ids = [int(i) for i in re.findall(r'<object id="(\d+)"', obj)] + [int(i) for i in re.findall(r'<object id="(\d+)"', m3)]
    novo = max(ids) + 1
    xml_objs, comps, parts = "", "", ""
    for k, c in enumerate(caixas):
        cantos = np.array([[x, y, zz, 1] for x in (c["min"][0], c["max"][0]) for y in (c["min"][1], c["max"][1]) for zz in (c["min"][2], c["max"][2])])
        loc = (inv @ cantos.T).T[:, :3]
        oid = novo + k
        uuid = f"{int(n_obj):04x}{k + 1:04x}-81cb-4c03-9d28-80fed5dfa1dc"
        xml_objs += caixa_xml(oid, uuid, loc.min(0), loc.max(0))
        comps += comp.replace(re.search(r'objectid="\d+"', comp).group(0), f'objectid="{oid}"').replace(
            re.search(r'p:UUID="[^"]+"', comp).group(0), f'p:UUID="{int(n_obj):04x}{k + 1:04x}-b206-40ff-9872-83e8017abed1"')
        parts += (f'\n    <part id="{oid}" subtype="{tipo}">\n      <metadata key="name" value="{c.get("nome", "Bloqueador")}"/>\n'
                  f'      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
                  f'      <mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>\n    </part>')
    obj = obj.replace("</resources>", xml_objs + "</resources>")
    m3 = m3.replace(comp, comp + comps)
    i = ms.index(f'<object id="{wrapper}">'); j = ms.index("</object>", i)
    last_part = ms.rindex("</part>", i, j) + len("</part>")
    ms = ms[:last_part] + parts + ms[last_part:]

    zo = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    for it in z.infolist():
        data = z.read(it.filename)
        if it.filename == path: data = obj.encode()
        elif it.filename == "3D/3dmodel.model": data = m3.encode()
        elif it.filename == "Metadata/model_settings.config": data = ms.encode()
        zo.writestr(it, data)
    zo.close()
    assert zipfile.ZipFile(dst).testzip() is None
    print(f"ok: {len(caixas)} caixa(s) {tipo} no objeto {wrapper} -> {dst}")


if __name__ == "__main__":
    main()
