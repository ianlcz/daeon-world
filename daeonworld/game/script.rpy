# Vous pouvez placer le script de votre jeu dans ce fichier.

# Déclarez sous cette ligne les images, avec l'instruction 'image'
# ex: image eileen heureuse = "eileen_heureuse.png"

# Déclarez les personnages utilisés dans le jeu.

image bg uni = "bg uni.jpg"
image bg club = "bg club.jpg"

image thrall attaque = "thrall attaque.png"
image thrall base = "thrall base.png"

image cf base = "cf base.png"

image mdf base = "mdj base.png"

define t = Character('Thrall Loupdegivre', color="#000000")
define player = Character('Joueur P1', color="#c8c8ff")
define gui.choice_button_text_idle_color = '#000000'
define gui.choice_text_hover_color = '#0066cc'

#Le jeu commence
label start:
    scene bg uni
    show thrall base at truecenter
    with fade

    "!!!"

    t "Hum...où suis-je?"
    t "Je dois certainement faire un mauvais rêve.."

    show thrall attaque

    t "Arrrgh !!"

    show thrall base at left
    with dissolve
    t "Pourtant tout semble si réel pour un rêve.."
    t "Hmmm...."

    scene bg uni
    "..."
    player "Wow THRALL ???"

    show thrall base 
    with fade

    t "QUI EST TU HOMINOIDE ??"
    t "Que fais-tu dans mon rêve ?"

    scene bg uni
    with dissolve

    player "Je suis...."

    menu:
        "Claude François":
            jump claudef
                
        "Le maître du jeu":
            jump mdjeu
    
    label claudef:
        show cf base at truecenter
        player "Je suis le grand chanteur déchu Claude François !"
        jump path2

    label mdjeu:
        show mdj base at truecenter
        player "Je suis le maitre du jeu, l'omnipotent !"       
        jump path2
    
    label path2:
        scene black
        with dissolve

        "--- Quelques instants plus tard ---"


    ".:. Fin 1 débloquée."

    return
