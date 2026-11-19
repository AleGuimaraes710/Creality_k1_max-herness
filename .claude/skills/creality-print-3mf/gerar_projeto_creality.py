#!/usr/bin/env python3
"""
Gera um projeto .3mf do Creality Print 7 (base OrcaSlicer) sem abrir o programa.

Como funciona
-------------
Um .3mf e um arquivo ZIP. Num projeto salvo pelo Creality Print ha:
  3D/3dmodel.model                 -> itens na mesa (posicao/rotacao = atributo "transform")
  3D/Objects/object_1.model        -> a malha (vertices e triangulos)
  Metadata/project_settings.config -> JSON com TODAS as configuracoes (impressora, filamento, processo)
  Metadata/model_settings.config   -> nome do objeto e transform de montagem
  (+ miniaturas, plate_1.json, rels)

O script usa um projeto MODELO salvo pelo proprio usuario (com 1 objeto na mesa),
troca a malha, posiciona no centro da mesa, pega as configuracoes de um projeto do
usuario (para herdar os perfis e calibracoes dele) e altera so as chaves pedidas.

Uso
---
  pip install trimesh numpy
  python3 gerar_projeto_creality.py MODELO.3mf CONFIG.3mf peca.stl SAIDA.3mf NOME '{"layer_height":"0.12"}'

  MODELO.3mf : projeto salvo no Creality Print com 1 objeto (so a estrutura e usada)
  CONFIG.3mf : projeto do usuario de onde vem o project_settings (perfil de filamento calibrado)
  peca.stl   : malha ja escalada e orientada (mm). Pode conter varias pecas (vira 1 objeto)
  JSON       : chaves de PROCESSO a alterar. Valores por extrusora vao em lista: {"outer_wall_speed":["80"]}

Regras importantes
------------------
- Nao altere chaves de filamento (filament_*, nozzle_temperature*, hot_plate_temp*, fan_*,
  pressure_advance, slow_down_*) se o usuario calibrou o filamento.
- Para o brim encostar na peca: "brim_object_gap":"0" E "elefant_foot_compensation":"0".
- O script registra as chaves alteradas em different_settings_to_system[0] (processo),
  senao o Creality pode tratar o valor como perfil de fabrica.
"""
import json, re, sys, zipfile

import trimesh

FILAMENT_PREFIXES = ("filament_", "nozzle_temperature", "hot_plate", "textured_plate", "pressure_advance",
                     "enable_pressure", "fan_", "close_fan", "slow_down", "overhang_fan", "additional_cooling",
                     "support_material_interface_fan", "during_print", "complete_print", "activate_air")


def main():
    tmpl, settings_src, mesh_path, dst, name = sys.argv[1:6]
    changes = json.loads(sys.argv[6]) if len(sys.argv) > 6 else {}

    # 1) malha: centraliza na origem em XY e com o meio da altura em z=0 (padrao do Creality)
    mesh = trimesh.load(mesh_path, force="mesh")
    bed_center = (150.0, 150.0)            # K1 Max: mesa 300 x 300
    half_h = mesh.extents[2] / 2
    c = mesh.bounds.mean(axis=0)
    mesh.apply_translation([-c[0], -c[1], -mesh.bounds[0][2] - half_h])

    zin = zipfile.ZipFile(tmpl)
    obj = zin.read("3D/Objects/object_1.model").decode()
    head = obj[:obj.index("<vertices>")]
    tail = obj[obj.index("</triangles>") + len("</triangles>"):]
    verts = "".join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x, y, z in mesh.vertices)
    tris = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c_}"/>' for a, b, c_ in mesh.faces)
    new_obj = head + "<vertices>" + verts + "</vertices><triangles>" + tris + "</triangles>" + tail

    # 2) configuracoes: copia do projeto do usuario e altera so o pedido
    settings = json.loads(zipfile.ZipFile(settings_src).read("Metadata/project_settings.config"))
    diff = settings["different_settings_to_system"]
    proc = [k for k in diff[0].split(";") if k]
    for k, v in changes.items():
        if k not in settings:
            raise SystemExit(f"chave inexistente nesta versao: {k}")
        if k.startswith(FILAMENT_PREFIXES):
            print(f"AVISO: {k} e configuracao de filamento")
        print(f"{k}: {settings[k]} -> {v}")
        settings[k] = v
        if k not in proc:
            proc.append(k)
    diff[0] = ";".join(proc)

    # 3) transform do item na mesa (posicao do centro da peca)
    transform = f"1 0 0 0 1 0 0 0 1 {bed_center[0]} {bed_center[1]} {half_h:.6f}"

    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "3D/Objects/object_1.model":
            data = new_obj.encode()
        elif item.filename == "Metadata/project_settings.config":
            data = json.dumps(settings, indent=4, ensure_ascii=False).encode()
        elif item.filename == "3D/3dmodel.model":
            t = data.decode()
            t, n = re.subn(r'(<item objectid="\d+"[^>]*?transform=")[^"]+(")', r"\g<1>" + transform + r"\2", t)
            assert n == 1, "o modelo precisa ter exatamente 1 objeto na mesa"
            data = t.encode()
        elif item.filename == "Metadata/model_settings.config":
            t = data.decode()
            t = re.sub(r'(assemble_item[^>]*?transform=")[^"]+(")', r"\g<1>" + transform + r"\2", t)
            t = re.sub(r'(<metadata key="name" value=")[^"]*(")', r"\g<1>" + name + r"\2", t)
            data = t.encode()
        zout.writestr(item, data)
    zout.close()

    # 4) conferencia
    assert zipfile.ZipFile(dst).testzip() is None
    print("ok:", dst)


if __name__ == "__main__":
    main()
