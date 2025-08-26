# 🎬 Multi Downloader com Login (YouTube, Instagram, X, etc.)

Este projeto é um **aplicativo em Python com interface gráfica (Tkinter)** que permite baixar vídeos e músicas de várias plataformas (YouTube, Instagram, X/Twitter, etc.) em **MP4 (vídeo)** ou **MP3 (áudio)**.  
O sistema conta ainda com uma **tela de login protegida por hash (SHA-256)**, garantindo acesso restrito.

---

## ✨ Funcionalidades

- 🔐 **Login com autenticação SHA-256** (usuário/senha embutidos + validade de licença)  
- ⬇️ **Download de vídeos (MP4)** ou apenas **áudio (MP3)**  
- 🎨 Interface moderna em **Tkinter** com barra de progresso animada  
- 📂 Escolha de destino para salvar os arquivos  
- 🎵 Conversão automática para MP3 usando **ffmpeg**  
- ⚠️ Exibição de mensagens de erro/sucesso com `messagebox`  

---

## 🖼️ Prints da Interface

### Tela de Login
🔑 Acesso restrito com usuário e senha.  
*(usuário padrão: `admin` / senha: `senha123`)*  

### Tela Principal
- Campo para colar o link  
- Botões de escolha de formato (🎥 MP4 ou 🎵 MP3)  
- Barra de progresso com status em tempo real  
- Botão “Baixar Agora”  

---

## ⚙️ Requisitos

- **Python** 3.8+  
- **Dependências**:
  ```bash
  pip install yt-dlp
