import pygame,re,json,random

pygame.font.init()

def generador_palabra(lista_tematicas:list)-> str:
    '''
    Genera un string con una palabra aleatoria de una posicion de la lista aleatoria (tematica) y lo pasa a mayusculas. 
    Recibe una lista.
    Retorna un string.
    '''
    diccionario_tematica_elegida = random.choice(lista_tematicas)
    palabra_elegida = random.choice(diccionario_tematica_elegida["palabras"])
    palabra_elegida = palabra_elegida.upper()
    return palabra_elegida

def generador_palabra_oculta(palabra)-> str:
    '''
    Reemplaza todas las letras alfabeticas incluyendo la ñ por guiones bajos.
    Recibe un string.
    Retorna el string modificado.
    '''
    palabra_oculta = re.sub("[a-zA-ZñÑ]", "_" , palabra)
    return palabra_oculta

def buscador_tematica(palabra:str,lista_tematicas:list):
    '''
    Busca la tematica elegida segun la palabra pasada por parametro.
    Recibe un string y una lista.
    Retorna un string con la tematica a la cual pertenece.
    '''
    for tema in lista_tematicas:
        if tema["tema"] == "paises":
            palabra = palabra.capitalize()
            if palabra in tema["palabras"]:
                tematica = tema["tema"]
        else:
            palabra = palabra.lower()
            if palabra in tema["palabras"]:
                tematica = tema["tema"]
    try:
        return tematica
    except UnboundLocalError:
        tematica = "Indefinida"
        return tematica

def generar_csv(score:str,path:str):
    '''
    Guarda en un archivo csv los puntajes obtenidos en las partidas ganadas .
    Recibe un string con el puntaje y la ruta del archivo a anexar.
    Retorna un booleano.
    '''
    with open(path,"a") as archivo:
        archivo.write(score)
    return True
    
def mostrar_game_over(pantalla):
    '''
    Muestra el mensaje de Game over en la pantalla.
    Recibe la pantalla (Surface).
    Retorna un booleano.
    '''
    mensaje_game_over = "Game Over"
    mensaje_game_over_render = renderizar_texto(mensaje_game_over,"bahnschrift",(0,0,0),80)
    pantalla.blit(mensaje_game_over_render,((ANCHO/2)-200,(ALTO/2)-100))
    return True
    
def tachar_letras_teclado(letras_alfabeticas:list,letras_ingresadas:list,lista_superficies_teclado:list,icono):
    '''
    Tacha las letras ingreasadas en la subsuperficie del teclado en pantalla correspondiente.
    Recibe 3 listas (2 de strings y una de Surface) y una imagen (Surface).
    Retorna un booleano.
    '''
    if len(letras_ingresadas) > 0:
        for i in range(len(letras_alfabeticas)):
            for letras in letras_ingresadas:
                if letras_alfabeticas[i] == letras:
                    lista_superficies_teclado[i].blit(icono,(0,0))
        return True
    else:
        return False

def generar_json(lista:list,ruta:str):
    '''
    Guarda en un archivo .json los datos de una lista
    Recibe una lista y un string.
    Retorna un booleano.
    '''
    with open(ruta,"w") as archivo:
        json.dump(lista,archivo,indent = 4,ensure_ascii=False)
    return True
        
def leer_json(ruta:str):
    try:
        with open(ruta,"r") as archivo:
            lista = json.load(archivo)
            return lista
    except FileNotFoundError as error:
        print(f"Error, no se encontro el archivo ({error})")
        
def dibujar_figuras(intentos:int,pantalla:pygame.Surface):
    '''
    Muestra en pantalla imagenes segun la cantidad de intentos.
    Recibe un entero y una Surface.
    Retorna un booleano.
    '''
    match intentos:
        case 6:
            pantalla.blit(tarima,((ANCHO -300),170))
        case 5:
            pantalla.blit(tarima,((ANCHO -300),170))
            pantalla.blit(soga,(755,222))
            pantalla.blit(cabeza,(723,234))
        case 4:
            pantalla.blit(tarima,((ANCHO -300),170))
            pantalla.blit(soga,(755,222))
            pantalla.blit(cabeza,(723,234))
            pantalla.blit(cuerpo,(742,291))
        case 3:
            pantalla.blit(tarima,((ANCHO -300),170))
            pantalla.blit(soga,(755,222))
            pantalla.blit(cabeza,(723,234))
            pantalla.blit(cuerpo,(742,291))
            pantalla.blit(brazo_derecho,(767,290)) #brazo derecho
        case 2:
            pantalla.blit(tarima,((ANCHO -300),170))
            pantalla.blit(soga,(755,222))
            pantalla.blit(cabeza,(723,234))
            pantalla.blit(cuerpo,(742,291))
            pantalla.blit(brazo_derecho,(767,290)) #brazo derecho
            pantalla.blit(brazo_izquierdo,(730,290))
        case 1:
            pantalla.blit(tarima,((ANCHO -300),170))
            pantalla.blit(soga,(755,222))
            pantalla.blit(cabeza,(723,234))
            pantalla.blit(cuerpo,(742,291))
            pantalla.blit(brazo_derecho,(767,290)) #brazo derecho
            pantalla.blit(brazo_izquierdo,(730,290))
            pantalla.blit(brazo_derecho,(765,346)) 
        case 0:
            pantalla.blit(tarima,((ANCHO -300),170))
            pantalla.blit(soga,(755,222))
            pantalla.blit(cabeza,(723,234))
            pantalla.blit(cuerpo,(742,291))
            pantalla.blit(brazo_derecho,(767,290)) #brazo derecho
            pantalla.blit(brazo_izquierdo,(730,290))
            pantalla.blit(brazo_derecho,(765,346))
            pantalla.blit(brazo_izquierdo,(730,346))
    return True

def renderizar_texto(texto:str,estilo_letra:str,color,tamaño = 25):
    '''
    Renderiza un string y lo convierte en Surface.
    Recibe 2 strings, una tupla y un entero.
    Retorna una Surface.
    '''
    if estilo_letra == "tiza":
        fuente_tiza = pygame.font.Font(r"Ahorcado\Cheveuxdange.ttf",tamaño)
        texto_renderizado = fuente_tiza.render(texto,False, color, None)
    else:
        fuente = pygame.font.SysFont(estilo_letra,tamaño) 
        texto_renderizado = fuente.render(texto,True, color, None)
    return texto_renderizado

def obtener_tecla_presionada(evento_tecla):
    '''
    Captura que tecla se presiono dependiendo el evento pasado por parametro y lo pasa a mayuscula.
    Recibe un evento.
    Retorna un string.
    '''
    if evento_tecla.unicode == "ñ":
        tecla_presionada = "Ñ"
    else:
        tecla_presionada = pygame.key.name(evento_tecla.key)
        tecla_presionada = tecla_presionada.upper()
    return tecla_presionada

def detectar_tecla(tecla_presionada:str,lista_letras_teclado:list):
    '''
    Busca en un string letras alfabeticas incluyendo la ñ, si hay una sola coincidencia retorna un string, sino un booleano.
    Recibe un string y una lista.
    Retorna un string o un booleano.
    '''
    lista_letras = re.findall("[A-ZÑ]",tecla_presionada)
    if len(lista_letras) == 1:
        for letra in lista_letras:
            if letra in lista_letras_teclado:
                tecla = letra
                return tecla
    else:
        return False
    
def dibujar_figuras_teclado(pantalla:pygame.Surface):
    '''
    Crea rectangulos y sub-superficies en posiciones especificas.
    Recibe la pantalla (Surface).
    Retorna un booleano.
    '''
    pos_x = rectangulo_teclado.topleft[0] + 25
    pos_y = rectangulo_teclado.topleft[1] + 35
    largo = 38
    alto = 38
    espacio_rectangulos = 35
    for i in range(len(lista_letras_teclado)):
        rectangulo = pygame.Rect(pos_x,pos_y,largo,alto)
        sub_surface = pantalla.subsurface(rectangulo)
        lista_sub_surface.append(sub_surface)
        lista_rectanculos_teclado.append(rectangulo)
        pos_x += espacio_rectangulos + 4
        if i == 6:
            pos_x = rectangulo_teclado.topleft[0] + 25
            pos_y = rectangulo_teclado.topleft[1] + alto + espacio_rectangulos + 4
        elif i == 13:
            pos_x = rectangulo_teclado.topleft[0] + 25
            pos_y = rectangulo_teclado.topleft[1] + espacio_rectangulos + (alto *2) + 8
        elif i == 20:
            pos_x = rectangulo_teclado.topleft[0] + 25
            pos_y = rectangulo_teclado.topleft[1] + espacio_rectangulos + (alto*3) + 11
    return True

def blitear_letras_ingresadas(lista_letras:list,pantalla:pygame.Surface):
    '''
    Muestra en pantalla las letras (Surface) ingresadas.
    Recibe una lista y una Surface
    Retorna un booleano
    '''
    x = 215
    for letra in lista_letras:
        x += 18
        pantalla.blit(letra,(x,120))
    return True

def verificar_intentos(opcion_puntaje:str,intentos:int):
    '''
    Verifica si hay que restar intentos.
    Recibe un string y un entero.
    Retorna un entero.
    '''
    if opcion_puntaje == "restar":
        if intentos > 0:
            intentos -= 1
        return intentos
    else:
        return intentos

def verificar_puntaje(opcion_puntaje:str,puntaje:int):
    '''
    Verifica si hay que sumar o restar puntaje.
    Recibe un string y un entero.
    Retorna un entero.
    '''
    match opcion_puntaje:
        case "sumar":
            puntaje += 10
            return puntaje
        case "restar":
            if puntaje > 4:
                puntaje -= 5
            return puntaje
        case _:
            return puntaje

ANCHO = 1000
ALTO = 600
TAMAÑO_PANTALLA = (ANCHO,ALTO)

color_cheveuxdange = (221,236,227)

tematicas = leer_json(r"Ahorcado\tematicas.json")

palabra_elegida = generador_palabra(tematicas)
tematica_elegida = buscador_tematica(palabra_elegida,tematicas)

palabra_oculta = generador_palabra_oculta(palabra_elegida)
palabra_oculta_encode = palabra_oculta.encode('utf-8')
lista_palabra_oculta = list(palabra_oculta)

lista_letras_teclado = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", 
                        "K", "L", "M", "N", "Ñ" , "O", "P", "Q", "R", "S", "T",
                        "U", "V", "W", "X", "Y", "Z"]
lista_letras_ingresadas_render = []
lista_letras_ingresadas= []
lista_sub_surface = []
lista_rectanculos_teclado = []

tarima = pygame.image.load(r"Ahorcado\tarima.png")
tarima = pygame.transform.scale(tarima,(250,350))
cabeza = pygame.image.load(r"Ahorcado\cabeza.png")
cabeza = pygame.transform.scale(cabeza,(90,75))
soga = pygame.image.load(r"Ahorcado\soga.png")
soga = pygame.transform.scale(soga,(25,32))
cuerpo = pygame.image.load(r"Ahorcado\cuerpo.png")
cuerpo = pygame.transform.scale(cuerpo,(50,75))
brazo_derecho = pygame.image.load(r"Ahorcado\brazo derecha.png")
brazo_derecho = pygame.transform.scale(brazo_derecho,(40,60))
brazo_izquierdo = pygame.transform.flip(brazo_derecho,True,False)
icono_ahorcado = pygame.image.load(r"Ahorcado\icono_ahorcado.jpeg")
icono_ahorcado = pygame.transform.scale(icono_ahorcado,(30,30))
fondo = pygame.image.load(r"Ahorcado\fondo.jpg")
fondo = pygame.transform.scale(fondo,TAMAÑO_PANTALLA)

teclado_pantalla = pygame.image.load(r"Ahorcado\teclado_final.png")
teclado_pantalla = pygame.transform.scale(teclado_pantalla,(300,200))
rectangulo_teclado = teclado_pantalla.get_rect()
rectangulo_teclado.x = 360
rectangulo_teclado.y = 350

icono_x = pygame.image.load(r"Ahorcado\x.png")
icono_x = pygame.transform.scale(icono_x,(36,36))
x = 50
score_total = 0
boton_izquierdo_mouse = 1
