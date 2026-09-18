# 🤖 LEGO® MINDSTORMS® EV3 - Color Sorter (Classificador Automático de Cores)

![LEGO EV3 Color Sorter](https://img.shields.io/badge/LEGO-EV3-blue) ![Python](https://img.shields.io/badge/Python-MicroPython-yellow) ![Pybricks](https://img.shields.io/badge/Framework-Pybricks_v2.0-green)

Este repositório contém o código-fonte e a documentação técnica do **Color Sorter**, um protótipo robótico de classificação automática de objetos por cor construído com a plataforma LEGO® MINDSTORMS® EV3 e programado em Python (Pybricks MicroPython).

---

## 📌 Sobre o Projeto

O projeto simula um processo de automação industrial: identificar características de uma peça através de sensores e direcioná-la automaticamente para o compartimento de destino correto, eliminando a necessidade de classificação manual.

- **Curso**: Ciência da Computação (6º Semestre)
- **Instituição**: Faculdade Impacta Tecnologia
- **Disciplina**: Robótica / Automação
- **Orientador**: Prof. Gustavo Molina Figueiredo
- **Integrantes**: Gabriel Araújo, Guilherme Amorim, Matheus Deziderio, Richard Bernardino
- **RAs**: 2401592, 2401694, 2401416, 2401808
---

## 🛠️ Arquitetura de Hardware e Conexões

| Componente | Porta EV3 | Função no Sistema |
| :--- | :---: | :--- |
| **EV3 Brick** | - | Controlador principal e execução do Pybricks MicroPython |
| **Sensor de Cor** | `Port.S3` | Leitura e identificação de cores em tempo real |
| **Sensor de Toque** | `Port.S1` | Referência física (homing/zeramento) da esteira |
| **Motor da Esteira** | `Port.D` | Posicionamento angular para os compartimentos de cor |
| **Motor Alimentador** | `Port.A` | Ejeção mecânica da peça e retorno à posição inicial |

---

## 🔄 Ciclo de Funcionamento

1. **Calibração Inicial (Homing)**:
   - O motor alimentador gira até o fim mecânico e define o ponto zero.
   - O motor da esteira retrocede até acionar o Sensor de Toque (`Port.S1`), estabelecendo a referência zero absoluta.
2. **Escaneamento e Registro**:
   - O Sensor de Cor (`Port.S3`) identifica a cor da peça (Vermelho, Verde, Azul ou Amarelo).
   - O sistema armazena a sequência em uma lista (`color_list`) com capacidade para até 8 peças (ou encerramento antecipado pelo botão central do EV3).
3. **Posicionamento Angular da Esteira**:
   - A esteira se desloca via `run_target()` para a posição angular correspondente:
     - 🔵 **Azul**: 120°
     - 🟢 **Verde**: 240°
     - 🟡 **Amarelo**: 360°
     - 🔴 **Vermelho**: 480°
4. **Ejeção da Peça**:
   - O empurrador desce para liberar a peça no compartimento e passa para a posição da proxima cor a ser ejetada .

---

## 🛡️ Mecanismos de Defesa e Resiliência no Código

Para garantir alta confiabilidade em ambiente físico, a função `ejetar_peca()` implementa estratégias defensivas de software:

- **Controle de Torque e Ângulo Limite**: O motor opera a 700 deg/s com avanço limitado a 170° (evitando impacto contra o fim de curso mecânico em 180°).
- **Detecção de Stall e Timeout**: Utiliza `StopWatch()` e monitoramento `stalled()`. Caso ocorra enrosco mecânico ou o tempo ultrapasse 1200ms, o avanço é interrompido imediatamente para proteger os motores e evitar o congelamento do sistema.
---

## 💻 Requisitos e Instalação

### Pré-requisitos
- Kit **LEGO® MINDSTORMS® EV3 Core Set (45544)**
- Cartão MicroSD com **LEGO® EV3 MicroPython v2.0**
- Visual Studio Code com a extensão oficial **EV3 MicroPython**

### Execução
1. Clone este repositório:
   ```bash
   git clone https://github.com/devbiel12/projeto_esteira_ev3.git
   ```
2. Abra a pasta do projeto no VS Code.
3. Conecte o bloco EV3 via USB ou Wi-Fi/Bluetooth.
4. Execute o arquivo `main.py` diretamente pelo painel do EV3 no VS Code.

---
