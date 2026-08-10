import pygame
import math

pygame.mixer.init()
sonido_rebote = pygame.mixer.Sound("music/rebote.mp3")
sonido_rebote.set_volume(0.5) #volumen del rebote

sonido_golpe = pygame.mixer.Sound("music/golpe.mp3")
sonido_golpe.set_volume(0.5) # volumen del golpe

sonido_ganar_punto = pygame.mixer.Sound("music/ganarpunto.mp3")
sonido_ganar_punto.set_volume(0.5) # volumen del ganar punto

sonido_ganaste = pygame.mixer.Sound("music/ganaste.mp3")
sonido_ganaste.set_volume(0.2) # volumen del ganar

# Definición de dimensiones y colores de la pantalla
ANCHO = 1280
ALTO = 720
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

class Cancha:
    def __init__(self, ancho, alto):
        #centrar elementos
        self.centro_x = ancho // 2
        
        # Carga de la imagen de fondo de la cancha y escalado al tamaño de la pantalla
        cancha_img = pygame.image.load("sprites/cancha.png").convert_alpha()
        self.cancha = pygame.transform.scale(cancha_img, (ancho, alto))

        # Carga del sprite del árbitro 1
        arbitro1 = pygame.image.load("sprites/arbitro1.png").convert_alpha()
        arbitro1_escalado = pygame.transform.scale(arbitro1, (60, 60))
        self.arbitro1 = pygame.transform.flip(arbitro1_escalado, False, False)

        # Carga del sprite del árbitro 2
        arbitro2 = pygame.image.load("sprites/arbitro2.png").convert_alpha()
        self.arbitro2 = pygame.transform.scale(arbitro2, (60, 60))

        # Definición del área de juego válida 
        offset_y = 50 
        self.ancho = 680  
        self.alto = 420
        self.area_juego = pygame.Rect(
            self.centro_x - (self.ancho // 2), 
            (alto // 2) - (self.alto // 2) + offset_y, 
            self.ancho, self.alto
        )

    def dibujar(self, pantalla):
        pantalla.blit(self.cancha, (0, 0))
        if self.arbitro1:
            pantalla.blit(self.arbitro1, (self.centro_x + (self.ancho // 2.1) - 30, (720 // 2) - 40))
        if self.arbitro2:
            pantalla.blit(self.arbitro2, (self.centro_x - (self.ancho // 2.1) - 15, (720 // 2) - 20))

class Pelota:
    def __init__(self, x, y):
        # Posición espacial de la pelota: x, y
        self.x = x
        self.y = y
        self.z = 30
        
        # Componentes direccionales de la velocidad de la pelota
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0
        self.gravedad = 400  # Gravedad simulada
        self.radio = 5
        
        # carga del sprite para la pelota
        img = pygame.image.load("sprites/pelota.png").convert_alpha()
        self.imagen = pygame.transform.scale(img, (14, 14))
            
        # Variables de estado y control del partido
        self.en_juego = False
        self.ultimo_golpe = 0 # Identificador del jugador (1 o 2) que impactó por última vez
        self.efecto_golpe = 0 # Temporizador visual del destello del impacto
        self.botes = 0 # Conteo consecutivo de botes contra el suelo en una jugada

    def update(self, dt):
        # Disminuye el efecto visual de impacto 
        if self.efecto_golpe > 0:
            self.efecto_golpe -= 1
            
        # Si la pelota no está activa no se procesa la físicca
        if not self.en_juego: return False
        
        # desacelera progresivamente en plano XY
        self.vel_x *= (1 - 0.5 * dt)
        self.vel_y *= (1 - 0.5 * dt)
        
        # Integración de posición en base a su velocidad respectiva, y aplicación de gravedad
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.vel_z -= self.gravedad * dt
        self.z += self.vel_z * dt

        boto = False
        # Detección de golpe (El plano Z <= 0)
        if self.z <= 0:
            self.z = 0
            # Aplica rebote invirtiendo la velocidad Z y perdiendo un porcentaje de energía
            self.vel_z *= -0.7  
            boto = True
            self.botes += 1
            if sonido_rebote: sonido_rebote.play()
            
            if abs(self.vel_z) < 30:
                self.vel_z = 0
                self.vel_x = 0
                self.vel_y = 0
                self.en_juego = False
        return boto

    def golpear(self, vel_x, vel_y, vel_z, jugador_id):
        # ve las nuevas fuerzas por el impacto con la raqueta
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.vel_z = vel_z
        self.z = 10 # eleva la pelota
        
        # reactiva estados de juego y resetea contadores
        self.en_juego = True
        self.ultimo_golpe = jugador_id
        self.efecto_golpe = 10  # destello visual por 10 iteraciones
        self.botes = 0

    def dibujar(self, pantalla):
        # la sombra se encoge con la altura para dar efecto 3D
        escala_sombra = max(0.2, 1 - (self.z / 200))
        ancho_sombra = int(16 * escala_sombra)
        alto_sombra = int(8 * escala_sombra)
        
        sombra_rect = pygame.Rect(int(self.x - ancho_sombra/2), int(self.y - alto_sombra/2), ancho_sombra, alto_sombra)
        pygame.draw.ellipse(pantalla, (50, 50, 50), sombra_rect)
        
        # Dibujar pelota
        if hasattr(self, 'imagen') and self.imagen:
            rect = self.imagen.get_rect(center=(int(self.x), int(self.y - self.z)))
            pantalla.blit(self.imagen, rect)
        else:
            pygame.draw.circle(pantalla, (255, 255, 0), (int(self.x), int(self.y - self.z)), self.radio)
        
        # Efecto visual al golpear la pelota
        if self.efecto_golpe > 0:
            radio_efecto = self.radio + (10 - self.efecto_golpe) * 2
            pygame.draw.circle(pantalla, (255, 255, 255), (int(self.x), int(self.y - self.z)), radio_efecto, 2)

class Jugador:
    def __init__(self, x, y, datos_sprites, controles, id_jugador, escala_sprite=0.8):
        # Posicionamiento inicial en 2D 
        self.x = x
        self.y = y
        self.id = id_jugador
        self.controles = controles
        self.velocidad = 300 
        self.escala_sprite = escala_sprite
        
        # carga de las animaciones de los jugadores
        self.anim_quieto = self._cargar_frames(datos_sprites['quieto'])
        self.anim_correr = self._cargar_frames(datos_sprites['correr'])
        self.anim_golpe = self._cargar_frames(datos_sprites['golpe'])
        self.anim_saque = self._cargar_frames(datos_sprites['saque'])
        
        # estados de animacion
        self.estado = "QUIETO"
        self.frames_actuales = self.anim_quieto
        self.indice_frame = 0 
        self.tiempo_animacion = 0
        self.velocidad_animacion = 0.12  # Intervalo de tiempo para pasar al siguiente frame
        self.mirando_derecha = True # Orienta la mirada hacia dónde caminar
        
        self.imagen = self.frames_actuales[self.indice_frame]
        self.rect = self.imagen.get_rect(midbottom=(self.x, self.y))
        self.rango_golpe = 70 # Alcance en pixeles en donde un raquetazo registra impacto con la pelota

    def _cargar_frames(self, ruta):
            import os
            escala = self.escala_sprite
            lista = []
            
            if os.path.isdir(ruta):
                archivos = sorted([f for f in os.listdir(ruta) if f.endswith('.png')])
                for archivo in archivos:
                    img = pygame.image.load(os.path.join(ruta, archivo)).convert_alpha()
                    nuevo_ancho = int(img.get_width() * escala)
                    nuevo_alto = int(img.get_height() * escala)
                    frame_pequeno = pygame.transform.scale(img, (nuevo_ancho, nuevo_alto))
                    lista.append(frame_pequeno)
                return lista
            else:
                # Carga una sola imagen
                img = pygame.image.load(ruta).convert_alpha()
                nuevo_ancho = int(img.get_width() * escala)
                nuevo_alto = int(img.get_height() * escala)
                frame_pequeno = pygame.transform.scale(img, (nuevo_ancho, nuevo_alto))
                lista.append(frame_pequeno)
                return lista

    def _cambiar_estado(self, nuevo_estado, nueva_lista):
        # reemplaza la animación actual de forma limpia
        if self.estado != nuevo_estado:
            self.estado = nuevo_estado
            self.frames_actuales = nueva_lista
            self.indice_frame = 0
            self.tiempo_animacion = 0

    def update(self, dt, teclas):
        moviendo = False
        # Impide desplazamientos en el suelo mientras el personaje está atrapado en la animación de golpe/saque
        if self.estado not in ["GOLPEANDO", "SACANDO"]: 
            # Controles de dirección e inercia posicional
            if teclas[self.controles['izq']]: 
                self.x -= self.velocidad * dt
                self.mirando_derecha = False 
                moviendo = True
            if teclas[self.controles['der']]: 
                self.x += self.velocidad * dt
                self.mirando_derecha = True  
                moviendo = True
            if teclas[self.controles['arriba']]: 
                self.y -= self.velocidad * dt
                moviendo = True
            if teclas[self.controles['abajo']]: 
                self.y += self.velocidad * dt
                moviendo = True

            # limita los lados
            self.x = max(20, min(self.x, 1260))
            
            # Barreras virtuales para simular la red física (aprox y=410)
            limite_red_j1 = 430  # Limita al J1 de cruzar al otro lado
            limite_red_j2 = 360  # Limita al J2 
            
            if self.id == 1:
                # J1 nunca sube más allá de la red
                self.y = max(limite_red_j1, min(self.y, 700))
            else:
                # J2 nunca baja más de la red, ni se sale del marco superior
                self.y = max(200, min(self.y, limite_red_j2))

            # Dispara los estados QUIETO o CORRIENDO
            if moviendo:
                self._cambiar_estado("CORRIENDO", self.anim_correr)
            else:
                self._cambiar_estado("QUIETO", self.anim_quieto)
                
        # logica de animaciones
        self.tiempo_animacion += dt
        if self.tiempo_animacion >= self.velocidad_animacion:
            self.tiempo_animacion = 0
            self.indice_frame += 1
            # Cuando la secuencia de imágenes termina
            if self.indice_frame >= len(self.frames_actuales):
                # Las animaciones de una sola pasada
                if self.estado in ["GOLPEANDO", "SACANDO"]:
                    self._cambiar_estado("QUIETO", self.anim_quieto)
                else:
                    # Las animaciones de correr inician su bucle infinito
                    self.indice_frame = 0

        #Espejo si el personaje cambio de dirección
        frame_crudo = self.frames_actuales[self.indice_frame]
        self.imagen = pygame.transform.flip(frame_crudo, True, False) if not self.mirando_derecha else frame_crudo
        self.rect.midbottom = (int(self.x), int(self.y))

    def intentar_golpe(self, pelota, teclas, tipo_golpe):
        if teclas[self.controles['golpe']] and self.estado not in ["GOLPEANDO", "SACANDO"]:
            # Realiza la animación visual sea o no un golpe exitoso 
            animacion = self.anim_saque if tipo_golpe == "SACANDO" else self.anim_golpe
            self._cambiar_estado(tipo_golpe, animacion)
            
            # comprobación del hitbox
            distancia = math.hypot(self.x - pelota.x, self.y - pelota.y)
            if distancia < self.rango_golpe and pelota.z < 250:
                # Cálculo del desvío horizontal del raquetazo.
                offset_x = pelota.x - self.x
              
                vel_x = offset_x * 2.5 
                vel_y = -320 if self.id == 1 else 320
                vel_z = 180
                pelota.golpear(vel_x=vel_x, vel_y=vel_y, vel_z=vel_z, jugador_id=self.id)
                if sonido_golpe: sonido_golpe.play()
                
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class GestorPartido:
    def __init__(self, cancha, j1, j2, nombre_p1="P1", nombre_p2="P2"):
        # módulos requeridos en la escena
        self.cancha = cancha
        self.j1 = j1
        self.j2 = j2
        self.nombre_p1 = nombre_p1
        self.nombre_p2 = nombre_p2
        # Generación de la pelota en el origen céntrico
        self.pelota = Pelota(ANCHO // 2, ALTO // 2)
        
        # control del bucle de vida de la partida
        self.estado = "ESPERANDO_SAQUE"
        self.puntos = [0, 0] # 0: J1, 1: J2
        self.textos_puntos = ["0", "15", "30", "40", "JUEGO"]
        self.servidor_actual = 1 # quién saca
        self.ganador = None # ID del ganador

    def update(self, dt, teclas):
        # Actualización de personajes
        self.j1.update(dt, teclas)
        self.j2.update(dt, teclas)

        #ETAPA 1 - PREVIO AL TOQUE INICIAL
        if self.estado == "ESPERANDO_SAQUE":
            self.pelota.ultimo_golpe = 0
            # Lanzamiento de pelota
            if self.servidor_actual == 1:
                self.pelota.x, self.pelota.y = self.j1.x + 30, self.j1.y - 40
                # salto de la pelota simulando el lanzamiento
                if teclas[self.j1.controles['golpe']] and self.j1.estado != "SACANDO":
                    self.j1._cambiar_estado("SACANDO", self.j1.anim_saque)
                    self.pelota.vel_z = 200
                    self.pelota.z = 40
                    self.pelota.en_juego = True
                    self.estado = "SAQUE_AL_AIRE"
            else:
                self.pelota.x, self.pelota.y = self.j2.x - 30, self.j2.y - 40
                if teclas[self.j2.controles['golpe']] and self.j2.estado != "SACANDO":
                    self.j2._cambiar_estado("SACANDO", self.j2.anim_saque)
                    self.pelota.vel_z = 200
                    self.pelota.z = 40
                    self.pelota.en_juego = True
                    self.estado = "SAQUE_AL_AIRE"
                    
        # ETAPA 2 - BOLA AL AIRE ESPERANDO SEGUNDO TOQUE DE RAQUETA
        elif self.estado == "SAQUE_AL_AIRE":
            # Permite el intento repetido hasta conectar el golpe
            if self.servidor_actual == 1:
                self.j1.intentar_golpe(self.pelota, teclas, "SACANDO")
            else:
                self.j2.intentar_golpe(self.pelota, teclas, "SACANDO")
                
            boto = self.pelota.update(dt)
            if boto:
                # cuando se equivoque y no le de al saque
                self.estado = "ESPERANDO_SAQUE"
                self.pelota.en_juego = False
                self.pelota.vel_z = 0
                
            # Si se logró golpear la bola, empieza el juego como tal
            if self.pelota.ultimo_golpe != 0:
                self.estado = "BOLA_EN_JUEGO"

        # ETAPA 3 - JUEGOOO
        elif self.estado == "BOLA_EN_JUEGO":
            # Busca intenciones de golpe por cualquiera de los dos lados
            self.j1.intentar_golpe(self.pelota, teclas, "GOLPEANDO")
            self.j2.intentar_golpe(self.pelota, teclas, "GOLPEANDO")
            
            # Chequea rebotes y colisiones
            if self.pelota.update(dt):
                if self.pelota.botes == 1:
                    #faltas y outs
                    fuera = not self.cancha.area_juego.collidepoint((self.pelota.x, self.pelota.y))
                    mitad_y = 720 // 2
                    
                    if fuera:
                        #Si la bola cayó fuera
                        ganador = 2 if self.pelota.ultimo_golpe == 1 else 1
                        self.anotar_punto(ganador)
                    else:
                        # Si cayó adentro
                        if self.pelota.ultimo_golpe == 1 and self.pelota.y >= mitad_y:
                            self.anotar_punto(2)  # J1 fracasó: el tiro no pasó la red
                        elif self.pelota.ultimo_golpe == 2 and self.pelota.y < mitad_y:
                            self.anotar_punto(1)  # J2 fracasó: el tiro no pasó la red
                            
                elif self.pelota.botes >= 2:
                    # si luego del 1er bote válido da un segundo bote, ganó el ofensor
                    self.anotar_punto(self.pelota.ultimo_golpe)

    def anotar_punto(self, jugador_id):
        # Actualiza el registro de puntuaciones
        self.puntos[jugador_id - 1] += 1
        
        # Ciclo de ganar cuando llegue a 40
        if self.puntos[0] >= 4 or self.puntos[1] >= 4:
            if sonido_ganaste: sonido_ganaste.play()
            self.ganador = 1 if self.puntos[0] >= 4 else 2
        else:
            if sonido_ganar_punto: sonido_ganar_punto.play()
            
        # Re-inicia la bola
        self.pelota.en_juego = False
        self.pelota.vel_x = self.pelota.vel_y = self.pelota.vel_z = 0
        self.pelota.z = 30
        self.estado = "ESPERANDO_SAQUE"

    def dibujar(self, pantalla, fuente_marcador):
        self.cancha.dibujar(pantalla)
        
        if self.j1.y < self.j2.y:
            self.j1.dibujar(pantalla)
            self.j2.dibujar(pantalla)
        else:
            self.j2.dibujar(pantalla)
            self.j1.dibujar(pantalla)
            
        # La pelota va arriba de los jugadores
        self.pelota.dibujar(pantalla)
        
        # marcadores 
        pantalla.blit(fuente_marcador.render(f"{self.nombre_p1}  {self.textos_puntos[min(self.puntos[0], 4)]}", True, NEGRO), (50, 150))
        texto_p2 = fuente_marcador.render(f"{self.nombre_p2}  {self.textos_puntos[min(self.puntos[1], 4)]}", True, NEGRO)
        pantalla.blit(texto_p2, (ANCHO - texto_p2.get_width() - 50, 150))     