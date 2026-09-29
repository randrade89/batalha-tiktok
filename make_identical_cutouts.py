import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# 1. ATUALIZAR LULA COM A CAMISA 13 FAZ O L IDÊNTICA AO ANÚNCIO
lula = Image.open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\lula_cutout.png").convert("RGBA")
red_shirt = Image.open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\camisa_vermelha_oficial.png").convert("RGBA")

# Extrair elementos da camisa vermelha oficial:
# 13: x: 155 to 220, y: 55 to 110 (proporcional)
rw, rh = red_shirt.size
crop_13 = red_shirt.crop((int(rw * 0.33), int(rh * 0.15), int(rh * 0.50), int(rh * 0.32)))
crop_escudo = red_shirt.crop((int(rw * 0.55), int(rh * 0.14), int(rw * 0.70), int(rh * 0.33)))
crop_l_star = red_shirt.crop((int(rw * 0.20), int(rh * 0.35), int(rw * 0.65), int(rh * 0.98)))

# Cobrir a estampa antiga do peito do Lula com a cor vermelha da camisa
lula_draw = ImageDraw.Draw(lula)
# A estampa antiga estava entre x: 350 a 680, y: 600 a 800
# Pintar com vermelho da camisa do Lula (cerca de RGB 210, 45, 50)
lula_draw.rectangle([340, 580, 680, 820], fill=(205, 45, 52, 255))

# Redimensionar e colar a nova estampa idêntica
# Número 13 no peito direito (visão do observador: esquerda)
elem_13 = crop_13.resize((110, 80), Image.Resampling.LANCZOS)
# Escudo Brasil no peito esquerdo (visão do observador: direita)
elem_escudo = crop_escudo.resize((95, 100), Image.Resampling.LANCZOS)
# Estrela com o L na parte inferior
elem_l_star = crop_l_star.resize((270, 270), Image.Resampling.LANCZOS)

lula.paste(elem_13, (360, 610), elem_13)
lula.paste(elem_escudo, (540, 600), elem_escudo)
lula.paste(elem_l_star, (310, 710), elem_l_star)

lula.save(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\lula_cutout.png", "PNG")
print("Lula atualizado com a estampa IDÊNTICA do anúncio (13 + Escudo + Faz o L)!")


# 2. ATUALIZAR FLÁVIO COM A ESTAMPA IDÊNTICA ACORDA BRASIL
flavio = Image.open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\flavio_cutout.png").convert("RGBA")
estampa_y = Image.open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\estampa_amarela.png").convert("RGBA")

# Cobrir a estampa antiga do Flávio com o tom de amarelo da camisa dele
flavio_draw = ImageDraw.Draw(flavio)
# A estampa antiga estava entre x: 400 a 700, y: 530 a 800
flavio_draw.rectangle([390, 530, 700, 810], fill=(234, 200, 52, 255))

# Redimensionar a estampa real do Acorda Brasil com bandeira
est_w = 260
est_aspect = estampa_y.height / estampa_y.width
est_h = int(est_w * est_aspect)
est_resized = estampa_y.resize((est_w, est_h), Image.Resampling.LANCZOS)

flavio.paste(est_resized, (420, 540), est_resized)

flavio.save(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\flavio_cutout.png", "PNG")
print("Flávio atualizado com a estampa IDÊNTICA do anúncio (Acorda Brasil + Bandeira desgastada)!")