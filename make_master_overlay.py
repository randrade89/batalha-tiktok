import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_master_overlay():
    W, H = 1080, 1920
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # 1. Carregar recortes com transparência
    lula_cutout = Image.open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\lula_cutout.png")
    flavio_cutout = Image.open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\flavio_cutout.png")

    # Fontes
    font_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
    try:
        f_title = ImageFont.truetype(font_bold, 36)
        f_subtitle = ImageFont.truetype(font_bold, 28)
        f_badge = ImageFont.truetype(font_bold, 22)
        f_name = ImageFont.truetype(font_bold, 28)
        f_inst = ImageFont.truetype(font_bold, 20)
        f_boost = ImageFont.truetype(font_bold, 24)
        f_cta = ImageFont.truetype(font_bold, 34)
    except:
        f_title = ImageFont.load_default()
        f_subtitle = ImageFont.load_default()
        f_badge = ImageFont.load_default()
        f_name = ImageFont.load_default()
        f_inst = ImageFont.load_default()
        f_boost = ImageFont.load_default()
        f_cta = ImageFont.load_default()

    # ==========================
    # TOPO: HEADER DA BATALHA
    # ==========================
    header_h = 160
    header_box = [(20, 20), (W - 20, header_h)]
    draw.rounded_rectangle(header_box, radius=24, fill=(10, 12, 22, 235), outline=(255, 215, 0, 240), width=4)

    draw.text((W // 2, 45), "BATALHA DE CAMISAS: QUEM VENCE?", fill=(255, 255, 255), font=f_title, anchor="mm")
    draw.text((W // 2, 85), "TIME LULA (13)   VS   TIME BOLSONARO (22)", fill=(255, 215, 0), font=f_subtitle, anchor="mm")

    # Barra de Disputa no Topo
    bar_x1, bar_x2 = 60, W - 60
    bar_y = 115
    bar_h = 24
    draw.rounded_rectangle([(bar_x1, bar_y), (W // 2, bar_y + bar_h)], radius=12, fill=(220, 20, 40, 255))
    draw.rounded_rectangle([(W // 2, bar_y), (bar_x2, bar_y + bar_h)], radius=12, fill=(245, 180, 0, 255))
    draw.line([(W // 2, bar_y - 6), (W // 2, bar_y + bar_h + 6)], fill=(255, 255, 255), width=6)

    # ==========================
    # LADO ESQUERDO: LULA / CAMISA 13
    # ==========================
    char_w = 400
    lula_aspect = lula_cutout.height / lula_cutout.width
    lula_h = int(char_w * lula_aspect)
    lula_resized = lula_cutout.resize((char_w, lula_h), Image.Resampling.LANCZOS)

    # Card
    card_y = 190
    card_h = lula_h + 230
    left_card_box = [(15, card_y), (425, card_y + card_h)]
    draw.rounded_rectangle(left_card_box, radius=24, fill=(18, 10, 14, 225), outline=(239, 68, 68, 255), width=4)

    # Badge Sacola
    draw.rounded_rectangle([(30, card_y - 15), (230, card_y + 25)], radius=12, fill=(239, 68, 68, 255))
    draw.text((130, card_y + 5), "ITEM SACOLA #1", fill=(255, 255, 255), font=f_badge, anchor="mm")

    # Imagem
    canvas.paste(lula_resized, (20, card_y + 25), lula_resized)

    # Titulo do Produto
    title_y_lula = card_y + lula_h + 35
    draw.text((220, title_y_lula), "CAMISA BRASIL 13", fill=(255, 75, 75), font=f_name, anchor="mm")

    # Instruções
    box_inst_y = title_y_lula + 25
    draw.rounded_rectangle([(30, box_inst_y), (410, box_inst_y + 130)], radius=14, fill=(0, 0, 0, 200), outline=(239, 68, 68, 180), width=2)
    draw.text((45, box_inst_y + 15), "Comente LULA / PT: +1 Pt", fill=(255, 255, 255), font=f_inst)
    draw.text((45, box_inst_y + 45), "Envie ROSA: +5 Pts", fill=(255, 160, 210), font=f_inst)
    draw.text((45, box_inst_y + 85), "COMPRE NA SACOLA: +50 PTS!", fill=(255, 220, 0), font=f_boost)

    # ==========================
    # LADO DIREITO: FLÁVIO / ACORDA BRASIL
    # ==========================
    flavio_aspect = flavio_cutout.height / flavio_cutout.width
    flavio_h = int(char_w * flavio_aspect)
    flavio_resized = flavio_cutout.resize((char_w, flavio_h), Image.Resampling.LANCZOS)

    right_card_box = [(W - 425, card_y), (W - 15, card_y + card_h)]
    draw.rounded_rectangle(right_card_box, radius=24, fill=(18, 18, 10, 225), outline=(245, 180, 0, 255), width=4)

    # Badge Sacola
    draw.rounded_rectangle([(W - 230, card_y - 15), (W - 30, card_y + 25)], radius=12, fill=(245, 180, 0, 255))
    draw.text((W - 130, card_y + 5), "ITEM SACOLA #2", fill=(0, 0, 0), font=f_badge, anchor="mm")

    # Imagem
    canvas.paste(flavio_resized, (W - 420, card_y + 25), flavio_resized)

    # Titulo do Produto
    title_y_flavio = card_y + flavio_h + 35
    draw.text((W - 220, title_y_flavio), "ACORDA BRASIL 22", fill=(255, 215, 0), font=f_name, anchor="mm")

    # Instruções
    draw.rounded_rectangle([(W - 410, box_inst_y), (W - 30, box_inst_y + 130)], radius=14, fill=(0, 0, 0, 200), outline=(245, 180, 0, 180), width=2)
    draw.text((W - 395, box_inst_y + 15), "Comente MITO / 22: +1 Pt", fill=(255, 255, 255), font=f_inst)
    draw.text((W - 395, box_inst_y + 45), "Envie 1 MOEDA: +5 Pts", fill=(255, 230, 120), font=f_inst)
    draw.text((W - 395, box_inst_y + 85), "COMPRE NA SACOLA: +50 PTS!", fill=(255, 220, 0), font=f_boost)

    # ==========================
    # RODAPÉ: CTA TIKTOK SHOP
    # ==========================
    footer_h = 130
    footer_box = [(20, H - footer_h - 25), (W - 20, H - 25)]
    draw.rounded_rectangle(footer_box, radius=24, fill=(255, 0, 85, 245), outline=(255, 255, 255, 255), width=4)
    draw.text((W // 2, H - footer_h // 2 - 40), "CLIQUE NA SACOLA LARANJA!", fill=(255, 255, 255), font=f_cta, anchor="mm")
    draw.text((W // 2, H - footer_h // 2), "COMPRE A CAMISA E DÊ +50 PONTOS PRO SEU TIME!", fill=(255, 245, 120), font=f_subtitle, anchor="mm")

    dest_desktop = r"C:\Users\Rogerio\Desktop\OVERLAY_BATALHA_TIKTOK.png"
    dest_public = r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\images\overlay_batalha.png"
    
    canvas.save(dest_desktop, "PNG")
    canvas.save(dest_public, "PNG")
    print("Master Overlay atualizado com sucesso!")

create_master_overlay()