Uma calculadora de enlace de rádio (RF) robusta, desenvolvida originalmente em **Python** e adaptada para **HTML/JavaScript** para fácil integração em blogs (Blogger/WordPress) ou hospedagem via GitHub Pages.

Este projeto permite calcular o balanço de potência de um enlace wireless, considerando ganhos de antena, perdas em cabos, conectores e acessórios, além de oferecer um modo para **Repetidor Passivo**.

## 🚀 Funcionalidades

- **Modo Ponto a Ponto (Simples):** Cálculo direto entre Transmissor (TX) e Receptor (RX).
- **Modo Repetidor Passivo:** Cálculo de enlaces com espelhos ou repetidores sem eletrônica ativa.
- **Gestão de Cabos Dinâmica:** Adicione múltiplos segmentos de cabos em ambos os lados.
- **Base de Dados Editável:** Sugestões de perda (dB/m) para RG-58 e RG-213 conforme a frequência (2.45, 5.0 e 5.8 GHz), com opção de ajuste manual.
- **Memorial de Cálculo:** Exibição do passo a passo das fórmulas utilizadas.

## 📐 Lógica de Cálculo

A ferramenta utiliza as fórmulas fundamentais de propagação:

1. **EIRP (Potência Irradiada):** $P_{tx} - Perdas + Ganho_{antena}$
2. **FSL (Perda de Espaço Livre):** $92.5 + 20 \log_{10}(D \times F)$
3. **Margem de Link (Fade Margin):** $EIRP - FSL + Sensibilidade_{efetiva}$
