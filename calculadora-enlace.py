
import math

class CalculadoraEnlaceWireless:
    def __init__(self):
        self.valor_conector = 0.2
        self.valor_pigtail = 1.5
        self.perdas_cabos_padrao = {
            2.45: {1: 1.05, 2: 0.5},
            5.0: {1: 1.3, 2: 0.3},
            5.8: {1: 1.7, 2: 0.93},
        }
        self.nomes_cabos = {1: "RG-58", 2: "RG-213"}

    def fmt(self, valor, casas=2):
        return f"{valor:.{casas}f}".replace('.', ',')

    def limpar(self):
        print("\n" * 2)

    def entrada_numero(self, texto):
        while True:
            bruto = input(texto).strip().replace(',', '.')
            try:
                return float(bruto)
            except ValueError:
                print("Valor inválido. Digite usando número, por exemplo: 2,45")

    def entrada_inteiro(self, texto, minimo=0):
        while True:
            valor = self.entrada_numero(texto)
            if int(valor) == valor and valor >= minimo:
                return int(valor)
            print(f"Digite um número inteiro maior ou igual a {minimo}.")

    def entrada_opcao_cabo(self, texto):
        while True:
            print(texto)
            print("1 - RG-58")
            print("2 - RG-213")
            op = input("Escolha uma opção: ").strip()
            if op in ("1", "2"):
                return int(op)
            print("Opção inválida. Escolha 1 ou 2.")

    def entrada_frequencia(self, texto):
        while True:
            valor = round(self.entrada_numero(texto), 2)
            if valor in (2.45, 5.0, 5.8):
                return valor
            print("A frequência deve ser 2,45, 5,0 ou 5,8.")

    def perda_espaco_livre(self, distancia_km, frequencia_ghz):
        return 92.5 + 20 * math.log10(distancia_km * frequencia_ghz)

    def cadastrar_cabo(self, lado, indice, frequencia):
        print(f"\nCabo {indice} do {lado}:")
        comprimento = self.entrada_numero("Comprimento (m) = ")
        tipo = self.entrada_opcao_cabo("Tipo do cabo:")
        nome_tipo = self.nomes_cabos[tipo]

        if frequencia in self.perdas_cabos_padrao and tipo in self.perdas_cabos_padrao[frequencia]:
            perda_padrao = self.perdas_cabos_padrao[frequencia][tipo]
            usar_padrao = input(f"Usar perda padrão {self.fmt(perda_padrao)} dB/m para {nome_tipo}? (s/n): ").strip().lower()
            if usar_padrao == 's':
                perda_m = perda_padrao
            else:
                perda_m = self.entrada_numero("Digite a perda dB/m: ")
        else:
            perda_m = self.entrada_numero("Digite a perda dB/m: ")

        perda_total = comprimento * perda_m
        nome_final = nome_tipo if perda_m == self.perdas_cabos_padrao.get(frequencia, {}).get(tipo, 0) else f"Custom ({self.fmt(perda_m)} dB/m)"

        return {
            'indice': indice,
            'comprimento': comprimento,
            'tipo': tipo,
            'nome': nome_final,
            'perda_m': perda_m,
            'perda_total': perda_total,
        }

    def cadastrar_cabos(self, lado, frequencia):
        cabos = []
        quantidade = self.entrada_inteiro(f"Quantidade de cabos no {lado} = ", minimo=1)
        for i in range(1, quantidade + 1):
            cabo = self.cadastrar_cabo(lado, i, frequencia)
            cabos.append(cabo)
        return cabos

    def resumo_cabos(self, cabos):
        partes = []
        for cabo in cabos:
            partes.append(f"Cabo {cabo['indice']}: {cabo['nome']} {self.fmt(cabo['comprimento'])}m")
        return ' | '.join(partes)

    def expressao_cabos(self, cabos):
        partes = []
        for cabo in cabos:
            partes.append(f"({self.fmt(cabo['comprimento'])} x {self.fmt(cabo['perda_m'])})")
        return ' + '.join(partes)

    def total_perdas_cabos(self, cabos):
        return sum(cabo['perda_total'] for cabo in cabos)

    def revisar_dados(self, dados):
        print("\n" + "=" * 72)
        print("REVISÃO DOS DADOS")
        print("=" * 72)
        for i, item in enumerate(dados, start=1):
            print(f"{i}. {item}")
        print("=" * 72)

    def modo_simples(self):
        self.limpar()
        print("=" * 72)
        print("MODO SIMPLES")
        print("=" * 72)

        p_ap1 = self.entrada_numero("Potência AP-1 = ")
        s_ap2 = self.entrada_numero("Sensibilidade AP-2 = ")
        protetor_tx = self.entrada_inteiro("Quantidade de protetores de surtos no TX = ", minimo=0)
        protetor_rx = self.entrada_inteiro("Quantidade de protetores de surtos no RX = ", minimo=0)
        ga1 = self.entrada_numero("Ganho da Antena-1 (GA-1) = ")
        ga2 = self.entrada_numero("Ganho da Antena-2 (GA-2) = ")
        distancia = self.entrada_numero("Distância entre Antenas (D) em km = ")
        frequencia = self.entrada_frequencia("Frequência de Transmissão (2,45, 5,0 ou 5,8) = ")

        print("\n--- CABOS DO TX ---")
        cabos_tx = self.cadastrar_cabos("TX", frequencia)
        print("\n--- CABOS DO RX ---")
        cabos_rx = self.cadastrar_cabos("RX", frequencia)

        pigtail_tx = self.entrada_inteiro("Quantidade de pigtails no TX = ", minimo=0)
        pigtail_rx = self.entrada_inteiro("Quantidade de pigtails no RX = ", minimo=0)

        dados = [
            f"Potência AP-1: {self.fmt(p_ap1)} dBm",
            f"Sensibilidade AP-2: {self.fmt(s_ap2)} dBm",
            f"Protetores de surtos no TX: {protetor_tx}",
            f"Protetores de surtos no RX: {protetor_rx}",
            f"Ganho da Antena-1 (GA-1): {self.fmt(ga1)} dBi",
            f"Ganho da Antena-2 (GA-2): {self.fmt(ga2)} dBi",
            f"Distância entre Antenas (D): {self.fmt(distancia)} km",
            f"Frequência de Transmissão: {self.fmt(frequencia)} GHz",
            f"Cabos do TX: {self.resumo_cabos(cabos_tx)}",
            f"Cabos do RX: {self.resumo_cabos(cabos_rx)}",
            f"Quantidade de pigtails no TX: {pigtail_tx}",
            f"Quantidade de pigtails no RX: {pigtail_rx}",
        ]
        self.revisar_dados(dados)

        if input("Confirmar e calcular? (s/n): ").strip().lower() != 's':
            return

        perda_con_tx = len(cabos_tx) * 2 * self.valor_conector
        perda_con_rx = len(cabos_rx) * 2 * self.valor_conector
        perda_pig_tx = pigtail_tx * self.valor_pigtail
        perda_pig_rx = pigtail_rx * self.valor_pigtail
        perda_prot_tx = protetor_tx * 2.0
        perda_prot_rx = protetor_rx * 2.0
        perda_cabos_tx = self.total_perdas_cabos(cabos_tx)
        perda_cabos_rx = self.total_perdas_cabos(cabos_rx)

        perdas_tx = perda_cabos_tx + perda_con_tx + perda_pig_tx + perda_prot_tx
        perdas_rx = perda_cabos_rx + perda_con_rx + perda_pig_rx + perda_prot_rx

        p_irradiada = p_ap1 - perdas_tx + ga1
        p_espaco = self.perda_espaco_livre(distancia, frequencia)
        s_efetiva = ga2 - perdas_rx + s_ap2
        p_link = p_irradiada - p_espaco + s_efetiva

        self.limpar()
        print("=" * 72)
        print("SOLUÇÃO PASSO A PASSO - MODO SIMPLES")
        print("=" * 72)
        print("\n1. Potência efetivamente irradiada:")
        print(f"P_irradiada = {self.fmt(p_ap1)} - ({self.fmt(perda_pig_tx)} + {self.fmt(perda_prot_tx)} + ({len(cabos_tx)*2} x {self.fmt(self.valor_conector,1)}) + {self.expressao_cabos(cabos_tx)}) + {self.fmt(ga1)}")
        print(f"P_irradiada = {self.fmt(p_irradiada)} dB")

        print("\n2. Perda no espaço livre:")
        print(f"P_espaco = 92,5 + 20 log ({self.fmt(distancia)} x {self.fmt(frequencia)})")
        print(f"P_espaco = {self.fmt(p_espaco)} dB")

        print("\n3. Sensibilidade efetiva do receptor:")
        print(f"S_efetiva = {self.fmt(ga2)} - (({len(cabos_rx)*2} x {self.fmt(self.valor_conector,1)}) + {self.expressao_cabos(cabos_rx)} + {self.fmt(perda_prot_rx)} + {self.fmt(perda_pig_rx)}) + {self.fmt(s_ap2)}")
        print(f"S_efetiva = {self.fmt(s_efetiva)} dB")

        print("\n4. P_link (Fade Margin):")
        print(f"P_link = {self.fmt(p_irradiada)} - {self.fmt(p_espaco)} + {self.fmt(s_efetiva)}")
        print(f"P_link = {self.fmt(p_link)} dB")
        print("\n" + "=" * 72)
        print(f"Resultado final: {self.fmt(p_link)} dB")
        print("=" * 72)

    def modo_repetidor(self):
        self.limpar()
        print("=" * 72)
        print("MODO COM REPETIDOR PASSIVO")
        print("=" * 72)

        p_ap1 = self.entrada_numero("Potência AP1 = ")
        s_ap2 = self.entrada_numero("Sensibilidade AP2 = ")
        protetor_tx = self.entrada_inteiro("Quantidade de protetores de surtos no TX = ", minimo=0)
        protetor_rx = self.entrada_inteiro("Quantidade de protetores de surtos no RX = ", minimo=0)
        ga1 = self.entrada_numero("Ganho da Antena1 (GA-1) = ")
        ga2 = self.entrada_numero("Ganho da Antena2 (GA-2) = ")
        ga3 = self.entrada_numero("Ganho da Antena3 (GA-3) = ")
        ga4 = self.entrada_numero("Ganho da Antena4 (GA-4) = ")
        d1 = self.entrada_numero("Distância entre Antenas (D1) em km = ")
        d2 = self.entrada_numero("Distância entre Antenas (D2) em km = ")
        f1 = self.entrada_frequencia("Frequência de Transmissão F1 (2,45, 5,0 ou 5,8) = ")
        f2 = self.entrada_frequencia("Frequência de Transmissão F2 (2,45, 5,0 ou 5,8) = ")

        print("\n--- CABOS DO TX ---")
        cabos_tx = self.cadastrar_cabos("TX", f1)
        print("\n--- CABOS DO RX ---")
        cabos_rx = self.cadastrar_cabos("RX", f2)

        pigtail_tx = self.entrada_inteiro("Quantidade de pigtails no TX = ", minimo=0)
        pigtail_rx = self.entrada_inteiro("Quantidade de pigtails no RX = ", minimo=0)

        dados = [
            f"Potência AP1: {self.fmt(p_ap1)} dBm",
            f"Sensibilidade AP2: {self.fmt(s_ap2)} dBm",
            f"Protetores de surtos no TX: {protetor_tx}",
            f"Protetores de surtos no RX: {protetor_rx}",
            f"Ganho da Antena1 (GA-1): {self.fmt(ga1)} dBi",
            f"Ganho da Antena2 (GA-2): {self.fmt(ga2)} dBi",
            f"Ganho da Antena3 (GA-3): {self.fmt(ga3)} dBi",
            f"Ganho da Antena4 (GA-4): {self.fmt(ga4)} dBi",
            f"Distância entre Antenas (D1): {self.fmt(d1)} km",
            f"Distância entre Antenas (D2): {self.fmt(d2)} km",
            f"Frequência de Transmissão F1: {self.fmt(f1)} GHz",
            f"Frequência de Transmissão F2: {self.fmt(f2)} GHz",
            f"Cabos do TX: {self.resumo_cabos(cabos_tx)}",
            f"Cabos do RX: {self.resumo_cabos(cabos_rx)}",
            f"Quantidade de pigtails no TX: {pigtail_tx}",
            f"Quantidade de pigtails no RX: {pigtail_rx}",
        ]
        self.revisar_dados(dados)

        if input("Confirmar e calcular? (s/n): ").strip().lower() != 's':
            return

        perda_con_tx = len(cabos_tx) * 2 * self.valor_conector
        perda_con_rx = len(cabos_rx) * 2 * self.valor_conector
        perda_pig_tx = pigtail_tx * self.valor_pigtail
        perda_pig_rx = pigtail_rx * self.valor_pigtail
        perda_prot_tx = protetor_tx * 2.0
        perda_prot_rx = protetor_rx * 2.0
        perda_cabos_tx = self.total_perdas_cabos(cabos_tx)
        perda_cabos_rx = self.total_perdas_cabos(cabos_rx)

        perdas_tx = perda_cabos_tx + perda_con_tx + perda_pig_tx + perda_prot_tx
        perdas_rx = perda_cabos_rx + perda_con_rx + perda_pig_rx + perda_prot_rx

        p_irradiada = p_ap1 - perdas_tx + ga1
        lfs1 = self.perda_espaco_livre(d1, f1)
        g_rep = ga2 + ga3
        lfs2 = self.perda_espaco_livre(d2, f2)
        s_efetiva = ga4 - perdas_rx + s_ap2
        p_link = p_irradiada - lfs1 + g_rep - lfs2 + s_efetiva

        self.limpar()
        print("=" * 72)
        print("SOLUÇÃO PASSO A PASSO - MODO REPETIDOR PASSIVO")
        print("=" * 72)
        print("\n1. Potência efetivamente irradiada:")
        print(f"P_irradiada = {self.fmt(p_ap1)} - ({self.fmt(perda_pig_tx)} + {self.fmt(perda_prot_tx)} + ({len(cabos_tx)*2} x {self.fmt(self.valor_conector,1)}) + {self.expressao_cabos(cabos_tx)}) + {self.fmt(ga1)}")
        print(f"P_irradiada = {self.fmt(p_irradiada)} dB")

        print("\n2. Perda no espaço livre do trecho 1:")
        print(f"Lfs1 = 92,5 + 20 log ({self.fmt(d1)} x {self.fmt(f1)})")
        print(f"Lfs1 = {self.fmt(lfs1)} dB")

        print("\n3. Ganho do repetidor passivo:")
        print(f"G_rep = {self.fmt(ga2)} + {self.fmt(ga3)}")
        print(f"G_rep = {self.fmt(g_rep)} dBi")

        print("\n4. Perda no espaço livre do trecho 2:")
        print(f"Lfs2 = 92,5 + 20 log ({self.fmt(d2)} x {self.fmt(f2)})")
        print(f"Lfs2 = {self.fmt(lfs2)} dB")

        print("\n5. Sensibilidade efetiva do receptor:")
        print(f"S_efetiva = {self.fmt(ga4)} - (({len(cabos_rx)*2} x {self.fmt(self.valor_conector,1)}) + {self.expressao_cabos(cabos_rx)} + {self.fmt(perda_prot_rx)} + {self.fmt(perda_pig_rx)}) + {self.fmt(s_ap2)}")
        print(f"S_efetiva = {self.fmt(s_efetiva)} dB")

        print("\n6. P_link (Fade Margin):")
        print(f"P_link = {self.fmt(p_irradiada)} - {self.fmt(lfs1)} + {self.fmt(g_rep)} - {self.fmt(lfs2)} + {self.fmt(s_efetiva)}")
        print(f"P_link = {self.fmt(p_link)} dB")
        print("\n" + "=" * 72)
        print(f"Resultado final: {self.fmt(p_link)} dB")
        print("=" * 72)

    def menu(self):
        while True:
            self.limpar()
            print("=" * 72)
            print("CALCULADORA DE ENLACE WIRELESS")
            print("1 - Modo simples")
            print("2 - Modo com repetidor passivo")
            print("0 - Sair")
            print("=" * 72)
            op = input("Escolha uma opção: ").strip()
            if op == '1':
                self.modo_simples()
                input("\nPressione ENTER para voltar ao menu...")
            elif op == '2':
                self.modo_repetidor()
                input("\nPressione ENTER para voltar ao menu...")
            elif op == '0':
                break
            else:
                print("Opção inválida.")
                input("Pressione ENTER para continuar...")


if __name__ == '__main__':
    CalculadoraEnlaceWireless().menu()
