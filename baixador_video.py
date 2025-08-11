import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from yt_dlp import YoutubeDL
import hashlib
from datetime import datetime

# ======================== USUÁRIOS EMBUTIDOS ========================
senha = "senha123"
hash_gerado = hashlib.sha256(senha.encode('utf-8')).hexdigest()
print(hash_gerado)

def carregar_usuarios():
    return [
        {
            "usuario": "admin",
            "senha_hash": "55a5e9e78207b4df8699d60886fa070079463547b095d1a05bc719bb4e6cd251",  # senha123
            "ativo": True,
            "validade": "2099-07-26"
        }
    ]

def verificar_login_json(usuario_input, senha_input):
    usuarios = carregar_usuarios()
    senha_hash_input = hashlib.sha256(senha_input.encode('utf-8')).hexdigest()
    agora = datetime.now()

    for usuario in usuarios:
        if usuario["usuario"] == usuario_input and usuario["senha_hash"] == senha_hash_input:
            if not usuario.get("ativo", True):
                return False, "Licença inativa."
            validade_str = usuario.get("validade", "2099-12-31")
            validade_data = datetime.strptime(validade_str, "%Y-%m-%d")
            if agora > validade_data:
                return False, "Licença expirada."
            return True, "Licença válida."
    return False, "Usuário ou senha inválidos."

# ======================== TELA PRINCIPAL ========================
def iniciar_aplicacao():
    janela = tk.Tk()
    janela.title("🎬 Downloader YouTube, X, IG, etc - por Natan")
    janela.geometry("500x330")
    janela.configure(bg="#1e1e1e")
    janela.resizable(False, False)

    fonte = ("Segoe UI", 11)

    style = ttk.Style(janela)
    style.theme_use('clam')
    style.configure("TProgressbar", thickness=20, troughcolor='#2e2e2e',
                    background='#00cc66', bordercolor='#1e1e1e',
                    lightcolor='#00cc66', darkcolor='#00b359')

    tk.Label(janela, text="⬇️ Multi Downloader", font=("Segoe UI Semibold", 16),
             bg="#1e1e1e", fg="#00ff99").pack(pady=(15, 5))

    tk.Label(janela, text="Cole o link do vídeo (YouTube, Instagram, etc):",
             font=fonte, bg="#1e1e1e", fg="white").pack()

    url_entry = tk.Entry(janela, width=55, font=fonte,
                         bg="#2e2e2e", fg="white", insertbackground="white", relief="flat")
    url_entry.pack(pady=5)

    var_formato = tk.StringVar(value="mp4")

    formato_frame = tk.Frame(janela, bg="#1e1e1e")
    formato_frame.pack(pady=10)

    tk.Radiobutton(formato_frame, text="🎥 MP4 (vídeo)", variable=var_formato, value="mp4",
                   font=fonte, bg="#1e1e1e", fg="white", selectcolor="#2e2e2e", activebackground="#1e1e1e").pack(side="left", padx=20)
    tk.Radiobutton(formato_frame, text="🎵 MP3 (áudio)", variable=var_formato, value="mp3",
                   font=fonte, bg="#1e1e1e", fg="white", selectcolor="#2e2e2e", activebackground="#1e1e1e").pack(side="left", padx=20)

    progresso_label = tk.Label(janela, text="", font=("Segoe UI", 10, "italic"),
                               bg="#1e1e1e", fg="white")
    progresso_label.pack()

    barra = ttk.Progressbar(janela, length=400, mode='determinate')
    barra.pack(pady=10)

    def mostrar_progresso(d):
        if d['status'] == 'downloading':
            percentual_str = d.get('_percent_str', '0.0%').strip()
            try:
                percentual = float(percentual_str.strip('%'))
            except:
                percentual = 0
            barra['value'] = percentual
            progresso_label.config(text=f"📥 Baixando: {percentual_str}")
            janela.update_idletasks()
        elif d['status'] == 'finished':
            progresso_label.config(text="✅ Download finalizado!")
            barra['value'] = 100
            janela.update_idletasks()

    def baixar():
        url = url_entry.get().strip()
        formato = var_formato.get()
        destino = filedialog.askdirectory(title="Escolha onde salvar")

        if not url or not destino:
            messagebox.showerror("Erro", "⚠️ URL ou destino inválido!")
            return

        ydl_opts = {
            'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'progress_hooks': [mostrar_progresso],
            'ffmpeg_location': 'ffmpeg.exe'
        }

        if formato == "mp4":
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'merge_output_format': 'mp4',
            })
        else:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Concluído", "✅ Download finalizado com sucesso!\nFeito por Natan")
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Ocorreu um erro:\n{str(e)}")
            progresso_label.config(text="")
            barra['value'] = 0

    def on_enter(e): botao.config(bg="#00e673")
    def on_leave(e): botao.config(bg="#00cc66")

    botao = tk.Button(janela, text="⬇️ Baixar Agora", command=baixar,
                      bg="#00cc66", fg="white", font=("Segoe UI Semibold", 11),
                      activebackground="#00b359", activeforeground="white",
                      relief="flat", padx=20, pady=8, bd=0)
    botao.pack(pady=10)
    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)

    janela.mainloop()

# ======================== TELA DE LOGIN ========================
def login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    valido, mensagem = verificar_login_json(usuario, senha)
    if valido:
        login_janela.destroy()
        iniciar_aplicacao()
    else:
        messagebox.showerror("Erro", mensagem)

login_janela = tk.Tk()
login_janela.title("🔐 Acesso Restrito")
login_janela.geometry("350x200")
login_janela.configure(bg="#1e1e1e")
login_janela.resizable(False, False)

tk.Label(login_janela, text="🔒 Login de Acesso", font=("Segoe UI", 14, "bold"),
         bg="#1e1e1e", fg="#00ff99").pack(pady=10)

tk.Label(login_janela, text="Usuário:", bg="#1e1e1e", fg="white").pack()
entrada_usuario = tk.Entry(login_janela, font=("Segoe UI", 11),
                           bg="#2e2e2e", fg="white", relief="flat")
entrada_usuario.pack(pady=5)

tk.Label(login_janela, text="Senha:", bg="#1e1e1e", fg="white").pack()
entrada_senha = tk.Entry(login_janela, show="*", font=("Segoe UI", 11),
                         bg="#2e2e2e", fg="white", relief="flat")
entrada_senha.pack(pady=5)

tk.Button(login_janela, text="Entrar", command=login,
          bg="#00cc66", fg="white", font=("Segoe UI", 10),
          activebackground="#00b359", relief="flat", padx=15).pack(pady=10)

login_janela.mainloop()
