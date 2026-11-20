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
- **PETG MASTERPRINT 220/230 °C confirmado por ele em 19/11/2026** (print da tela do Creality). Projetos antigos (`Tampa_ventoinha_PETG_Masterprint.3mf`, `Gaveta_K1_Max_PETG*.3mf`) ainda têm **240/240 °C e mesa 80/85**. Se usar um deles como fonte de configuração, corrija as temperaturas do bico para 230/220 e avise sobre a mesa.
- **PLA FLEXYGREEN 0,4 tem retração de 0,4 mm**, que se sobrepõe aos 0,8 mm da impressora. Com várias peças na mesa (muitas viagens), isso deixou **fios entre as peças** (Queen Rearing, 20/11/2026). Com autorização dele, usou-se 0,8 mm e bico a 205 °C só naquele projeto.
- **Limite de fluxo nas receitas:** fluxo = velocidade × largura × camada, que precisa ficar abaixo de `filament_max_volumetric_speed`. Ao **subir a altura de camada**, baixe as velocidades na mesma proporção. Senão a peça inteira roda no teto, que no PETG a 220 °C é arriscado.
  - Exemplo do que deu errado: camada 0,28 com parede interna 150 e preenchimento 200 (linha 0,45) bateu nos 18 mm³/s. Saíram linhas falhadas, bolinhas e camadas mal grudadas. Ele também tinha trocado o bico sem nivelar, então não deu para isolar a causa.
  - O hotend da K1 Max aguenta 32 mm³/s, mas o limite do PETG depende da temperatura. Os 18 do perfil 0,4 não foram testados no teste de fluxo máximo.

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
  - suporte Organic com folga Z de 0,24 em cima e embaixo (o pacote de perfis de 18/11 saiu com 0,16 e foi corrigido em 20/11);
  - brim só por fora, 3 mm, gap 0, compensação de pé de elefante 0.
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
  - `support_top_z_distance` e `support_bottom_z_distance` = **0,24 mm**: 2 camadas de 0,12 ou 3 camadas de 0,08. Nunca menos que 0,24 em PLA, mesmo com o bico 0,2 (0,16 é apertado demais);
  - `support_interface_top_layers` = 0 e `support_interface_bottom_layers` = 0. A interface inferior solda nos galhos que pousam no próprio boneco;
  - `support_object_xy_distance` 0,6 e `support_xy_overrides_z` = z_overrides_xy;
  - `support_threshold_angle` 40;
  - ponta do galho 0,6–0,8 e galho Organic de 2.
- **Erro anterior:** Tree Slim com XY 0,35, interface inferior 2 e 2 paredes nos galhos colou tanto que ele teve que cortar os suportes.
- **Organic não funciona com altura de camada variável.** Se o projeto tiver `Metadata/layer_heights_profile.txt`, remova o arquivo ou use Tree Slim.
- **Partes finas:**
  - esquis e prancha com cerca de 0,7 mm ficam frágeis; ofereça dobrar para cerca de 1,5 mm, crescendo só por baixo;
  - bastões finos (cerca de 0,5 mm): remova e faça furos de Ø1,0 × 5 mm nas mãos para arame.
- **Base:** aplaine ou preencha a curvatura (camber) da prancha para aumentar o contato com a mesa (de 150 para cerca de 670 mm²).
- **Bloqueador de suporte** embaixo dos bicos da prancha e das pontas dos esquis. Sem ele, saem suportes baixinhos (0,3 a 2 mm), difíceis de tirar, e os bicos sobem devagar (10 a 20°), então imprimem bem sem apoio.
- **Antes de entregar:** estime onde vai ter suporte (faces com inclinação abaixo do limite de 40°, agrupadas por região) e diga onde ele fica. No snowboarder, o bloco maior ficou embaixo do quadril agachado, com cerca de 170 mm².
- **Na hora de tirar o suporte:** espere esfriar totalmente, comece pelos galhos de fora, gire em vez de puxar e use alicate de bico fino ou pinça no bloco maior.
- **Projeto de referência:** `Snowboarder_1-25_PLA_bico_0.2_v5.3mf` (bico 0,2, Detalhe Miniaturas, PLA 0,2 calibrado, Organic com folga de 0,24, bloqueadores nos bicos).

### Peças funcionais (dobradiças, suportes, gavetas)
- 4 paredes, base 5, infill 40% gyroid.
- Parede externa 80 mm/s com aceleração 2500, para precisão.
- **Print-in-place:** meça as folgas por camada (seções em Z).
  - Abaixo de 0,15 mm tende a grudar com bico 0,4.
  - Aumento mínimo: `xy_contour_compensation` −0,05 e `xy_hole_compensation` +0,05, o que soma +0,1 mm na folga.
- **Peça perto do calor da câmara:** PLA amolece a 55–60 °C. Sugira PETG, mas respeite a escolha dele.
- **Alojamento de porca M3:** 5,5 mm entre faces. A compensação de furo ajuda.

### Peças que levam muito esforço (garras de morsa, ferramentas)
- **Exemplo:** garras macias de 50 mm para prender as bengalas (tubos da suspensão KYB) na morsa, em PETG.
- **Orientação:** o aperto deve ficar **no plano das camadas**, nunca empurrando para separá-las. O canal do tubo fica na vertical, e a força da morsa atravessa cada camada. Assim não precisa de suporte.
- **Configuração:**
  - 8 paredes (cerca de 3,6 mm), topo e base com 6 camadas, 60% gyroid;
  - camada 0,2, Arachne;
  - parede externa 100 mm/s, interna 150;
  - brim de 5 mm encostado.
- **Temperatura:** PETG mais quente (cerca de 240 °C) e com menos ventoinha (30 a 50%) cola melhor as camadas, mas foge da calibração dele (220/230 °C, ventoinha 40 a 90%). **Pergunte sempre** antes de usar.
- **O que foi feito nas garras KYB (19/11/2026):**
  - O arquivo herdou 240/240 °C de um projeto antigo. Ele confirmou que o perfil certo é 220/230 °C, e o arquivo foi corrigido.
  - Ventoinha 20–30% só nessa impressão, com autorização dele.
  - **Aba de apoio na morsa:** ele quer que a peça fique apoiada em cima da mandíbula de aço.
    - Faça uma aba (5 mm × 10 mm para trás) no topo da face traseira. Ela entra como segunda parte do objeto (veja `creality-print-3mf`).
    - Não faça rebaixo na traseira se houver um canal profundo na frente: no KYB, sobravam só 7,75 mm de parede atrás do canal.
    - Imprima de cabeça para baixo, com a aba na mesa, sem suporte.
  - **Versão mais rápida:** 6 paredes e 40% gyroid. Camada 0,28 **só com velocidades reduzidas** (veja o limite de fluxo nas notas dos perfis).

### Peças pequenas de apicultura (Queen Rearing System, PLA, bico 0,4)
- **Projeto:** `Queen_Rearing_PLA_FLEXYGREEN_bico0.4.3mf` (20/11/2026): 2 gaiolas de nascimento (20 × 20 × 64,5 mm), 5 cúpulas de 3,5 mm (16 × 16 × 23 mm), tampa e blank, numa mesa só. Origem: .3mf do Bambu Studio com 4 mesas.
- **Base:** camada 0,12, 1ª camada 0,16, 3 paredes Arachne, parede externa com linha de 0,4 mm, a 40 mm/s e aceleração 1500, 15% gyroid.
- **Cúpulas:** ele quis o contrário da orientação do autor: tubo na mesa (~30 mm²), aba de Ø16 mm no meio, copo aberto para cima. Só a aba precisa de suporte; o interior do copo fica limpo.
- **Suporte só em alguns objetos:** `enable_support = 0` no projeto e `<metadata key="enable_support" value="1"/>` só nas cúpulas (no `model_settings.config`). As gaiolas são vazadas: suporte dentro delas não sai.
- **Acabamento embaixo da aba** (escolha dele): Organic com folga Z de 0,24 e XY de 0,6, só a partir da mesa, mais **2 camadas de interface concêntrica com espaçamento 0,2**. Sem interface, solta mais fácil, mas a face fica caída.
- **Brim de 5 mm** em tudo: as peças são altas e têm pouca área na mesa.
- **Camada falhada em todas as peças na mesma altura** = faltou filamento por um instante: carretel prendendo, bico mal apertado depois da troca, filamento úmido ou calor (a tampa estava aberta, então o calor foi descartado). Pergunte em que altura foi.

## Custos (premissas dele, 20/11/2026)
- PLA R$ 120/kg; energia R$ 1,10/kWh (São Paulo, arredondado para cima); K1 Max com ~0,2 kW de média; impressora R$ 4.000 em 5.000 h + R$ 0,20/h de manutenção = R$ 1,22/h de máquina; +10% para falhas.
- O custo da máquina pesa mais que o do plástico em peças pequenas. Divida o custo da mesa pela massa de cada peça.
- **Queen Rearing:** kit de 23 g ≈ R$ 7,74 numa mesa; em mesas cheias, ≈ R$ 5. Preço para o tio dele: kit R$ 10 (avulso) / R$ 8 (em quantidade); atacado R$ 15–18; varejo R$ 25–30.
- Mão de obra não entra no custo; tirar o suporte das cúpulas leva ~1 min cada.

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
- **Engrossar uma parte fina (prancha, esquis):** NÃO desloque vértices pelas normais. Isso deixou bordas serrilhadas, "triângulos" embaixo e defeitos na união com a bota (erro de 17/11/2026).
  - **Método correto:**
    1. Recorte a região da prancha com um prisma do contorno visto de cima. Na parte plana, use z até cerca de 0,9, abaixo das botas; nas pontas, até cerca de 3,5.
    2. Some (union, manifold3d) cópias dessa região deslocadas para baixo em passos de 0,15 mm, até a espessura extra.
    3. Corte plano embaixo (`trim_by_plane`) 0,3 mm acima do ponto mais baixo, para a base ficar plana.
  - O resultado mantém as superfícies originais, fica fechado e com base plana.
- **Depois de mudar a malha:** confira fechada, `is_volume`, dimensões e área de contato, E **renderize de perto** (por baixo, borda lateral, união com a bota) comparando com o original. A conferência numérica sozinha não pega defeito visual.
