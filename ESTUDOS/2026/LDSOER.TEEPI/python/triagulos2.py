import math
import tkinter as tk
from tkinter import messagebox, ttk


def triangulos(lado1, lado2, lado3):
	"""Classifica o triangulo pelos lados."""
	if math.isclose(lado1, lado2) and math.isclose(lado2, lado3):
		return "equilatero"
	if math.isclose(lado1, lado2) or math.isclose(lado1, lado3) or math.isclose(lado2, lado3):
		return "isosceles"
	return "escaleno"


def triangulos2(angulo1, angulo2, angulo3):
	"""Classifica o triangulo pelos angulos."""
	angulos = [angulo1, angulo2, angulo3]
	if any(math.isclose(angulo, 90.0, abs_tol=1e-3) for angulo in angulos):
		return "retangulo"
	if any(angulo > 90.0 for angulo in angulos):
		return "obtusangulo"
	return "acutangulo"


def validar_lados(lado1, lado2, lado3):
	if lado1 <= 0 or lado2 <= 0 or lado3 <= 0:
		return False, "todos os lados devem ser maiores que zero"

	if (lado1 < lado2 + lado3) and (lado2 < lado1 + lado3) and (lado3 < lado1 + lado2):
		return True, "os lados formam um triangulo"

	return False, "os lados nao formam um triangulo"


def validar_angulos(angulo1, angulo2, angulo3):
	if angulo1 <= 0 or angulo2 <= 0 or angulo3 <= 0:
		return False, "todos os angulos devem ser maiores que zero"

	soma = angulo1 + angulo2 + angulo3
	if math.isclose(soma, 180.0, abs_tol=1e-2):
		return True, "os angulos formam um triangulo"

	return False, f"a soma dos angulos deve ser 180 (atual: {soma:.2f})"


class TrianguloApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Classificador de Triangulos")
		self.root.geometry("780x520")
		self.root.resizable(False, False)

		self.campos = {}
		self._criar_layout()

	def _criar_layout(self):
		frame_principal = ttk.Frame(self.root, padding=12)
		frame_principal.pack(fill="both", expand=True)

		frame_entrada = ttk.LabelFrame(frame_principal, text="Entradas")
		frame_entrada.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=4)

		frame_resultado = ttk.LabelFrame(frame_principal, text="Resultado")
		frame_resultado.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=4)

		frame_desenho = ttk.LabelFrame(frame_principal, text="Desenho")
		frame_desenho.grid(row=0, column=1, rowspan=2, sticky="nsew", pady=4)

		frame_principal.columnconfigure(0, weight=1)
		frame_principal.columnconfigure(1, weight=1)
		frame_principal.rowconfigure(0, weight=1)
		frame_principal.rowconfigure(1, weight=1)

		self._criar_entradas(frame_entrada)
		self._criar_resultado(frame_resultado)
		self._criar_canvas(frame_desenho)

	def _criar_entradas(self, parent):
		labels = [
			("lado1", "Primeiro lado"),
			("lado2", "Segundo lado"),
			("lado3", "Terceiro lado"),
			("angulo1", "Primeiro angulo"),
			("angulo2", "Segundo angulo"),
			("angulo3", "Terceiro angulo"),
		]

		for indice, (chave, texto) in enumerate(labels):
			ttk.Label(parent, text=texto + ":").grid(row=indice, column=0, sticky="w", padx=8, pady=4)
			entrada = ttk.Entry(parent, width=18)
			entrada.grid(row=indice, column=1, sticky="w", padx=8, pady=4)
			self.campos[chave] = entrada

		frame_botoes = ttk.Frame(parent)
		frame_botoes.grid(row=len(labels), column=0, columnspan=2, sticky="w", padx=8, pady=8)

		ttk.Button(frame_botoes, text="Validar e classificar", command=self.validar).grid(
			row=0, column=0, padx=(0, 8)
		)
		ttk.Button(frame_botoes, text="Limpar", command=self.limpar).grid(row=0, column=1)

	def _criar_resultado(self, parent):
		self.texto_resultado = tk.Text(parent, height=10, width=48, state="disabled")
		self.texto_resultado.pack(fill="both", expand=True, padx=8, pady=8)

	def _criar_canvas(self, parent):
		self.canvas = tk.Canvas(parent, width=360, height=350, bg="white")
		self.canvas.pack(padx=8, pady=8)
		self._limpar_canvas("Informe os valores e clique em validar")

	def _mostrar_resultado(self, mensagem):
		self.texto_resultado.config(state="normal")
		self.texto_resultado.delete("1.0", tk.END)
		self.texto_resultado.insert(tk.END, mensagem)
		self.texto_resultado.config(state="disabled")

	def _ler_numero(self, chave):
		valor_texto = self.campos[chave].get().strip().replace(",", ".")
		if not valor_texto:
			raise ValueError(f"preencha o campo {chave}")
		return float(valor_texto)

	def validar(self):
		try:
			lado1 = self._ler_numero("lado1")
			lado2 = self._ler_numero("lado2")
			lado3 = self._ler_numero("lado3")
			angulo1 = self._ler_numero("angulo1")
			angulo2 = self._ler_numero("angulo2")
			angulo3 = self._ler_numero("angulo3")
		except ValueError as erro:
			messagebox.showerror("Entrada invalida", str(erro))
			return

		lados_ok, msg_lados = validar_lados(lado1, lado2, lado3)
		angulos_ok, msg_angulos = validar_angulos(angulo1, angulo2, angulo3)

		linhas = [msg_lados]
		if lados_ok:
			linhas.append(f"classificacao por lado: {triangulos(lado1, lado2, lado3)}")

		linhas.append(msg_angulos)
		if angulos_ok:
			linhas.append(f"classificacao por angulo: {triangulos2(angulo1, angulo2, angulo3)}")

		if lados_ok and angulos_ok:
			linhas.append("resultado final: triangulo valido por lado e por angulo")
		else:
			linhas.append("resultado final: condicoes incompletas para triangulo totalmente valido")
			linhas.append("desenho exibido: aproximacao visual com os valores informados")

		self._mostrar_resultado("\n".join(linhas))
		self._desenhar_triangulo(lado1, lado2, lado3, lados_ok)

	def limpar(self):
		for campo in self.campos.values():
			campo.delete(0, tk.END)
		self._mostrar_resultado("")
		self._limpar_canvas("Informe os valores e clique em validar")

	def _limpar_canvas(self, texto=None):
		self.canvas.delete("all")
		if texto:
			self.canvas.create_text(180, 175, text=texto, fill="#444", font=("TkDefaultFont", 11))

	def _desenhar_triangulo(self, lado1, lado2, lado3, lados_validos):
		# Usa modulo e piso minimo para sempre conseguir gerar uma representacao visual.
		lado1_desenho = max(abs(lado1), 1.0)
		lado2_desenho = max(abs(lado2), 1.0)
		lado3_desenho = max(abs(lado3), 1.0)

		ponto_a = (0.0, 0.0)
		ponto_b = (lado1_desenho, 0.0)
		x_c = (lado1_desenho**2 + lado3_desenho**2 - lado2_desenho**2) / (2 * lado1_desenho)
		y_quadrado = lado3_desenho**2 - x_c**2
		desenho_aproximado = False

		if y_quadrado >= 0:
			y_c = math.sqrt(y_quadrado)
		else:
			y_c = 0.0
			desenho_aproximado = True

		if not lados_validos:
			desenho_aproximado = True
			if math.isclose(y_c, 0.0, abs_tol=1e-9):
				y_c = max(lado1_desenho, lado2_desenho, lado3_desenho) * 0.22
				x_c = min(max(x_c, lado1_desenho * 0.10), lado1_desenho * 0.90)

		ponto_c = (x_c, y_c)

		pontos = [ponto_a, ponto_b, ponto_c]
		xs = [p[0] for p in pontos]
		ys = [p[1] for p in pontos]

		min_x, max_x = min(xs), max(xs)
		min_y, max_y = min(ys), max(ys)

		largura = max(max_x - min_x, 1e-6)
		altura = max(max_y - min_y, 1e-6)

		margem = 30
		largura_canvas = int(self.canvas["width"])
		altura_canvas = int(self.canvas["height"])

		area_largura = largura_canvas - 2 * margem
		area_altura = altura_canvas - 2 * margem
		escala_x = area_largura / largura
		escala_y = area_altura / altura
		escala = min(escala_x, escala_y)

		desenho_largura = largura * escala
		desenho_altura = altura * escala
		offset_x = (largura_canvas - desenho_largura) / 2
		offset_y = (altura_canvas - desenho_altura) / 2

		def converter(ponto):
			x = (ponto[0] - min_x) * escala + offset_x
			y = (max_y - ponto[1]) * escala + offset_y
			return x, y

		ax, ay = converter(ponto_a)
		bx, by = converter(ponto_b)
		cx, cy = converter(ponto_c)

		self.canvas.delete("all")
		if lados_validos and not desenho_aproximado:
			cor_borda = "#1f2937"
			cor_fundo = "#dbeafe"
			dash = None
			legenda = "Desenho em escala real dos lados"
		else:
			cor_borda = "#b91c1c"
			cor_fundo = "#fee2e2"
			dash = (6, 4)
			legenda = "Representacao aproximada (lados nao fecham triangulo)"

		self.canvas.create_polygon(
			ax,
			ay,
			bx,
			by,
			cx,
			cy,
			fill=cor_fundo,
			outline=cor_borda,
			width=2,
			dash=dash,
		)
		self.canvas.create_line(ax, ay, bx, by, fill=cor_borda, width=2, dash=dash)
		self.canvas.create_line(bx, by, cx, cy, fill=cor_borda, width=2, dash=dash)
		self.canvas.create_line(cx, cy, ax, ay, fill=cor_borda, width=2, dash=dash)

		self.canvas.create_text(ax - 12, ay + 12, text="A")
		self.canvas.create_text(bx + 12, by + 12, text="B")
		self.canvas.create_text(cx, cy - 12, text="C")
		self.canvas.create_text(
			180,
			330,
			text=legenda,
			fill=cor_borda,
			font=("TkDefaultFont", 9),
		)


if __name__ == "__main__":
	root = tk.Tk()
	app = TrianguloApp(root)
	root.mainloop()
