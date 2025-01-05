import pygame 
import random
pygame.init()

scrWidth = 274
scrHeight = 400

# Create game window
screen = pygame.display.set_mode((scrWidth, scrHeight))
background = pygame.image.load('backgroundimg.jpg')

# Character setup
character = pygame.image.load('character.png')
charWidth, charHeight = character.get_size()
charx = scrWidth // 2 - charWidth // 2
chary = scrHeight // 2 - charHeight // 2
charSpeed = 80

bigCat=pygame.image.load('bigcat.png')
cat=pygame.image.load('cat.png')

points = [(0, 0), (177, 117), (51, 199), (0, 162)] #points for unwalkable areas/polygons
points2= [(0, 331), (53, 365), (0, 400)]
points3= [(127,323),(131,318),(203,369),(222,359),(271,392),(211,399),(175,371),(172,355)]
points4=[(198,250),(245,222),(245,199),(256,187),(224,144),(152,193),(162,205),(160,232)]
unwalkable_polygon = pygame.Surface((scrWidth, scrHeight), pygame.SRCALPHA)  # Create a transparent surface
pygame.draw.polygon(unwalkable_polygon, (255, 0, 0, 128), points)  # Draw polygon with transparency
pygame.draw.polygon(unwalkable_polygon, (255,0,0,128), points2)
pygame.draw.polygon(unwalkable_polygon,(255,0,0,128), points3)
pygame.draw.polygon(unwalkable_polygon,(255,0,0,128),points4)

points5= [(30, 0), (207, 115), (51, 218), (0, 182)] #points for fishing area
points6=[(0,303),(71,360),(32,400)]
points7=[(105,321),(128,303),(203,347),(221,341),(271,368),(275,400),(190,400),(164,377)]
fishing_polygon=pygame.Surface((scrWidth,scrHeight),pygame.SRCALPHA)
pygame.draw.polygon(fishing_polygon,(0,0,100,128),points5)
pygame.draw.polygon(fishing_polygon,(0,0,100,128),points6)
pygame.draw.polygon(fishing_polygon,(0,0,100,128),points7)

points8=[(152,240),(184,259),(195,246),(162,227)] #point for shopping area
shopping_polygon=pygame.Surface((scrWidth,scrHeight),pygame.SRCALPHA)
pygame.draw.polygon(shopping_polygon,(0,0,100,128),points8)

#fshing button properties
font=pygame.font.SysFont(None, 23)
button_visible=False
button_text="Fish!"
button_rect=pygame.Rect(190,55,70,20)

#shopping button
shopButtonVisible=False
shopButton_rect=pygame.Rect(195,220,50,20)
#shopping page
shopVisible=False
shopRect=pygame.Rect((scrWidth-220)//2,(scrHeight-150)//2,220,150)
buy_rect=pygame.Rect(150,200,75,20)
buyVisible=False
boughtCat=False
catPosition=[]

#fish count
fishCount=0
fishCount_rect=pygame.Rect(10,scrHeight-30,90,20)

#caught fish screen
fish_font=pygame.font.SysFont(None,15)
fishCaught_visible=False
fishCaught_text="You caught a fish! \'k\' to continue \'x\' to exit"
fishCaught_rect=pygame.Rect((scrWidth-220)//2,200,220,40)

#fishing game popup
popup_visible=False
popupx=0
skinnyWidth=10
popup_width=50
popup_height=20
popup_speed=300
pop_right=True #direction of popup
popcatch_pos=0

# Create a clock for controlling frame rate
clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time for smooth movement
    # Process events (like keyboard or mouse input)
    for event in pygame.event.get():
        # Check if the close button was clicked
        if event.type == pygame.QUIT:
            running = False
        if event.type ==pygame.MOUSEBUTTONDOWN:
            mouse_pos=pygame.mouse.get_pos()
            if button_visible and button_rect.collidepoint(mouse_pos) and fishCaught_visible==False:
                popup_visible=True
                popcatch_pos=random.randint(0,scrWidth-popup_width)
            if shopButtonVisible and shopButton_rect.collidepoint(mouse_pos):
                shopVisible=True
            if buy_rect.collidepoint(mouse_pos) and buyVisible:
                if fishCount>=5:
                    fishCount-=5
                    tempPostion=(random.randint(0,scrWidth-cat.get_width()),random.randint(0,scrHeight-cat.get_height()))
                    while polygon_mask.overlap(pygame.mask.Mask((cat.get_width(),cat.get_height()),True),tempPostion):
                        tempPostion=(random.randint(0,scrWidth-cat.get_width()),random.randint(0,scrHeight-cat.get_height()))
                    catPosition.append(tempPostion)

        if event.type==pygame.KEYDOWN and popup_visible:
            if rectMoving.colliderect(rectCheck) and event.key==pygame.K_SPACE:
               fishCount+=1
               fishCaught_visible=True
               popup_visible=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_k and fishCaught_visible:
                fishCaught_visible=False
                popup_visible=True
                popcatch_pos=random.randint(0,scrWidth-popup_width)
            if event.key==pygame.K_x and fishCaught_visible:
                fishCaught_visible=False
            if event.key==pygame.K_x and shopVisible:
                shopVisible=False
                buyVisible=False
            if event.key==pygame.K_BACKSPACE:
                catPosition=[]
            if event.key==pygame.K_MINUS:
                catPosition.pop()

    if popup_visible: #fishing code game
        if popupx<=0:
            pop_right=True
        if popupx>=scrWidth-skinnyWidth:
            pop_right=False
        if pop_right==True:
            popupx+=popup_speed*dt
        else:
            popupx-=popup_speed*dt

    oldpos = (charx, chary)  # Store old position for collision handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and charx > 0 and fishCaught_visible==False and shopVisible==False:
        charx -= charSpeed * dt
    if keys[pygame.K_RIGHT] and charx < scrWidth - charWidth and fishCaught_visible==False and shopVisible==False:
        charx += charSpeed * dt
    if keys[pygame.K_UP] and chary > 0 and fishCaught_visible==False and shopVisible==False:
        chary -= charSpeed * dt
    if keys[pygame.K_DOWN] and chary < scrHeight - charHeight and fishCaught_visible==False and shopVisible==False:
        chary += charSpeed * dt

    # Check collision with the unwalkable polygon
    # First, create a mask for the polygon surface
    polygon_mask = pygame.mask.from_surface(unwalkable_polygon)
    fish_mask=pygame.mask.from_surface(fishing_polygon)
    shopping_mask=pygame.mask.from_surface(shopping_polygon)

    # Check if the character collides with the polygon mask
    if polygon_mask.overlap(pygame.mask.Mask((charWidth, 3), True), (charx, chary+charHeight-3)):
        charx, chary = oldpos
    if fish_mask.overlap(pygame.mask.Mask((charWidth,3),True),(charx,chary+charHeight-3)):
        button_visible=True
    else:
        button_visible=False
        popup_visible=False
    if shopping_mask.overlap(pygame.mask.Mask((charWidth,3),True),(charx,chary+charHeight-3)):
        shopButtonVisible=True
    else:
        shopButtonVisible=False

    screen.blit(background, (0, 0))
    #screen.blit(unwalkable_polygon, (0, 0))
    #screen.blit(fishing_polygon,(0,0))
    screen.blit(character, (charx, chary))
    #screen.blit(shopping_polygon,(0,0))
    for pos in catPosition:
        screen.blit(cat,pos)
    if button_visible:
        pygame.draw.rect(screen,(20,0,20,230),button_rect)
        text_surface=font.render(button_text,True,(255,255,255))
        text_rect=text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface,text_rect)
    if shopButtonVisible:
        pygame.draw.rect(screen,(0,0,0),shopButton_rect)
        shopButton_ts=font.render("Shop",True,(255,255,255))
        shopButton_tr=shopButton_ts.get_rect(center=shopButton_rect.center)
        screen.blit(shopButton_ts,shopButton_tr)
    if fishCaught_visible:
        pygame.draw.rect(screen,(50,50,100),fishCaught_rect)
        fishCaught_textSurface=fish_font.render(fishCaught_text,True,(255,255,255))
        fishCaught_textRect=fishCaught_textSurface.get_rect(center=fishCaught_rect.center)
        screen.blit(fishCaught_textSurface,fishCaught_textRect)
    if popup_visible:  # Only draw if it's on screen
        rectCheck = pygame.Rect(popcatch_pos,10,popup_width,popup_height)
        rectMoving = pygame.Rect(popupx,10,skinnyWidth,popup_height)
        pygame.draw.rect(screen,(0,0,0),(0,10,scrWidth,popup_height))
        pygame.draw.rect(screen,(255,0,0),(rectCheck))
        pygame.draw.rect(screen, (200, 200, 250), (rectMoving))
    if shopVisible:
        pygame.draw.rect(screen,(0,0,0),shopRect)
        close_text=fish_font.render("Press \"x\" to exit",True,(255,255,255))
        close_text_rect=close_text.get_rect(center=pygame.Rect((scrWidth-220)//2,255,220,20).center)
        sellingtxt=font.render("Exchange 5 fishes for a cat!",True,(255,255,255))
        sellingtxt_rect=sellingtxt.get_rect(center=pygame.Rect((scrWidth-220)//2,133,220,20).center)
        buyVisible=True
        buy_text=font.render("Exchange",True,(0,0,0))
        buy_textrect=buy_text.get_rect(center=buy_rect.center)
        screen.blit(sellingtxt,sellingtxt_rect)
        screen.blit(close_text,close_text_rect)
        pygame.draw.rect(screen,(250,200,250),buy_rect) #background for exchange button
        screen.blit(buy_text,buy_textrect)
        screen.blit(bigCat,(40,160))
    #fish count display
    pygame.draw.rect(screen,(50,50,100),fishCount_rect)
    fishCount_ts=font.render("Fish: " + str(fishCount),True,(255,255,255))
    fishCount_tr=fishCount_ts.get_rect(center=fishCount_rect.center)
    screen.blit(fishCount_ts,fishCount_tr)
    pygame.display.update()

pygame.quit()
