import tkinter as tk
import requests

def enviar_url():
    url = entry.get()
    resposta = requests.post("http://127.0.0.1:8000/processar-url", json={"url": url})
    if resposta.ok:
        texto.delete("1.0", tk.END)
        texto.insert(tk.END, resposta.json()["texto"])
    else:
        texto.insert(tk.END, "Erro ao processar URL")

root = tk.Tk()
root.title("Gerador de Currículo Inteligente")

tk.Label(root, text="Cole a URL da vaga:").pack()
entry = tk.Entry(root, width=50)
entry.pack()

btn = tk.Button(root, text="Gerar PDF", command=enviar_url)
btn.pack()

texto = tk.Text(root, wrap=tk.WORD, height=20, width=80)
texto.pack()

root.mainloop()
