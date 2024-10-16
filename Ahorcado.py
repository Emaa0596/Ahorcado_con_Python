import pygame
from Funciones_ahorcado import *

NEGRO = (0,0,0)
BLANCO = (250,244,227)
AMARILLO = (255,255,0)
ROJO = (255,0,0)
CELESTE = (0,191,255)
NARANJA = (255,165,0)

pygame.init()
pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)
pygame.display.set_caption("Ahorcado")
pygame.display.set_icon(icono_ahorcado)
pygame.mixer.init()
pygame.mixer.music.load("Ahorcado\sounds\musica.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)
sonido_tiza = pygame.mixer.Sound(r"Ahorcado\sounds\sonido_tiza.wav")
sonido_tiza.set_volume(0.2)
FPS = 15
clock = pygame.time.Clock()
tiempo_inicial = pygame.time.get_ticks()
intentos = 7
puntaje = 0
dibujar_figuras_teclado(pantalla)
flag = True
while flag:
    opcion_puntaje = "pasar"
    pantalla.blit(fondo,(0,0))
    pantalla.blit(teclado_pantalla,(rectangulo_teclado.x,rectangulo_teclado.y))
    clock.tick(FPS)
    texto_ingreso = renderizar_texto("Letras ingresadas: ","Arial",BLANCO)
    texto_tematica = renderizar_texto("Tematica: ","Arial",BLANCO)
    x = 50
    y = 100
    palabra_oculta_renderizada = renderizar_texto(palabra_oculta_encode,"tiza",BLANCO,50)
    pantalla.blit(palabra_oculta_renderizada,(375,275))
    tematica_elegida_renderizada = renderizar_texto(tematica_elegida,"tiza",AMARILLO,22)
    pantalla.blit(texto_tematica,(x,y+70))
    pantalla.blit(tematica_elegida_renderizada,(x+87,y+75))
    pantalla.blit(texto_ingreso,(x,y+15))
    mensaje_intentos = f"Te quedan {intentos} intentos"
    mensaje_intentos_render = renderizar_texto(mensaje_intentos,"Arial",NARANJA)
    pantalla.blit(mensaje_intentos_render,(x,50))
    puntaje_string = f"Puntaje: {puntaje}"
    score_string = f"Score total: {score_total}"
    puntaje_renderizado = renderizar_texto(puntaje_string,"Arial",CELESTE)
    score_renderizado = renderizar_texto(score_string,"Arial",NARANJA)
    pantalla.blit(puntaje_renderizado,(ANCHO - 400,50))
    pantalla.blit(score_renderizado,(ANCHO - 250,50))
    
    letra_ingresada = ""
    tecla = letra_ingresada
    lista_eventos = pygame.event.get()
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = tiempo_actual - tiempo_inicial
    tiempo_transcurrido = tiempo_transcurrido * 0.001
    string_tiempo = f"{tiempo_transcurrido:.00f}"
    tiempo_renderizado = renderizar_texto(string_tiempo,"tiza",BLANCO)
    pantalla.blit(tiempo_renderizado,(ANCHO /2, 50))

    tachar_letras_teclado(lista_letras_teclado,lista_letras_ingresadas,lista_sub_surface,icono_x)
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == boton_izquierdo_mouse:
                click_posicion = evento.pos
                for i in range(len(lista_rectanculos_teclado)):
                    if lista_rectanculos_teclado[i].collidepoint(click_posicion):
                        tecla = lista_letras_teclado[i]
                        letra_ingresada = tecla
        elif evento.type == pygame.KEYDOWN:
            tecla_presionada = obtener_tecla_presionada(evento)
            tecla = detectar_tecla(tecla_presionada,lista_letras_teclado)            
            if type(tecla) == str:
                letra_ingresada = tecla
            else:
                mensaje_error = renderizar_texto("Ingrese una tecla valida","Arial",NEGRO)
                pantalla.blit(mensaje_error,(50,125))
                opcion_puntaje = "pasar"

    if not letra_ingresada in lista_letras_ingresadas and (letra_ingresada != "" and type(tecla) == str):
        lista_letras_ingresadas.append(letra_ingresada)
        letra_ya_ingresada = lista_letras_ingresadas[-1]
        letras_ya_ingresadas_render = renderizar_texto(letra_ya_ingresada,"tiza",BLANCO)
        lista_letras_ingresadas_render.append(letras_ya_ingresadas_render)
        for i in range(len(palabra_elegida)):
            if palabra_elegida[i] == letra_ingresada:
                sonido_tiza.play()
                lista_palabra_oculta[i] = letra_ingresada
                palabra_oculta = "".join(lista_palabra_oculta)
                opcion_puntaje = "sumar"
                palabra_oculta_encode = palabra_oculta.encode('utf-8')
        if opcion_puntaje != "sumar":
            opcion_puntaje = "restar"
    elif letra_ingresada in lista_letras_ingresadas:
        mensaje_letra_repetida = "Letra ya ingresada anteriormente"
        mensaje_letra_repetida_render = renderizar_texto(mensaje_letra_repetida,"Arial",NEGRO)
        pantalla.blit(mensaje_letra_repetida_render,(x,200))
        opcion_puntaje = "pasar"    

    intentos = verificar_intentos(opcion_puntaje,intentos)
    puntaje = verificar_puntaje(opcion_puntaje,puntaje)
    if palabra_elegida == palabra_oculta and tiempo_transcurrido < 61:
        tiempo_restante = int(60 - tiempo_transcurrido)
        puntaje += tiempo_restante
        palabra_oculta_renderizada = renderizar_texto(palabra_elegida,"tiza",AMARILLO,50)
        pantalla.blit(palabra_oculta_renderizada,(390,325))
        mensaje_palabra_acertada = f"adivinaste la palabra, sumaste {puntaje} puntos"
        mensaje_palabra_acertada_render = renderizar_texto(mensaje_palabra_acertada,"tiza",AMARILLO,45)
        pantalla.blit(mensaje_palabra_acertada_render,(50,(ALTO/2)-100))
        score_total += puntaje
        pygame.display.update()
        pygame.time.delay(3000)
        generar_csv(str(score_total)+"; ","Ahorcado/scores_ahoracado.csv")
        palabra_elegida = generador_palabra(tematicas)
        tematica_elegida = buscador_tematica(palabra_elegida,tematicas)
        palabra_oculta = generador_palabra_oculta(palabra_elegida)
        palabra_oculta_encode = palabra_oculta.encode('utf-8')
        lista_palabra_oculta = list(palabra_oculta)
        lista_letras_ingresadas = []
        puntaje = 0
        intentos = 7
        lista_letras_ingresadas_render = []
        tiempo_inicial = pygame.time.get_ticks()

    elif (palabra_elegida != palabra_oculta and tiempo_transcurrido > 60) or (intentos == 0):
        dibujar_figuras(intentos,pantalla) 
        palabra_oculta_renderizada = renderizar_texto(palabra_elegida,"tiza",AMARILLO,50)
        pantalla.blit(palabra_oculta_renderizada,(390,325))
        mostrar_game_over(pantalla)
        pygame.display.update()
        pygame.time.delay(3000)
        score_total = 0
        puntaje = 0
        palabra_elegida = generador_palabra(tematicas)
        tematica_elegida = buscador_tematica(palabra_elegida,tematicas)
        palabra_oculta = generador_palabra_oculta(palabra_elegida)
        palabra_oculta_encode = palabra_oculta.encode('utf-8')
        lista_palabra_oculta = list(palabra_oculta)
        lista_letras_ingresadas = []
        intentos = 7
        lista_letras_ingresadas_render = []
        tiempo_inicial = pygame.time.get_ticks()
    
    blitear_letras_ingresadas(lista_letras_ingresadas_render,pantalla)
    dibujar_figuras(intentos,pantalla)    
    pygame.display.update()
pygame.quit()

