#!/usr/bin/env python3
"""
Altera configuracoes de um projeto .3mf do Creality Print 7 SEM abrir o programa.
Mantem malhas, posicoes e objetos intactos; muda so o Metadata/project_settings.config.

Uso:
  python3 alterar_config_3mf.py ENTRADA.3mf SAIDA.3mf '{"wall_loops":"4","outer_wall_speed":["80"]}' [--sem-altura-variavel]

- Cada chave alterada e registrada no grupo certo de different_settings_to_system
  ([0] processo, [1] filamento, [2] impressora).
- Chaves de filamento geram AVISO (regra: so mudar com autorizacao do Alexandre).
- --sem-altura-variavel remove Metadata/layer_heights_profile.txt (necessario para suporte Organic).
"""
import json, sys, zipfile

FILAMENTO = ("filament_", "nozzle_temperature", "hot_plate", "textured_plate", "cool_plate", "eng_plate",
             "pressure_advance", "enable_pressure", "fan_", "close_fan", "slow_down", "overhang_fan",
             "additional_cooling", "support_material_interface_fan", "full_fan", "reduce_fan",
             "chamber_temperature", "material_flow", "enable_filament")
IMPRESSORA = ("nozzle_diameter", "max_layer_height", "min_layer_height", "retraction_", "deretraction_",
              "z_hop", "retract_", "wipe", "curr_bed_type", "printer_", "machine_", "travel_slope")


def grupo(k):
    if k.startswith(FILAMENTO):
        return 1
    if k.startswith(IMPRESSORA) or k == "wipe_distance":
        return 2
    return 0


def main():
    src, dst, mudancas = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
    sem_var = "--sem-altura-variavel" in sys.argv
    zin = zipfile.ZipFile(src)
    s = json.loads(zin.read("Metadata/project_settings.config"))
    diff = s["different_settings_to_system"]
    grupos = [[k for k in diff[i].split(";") if k] for i in range(3)]
    for k, v in mudancas.items():
        if k not in s:
            raise SystemExit(f"chave inexistente nesta versao: {k}")
        if isinstance(s[k], list) and not isinstance(v, list):
            v = [v] * len(s[k])
        g = grupo(k)
        if g == 1:
            print(f"AVISO: {k} e configuracao de FILAMENTO")
        print(f"{k}: {s[k]} -> {v}")
        s[k] = v
        if k not in grupos[g]:
            grupos[g].append(k)
    for i in range(3):
        diff[i] = ";".join(grupos[i])

    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    for item in zin.infolist():
        if sem_var and item.filename == "Metadata/layer_heights_profile.txt":
            print("removida altura de camada variavel")
            continue
        data = zin.read(item.filename)
        if item.filename == "Metadata/project_settings.config":
            data = json.dumps(s, indent=4, ensure_ascii=False).encode()
        zout.writestr(item, data)
    zout.close()

    # conferencia
    zc = zipfile.ZipFile(dst)
    assert zc.testzip() is None
    assert all(zin.read(n) == zc.read(n) for n in zin.namelist() if n.startswith("3D/"))
    c = json.loads(zc.read("Metadata/project_settings.config"))
    for k in ["printer_settings_id", "nozzle_diameter", "filament_settings_id", "nozzle_temperature",
              "hot_plate_temp", "filament_flow_ratio", "pressure_advance", "layer_height", "enable_support",
              "support_style", "brim_type", "brim_object_gap", "elefant_foot_compensation"]:
        print(f"  ✓ {k}: {c.get(k)}")
    print("ok:", dst)


if __name__ == "__main__":
    main()
