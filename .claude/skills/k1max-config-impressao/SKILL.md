---
name: k1max-config-impressao
description: Perfis, regras e receitas de configuração de impressão para a Creality K1 Max do Alexandre (PLA FLEXYGREEN, PETG MASTERPRINT, bicos 0,4 e 0,2). Use ao preparar, revisar ou ajustar qualquer impressão dele.
---

# Configuração de impressão – K1 Max do Alexandre

## Equipamento
- **Impressora:** Creality K1 Max, fechada, mesa 300 × 300 × 300, centro da mesa em (150, 150).
- **Fatiador:** Creality Print 7.3 (base OrcaSlicer), interface em inglês, modo Expert.
- **Mesa:** `curr_bed_type = High Temp Plate` (usa `hot_plate_temp`).
- **Bicos:**
  - **0,4**: padrão, perfil de sistema `Creality K1 Max 0.4 nozzle`.
  - **0,2**: perfil de usuário `Creality K1 Max 0.2 nozzle`, importado do pacote da Creality. Herda do 0,4.
  - 0,6 e 0,8 existem como perfis de sistema, mas não são usados.
- **Modelagem:** ele projeta no Fusion 360 e no SolidCraft.

## Perfis de filamento (calibrados por ele, não alterar sem pedir)

| | PLA FLEXYGREEN (0,4) | PLA FLEXYGREEN @…0.2 nozzle | PETG MASTERPRINT (0,4) | PETG MASTERPRINT @…0.2 nozzle |
|---|---|---|---|---|
| Bico / 1ª camada | 210 / 215 °C | 210 / 215 °C | 220 / 230 °C | 220 / 230 °C |
| Mesa / 1ª camada | 50 / 50 | 50 / 50 | 75 / 80 (textured 75/75) | igual |
| Flow ratio | 0.98 | **1.035** (calibrado) | 0.95 | 0.95 (calibrar) |
| Pressure advance | 0.052 | **0.20** (calibrado) | 0.025 | 0.025 (referência Creality: 0.29) |
| Retração do filamento | 0.4 mm @ 40/40 | 0.4 | 0.7 | 0.7 |
| Fluxo máximo | 20 mm³/s | **5** (teste sem falha até 5) | 18 | 2.5 |
| Ventoinha | 100 / 100, lateral 80 | igual | 40–90, interface 100 | igual |
| slow_down_layer_time | 0 | 8 | 8 | 8 |

Notas:
- `enable_filament_dynamic_map = 0`, então `material_flow_temp_graph` não tem efeito.
- Mudar `slow_down_layer_time` para 8 em peças pequenas é uma mudança de filamento. Avise ou pergunte antes.

## Processos de usuário (bico 0,2)
- **0.10mm Standard @Creality K1 Max 0.2 nozzle**, valores da wiki da Creality:
  - camada 0,10, 1ª camada 0,14;
  - linha 0,22 (topo e 1ª camada 0,25);
  - 4 paredes, topo 7, base 5, infill 15% grid;
  - velocidades: externa 110, interna 130, infill 120, topo 100, 1ª camada 18;
  - aceleração 3000 nas paredes, 2000 na 1ª camada e no topo; jerk 3.
- **0.08mm Detalhe Miniaturas @Creality K1 Max 0.2 nozzle:**
  - camada 0,08, 1ª camada 0,12, Arachne, 4 paredes, topo 8, base 6, gyroid 15%;
  - velocidades: externa 60, interna 100, topo 80;
  - suporte Organic; brim só por fora, 3 mm, gap 0, compensação de pé de elefante 0.
- **Limite de velocidade do bico 0,2:** velocidade ≤ fluxo máximo ÷ (largura × camada). Exemplo: 0,22 × 0,08 a 150 mm/s dá 2,6 mm³/s.

## Regras do Alexandre
1. Não mexer em filamento sem pedir.
2. O brim encosta na peça só com **gap 0 e compensação de pé de elefante 0**.
   - Exceção: em peças print-in-place com folga pequena no chão, a compensação evita que a 1ª camada grude. Explique a troca e deixe ele decidir.
3. Perguntar sobre qualquer melhoria (espessura, folga, material) antes de aplicar.
4. Entregar o .3mf pronto, salvar em `C:\Users\alemg\Downloads` e mandar o checklist.
5. PLA com a tampa aberta.
6. Não usar repair automático de malha.

## Receitas por tipo de peça

### Miniaturas e bonecos (maquete 1:25 da esteira de esqui)
- **Escala:** pela altura do corpo. Pessoa agachada: cerca de 1,50 m, o que dá **60 mm** em 1:25. Nunca pela maior dimensão (bastões abertos enganam).
- **Bico 0,2** com o processo Detalhe Miniaturas, ou bico 0,4 com camada 0,12, 3 paredes e linha externa 0,4.
- **Suporte Organic**, configurado para soltar fácil:
  - `support_top_z_distance` e `support_bottom_z_distance` = 2 camadas (0,24 com camada 0,12; 0,16 com camada 0,08);
  - `support_interface_top_layers` = 0 e `support_interface_bottom_layers` = 0. A interface inferior solda nos galhos que pousam no próprio boneco;
  - `support_object_xy_distance` 0,6 e `support_xy_overrides_z` = z_overrides_xy;
  - `support_threshold_angle` 40;
  - ponta do galho 0,6–0,8 e galho Organic de 2.
- **Erro anterior:** Tree Slim com XY 0,35, interface inferior 2 e 2 paredes nos galhos colou tanto que ele teve que cortar os suportes.
- **Organic não funciona com altura de camada variável.** Se o projeto tiver `Metadata/layer_heights_profile.txt`, remova o arquivo ou use Tree Slim.
- **Partes finas:**
  - esquis e prancha com cerca de 0,7 mm ficam frágeis; ofereça dobrar para cerca de 1,5 mm, crescendo só por baixo;
  - bastões finos (cerca de 0,5 mm): remova e faça furos de Ø1,0 × 5 mm nas mãos para arame.
- **Base:** aplaine ou preencha a curvatura (camber) da prancha para aumentar o contato com a mesa (de 150 para cerca de 580 mm²).

### Peças funcionais (dobradiças, suportes, gavetas)
- 4 paredes, base 5, infill 40% gyroid.
- Parede externa 80 mm/s com aceleração 2500, para precisão.
- **Print-in-place:** meça as folgas por camada (seções em Z).
  - Abaixo de 0,15 mm tende a grudar com bico 0,4.
  - Aumento mínimo: `xy_contour_compensation` −0,05 e `xy_hole_compensation` +0,05, o que soma +0,1 mm na folga.
- **Peça perto do calor da câmara:** PLA amolece a 55–60 °C. Sugira PETG, mas respeite a escolha dele.
- **Alojamento de porca M3:** 5,5 mm entre faces. A compensação de furo ajuda.

### Peças de encaixe e furos
- Furos verticais saem menores no PLA. Use `xy_hole_compensation` de 0,05 a 0,1.
- Tolerância de furo: ele já usou um perfil "0.20mm PLA FLEXY 0.07 tolerancia furo".

## Orientação
- Teste orientações com trimesh comparando área de contato e área em balanço acima de 45°.
- Peças altas e finas: brim de 3 a 5 mm e aceleração mais baixa.
- Verifique se não há partes "flutuando" (ilhas sem apoio). Já aconteceu de uma aleta da tampa da ventoinha ficar solta no ar.

## Lições de malha (GLB do Tripo e outros)
- GLB é Y-up: gire 90° em X. Pode usar `KHR_mesh_quantization` (o trimesh lê).
- Reduza para cerca de 200–250 mil faces com `fast_simplification`.
- Corrija a orientação das faces com `trimesh.repair.fix_winding`/`fix_inversion` antes de booleanas e de medir espessura (manifold dá `NotManifold`).
- Malha gerada por marching cubes sai com volume negativo: inverta com `faces[:, ::-1]`.
- **Engrossar uma parte fina:** desloque só os vértices voltados para baixo da região (normal com z < −0,3) pela própria espessura medida por raio (embree), e os da lateral pela metade.
  - Inclua os vértices embaixo das botas, mesmo que não sejam finos; senão fica um degrau.
- **Base plana:** uma extrusão do contorno da seção, recuada 0,06 mm, de −0,05 até h, unida e depois cortada em z = 0. Isso evita arestas coincidentes.
- Depois de mudar a malha, confira: fechada, `is_volume`, dimensões e área de contato.
