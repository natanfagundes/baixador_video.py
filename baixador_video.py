import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from yt_dlp import YoutubeDL
import hashlib
from datetime import datetime
import re

# Função para carregar usuários (hardcoded)
def carregar_usuarios():
    return [
        {
            "usuario": "admin",
            "senha_hash": "55a5e9e78207b4df8699d60886fa070079463547b095d1a05bc719bb4e6cd251",  # senha123
            "ativo": True,
            "validade": "2099-07-26"
        }
    ]

# Função para verificar login
def verificar_login(usuario, senha):
    usuarios = carregar_usuarios()
    senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
    agora = datetime.now()

    for user in usuarios:
        if user["usuario"] == usuario and user["senha_hash"] == senha_hash:
            if not user["ativo"]:
                return False, "Licença inativa!"
            validade = datetime.strptime(user["validade"], "%Y-%m-%d")
            if agora > validade:
                return False, "Licença expirada!"
            return True, "Login bem-sucedido!"
    return False, "Usuário ou senha inválidos!"

# Função para tela de login
def tela_login():
    janela_login = tk.Tk()
    janela_login.title("🔐 Login")
    janela_login.geometry("300x180")
    janela_login.configure(bg="#1e1e1e")
    janela_login.resizable(False, False)

    tk.Label(janela_login, text="🔒 Login", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="#00ff99").pack(pady=10)

    tk.Label(janela_login, text="Usuário:", bg="#1e1e1e", fg="white").pack()
    entrada_usuario = tk.Entry(janela_login, bg="#2e2e2e", fg="white", relief="flat")
    entrada_usuario.pack(pady=5)

    tk.Label(janela_login, text="Senha:", bg="#1e1e1e", fg="white").pack()
    entrada_senha = tk.Entry(janela_login, show="*", bg="#2e2e2e", fg="white", relief="flat")
    entrada_senha.pack(pady=5)

    def fazer_login():
        usuario = entrada_usuario.get().strip()
        senha = entrada_senha.get().strip()
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha usuário e senha!")
            return
        valido, mensagem = verificar_login(usuario, senha)
        if valido:
            janela_login.destroy()
            tela_principal()
        else:
            messagebox.showerror("Erro", mensagem)

    tk.Button(janela_login, text="Entrar", command=fazer_login, bg="#00cc66", fg="white", relief="flat").pack(pady=10)

    janela_login.mainloop()

# Função para tela principal
def tela_principal():
    janela = tk.Tk()
    janela.title("⬇️ Downloader de Vídeos e Áudios")
    janela.geometry("500x400")
    janela.configure(bg="#1e1e1e")
    janela.resizable(False, False)

    # Estilo para a barra de progresso
    style = ttk.Style(janela)
    style.configure("TProgressbar", background="#00cc66", troughcolor="#2e2e2e")

    tk.Label(janela, text="⬇️ Downloader", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#00ff99").pack(pady=10)

    tk.Label(janela, text="Cole o link do vídeo:", bg="#1e1e1e", fg="white").pack()
    url_entry = tk.Entry(janela, width=50, bg="#2e2e2e", fg="white", relief="flat")
    url_entry.pack(pady=5)

    tk.Label(janela, text="Caminho do ffmpeg (opcional):", bg="#1e1e1e", fg="white").pack()
    ffmpeg_path_entry = tk.Entry(janela, width=50, bg="#2e2e2e", fg="white", relief="flat")
    ffmpeg_path_entry.insert(0, r"C:\\Users\\natan\\Desktop\\dist_v2\\ffmpeg.exe")  # Caminho fixo como padrão
    ffmpeg_path_entry.pack(pady=5)

    formato = tk.StringVar(value="mp4")
    frame_formato = tk.Frame(janela, bg="#1e1e1e")
    frame_formato.pack(pady=10)
    tk.Radiobutton(frame_formato, text="🎥 Vídeo (MP4)", variable=formato, value="mp4", bg="#1e1e1e", fg="white", selectcolor="#2e2e2e").pack(side="left", padx=10)
    tk.Radiobutton(frame_formato, text="🎵 Áudio (MP3)", variable=formato, value="mp3", bg="#1e1e1e", fg="white", selectcolor="#2e2e2e").pack(side="left", padx=10)

    # Adicionar escolha de qualidade
    tk.Label(janela, text="Qualidade do vídeo:", bg="#1e1e1e", fg="white").pack(pady=5)
    qualidade_var = tk.StringVar(value="best")
    qualidade_menu = ttk.Combobox(janela, textvariable=qualidade_var, values=["best", "1080p", "720p", "480p"], state="readonly", width=20)
    qualidade_menu.pack(pady=5)

    progresso_label = tk.Label(janela, text="", bg="#1e1e1e", fg="white")
    progresso_label.pack()

    barra = ttk.Progressbar(janela, length=400, mode="determinate")
    barra.pack(pady=10)

    # Função para mostrar progresso
    def mostrar_progresso(d):
        if d["status"] == "downloading":
            percentual_str = d.get("_percent_str", "0.0%")
            percentual_num = re.search(r"\d+\.?\d*", percentual_str.replace("%", "").strip())
            if percentual_num:
                percentual = float(percentual_num.group())
                barra["value"] = percentual
                progresso_label.config(text=f"Baixando: {percentual:.1f}%")
                janela.update()
        elif d["status"] == "finished":
            progresso_label.config(text="✅ Download concluído!")
            barra["value"] = 100
            janela.update()

    def baixar():
        url = url_entry.get().strip()
        tipo = formato.get()
        destino = filedialog.askdirectory(title="Escolha onde salvar")

        if not url or not destino:
            messagebox.showerror("Erro", "Coloque um link válido e escolha uma pasta!")
            return

        ffmpeg_path = ffmpeg_path_entry.get().strip() or r"C:\\Users\\natan\\Desktop\\dist_v2\\ffmpeg.exe"
        qualidade = qualidade_var.get()

        ydl_opts = {
            "outtmpl": os.path.join(destino, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "progress_hooks": [mostrar_progresso],
            "ffmpeg_location": ffmpeg_path,
        }

        if tipo == "mp4":
            # Configurações de qualidade
            if qualidade == "best":
                ydl_opts["format"] = "bestvideo[height<=?]+bestaudio/best"
            elif qualidade == "1080p":
                ydl_opts["format"] = "bestvideo[height<=1080]+bestaudio/best"
            elif qualidade == "720p":
                ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best"
            elif qualidade == "480p":
                ydl_opts["format"] = "bestvideo[height<=480]+bestaudio/best"
            ydl_opts["merge_output_format"] = "mp4"
        else:
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Sucesso", "Download concluído!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no download: {str(e)}")
            progresso_label.config(text="")
            barra["value"] = 0

    tk.Button(janela, text="⬇️ Baixar", command=baixar, bg="#00cc66", fg="white", relief="flat").pack(pady=10)

    janela.mainloop()

# Iniciar o programa
tela_login()
