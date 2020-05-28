# Vous pouvez placer le script de votre jeu dans ce fichier.

# Déclarez sous cette ligne les images, avec l'instruction 'image'
# ex: image eileen heureuse = "eileen_heureuse.png"

# Déclarez les personnages utilisés dans le jeu.

image bg foret maison = "bg foret maison.jpg"
image bg foret = "bg foret.jpg"
image bg plaine 2 ="bg plaine 2.jpg"
image bg plaine 3 ="bg plaine 3.jpg"
image bg plaine = "bg plaine.jpg"
image bg pont = "bg pont.jpg"
image bg riviere = "bg riviere.jpg"
image bg ruine = "bg ruine.jpg"
image bg chateau = "bg chateau.jpg"


image humain base = "humain base.png"
image humain attaque = "humain attaque.png"

image orc base = "orc base.png"
image orc attaque = "orc attaque.png"


define player = Character('Moi', color="#c8c8ff")
define gui.choice_button_text_idle_color = '#ffffff'
define gui.choice_text_hover_color = '#0066cc'

#Le jeu commence
label start:
    "Un jeune aventurier se reveille sans se souvenir où il est se trouve ni qui il est..."
    "...Il devra parcourir le mon à le recherche d'informations le concernant..."
    "... tout en faisant face aux danger qui le composent."
    scene bg plaine 2
    with fade

    menu:
        "Se diriger vers une plaine ensoleillée..":
            jump choix1_plaine

        "Se rendre vers la forêt sombre..":
            jump choix2_foret
    
    label choix1_plaine:
        scene bg plaine
        with fade
        "Vous décidez d'arpenter ces bien vertes plaines..."

        scene bg ruine
        with fade

        "Vous tombez devant les ruines d'un ancien fort..."

        menu:
            "Visitez les ruines du fort..":
                jump choix1_ruine

            "Continuer son chemin..":
                jump riviere

        label choix1_ruine:
            "Après avoir fouillé un peu partout, vous trouvez un objet à la fois précieux et très ancien."
            "Vous poursuivez ensuite votre route..."
            jump riviere
        
    
    label choix2_foret:
        scene bg foret
        with fade
        "Vous vous enfoncer dans la foret...
        "
        scene bg foret maison
        with fade

        "Vous apercevez une vielle bâtisse au loin..."

        menu:
            "S'approcher de la maison..":
                jump choix2_maison

            "Continuer en longeant la rivière..":
                jump riviere
        
        label choix2_maison:
            "Vous tombez nez à nez avec une créature hostile !"

            show orc base at right

            "Que comtez-vous faire ?"

            menu:
                "Combattre la créature..":
                    jump choix2_combat

                "Fuir..":
                    jump riviere
            
            label choix2_combat:
                show orc attaque at right
                "La créature s'énerve et s'en prend à vous..."
                scene black
                "Vous succombez de vos blessure, elle était clairement trop féroce pour vous."
                ".:. Fin 3 Débloquée .:."
                return
    
    label riviere:
        scene bg riviere
        with fade

        "Vous vous arrêtez quelques instants et contemplez la beauté du paysage..."

        scene black
        "Vous poursuivez votre route..."

        scene bg pont
        with fade

        menu:
            "Franchir le pont..":
                jump choix_pont

            "Contourner le pont..":
                jump choix_contourner
        
        label choix_pont:
            "Le pont est vraiment fragile, vous sentez qu'il pourrait se briser à tout moment..."
            menu:
                "Le franchir en courant..":
                    jump choix_courir

                "Continuer à marcher prudemment..":
                    jump choix_marcher

            label choix_marcher:
                "Vous arrivez tant bien que mal à franchir ce satané pont..."
                scene bg plaine 3
                with fade
                "Vous continuez votre chemin pendant un long moment..."
                "..."
                scene bg chateau
                with dissolve

                "A suivre..."
                ".:. Fin 4  débloquée .:."
                return

            label choix_courir:
                "Vous vous hâtez mais le pont se brise et vous tombez à l'eau..."
                "Eh bien bravo ! vous êtes tout mouillé maintenant !"
                "Vous apercevez une berge pour sortir de l'eau..."
                menu:
                    "Nager vers la berge..":
                        jump choix_nager

                    "Aller vers la rive..":
                        jump choix_aval
                
                label choix_nager:
                    "Vous nagez encore et encore, cette berge n'était qu'une désilution..."
                    "Vous avez quand même poursuivit par orgueil.."
                    "Mais vous vous retrouvez noyez dans l'eau par épuisement."
                    ".:. Fin 2 débloquée. .:."
                    return

        label choix_contourner:
            "Trop prudent pour s'aventurer sur un pont aussi grinçant, vous réfléchissez à la manière de le contourner..."

            menu:
                "Aller en amont..":
                    jump fin_amont

                "Aller en aval..":
                    jump choix_aval

            label fin_amont:
                "Hélas pour vous, on dirait bien que vous vous êtes perdu..."
                ".:. Fin 1 débloquée. .:."
                return

            label choix_aval:
                scene bg plaine 2
                with fade

                "Ah! Il semblerez que vous ayez tourné en rond.."

                menu:
                    "Se diriger vers une plaine ensoleillée..":
                        jump choix1_plaine

                    "Se rendre vers la forêt sombre..":
                        jump choix2_foret

    

    return
