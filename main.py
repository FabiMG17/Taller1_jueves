# Importación de módulos necesarios para el juego
import pygame
import sys
import traceback
# Importación de la logica del game
from logica import Cancha, Pelota, Jugador, GestorPartido
pygame.init()

ANCHO = 1280
ALTO = 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pixel Racket")

# COLORES Y FUENTES     
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADOPASTEL = (218, 178, 255)
ROSAPASTEL = (253, 165, 213)
AMARILLO = (255, 255, 0)

# Capa para oscurecer pantalla
capa_oscura = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
capa_oscura.fill((0, 0, 0, 128))

# Carga de fuentes
confirmacion = pygame.font.SysFont("ArcadeClassic", 50)
fuente_instrucciones = pygame.font.SysFont("ArcadeClassic", 30)
fuente_marcador = pygame.font.SysFont("ArcadeClassic", 40)
fuente_gano = pygame.font.SysFont("ArcadeClassic", 100)

# Renderizado estático de textos para la pantalla de confirmación de salida
preguntap = confirmacion.render("Salir  al  menu  principal", True, NEGRO)
sip = confirmacion.render("Si", True, NEGRO)
nop = confirmacion.render("No", True, NEGRO)

# Posicionamiento de los botones "Si" y "No" en pantalla (centrados)
r_si = sip.get_rect(center=(ANCHO // 2 - 100, ALTO // 2 + 50))
r_no = nop.get_rect(center=(ANCHO // 2 + 100, ALTO // 2 + 50))

# botones
titulo = pygame.image.load("sprites/titulo.png").convert_alpha()
jugar = pygame.image.load("sprites/iniciar.png").convert_alpha()
comojugar = pygame.image.load("sprites/comojugar.png").convert_alpha()
salir = pygame.image.load("sprites/salir.png").convert_alpha()
# Imágenes interactivas cuando el mouse pasa por encima
jugar_p = pygame.image.load("sprites/iniciar_p.png").convert_alpha()
comojugar_p = pygame.image.load("sprites/comojugar_p.png").convert_alpha()
salir_p = pygame.image.load("sprites/salir_p.png").convert_alpha()
sprite_reglas = pygame.image.load("sprites/reglas.png").convert_alpha()
fondo_menu = pygame.transform.scale(pygame.image.load("sprites/gif.gif").convert(), (ANCHO, ALTO))
sprite_paraelfondo = pygame.transform.scale(pygame.image.load("sprites/paraelfondo.png").convert_alpha(), (ANCHO, ALTO))

# Carga de imagenes adicionales para pantalla ganador
sprite_ganop1_orig = pygame.image.load("sprites/ganop1.png").convert_alpha()
sprite_ganop1 = pygame.transform.scale(sprite_ganop1_orig, (sprite_ganop1_orig.get_width() * 4, sprite_ganop1_orig.get_height() * 4))

sprite_ganop2_orig = pygame.image.load("sprites/ganop2.png").convert_alpha()
sprite_ganop2 = pygame.transform.scale(sprite_ganop2_orig, (sprite_ganop2_orig.get_width() * 4, sprite_ganop2_orig.get_height() * 4))
sprite_return = pygame.transform.scale(pygame.image.load("sprites/return.png").convert_alpha(), (50, 50))
sprite_casa = pygame.transform.scale(pygame.image.load("sprites/casa.png").convert_alpha(), (50, 50))

# Se van a usar en la pantalla GANADOR
r_return = sprite_return.get_rect(center=(ANCHO // 2 - 60, ALTO // 2 + 150))
r_casa = sprite_casa.get_rect(center=(ANCHO // 2 + 60, ALTO // 2 + 150))

# Sprites de mute
mute_on = pygame.transform.scale(pygame.image.load("sprites/on.png").convert_alpha(), (50, 50))
mute_off = pygame.transform.scale(pygame.image.load("sprites/off.png").convert_alpha(), (50, 50))

#Escalado de los sprites de conteo
sprite_preparados = pygame.transform.scale(pygame.image.load("sprites/preparados.png").convert_alpha(), (800, 300))
sprite_listos = pygame.transform.scale(pygame.image.load("sprites/listos.png").convert_alpha(), (800, 300))
sprite_fuera = pygame.transform.scale(pygame.image.load("sprites/fuera.png").convert_alpha(), (800, 300))

# Escalado y dimensionado del logo principal
titulo = pygame.transform.scale(titulo, (700, 200))

# Obtención de rectángulos lógicos para procesar clics y colisiones
r_titulo = titulo.get_rect(center=(ANCHO // 2, 150)) 
r_jugar = jugar.get_rect(center=(ANCHO // 2, 330))
r_comojugar = comojugar.get_rect(center=(ANCHO // 2, 430))
r_salir = salir.get_rect(center=(ANCHO // 2, 530))
r_mute = mute_on.get_rect(topright=(ANCHO - 20, 20))

#Carga de musica
import os
pygame.mixer.init()

sonido_conteo = pygame.mixer.Sound("music/conteo.mp3")
sonido_conteo.set_volume(0.8) #volumen del conteo
sonido_opciones = pygame.mixer.Sound("music/opciones.mp3")
sonido_opciones.set_volume(0.2) #volumen de las opciones
sonido_presionado = pygame.mixer.Sound("music/presionado.mp3")
sonido_presionado.set_volume(0.2) #volumen del presionado

# Volúmenes para las músicas de fondo
volumen_musica_menu = 1.0 #volumen de la musica del menu
volumen_musica_juego = 0.3 #volumen de la musica del juego

ruta_musica_menu = None
ruta_musica_juego = None

if os.path.exists("music"):
    for archivo in os.listdir("music"):
        if archivo.startswith("menu"):
            ruta_musica_menu = os.path.join("music", archivo)
        elif archivo.startswith("parajugarmario"):
            ruta_musica_juego = os.path.join("music", archivo)

def mostrar_menu():
    pantalla.blit(fondo_menu, (0, 0)) 
    pantalla.blit(sprite_paraelfondo, (0, 0))
    pantalla.blit(titulo, r_titulo)
    pos_raton = pygame.mouse.get_pos()
    
    # Evalúa si el puntero del mouse esta encima del botón para pintar la imagen normal o la imagen presionada
    if r_jugar.collidepoint(pos_raton): pantalla.blit(jugar_p, r_jugar)
    else: pantalla.blit(jugar, r_jugar)

    if r_comojugar.collidepoint(pos_raton): pantalla.blit(comojugar_p, r_comojugar)
    else: pantalla.blit(comojugar, r_comojugar)

    if r_salir.collidepoint(pos_raton): pantalla.blit(salir_p, r_salir)
    else: pantalla.blit(salir, r_salir)

# INICIALIZACIÓN ANTES DEL BUCLE
estado_juego = "MENU" # Define el escenario activo
en_juego = True 
reloj = pygame.time.Clock() #Control de frames por segundo
tiempo_inicio_conteo = 0
musica_actual = None
opcion_hover_actual = None
musica_muteada = False

# Inicializa variables de nombres
nombre_p1 = ""
nombre_p2 = ""
ingresando_p1 = True

# Inicializa la instancia del mapa/cancha
mi_cancha = Cancha(ANCHO, ALTO)

# Movimientos de los jugadores 1 y 2
controles_j1 = {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izq': pygame.K_a, 'der': pygame.K_d, 'golpe': pygame.K_SPACE}
controles_j2 = {'arriba': pygame.K_UP, 'abajo': pygame.K_DOWN, 'izq': pygame.K_LEFT, 'der': pygame.K_RIGHT, 'golpe': pygame.K_RETURN}

# Rutas a sprites y cantidad de repeticiones por cada estado de la animación
datos_j1_azul = {
    'quieto': 'sprites/quieto_pd.png', 
    'correr': 'sprites/correr_pd', 
    'golpe':  'sprites/golpear_pd', 
    'saque':  'sprites/golpear_pd'
}
datos_j2_rosa = {
    'quieto': 'sprites/quieta_pf.png', 
    'correr': 'sprites/correr_pf', 
    'golpe':  'sprites/golpear_pf', 
    'saque':  'sprites/golpear_pf'
}

# Generación de los objetos jugadores que se utilizaran en el Gestor del Partido
j1 = Jugador(ANCHO // 2, 600, datos_j1_azul, controles_j1, 1, 0.8) 
j2 = Jugador(ANCHO // 2, 300, datos_j2_rosa, controles_j2, 2, 1.2)

partido = GestorPartido(mi_cancha, j1, j2)

# BUCLE PRINCIPAL
while en_juego:
    # Lógica de reproducción de música (Menú y Juego)
    if estado_juego in ["MENU", "COMO_JUGAR", "INGRESO_NOMBRES"]:
        nueva_musica = "MENU"
    elif estado_juego in ["JUGANDO", "CONFIRMAR_SALIDA"]:
        nueva_musica = "JUEGO"
    else:
        nueva_musica = "SILENCIO"
    
    if musica_actual != nueva_musica:
        pygame.mixer.music.stop()
        
        ruta_a_cargar = None
        volumen_a_cargar = 0.0
        
        if nueva_musica == "MENU":
            ruta_a_cargar = ruta_musica_menu
            volumen_a_cargar = volumen_musica_menu
        elif nueva_musica == "JUEGO":
            ruta_a_cargar = ruta_musica_juego
            volumen_a_cargar = volumen_musica_juego
        
        if ruta_a_cargar:
            try:
                pygame.mixer.music.load(ruta_a_cargar)
                pygame.mixer.music.set_volume(0.0 if musica_muteada else volumen_a_cargar)
                pygame.mixer.music.play(-1)
            except:
                pass
        musica_actual = nueva_musica

    # 60 FPS
    dt = reloj.tick(60) / 1000.0
    pos_raton = pygame.mouse.get_pos()
    teclas = pygame.key.get_pressed()

    # Sonido al pasar el mouse por encima de los botones
    opcion_hover_nueva = None
    if estado_juego == "MENU":
        if r_jugar.collidepoint(pos_raton): opcion_hover_nueva = "JUGAR"
        elif r_comojugar.collidepoint(pos_raton): opcion_hover_nueva = "COMO_JUGAR"
        elif r_salir.collidepoint(pos_raton): opcion_hover_nueva = "SALIR"
    elif estado_juego == "CONFIRMAR_SALIDA":
        if r_si.collidepoint(pos_raton): opcion_hover_nueva = "SI"
        elif r_no.collidepoint(pos_raton): opcion_hover_nueva = "NO"

    if r_mute.collidepoint(pos_raton): opcion_hover_nueva = "MUTE"

    if opcion_hover_nueva != opcion_hover_actual:
        if opcion_hover_nueva is not None and sonido_opciones:
            sonido_opciones.play()
        opcion_hover_actual = opcion_hover_nueva

    # Procesamiento de eventos en la cola
    for evento in pygame.event.get():
        # Evento natural del sistema operativo (Cierre de ventana en X)
        if evento.type == pygame.QUIT:
            en_juego = False

        # Boton de mute global
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if r_mute.collidepoint(pos_raton):
                if sonido_presionado: sonido_presionado.play()
                musica_muteada = not musica_muteada
                if musica_muteada:
                    pygame.mixer.music.set_volume(0.0)
                else:
                    vol_actual = volumen_musica_menu if musica_actual == "MENU" else volumen_musica_juego
                    pygame.mixer.music.set_volume(vol_actual)
                continue

        # Interacción del mouse con la interfaz del menú principal
        if estado_juego == "MENU":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if r_jugar.collidepoint(pos_raton):
                    if sonido_presionado: sonido_presionado.play()
                    estado_juego = "INGRESO_NOMBRES"
                    nombre_p1 = ""
                    nombre_p2 = ""
                    ingresando_p1 = True
                elif r_comojugar.collidepoint(pos_raton):
                    if sonido_presionado: sonido_presionado.play()
                    estado_juego = "COMO_JUGAR"
                elif r_salir.collidepoint(pos_raton):
                    if sonido_presionado: sonido_presionado.play()
                    en_juego = False

        # Regreso desde el menú de instrucciones
        elif estado_juego == "COMO_JUGAR":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado_juego = "MENU"

        elif estado_juego == "INGRESO_NOMBRES":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado_juego = "MENU"
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    if ingresando_p1:
                        if len(nombre_p1) > 0:
                            ingresando_p1 = False
                    else:
                        if len(nombre_p2) > 0:
                            partido.nombre_p1 = nombre_p1
                            partido.nombre_p2 = nombre_p2
                            partido.puntos = [0, 0]
                            partido.ganador = None
                            estado_juego = "PRE_CONTEO"
                            tiempo_inicio_conteo = pygame.time.get_ticks()
                elif evento.key == pygame.K_BACKSPACE:
                    if ingresando_p1:
                        nombre_p1 = nombre_p1[:-1]
                    else:
                        nombre_p2 = nombre_p2[:-1]
                else:
                    char = evento.unicode
                    if char.isalnum() or char == " ":
                        if ingresando_p1 and len(nombre_p1) < 10:
                            nombre_p1 += char
                        elif not ingresando_p1 and len(nombre_p2) < 10:
                            nombre_p2 += char

        elif estado_juego == "GANADOR":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if r_return.collidepoint(pos_raton):
                    if sonido_presionado: sonido_presionado.play()
                    partido.puntos = [0, 0]
                    partido.ganador = None
                    estado_juego = "PRE_CONTEO"
                    tiempo_inicio_conteo = pygame.time.get_ticks()
                elif r_casa.collidepoint(pos_raton):
                    if sonido_presionado: sonido_presionado.play()
                    estado_juego = "MENU"

        # Pausa/salida durante la partida pulsando Escape
        elif estado_juego == "JUGANDO":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado_juego = "CONFIRMAR_SALIDA"

        # confirmación en medio del juego para salir
        elif estado_juego == "CONFIRMAR_SALIDA":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if r_si.collidepoint(pos_raton):
                    if sonido_presionado: sonido_presionado.play()
                    estado_juego = "MENU"
                elif r_no.collidepoint(pos_raton):
                    if sonido_presionado: sonido_presionado.play()
                    estado_juego = "JUGANDO"

    # Conteo antes de iniciar el partido como tal
    if estado_juego == "JUGANDO":
        # cálculos
        partido.update(dt, teclas)
        if getattr(partido, 'ganador', None) is not None:
            estado_juego = "GANADOR"
    elif estado_juego == "PRE_CONTEO":
        if pygame.time.get_ticks() - tiempo_inicio_conteo >= 1000:
            if sonido_conteo: sonido_conteo.play()
            estado_juego = "CONTEO"
            tiempo_inicio_conteo = pygame.time.get_ticks()
    elif estado_juego == "CONTEO":
        if pygame.time.get_ticks() - tiempo_inicio_conteo >= 3000:
            estado_juego = "JUGANDO"

    if estado_juego == "MENU":
        mostrar_menu()

    elif estado_juego == "INGRESO_NOMBRES":
        pantalla.blit(fondo_menu, (0, 0)) 
        titulo_ingreso = confirmacion.render("INGRESE  LOS  NOMBRES", True, BLANCO)
        pantalla.blit(titulo_ingreso, (ANCHO // 2 - titulo_ingreso.get_width() // 2, 100))
        
        # P1 nombre
        color_p1 = AMARILLO if ingresando_p1 else BLANCO
        pygame.draw.rect(pantalla, color_p1, (ANCHO//2 - 200, 250, 400, 60))
        pygame.draw.rect(pantalla, NEGRO, (ANCHO//2 - 200, 250, 400, 60), 3)
        texto_p1 = fuente_marcador.render(f"P1: {nombre_p1}", True, NEGRO)
        pantalla.blit(texto_p1, (ANCHO//2 - 180, 260))
        
        # P2 nombre
        color_p2 = AMARILLO if not ingresando_p1 else BLANCO
        pygame.draw.rect(pantalla, color_p2, (ANCHO//2 - 200, 350, 400, 60))
        pygame.draw.rect(pantalla, NEGRO, (ANCHO//2 - 200, 350, 400, 60), 3)
        texto_p2 = fuente_marcador.render(f"P2: {nombre_p2}", True, NEGRO)
        pantalla.blit(texto_p2, (ANCHO//2 - 180, 360))
        inst = fuente_instrucciones.render("Presione  ENTER  para  continuar", True, BLANCO)
        pantalla.blit(inst, (ANCHO // 2 - inst.get_width() // 2, 500))

    elif estado_juego == "GANADOR":
        partido.dibujar(pantalla, fuente_marcador)
        pantalla.blit(capa_oscura, (0, 0))
        
        if partido.ganador == 1:
            sprite_ganador = sprite_ganop1
            nombre_ganador = partido.nombre_p1
        else:
            sprite_ganador = sprite_ganop2
            nombre_ganador = partido.nombre_p2
            
        # Dibujar sprite del que llego a ganar en el medio de la pantalla
        r_sprite_ganador = sprite_ganador.get_rect(center=(ANCHO//2, ALTO//2))
        pantalla.blit(sprite_ganador, r_sprite_ganador)
        
        # poner el nombre del jugador que gano
        texto_gano = fuente_gano.render(f"GANO {nombre_ganador}", True, NEGRO)
        r_texto = texto_gano.get_rect(center=(r_sprite_ganador.centerx + 120, r_sprite_ganador.centery))
        pantalla.blit(texto_gano, r_texto)
        
        # Botones de volver a jugar o ir al menu principal
        pantalla.blit(sprite_return, r_return)
        pantalla.blit(sprite_casa, r_casa)

    elif estado_juego == "JUGANDO":
        # Dibuja sobre el césped de la cancha
        partido.dibujar(pantalla, fuente_marcador)

    elif estado_juego == "PRE_CONTEO":
        partido.dibujar(pantalla, fuente_marcador)
        pantalla.blit(capa_oscura, (0, 0))

    elif estado_juego == "CONTEO":
        partido.dibujar(pantalla, fuente_marcador)
        pantalla.blit(capa_oscura, (0, 0))
        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_conteo
        if tiempo_transcurrido < 1000:
            imagen_conteo = sprite_preparados
        elif tiempo_transcurrido < 2000:
            imagen_conteo = sprite_listos
        else:
            imagen_conteo = sprite_fuera
        pantalla.blit(imagen_conteo, (ANCHO // 2 - imagen_conteo.get_width() // 2, ALTO // 2 - imagen_conteo.get_height() // 2))

    elif estado_juego == "CONFIRMAR_SALIDA":
        partido.dibujar(pantalla, fuente_marcador)
        pantalla.blit(capa_oscura, (0, 0))
        pygame.draw.rect(pantalla, ROSAPASTEL, (ANCHO//2 - 350, ALTO//2 - 100, 700, 200)) 
        pygame.draw.rect(pantalla, NEGRO, (ANCHO//2 - 350, ALTO//2 - 100, 700, 200), 5)
        pantalla.blit(preguntap, (ANCHO // 2 - preguntap.get_width() // 2, ALTO // 2 - 50))

        # Efectos de encima del boton y oscurecerlo un poco
        if r_si.collidepoint(pos_raton): pantalla.blit(confirmacion.render("SI", True, AMARILLO), r_si)
        else: pantalla.blit(sip, r_si)

        if r_no.collidepoint(pos_raton): pantalla.blit(confirmacion.render("NO", True, AMARILLO), r_no)
        else: pantalla.blit(nop, r_no)

    elif estado_juego == "COMO_JUGAR":
        pantalla.fill(ROSAPASTEL) 
        pantalla.blit(sprite_reglas, (ANCHO // 2 - sprite_reglas.get_width() // 2, ALTO // 2 - sprite_reglas.get_height() // 2))

    # Dibuja el botón de mute
    if musica_muteada:
        pantalla.blit(mute_off, r_mute)
    else:
        pantalla.blit(mute_on, r_mute)

    pygame.display.update()

pygame.quit()
sys.exit()