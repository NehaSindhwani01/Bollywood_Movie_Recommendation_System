import pygame
import sys
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = [
    ("Taare Zameen Par", "Emotions, dyslexia, childhood, art, teacher bond. A misunderstood boy with dyslexia finds support from an empathetic teacher."),
    ("Barfi!", "Love, disability, comedy, emotions, triangle. A deaf-mute man navigates love and life with innocence and charm."),
    ("PK", "Alien, comedy, religion, social satire, curiosity. An alien questions religious dogmas after landing in India."),
    ("3 Idiots", "Education, innovation, friendship, pressure, college life. Three friends challenge the norms of the rigid Indian education system."),
    ("Bajrangi Bhaijaan", "Humanity, cross-border, compassion, child rescue, faith. A devoted man helps a mute girl return to Pakistan."),
    ("Kesari", "War, bravery, patriotism, real story, sacrifice. 21 Sikh soldiers fight against thousands in the Battle of Saragarhi."),
    ("Padman", "Social change, health, innovation, taboo, inspiration. A man invents affordable sanitary pads for rural women."),
    ("Neerja", "Hijack, courage, flight, sacrifice, real-life hero. A flight attendant saves passengers during a terrorist hijack."),
    ("Pink", "Consent, courtroom, feminism, rights, harassment. A lawyer defends three women falsely accused of wrongdoing."),
    ("Chak De! India", "Sports, redemption, women empowerment, leadership, patriotism. A former player coaches the Indian women's hockey team to glory."),
    ("Article 15", "Caste, social justice, police, discrimination, investigation. A cop investigates the disappearance of Dalit girls in rural India."),
    ("Stree", "Horror-comedy, folklore, mystery, ghosts, satire. A village is haunted by a female spirit that abducts men at night."),
    ("Tumbbad", "Mythology, horror, greed, curse, fantasy. A man discovers a hidden treasure guarded by a cursed god."),
    ("Piku", "Father-daughter, comedy, road trip, health, emotions. A quirky journey of a daughter dealing with her aging father."),
    ("Bhaag Milkha Bhaag", "Biopic, sports, determination, partition, running. The life story of Indian sprinter Milkha Singh."),
    ("Kai Po Che", "Friendship, politics, religion, cricket, Gujarat riots. Three friends navigate life amidst social and political turmoil."),
    ("Rang De Basanti", "Youth, rebellion, patriotism, awakening, martyrdom. College students reenact freedom fighters and ignite change."),
    ("Talvar", "Murder mystery, investigation, truth, CBI, media. A layered investigation into a high-profile double murder case."),
    ("Paa", "Disease, father-son bond, drama, emotions, politics. A child with a rare genetic condition unites his estranged parents."),
    ("Haider", "Shakespeare, revenge, Kashmir, conflict, family. A young man returns home to find the truth about his father’s disappearance."),
    ("Tamasha", "Self-discovery, identity, love, performance, dual life. A man rediscovers his true self through love and storytelling."),
    ("Rockstar", "Music, heartbreak, fame, pain, transformation. A young musician becomes a star while dealing with emotional turmoil."),
    ("Lunchbox", "Loneliness, food, letters, connection, Mumbai. A mistaken lunchbox delivery sparks a heartfelt correspondence."),
    ("Udaan", "Freedom, abuse, teenage dreams, rebellion, poetry. A teen boy escapes his abusive father to chase his dreams."),
    ("Swades", "NRI, rural development, water crisis, village, change. An NRI returns to India and works to improve village life."),
    ("My Name is Khan", "Disability, terrorism, identity, journey, humanity. A Muslim man with Asperger’s sets out to meet the US President."),
    ("Lagaan", "Colonialism, cricket, tax, rebellion, rural India. Villagers challenge British rulers to a game of cricket to avoid taxes."),
    ("Black", "Disability, education, inspiration, darkness, learning. A deaf-blind girl learns to communicate through her teacher."),
    ("Sultan", "Wrestling, comeback, love, fitness, sports drama. A wrestler fights personal loss and rises again to win back his life."),
    ("Dil Dhadakne Do", "Family, cruise, relationships, drama, elite class. A dysfunctional family confronts its issues on a luxury cruise."),
    ("Jab We Met", "Romance, journey, self-love, transformation, travel. A quirky girl helps a heartbroken man find love again."),
    ("Raees", "Crime, bootlegging, politics, power, action. A bootlegger rises to power in Gujarat but faces challenges from the law."),
    ("Baazigar", "Revenge, thriller, love, identity, murder. A man hides his identity to avenge his family's downfall."),
    ("Baahubali: The Beginning", "War, kingdom, loyalty, mystery, betrayal. A young warrior discovers his royal heritage and destiny."),
    ("Baahubali 2: The Conclusion", "Revenge, battle, justice, love, legacy. The conclusion to the epic saga of Mahendra Baahubali's revenge."),
    ("Don", "Underworld, double role, chase, crime, twist. A man impersonates a crime lord to bring down a drug empire."),
    ("Hum Aapke Hain Koun", "Family, wedding, love, tradition, sacrifice. A joyful celebration of Indian family values and relationships."),
    ("Kal Ho Naa Ho", "Romance, sacrifice, friendship, illness, emotions. A terminally ill man brings love and happiness into others’ lives."),
    ("Kabhi Khushi Kabhie Gham", "Family, drama, tradition, reunion, emotions. A son tries to reunite with his estranged father."),
    ("Veer-Zaara", "Cross-border love, sacrifice, justice, timeless romance. An Indian pilot and Pakistani woman fight for their love."),
    ("Mohabbatein", "Love, discipline, clash, inspiration, music. A music teacher challenges a strict principal on the meaning of love."),
    ("Dilwale Dulhania Le Jayenge", "Romance, family, tradition, travel, love story. A young couple falls in love during a trip to Europe."),
    ("Om Shanti Om", "Reincarnation, revenge, Bollywood, love, mystery. A junior artist is reborn to avenge his murder."),
    ("Fan", "Obsession, identity, thriller, fame, dark side. A fan’s admiration turns dangerous when rejected by his idol."),
    ("Pathaan", "Spy, action, patriotism, mission, terrorism. An elite agent returns from exile to stop a deadly threat."),
    ("Jawan", "Action, justice, dual roles, political drama, mass hero. A man sets out to correct system corruption in his own way."),
    ("War", "Espionage, betrayal, action, agents, chase. Two elite agents clash in a high-octane game of loyalty and secrets."),
    ("Satyameva Jayate", "Vigilante, corruption, justice, action, brothers. A man punishes corrupt officials while hiding a personal truth."),
    ("Batla House", "Encounter, investigation, patriotism, media trial, truth. A police officer defends the legitimacy of a controversial encounter."),
    ("Special 26", "Heist, thriller, fake CBI, clever team, 80s setting. A group pulls off daring heists by posing as CBI officers."),
    ("Ek Tha Tiger", "Spy, romance, undercover, action, international. An Indian spy falls in love during a mission in Pakistan."),
    ("Tiger Zinda Hai", "Sequel, rescue mission, terrorism, high-stakes, action. Tiger returns to save nurses held hostage in Iraq."),
    ("Dhoom", "Heist, bikes, cops and robbers, action, thrill. A bike gang robs banks while a clever cop tries to catch them."),
    ("Dhoom 2", "Sequel, thief, disguises, international, romance. A master thief challenges the law and wins hearts."),
    ("Dhoom 3", "Circus, revenge, twins, illusion, emotional drama. A circus performer seeks revenge for his father's death."),
    ("Bang Bang!", "Action, mistaken identity, romance, chase, comedy. A woman gets involved in a spy mission by accident."),
    ("Krrish", "Superhero, powers, sci-fi, romance, origin story. A man with extraordinary powers becomes a masked hero."),
    ("Krrish 3", "Mutation, villains, love, action, heroism. Krrish battles mutants to save the world from destruction."),
    ("Ra.One", "Gaming, sci-fi, villain, virtual reality, father-son. A game character comes to life and causes chaos."),
    ("Bodyguard", "Romance, action, duty, loyalty, identity. A bodyguard falls for the woman he's assigned to protect."),
    ("Ready", "Comedy, romance, confusion, mistaken identity, family drama. A man pretends to be someone else to win love."),
    ("Housefull", "Comedy, chaos, relationships, confusion, marriage. A man’s bad luck creates hilarious situations in love."),
    ("Housefull 2", "Sequel, mix-ups, family, fake identities, fun. Multiple couples and families get entangled in a wedding mess."),
    ("Housefull 3", "Superstition, love, lies, laughter, triple trouble. Three men fake disabilities to marry three sisters."),
    ("Welcome", "Gangster, comedy, marriage, lies, chaos. A respectable man falls in love with a don’s sister."),
    ("Welcome Back", "Sequel, mistaken identity, fun, underworld, marriage. The dons try to marry off their sister again, hilariously."),
    ("Singh is Kinng", "Action, comedy, mistaken identity, goodwill, redemption. A fun-loving man accidentally becomes a mafia king."),
    ("Rowdy Rathore", "Double role, police, action, masala, love. A small-time thief discovers he's a cop’s lookalike."),
    ("Gabbar is Back", "Vigilante, corruption, justice, teacher, suspense. A mysterious man punishes corrupt officials across the city."),
    ("Toilet: Ek Prem Katha", "Social message, love, sanitation, reform, village. A man builds a toilet to win his wife's respect."),
    ("Bhoot", "Horror, possession, apartment, mystery, tension. A newly married couple is haunted in their new home."),
    ("Bhoot Returns", "Sequel, horror, spirits, family, suspense. A family faces eerie events in a new house."),
    ("Bhool Bhulaiyaa", "Psychological thriller, spirit, illusion, comedy, twist. A woman’s behavior is misunderstood as possession."),
    ("Bhool Bhulaiyaa 2", "Sequel, spirit, drama, horror-comedy, secrets. A fake exorcist meets a real ghost."),
    ("Hungama", "Comedy, misunderstanding, city life, fun, love triangle. Multiple characters create chaos with their deceptions."),
    ("Phir Hera Pheri", "Sequel, money, scam, hilarious, trio. The iconic trio gets trapped in another get-rich scheme."),
    ("Golmaal: Fun Unlimited", "Comedy, blind couple, friendship, pranks, deception. Friends fake identities to live rent-free."),
    ("Golmaal Returns", "Suspicion, lies, office romance, funny, family drama. A wife suspects her husband of cheating, hilarity follows."),
    ("Golmaal 3", "Rivalry, step-siblings, love-hate, chaos, comedy. Two rival groups of siblings clash after their parents marry."),
    ("De Dana Dan", "Chase, confusion, hotel, kidnapping, money. Two men fake a kidnapping to escape poverty."),
    ("Khatta Meetha", "Construction, corruption, comedy, family, struggle. A road contractor fights injustice with his quirky team."),
    ("Dhamaal", "Treasure hunt, road trip, comedy, misfits, fun. Four guys hunt for treasure in a laugh riot."),
    ("Double Dhamaal", "Sequel, betrayal, revenge, tricks, silly fun. The gang returns for another round of mischief and madness."),
    ("Jolly LLB", "Courtroom drama, small lawyer, justice, corruption. A struggling lawyer takes on a powerful case."),
    ("Jolly LLB 2", "Sequel, court battle, police, fake encounter, drama. A lawyer fights for truth against the system."),
    ("Bala", "Insecurity, hair loss, comedy, self-love, confidence. A young man with premature baldness learns self-worth."),
    ("Dream Girl", "Call center, voice acting, comedy, identity, love. A man’s female voice on a helpline creates unexpected romance."),
    ("Badhaai Ho", "Family, pregnancy, embarrassment, emotions, social norms. A middle-aged couple expecting a child surprises everyone."),
    ("Shubh Mangal Zyada Saavdhan", "LGBTQ, acceptance, comedy, family drama, love. Two men fight for their love and family’s approval."),
    ("Mimi", "Surrogacy, motherhood, sacrifice, emotions, single parenting. A woman agrees to be a surrogate and raises the child herself."),
    ("Luka Chuppi", "Live-in, society, marriage pressure, rom-com, secrets. A couple pretends to be married while living together."),
    ("Pati Patni Aur Woh", "Love triangle, comedy, temptation, loyalty, confusion. A married man juggles love and lust hilariously."),
    ("Jawaani Jaaneman", "Bachelor life, fatherhood, surprise, emotions, change. A carefree man discovers he has a grown-up daughter."),
    ("Malang", "Revenge, passion, drugs, thriller, romance. A man's dark past leads him to a deadly path of vengeance."),
    ("Ek Villain", "Revenge, crime, love, tragedy, transformation. A man changes his life after falling in love but loses her."),
    ("Aashiqui 2", "Music, love, downfall, addiction, sacrifice. A singer’s love story is tested by fame and self-destruction."),
    ("Ashoka", "Historical, war, love, transformation, emperor. The story of Ashoka’s rise and transformation into a peace lover."),
    ("Guzaarish", "Euthanasia, magician, court case, emotions, dignity. A paralyzed magician pleads for the right to die with dignity.")
]

titles = [title for title , desc in movies]
description = [desc for title , desc in movies]

#vectorize the description
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(description)

# for cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix)

#recommendation function
def recommend(title , top_n = 5):
    if title not in titles:
        return ["Movie not found in database.."]
    idx = titles.index(title)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores , key = lambda x : x[1] , reverse=True) #DESC ORDER BASED ON 2ND ELEMNT OF COSINE MATRIX
    
    recommendations = []
    for i , score in sim_scores[1 : top_n+1]:
        recommendations.append(f"{titles[i]} (Similarity : {score:.2f})")
    return recommendations

pygame.init()
WIDTH , HEIGHT = 800 , 600
screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Bollywood Movie recommendation System")

WHITE = (255 , 255 , 255)
LIGHT_GRAY = (240 , 240 , 240)
GRAY = (200 , 200 , 200)
DARK_GRAY = (50 , 50 , 50)
BLACK = (0 , 0 , 0)
BLUE = (100 , 149 , 237)
DARK_BLUE = (70 , 130 , 180)
BG_TOP = (255 , 200 , 200)
BG_BUTTON = (200 , 220 , 255)

font = pygame.font.SysFont("Arial" , 24)
big_font = pygame.font.SysFont("Arial" , 36 , bold=True)
title_font = pygame.font.SysFont("Arial" , 28 , bold=True)

input_box = pygame.Rect(50 , 80 , 700 , 45)
input_text = ''
active = False

button_rect = pygame.Rect(330 , 140 , 140 , 45)

output_box = pygame.Rect(50 , 220 , 700 , 250)

recommendations = []
suggestions = []


def draw_rounded_rect(surface , color , rect , radius=10):
    pygame.draw.rect(surface , color , rect , border_radius=radius)

def draw_gradient_background(surface , top_color , bottom_color):
    for y in range(HEIGHT):
        blend = y / HEIGHT
        r = int(top_color[0] * (1 - blend) + bottom_color[0] * blend)
        g = int(top_color[1] * (1 - blend) + bottom_color[1] * blend)
        b = int(top_color[2] * (1 - blend) + bottom_color[2] * blend)
        pygame.draw.line(surface , (r , g , b) , (0 , y) , (WIDTH , y))

running = True
while running :
    
    # Draw Gradient Background
    draw_gradient_background(screen , BG_TOP , BG_BUTTON)
    
    # Draw Header Text
    header = title_font.render("Bollywood Movie Recommendation System" , True , DARK_GRAY)
    screen.blit(header , (WIDTH // 2 - header.get_width() // 2 , 20))
    
    # Draw "Enter Movie Title" Label
    label = font.render("Enter Movie Title" , True , BLACK)
    screen.blit(label , (50 , 50))
    
    # Draw Input Box
    draw_rounded_rect(screen , WHITE , input_box , radius=8)
    pygame.draw.rect(screen , BLUE if active else GRAY , input_box , 2 , border_radius=8)
    txt_surface = font.render(input_text , True , BLACK)
    screen.blit(txt_surface , (input_box.x + 10 , input_box.y + 10))
    
    if suggestions:
        suggestion_box = pygame.Rect(input_box.x, input_box.y + input_box.height + 5, input_box.width, 30 * len(suggestions))
        draw_rounded_rect(screen, LIGHT_GRAY, suggestion_box, radius=5)
        for idx, suggestion in enumerate(suggestions):
            sug_text = font.render(suggestion, True, BLACK)
            screen.blit(sug_text, (input_box.x + 10, input_box.y + input_box.height + 5 + idx * 30))

    
    # Draw Button ("Recommend")
    draw_rounded_rect(screen , DARK_BLUE , button_rect , radius=8)
    button_text = font.render("Recommend" , True , WHITE)
    screen.blit(button_text , (button_rect.x + 20 , button_rect.y + 10))
    
    # Draw Output Box (for results)
    draw_rounded_rect(screen , WHITE , output_box , radius=10)
    pygame.draw.rect(screen , DARK_BLUE , output_box , 2 , border_radius=10)
    
    # Display Recommendations
    y = output_box.y + 20
    if recommendations :
        result_label = font.render("Top Recommendations : " , True , BLACK)
        screen.blit(result_label , (output_box.x + 20 , y))
        y += 40
        for rec in recommendations:
            bullet_x = output_box.x + 30
            bullet_y = y + 10
            pygame.draw.circle(screen ,DARK_BLUE , (bullet_x , bullet_y) , 5)
            rec_text = font.render(rec , True , DARK_GRAY)
            screen.blit(rec_text , (bullet_x + 20 , y))
            y += 35
            
    # Event Handling (User Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else :
                active = False
            if suggestions:
                for idx, suggestion in enumerate(suggestions):
                    sug_rect = pygame.Rect(input_box.x, input_box.y + input_box.height + 5 + idx * 30, input_box.width, 30)
                    if sug_rect.collidepoint(event.pos):
                        input_text = suggestion
                        suggestions = []
                        recommendations = recommend(input_text)
                        break
            if button_rect.collidepoint(event.pos):
                if input_text.strip():
                    recommendations = recommend(input_text.strip())
                else :
                    recommendations = ["Please enter a Movie Title"]
        elif event.type == pygame.KEYDOWN:
            if active :
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        recommendations = recommend(input_text.strip())
                    else :
                        recommendations = ["Please enter a Movie Title"]
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else :
                    input_text += event.unicode
                # ==== Update Suggestions ====
                if input_text.strip():
                    suggestions = difflib.get_close_matches(input_text.strip(), titles, n=5, cutoff=0.3)
                else:
                    suggestions = []
    pygame.display.flip()

pygame.quit()
sys.exit()
                    
                
        
    
    

    
    



