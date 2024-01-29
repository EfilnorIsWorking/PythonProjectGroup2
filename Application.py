import pygame
import sys
import os 
from pygame.locals import KEYDOWN, K_ESCAPE, K_RETURN, K_BACKSPACE
import main

pygame.init()
#os.chdir("/home/adeleris/Desktop")

original_largeur, original_hauteur = 1920, 1080
largeur, hauteur = original_largeur, original_hauteur

window_surface = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("The Game Of Life")

original_image = pygame.image.load(r"src\img\background.jpg")
background = pygame.transform.scale(original_image, (largeur, hauteur))

instructions_image_path = r'src\img\background.jpg'
instructions_image = pygame.image.load(instructions_image_path)
instructions_image = pygame.transform.scale(instructions_image, (largeur, hauteur))

police = pygame.font.Font(None, 36)

noir = (0, 0, 0)
blanc = (255, 255, 255)
gris = (128, 128, 128)
violet = (122, 55, 139)
bleu = (92, 172, 238)
vert = (164, 205, 50)

capacite_bob = 1
luminosite = 1.0

musique = r"src\img\start.mp3"

fullscreen = False
valeurs_formulaire = [0] * 14

# Ajouter une variable globale pour le bouton "Luminosité"
bouton_luminosite_rect = pygame.Rect(largeur * 0.75, hauteur * 0.90, largeur * 0.22, hauteur * 0.09)

def afficher_texte(texte, x, y):
    texte_surface = police.render(texte, True, blanc)
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (x, y)
    window_surface.blit(texte_surface, texte_rect)



def afficher_formulaire():
    global valeurs_formulaire
    labels = ["mapWidth", "mapHeight", "bobAmount", "foodAmount", "dayLength", "bob_energy", "bob_speed", "bob_mass", "bob_perc","nrg/move", "nrg@birth", "nrg/birth", "nrg_m_birth", "nrg/tick"]

    font = pygame.font.Font(None, 25)
    input_rects_left = []
    input_rects_right = []
    color_active = pygame.Color('dodgerblue2')
    color_inactive = pygame.Color(vert)
    colors = [color_inactive] * 14
    active = [False] * 14
    texts = [""] * 14
    current_index = 0

    save_button_rect = pygame.Rect(largeur * 0.75, hauteur * 0.80, largeur * 0.22, hauteur * 0.09)
    return_button_rect = pygame.Rect(largeur * 0.75, hauteur * 0.70, largeur * 0.22, hauteur * 0.09)

    for i in range(7):
        input_rects_left.append(pygame.Rect(largeur * 0.15, hauteur * (0.29 + 0.1 * i), largeur * 0.2, hauteur * 0.05))
        input_rects_right.append(pygame.Rect(largeur * 0.5, hauteur * (0.29 + 0.1 * i), largeur * 0.2, hauteur * 0.05))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                norm_x = x / largeur
                norm_y = y / hauteur
                print(norm_x,norm_y)
                for i in range(len(labels)):
                    if i < 7 and input_rects_left[i].collidepoint(event.pos):
                        active[i] = not active[i]
                        current_index = i
                    elif i >= 7 and input_rects_right[i-7].collidepoint(event.pos):
                        active[i] = not active[i]
                        current_index = i
                    else:
                        active[i] = False
                
                if 0.75 <= norm_x <= 1.00:
                    if 0.65 <= norm_y <= 0.87:
                        options_menu_open = False
                        print("return")
                        return 1

                

            elif event.type == KEYDOWN:
                if any(active):
                    if event.key == K_RETURN:
                        valeurs_formulaire[current_index] = int(texts[current_index].strip()) if texts[current_index].strip().isdigit() else 0
                        active[current_index] = False
                        
                    elif event.key == K_BACKSPACE:
                        texts[current_index] = texts[current_index][:-1]
                        
                    else:
                        texts[current_index] += event.unicode
                        
                elif event.key == K_ESCAPE:
                    return 1


                    


        window_surface.fill((0, 0, 0))
        window_surface.blit(background, (0, 0))
        afficher_texte("OPTIONS", largeur // 2, 100)

        for i in range(len(labels)):
            if i < 7:
                pygame.draw.rect(window_surface, colors[i], input_rects_left[i], 2)
                label_rect_x = input_rects_left[i].x - font.size(f"{labels[i]}:")[0] - 20
                label_rect_y = input_rects_left[i].centery - font.size(f"{labels[i]}:")[1] // 2
            else:
                pygame.draw.rect(window_surface, colors[i], input_rects_right[i-7], 2)
                label_rect_x = input_rects_right[i-7].x - font.size(f"{labels[i]}:")[0] - 20
                label_rect_y = input_rects_right[i-7].centery - font.size(f"{labels[i]}:")[1] // 2

            label_surface = font.render(f"{labels[i]}:", True, noir)
            label_rect = label_surface.get_rect(topleft=(label_rect_x, label_rect_y))
            window_surface.blit(label_surface, label_rect)

            txt_surface = font.render(texts[i] if active[i] else str(valeurs_formulaire[i]), True, violet)
            if i < 7:
                width = max(200, txt_surface.get_width() + 10)
                input_rects_left[i].w = width
                window_surface.blit(txt_surface, (input_rects_left[i].x + 5, input_rects_left[i].y))
                pygame.draw.rect(window_surface, colors[i], input_rects_left[i], 2)
            else:
                width = max(200, txt_surface.get_width() + 10)
                input_rects_right[i-7].w = width
                window_surface.blit(txt_surface, (input_rects_right[i-7].x + 5, input_rects_right[i-7].y))
                pygame.draw.rect(window_surface, colors[i], input_rects_right[i-7], 2)

        pygame.draw.rect(window_surface, violet, return_button_rect)
        afficher_texte("Retour", largeur * 0.85, int(hauteur * 0.75))

        pygame.display.flip()








def ajuster_positions_plein_ecran():
    global largeur, hauteur, background, instructions_image, bouton_luminosite_rect

    if fullscreen:
        largeur, hauteur = pygame.display.get_surface().get_size()
        bouton_luminosite_rect = pygame.Rect(largeur * 0.75, hauteur * 0.90, largeur * 0.22, hauteur * 0.09)
    else:
        largeur, hauteur = original_largeur, original_hauteur
        bouton_luminosite_rect = pygame.Rect(largeur * 0.75, hauteur * 0.90, largeur * 0.22, hauteur * 0.09)

    background = pygame.transform.scale(original_image, (largeur, hauteur))
    instructions_image = pygame.transform.scale(instructions_image, (largeur, hauteur))

    bouton_largeur = 200
    bouton_hauteur = 40
    bouton_y = hauteur // 2 - bouton_hauteur // 2
    
    pygame.display.update()

    # Mise à jour des positions des boutons dans le menu principal
    bouton_luminosite_rect = pygame.Rect(largeur * 0.75, hauteur * 0.90, largeur * 0.22, hauteur * 0.09)
    bouton_options_rect = pygame.Rect(largeur * 0.39, hauteur * 0.57, largeur * 0.22, hauteur * 0.09)
    bouton_quit_rect = pygame.Rect(largeur * 0.39, hauteur * 0.69, largeur * 0.22, hauteur * 0.09)
    bouton_plein_ecran_rect = pygame.Rect(largeur * 0.75, hauteur * 0.02, largeur * 0.19, hauteur * 0.1)
    bouton_musique_rect = pygame.Rect(largeur * 0.75, hauteur * 0.14, largeur * 0.19, hauteur * 0.1)
    bouton_rejouer_musique_rect = pygame.Rect(largeur * 0.75, hauteur * 0.32, largeur * 0.19, hauteur * 0.1)

    bouton_retour_rect = pygame.Rect(largeur * 0.75, hauteur * 0.78, largeur * 0.22, hauteur * 0.09)

    # Mise à jour de la position du texte du bouton plein écran
    bouton_plein_ecran_texte_rect = pygame.Rect(largeur * 0.84, hauteur * 0.07, 0, 0)

    # Mise à jour de la position du texte du bouton musique
    bouton_musique_texte_rect = pygame.Rect(largeur * 0.84, hauteur * 0.19, 0, 0)

    # Mise à jour de la position du texte du bouton rejouer musique
    bouton_rejouer_musique_texte_rect = pygame.Rect(largeur * 0.84, hauteur * 0.38, 0, 0)

    pygame.display.update()

def toggle_fullscreen():
    global fullscreen, largeur, hauteur, background
    fullscreen = not fullscreen

    if fullscreen:
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        largeur, hauteur = original_largeur, original_hauteur
        pygame.display.set_mode((largeur, hauteur))

    pygame.display.update()
    ajuster_positions_plein_ecran()

def gerer_redimensionnement(event):
    global largeur, hauteur
    largeur, hauteur = event.w, event.h
    ajuster_positions_plein_ecran()

def stopper_toutes_musiques():
    pygame.mixer.music.stop()

def rejouer_toutes_musiques():
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(-1)

def toggle_musique():
    if pygame.mixer.music.get_busy():
        stopper_toutes_musiques()
    else:
        rejouer_toutes_musiques()

pygame.mixer.music.load(musique)
pygame.mixer.music.play(-1)

# Fonction pour afficher le bouton "Luminosité"
def afficher_bouton_luminosite():
    pygame.draw.rect(window_surface, violet, bouton_luminosite_rect)

    afficher_texte("Luminosité", largeur * 0.85, int(hauteur * 0.95))

# Fonction pour afficher le bouton "Options"
def afficher_bouton_options():
    pygame.draw.rect(window_surface, violet, (largeur * 0.39, hauteur * 0.57, largeur * 0.22, hauteur * 0.09))
    afficher_texte("Options", largeur // 2, int(hauteur * 0.61))

# Fonction pour afficher le bouton "Quit"
def afficher_bouton_quit():
    pygame.draw.rect(window_surface, violet, (largeur * 0.39, hauteur * 0.69, largeur * 0.22, hauteur * 0.09))
    afficher_texte("Quitter", largeur // 2, int(hauteur * 0.73))

def menu_luminosite():
    while True:
        for event in pygame.event.get():
            print(pygame.event.get())
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                norm_x = x / largeur
                norm_y = y / hauteur
                print("luminosite")
                if 0.33 <= norm_x <= 0.67:
                    if 0.56 <= norm_y <= 0.65:
                        augmenter_luminosite()
                    elif 0.67 <= norm_y <= 0.76:
                        diminuer_luminosite()
                    elif 0.78 <= norm_y <= 0.87:
                        return  # Retour au menu principal

        window_surface.fill((0, 0, 0))
        window_surface.blit(background, (0, 0))
        afficher_texte("MENU LUMINOSITÉ", largeur // 2, 100)
        pygame.draw.rect(window_surface, bleu, (largeur * 0.33, hauteur * 0.56, largeur * 0.34, hauteur * 0.09))
        afficher_texte("Augmenter Luminosité", largeur // 2, int(hauteur * 0.60))
        pygame.draw.rect(window_surface, bleu, (largeur * 0.33, hauteur * 0.67, largeur * 0.34, hauteur * 0.09))
        afficher_texte("Diminuer Luminosité", largeur // 2, int(hauteur * 0.71))
        pygame.draw.rect(window_surface, violet, (largeur * 0.33, hauteur * 0.78, largeur * 0.34, hauteur * 0.09))
        afficher_texte("Retour", largeur // 2, int(hauteur * 0.82))
        pygame.display.update()

def augmenter_luminosite():
    global luminosite
    luminosite += 0.1
    pygame.display.set_gamma(luminosite)

def diminuer_luminosite():
    global luminosite
    luminosite -= 0.1
    pygame.display.set_gamma(luminosite)


mapLargeur= 20
mapHauteur= 0
bobAmount= 0
foodAmount=0
dayLength= 0

bobNrj=0
bobSpeed=0
bobMass=0
bobPerc=0


nrj_spent_per_move=0
nrj_at_birth=0
nrj_spent_per_birth=0
nrj_min_at_birth=0
njr_min_spent_tick=0
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                norm_x = x / largeur
                norm_y = y / hauteur

                if 0.39 <= norm_x <= 0.61:
                    if 0.44 <= norm_y <= 0.53:
                        afficher_instructions()
                        return "start_game"
                    elif 0.57 <= norm_y <= 0.67:
                        afficher_bouton_options()
                        return "options_menu"
                    elif 0.69 <= norm_y <= 0.79:
                        pygame.quit()
                        sys.exit()
                elif 0.75 <= norm_x <= 0.94 and 0.02 <= norm_y <= 0.12:
                    toggle_fullscreen()
                elif 0.75 <= norm_x <= 0.94 and 0.13 <= norm_y <= 0.31:
                    toggle_musique()
                elif 0.75 <= norm_x <= 0.94 and 0.32 <= norm_y <= 0.42:
                    rejouer_toutes_musiques()
                elif bouton_luminosite_rect.collidepoint(x, y):  # Vérifier si le bouton "Luminosité" est cliqué
                    print("Clic sur le bouton Luminosité")
                    return "luminosite_menu"

        window_surface.fill((0, 0, 0))
        window_surface.blit(background, (0, 0))
        afficher_texte("GAME OF LIFE", largeur // 2, 100)
        pygame.draw.rect(window_surface, bleu, (largeur * 0.39, hauteur * 0.44, largeur * 0.22, hauteur * 0.09))
        afficher_texte("Démarrer", largeur // 2, int(hauteur * 0.48))
        afficher_bouton_options()
        afficher_bouton_luminosite()
        afficher_bouton_quit()
        pygame.draw.ellipse(window_surface, vert, (largeur * 0.75, hauteur * 0.02, largeur * 0.19, hauteur * 0.1))
        afficher_texte("Plein écran", int(largeur * 0.84), int(hauteur * 0.07))
        pygame.draw.ellipse(window_surface, vert, (largeur * 0.75, hauteur * 0.14, largeur * 0.19, hauteur * 0.1))
        afficher_texte("Musique", int(largeur * 0.84), int(hauteur * 0.19))
        pygame.display.update()




def afficher_instructions():
    instruction_text = [
        "Bienvenue dans le Game of Life! Découvrez ces éléments qui rendent ce jeu irrésistible :",
        "Évolution Surprenante : Observez vos bobs évoluer avec des reproductions, des mutations et des comportements uniques.",
        "Cannibalisme Intrigant : Vivez une dynamique où les bobs peuvent se manger, ajoutant une dimension stratégique.",
        "Personnalisation Facile : Ajustez les paramètres selon vos préférences pour une expérience unique.",
        "Mécaniques de Jeu Sophistiquées : Du mouvement à la perception, plongez dans des mécaniques immersives.",
        "Vie Virtuelle Vibrante : Explorez la recherche de nourriture, la reproduction, et la survie pour une expérience passionnante.",
        "Préparez-vous à être captivé par les interactions, les choix stratégiques et l'évolution étonnante de votre population de bobs. Êtes-vous prêt pour l'aventure ?",
        "Appuyez sur 'Entrer' pour lancer le jeu"
    ]



    instruction_font = pygame.font.Font(None, 24)

    instruction_screen = pygame.display.set_mode((largeur, hauteur))
    instruction_screen.blit(instructions_image, (0, 0))

    y_offset = 50
    for line in instruction_text:
        instruction_surface = instruction_font.render(line, True, noir)
        instruction_rect = instruction_surface.get_rect(center=(largeur // 2, y_offset))
        instruction_screen.blit(instruction_surface, instruction_rect)
        y_offset += 30

    pygame.display.flip()

    waiting_for_escape = True
    while waiting_for_escape:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting_for_escape = False


       
x = 0
def options_menu():
    global luminosite
    global x 
    while True:
        window_surface.fill((0, 0, 0))
        window_surface.blit(background, (0, 0))
        afficher_texte("OPTIONS", largeur // 2, 100)

        if (x == 0) :
            x = afficher_formulaire()  # Appelez la fonction pour afficher le formulaire
        if (x ==1) :
            return 
        pygame.draw.rect(window_surface, violet, (largeur * 0.33, hauteur * 0.78, largeur * 0.34, hauteur * 0.09))
        afficher_texte("Retour", largeur // 2, int(hauteur * 0.82))
        pygame.display.update()
        


        

def start_game():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(-1)
    
    jeu_en_cours = True
    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                norm_x = x / largeur
                norm_y = y / hauteur

               
                

        window_surface.fill((0, 0, 0))
        afficher_texte("Le jeu a commencé", largeur // 2, hauteur // 2 - 50)

        
        pygame.display.update()

 


if __name__ == "__main__":
    game_started = False
    while True:
        if not game_started:
            
            action = main_menu()
            
            if action == "start_game":
                game_started = True
                main.main()
            elif action == "options_menu":
                print(action)
                x=0
                options_menu()
                print("fin du menu option")
            elif action == "luminosite_menu":
                print(action)
                menu_luminosite()


        ajuster_positions_plein_ecran() 
