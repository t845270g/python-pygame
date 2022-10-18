
from cmath import rect
from re import S
from tkinter import CENTER, FALSE
from numpy import size
import pygame,random,os
#初始化遊戲
pygame.init()
pygame.mixer.init()#音效模組初始化

#固定的變數值，用大寫表示往後不會更動
FPS=60#跑迴圈的頻率
WIDTH=500#視窗寬
HIGH=600#視窗高
high_score=0
tt=0
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
ORG=(255, 120, 0)
yellow=(255,255,0)

#創建視窗
screen=pygame.display.set_mode((WIDTH,HIGH),pygame.RESIZABLE)#寬x高 像素
pygame.display.set_caption("太空生存戰")#設置標題，修改視窗標題名稱

clock=pygame.time.Clock()#創建時間物件

#載入圖片
backround_img=pygame.image.load(os.path.join("img","backround.jpg")).convert()#os.path指當前檔案位置找當中的img資料夾，裡面的指定檔案。convert轉成pygame易讀格式，讓執行速度比較快


player_img=pygame.image.load(os.path.join("img","player.jpg")).convert()
mini_img_w=20
mini_img_h=30
player_mini__img=pygame.transform.scale(player_img,(mini_img_w,mini_img_h))
player_mini__img.set_colorkey(BLACK)

pygame.display.set_icon(player_mini__img)

bullet_img=pygame.image.load(os.path.join("img","bullet.jpg")).convert()
bullet_img.set_colorkey(BLACK)

sp_img=pygame.image.load(os.path.join("img","spshoot.jpg")).convert()
sp_img.set_colorkey(BLACK)

rock_img=pygame.image.load(os.path.join("img","rock.jpg")).convert()

掉寶字典={}
掉寶字典["hp"]=pygame.image.load(os.path.join("img","HP.jpg")).convert()
掉寶字典["shoot"]=pygame.image.load(os.path.join("img","sp.jpg")).convert()
掉寶字典["pro"]=pygame.image.load(os.path.join("img","pro.jpg")).convert()



#爆炸動畫
#匯入爆炸圖片，用字典存成兩個key，分別是大爆炸與小爆炸，每個key對應一個列表，存放匯入調整好尺寸的圖片
爆炸圖片字典 = {}
爆炸圖片字典["lg"]=[]
爆炸圖片字典["sm"]=[]
爆炸圖片字典["fs"]=[]
for i in range(1,8):
    expl_img = pygame.image.load(os.path.join("img",f"f0{i}.jpg")).convert()
    fs_img = pygame.image.load(os.path.join("img",f"fs0{i}.jpg")).convert()
    expl_img.set_colorkey(BLACK)
    fs_img.set_colorkey(BLACK)
    爆炸圖片字典["lg"].append(pygame.transform.scale(expl_img,(75,75)))
    爆炸圖片字典["sm"].append(pygame.transform.scale(expl_img,(30,30)))
    爆炸圖片字典["fs"].append(pygame.transform.scale(fs_img,(200,200)))
#{"lg":[.,.,.,.] , "sm":[.,.,.,.] }

開始遊戲時間=0
#載入音效
shoot_sound=pygame.mixer.Sound(os.path.join("music","shoot.wav"))#實體化音樂檔案
sp_shoot_sound=pygame.mixer.Sound(os.path.join("music","laser_beam.mp3"))#實體化音樂檔案
bloom_sound=pygame.mixer.Sound(os.path.join("music","bloom.mp3"))
sp_bloom_sound=pygame.mixer.Sound(os.path.join("music","explosion2.mp3"))
die_sound=pygame.mixer.Sound(os.path.join("music","fs_bloom.mp3"))
被攻擊音效=pygame.mixer.Sound(os.path.join("music","pyo1.mp3"))
吃心音效=pygame.mixer.Sound(os.path.join("music","poka03.mp3"))
吃閃電音效=pygame.mixer.Sound(os.path.join("music","minimam_laser.mp3"))
吃盾牌音效=pygame.mixer.Sound(os.path.join("music","powerup10.mp3"))
加命音效=pygame.mixer.Sound(os.path.join("music","coin08.mp3"))

#顯示初始畫面
def draw_init():
    #播放背景音樂
    pygame.mixer.music.load(os.path.join("music","BGM.mp3"))#背景音樂要重播用.music.load載入音樂慢慢撥出
    pygame.mixer.music.set_volume(0.2)#調整音量
    pygame.mixer.music.play(-1)#-1為重複撥放

    #畫背景
    screen.blit(backround_img,(0,0))

    #寫字
    draw_text(screen,"太空生存戰",64,WIDTH/2,HIGH/4)
    draw_text(screen,"← → ↑ ↓ 鍵移動飛船，空白鍵發射子彈",22,WIDTH/2,HIGH/2)
    draw_text(screen,"最高分:"+str(high_score),30,int(WIDTH/2),HIGH/1.6,yellow)#印出分數
    draw_text(screen,"~請按任意鍵，開始遊戲~",18,WIDTH/2,HIGH*3/4,RED)

    #顯示更新
    pygame.display.update()

    #一開始直接跑迴圈
    waiting = True
    while waiting:
        clock.tick(FPS)#每秒最多被執行十次

        for event in pygame.event.get():#回傳發生得所有事件，用列表回傳
            if event.type==pygame.QUIT:#<Event(256-Quit {})>，可以寫呼叫的方法也可以寫代號值，如果按了叉叉就關掉
                pygame.quit()
                return True

            elif event.type==pygame.KEYUP:#如果有按鍵被按下放開
                pygame.time.wait(1000)
                開始遊戲時間=pygame.time.get_ticks()
                waiting = False
                return False

#畫生命條
def draw_health(surf,hp,x,y):
    if hp < 0 :
        hp = 0
        
    BAR_LENGTH = 100 #生命條寬度
    BAR__HIGH = 10 #生命條高度
    fill=(hp/100)*BAR_LENGTH #生命條填滿多少(寬)

    #Rect(left, top, 寬, 高)
    fill_rect = pygame.Rect(x,y,fill,BAR__HIGH)#生命值填色與樣式
    pygame.draw.rect(surf,GREEN,fill_rect)#61~100填綠色

    if 30<=hp<=60:
        pygame.draw.rect(surf,ORG,fill_rect)#30~60填橘色
    elif hp<30:
        pygame.draw.rect(surf,RED,fill_rect)#小於30填紅色

    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR__HIGH)#生命值框框樣式，寫在下面會顯示在最上層
    pygame.draw.rect(surf,WHITE,outline_rect,2)

#加隕石回群組函式
def new_rock():
    r=Rock()
    rocks群組.add(r)
    all_sprites群組.add(r)

#印出分數
font_name = os.path.join("word","msjhbd.ttc")# 匯入字體，在系統中搜索一種特殊的字體，將字體存入記憶體中
def draw_text(surf,text,size,x,y,color=WHITE):#寫在哪,文字內容,大小,座標
    font = pygame.font.Font(font_name,size)#取用字體，設定字體大小
    印出的字 = font.render(text,True,color)#印出的字串,(布林值)是否開啟抗鋸齒,字體顏色,背景顏色(默認透明)
    text_rect = 印出的字.get_rect()#定位文字
    text_rect.centerx = x #x座標
    text_rect.top = y  #y座標
    surf.blit(印出的字,text_rect)#畫出來(印的字串,定位點)

#畫命數量
def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 25*i
        img_rect.y = y
        surf.blit(img,img_rect)




#設定物件類別
#玩家
class Player(pygame.sprite.Sprite):#設定類別Player，繼承pygame模組中內建的類別Sprite
    
    def __init__(self):#初始化Player類別
        pygame.sprite.Sprite.__init__(self)#呼叫繼承類別的初始化函數
        self.image=pygame.transform.scale(player_img,(50,70))#建立屬性image，放入一個改變尺寸的圖片
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()#建立屬性rect，定位此物件，可以調整前面建立的物件屬性的詳細參數
        self.radius=26#設定圓形判斷的範圍屬性
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)#畫出圓形位置檢查判斷範圍
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HIGH-20
        self.speed=8
        self.health=100
        self.lives=1
        self.hidden=False
        self.hide_time=0
        self.shoot_level=0
        

    def update(self):#update為Sprite的內建函數，所以必須要使用次名稱才能呼叫此函數
        key_pressed=pygame.key.get_pressed()#傳回所有鍵盤按鍵是否有被按下去的布林值，所有清單在constants.py中
        
        if key_pressed[pygame.K_RIGHT]:#判斷鍵盤按上的話，將物件每次右移指定像素
            self.rect.x+=self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x-=self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y-=self.speed-2
        if key_pressed[pygame.K_DOWN]:
            self.rect.y+=self.speed-2

        if self.rect.right > WIDTH:#如果物件右側位置超過式窗寬度，讓最右側位置設定為視窗寬度
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 45:
            self.rect.top = 45
        if self.hidden==False:
            if self.rect.bottom > HIGH:
                self.rect.bottom = HIGH   
        if    self.hidden    and     pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden=False
            self.rect.center=(WIDTH/2,HIGH-55)
    #普通子彈射擊
    def shoot(self):#呼叫此函式會提供Bullet Player的座標，並將其實體化，增加到顯示的群組中
        if self.hidden==False and sp_shoot==False and self.shoot_level==0:#活著，普通子彈模式，等級0
            bullet=Bullet(self.rect.centerx,self.rect.top)
            all_sprites群組.add(bullet)
            bullets群組.add(bullet)
            shoot_sound.play()
            shoot_sound.set_volume(0.1)
        elif self.hidden==False and sp_shoot==False and self.shoot_level==1:#活著，普通子彈模式，等級1>一次兩發
            bullet=Bullet(self.rect.left+15,self.rect.top)
            bullet2=Bullet(self.rect.right-15,self.rect.top)
            all_sprites群組.add(bullet)
            all_sprites群組.add(bullet2)
            bullets群組.add(bullet)
            bullets群組.add(bullet2)
            shoot_sound.play()
            shoot_sound.set_volume(0.1)

    #特殊子彈射擊    
    def spshoot(self):
        if sp_shoot==True:
            bullet=Bullet(self.rect.centerx,self.rect.top)
            all_sprites群組.add(bullet)
            spbullets群組.add(bullet)
            sp_shoot_sound.play()
            sp_shoot_sound.set_volume(0.1)

    #生命值歸零暫時隱藏
    def hide(self):
        self.hidden=True
        self.hide_time=pygame.time.get_ticks()
        self.rect.centery=HIGH+500

    #普通子彈等級升級
    def shoot_level_up(self):
        self.shoot_level=1


#隕石    
class Rock(pygame.sprite.Sprite):#設定類別Player，繼承pygame模組中內建的類別Sprite
    
    def __init__(self):#初始化Player類別
        pygame.sprite.Sprite.__init__(self)#呼叫繼承類別的初始化函數
        self.size=random.randrange(30,180,20)
        self.image_ori = pygame.transform.scale(rock_img,(self.size,self.size))#建立屬性image，開一個寬50，高40像素的框來表示<<物件>>
        self.image_ori.set_colorkey(BLACK)  
        self.image = self.image_ori.copy()
        self.rect=self.image.get_rect()#建立屬性rect，定位此物件，可以調整前面建立的物件屬性的詳細參數
        self.radius=self.rect.width/2#設定圓形判斷的範圍屬性
        #pygame.draw.circle(self.image_ori,RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,4)
        self.speedx = random.randrange(-3,3)
        self.total_degree=0#計算每次轉動加上去的角度總和
        self.rot_degree=random.randrange(-3,3)#每次轉動的角度

    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree%360#轉超過360度會取餘數值繼續轉動加上去
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)#轉動函數(原本的圖片,轉動的角度)
        center=self.rect.center#開一個記憶體，存入圖片中心點
        self.rect=self.image.get_rect()#重新取得(旋轉後的圖片的)定位
        self.rect.center=center#再將中心點提供給新角度的圖片中心
        #中心點固定，圖片每次旋轉都重新給原本的中心位置，就能在固定點原地旋轉

    def update(self):#update為Sprite的內建函數，所以必須要使用次名稱才能呼叫此函數
        self.rotate()
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top > HIGH    or   self.rect.right < 0     or    self.rect.left > WIDTH:
            self.rect.y=random.randrange(-100,-40)
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.speedy = random.randrange(2,4)
            self.speedx = random.randrange(-3,3)
            if score >= 500:
                self.speedy = random.randrange(2,6)
                self.speedx = random.randrange(-3,3)            
            if score >= 1000:
                self.speedy = random.randrange(6,10)
                self.speedx = random.randrange(-4,4)    
            if score >= 2000: 
                self.speedy = random.randrange(6,12)
                self.speedx = random.randrange(-5,5)   
            if score >= 5000: 
                self.speedy = random.randrange(8,15)
                self.speedx = random.randrange(-5,5)   
            if score >= 10000: 
                self.speedy = random.randrange(10,17)
                self.speedx = random.randrange(-5,5)  
            if score >= 15000: 
                self.speedy = random.randrange(13,17)
                self.speedx = random.randrange(-6,6)  
            if score >= 20000: 
                self.speedy = random.randrange(15,17)
                self.speedx = random.randrange(-7,7)  

#子彈
class Bullet(pygame.sprite.Sprite):#設定類別Player，繼承pygame模組中內建的類別Sprite
    
    def __init__(self,x,y):#初始化Player類別，還要傳入飛船的座標資訊才能決定子彈位置
        pygame.sprite.Sprite.__init__(self)#呼叫繼承類別的初始化函數

        #發射普通子彈
        if sp_shoot==False:
            self.image=pygame.transform.scale(bullet_img,(10,50))#建立屬性image，開一個寬50，高40像素的框來表示<<物件>>
            self.rect=self.image.get_rect()#建立屬性rect，定位此物件，可以調整前面建立的物件屬性的詳細參數
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = -10

        #發射特別子彈
        if sp_shoot==True:
            self.image=pygame.transform.scale(sp_img,(WIDTH,50 ))#建立屬性image，開一個寬50，高40像素的框來表示<<物件>>
            self.rect=self.image.get_rect()#建立屬性rect，定位此物件，可以調整前面建立的物件屬性的詳細參數
            self.rect.centerx= WIDTH/2
            self.rect.bottom = y
            self.speedy = -10

    def update(self):#update為Sprite的內建函數，所以必須要使用次名稱才能呼叫此函數
        self.rect.y+=self.speedy
        if self.rect.bottom < 0:#當子彈超出螢幕上方
            self.kill()#刪除此物件，kill函式在Sprite類別中的內建函式

#掉寶
class 掉寶(pygame.sprite.Sprite):#設定類別Player，繼承pygame模組中內建的類別Sprite
    
    def __init__(self):#初始化Player類別
        pygame.sprite.Sprite.__init__(self)#呼叫繼承類別的初始化函數
        a=random.randint(1,15)
        if a==1:#決定掉落的寶物的機率判斷
            self.photo="shoot" 
        elif a==2 or a==3:
            self.photo="pro"
        else:
            self.photo="hp"

        self.image=pygame.transform.scale(掉寶字典[self.photo],(30,30))#建立屬性image，放入一個改變尺寸的圖片
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.radius=13
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)#畫出圓形位置檢查判斷範圍
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,8)
        

    def update(self):#update為Sprite的內建函數，所以必須要使用次名稱才能呼叫此函數
        self.rect.y+=self.speedy
        if self.rect.top > HIGH:#當子彈超出螢幕上方
            self.kill()#刪除此物件，kill函式在Sprite類別中的內建函式

#爆炸
class bloom(pygame.sprite.Sprite):#設定類別Player，繼承pygame模組中內建的類別Sprite
    def __init__(self,center,size):#初始化Player類別，還要傳入飛船的座標資訊才能決定子彈位置
        pygame.sprite.Sprite.__init__(self)#呼叫繼承類別的初始化函數
        self.size = size# "lg"  or "sm" or "fs"
        self.image=爆炸圖片字典[self.size][0]#大或小爆炸的第0張圖片
        self.rect=self.image.get_rect()#定位
        self.rect.center = center#取中心座標
        self.frame = 0#紀錄顯示圖片的第幾張
        self.last_update = pygame.time.get_ticks()#初始化到當下經過的毫秒數。
        self.frame_rate = 60 #經過幾毫秒到下一張圖
    
    def update(self):
        now = pygame.time.get_ticks()#最新時間毫秒
        if now-self.last_update>self.frame_rate:#醉心時間減掉前一張圖的時候的時間，如果超過指定毫秒數
            self.last_update = now#把更新最後一張圖的時間換成最新時間
            self.frame += 1 # 把紀錄第幾張圖片的數值加一
            if self.frame == len(爆炸圖片字典[self.size]):#如果統計照片數值跟所有圖片一樣多(也就是所有圖片都顯示過一次了)
                self.kill()#刪除物件
            else:
                self.image = 爆炸圖片字典[self.size][self.frame]#否則針對大爆炸或小爆炸的列表，按照frame的順序取出圖片
                center = self.rect.center#紀錄第一章圖的中心點
                self.rect = self.image.get_rect()#把下一張圖片定位
                self.rect.center = center#將第一張圖的中心點座標給新的圖

#加命圖
class 加命(pygame.sprite.Sprite):
    def __init__(self):#初始化Player類別
        pygame.sprite.Sprite.__init__(self)#呼叫繼承類別的初始化函數
        self.image=player_mini__img
        self.image=pygame.transform.scale(player_img,(30,50))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.x=random.randint(0,WIDTH-mini_img_w)
        self.rect.y=random.randint(50,HIGH-150)
        self.radius=15
        screen.blit(self.image,self.rect)




show_init = True
running=True

while running:#迴圈每秒跑10萬次
    #顯示初始畫面
    
    if show_init ==True:
        close=draw_init()
        if close == True:#如果初始介面就按叉叉退出(回傳真)，直接跳出迴圈
            break
        else:#如果有按任意鍵進入遊戲(回傳假)，關掉初始介面
            show_init=False
        
        #一開始設定分數為0，特殊子彈不開啟，兩發子彈也不開啟
        score=0
        sp_shoot=False
        two_shoot=False
        
        #在視窗中顯示物件
        #建立顯示在視窗的物件群組，實體化以後，物件就會在設定的位置出現
        all_sprites群組 = pygame.sprite.Group()#建立物件的群組，pygame內建類別Group繼承了AbstractGroup類別，所以要使用裡面的函式就要從實體化的類別去呼叫
        rocks群組 = pygame.sprite.Group()
        bullets群組 = pygame.sprite.Group()
        spbullets群組 = pygame.sprite.Group()
        寶物群組 = pygame.sprite.Group()
        加命群組=pygame.sprite.Group()

        #實體化飛船
        player = Player()#實體化Player類別
        #顯示飛船
        all_sprites群組.add(player)#把實體化的物件加到群組中
        
        #顯示隕石掉落
        for i in range(15):#創建多個重複物件，都加到群組中
            new_rock()



    clock.tick(FPS)#每秒最多被執行十次
    
    #取得輸入
    for event in pygame.event.get():#回傳發生得所有事件，用列表回傳
        if event.type==pygame.QUIT:#<Event(256-Quit {})>，可以寫呼叫的方法也可以寫代號值，如果按了叉叉就關掉
       #if event.type==256:
            running=False
        elif event.type==pygame.KEYDOWN:#如果有按鍵被按下
            if event.key==pygame.K_SPACE:#判斷是不是空白建
            #if event.key==32:
                if sp_shoot == False:#如果沒開啟特殊子彈模式，打普通子彈
                    player.shoot()#是的話呼叫player的shoot函式
                if sp_shoot == True:#如果開啟特殊子彈模式，打特殊子彈一發，打出後關閉特殊子彈模式
                    player.spshoot()#是的話呼叫player的shoot函式
                    sp_shoot  = False
                
             



    #攻擊事件1-普通子彈攻擊，擊中會爆炸然後消失得分，且有一定機率掉寶，消失的隕石將會重新產生
    hits = pygame.sprite.groupcollide(rocks群組,bullets群組,True,True)#隕石群組與子彈群組發生碰撞，第一個布林值對應第一個物件是否消失，第二個布林值對第二個物件，回傳字典，碰撞的兩個物件{<Rock Sprite(in 0 groups)>: [<Bullet Sprite(in 0 groups)>]}                                              
    for h in hits:#如果hits有回傳字典，因為 物件會消失，所以就在把石頭加回群組顯示，石頭數量就會維持不變
        if h.size > 100 :
            score += int(h.size/8)
        if h.size <= 100 :
            score += int(h.size/10)
        if random.randint(1,15)==1:#如果攻擊到隕石，就產生一個數字 判斷這個數字是不是1

            寶=掉寶() #是的話就產生一個寶物掉出
            all_sprites群組.add(寶)#加到全部的群組呼叫更新才會顯示
            寶物群組.add(寶)#加到寶物的群組，後面才可以和玩家碰撞事件做判斷


        expl = bloom(h.rect.center,"lg")#爆炸的中心點取隕石圖片碰撞瞬間時的中心座標，讀取大爆炸的圖片
        all_sprites群組.add(expl)
        bloom_sound.play()
        bloom_sound.set_volume(0.1)
        new_rock()#產生新隕石
        
    #攻擊事件2-特殊子彈攻擊，擊中子彈不會消失，橫掃式攻擊    
    sphits = pygame.sprite.groupcollide(rocks群組,spbullets群組,True,False)#隕石消失，子彈不會消失 
    for h in sphits:
        if h.size > 100 :
            score += int(h.size/8)
        if h.size <= 100 :
            score += int(h.size/10)
        #如果攻擊到隕石，就產生一個數字
        if random.randint(1,15)==1:#判斷這個數字是不是小於5
            s=random.randint(1,15)
            if s>3:
                寶=掉寶() #是的話就產生一個加命物件掉出
                all_sprites群組.add(寶)#加到全部的群組呼叫更新才會顯示
                寶物群組.add(寶)#加到hp己的群組，後面才可以和玩家碰撞事件做判斷
            else:
                hp=加命()
                加命群組.add(hp)
                all_sprites群組.add(hp)

        expl = bloom(h.rect.center,"lg")#爆炸的中心點取隕石圖片碰撞瞬間時的中心座標，讀取大爆炸的圖片
        all_sprites群組.add(expl)
        sp_bloom_sound.play()
        sp_bloom_sound.set_volume(0.05)
        new_rock()#產生新隕石


    #被攻擊事件
    hits2 = pygame.sprite.spritecollide(player,rocks群組,True,pygame.sprite.collide_circle)#玩家與隕石發生碰撞
     #用圓形判斷碰撞，物件要增加radius的屬性，設定圓形尺寸當作判斷範圍
    for hit in hits2:
        if hit.size > 100:
            player.health-=int(hit.size/4)
        if hit.size <= 100:
            player.health-=int(hit.size/5)

        new_rock() 
        被攻擊音效.play()
        被攻擊音效.set_volume(0.2)
        expl = bloom(hit.rect.center,"sm")
        all_sprites群組.add(expl)

        player.shoot_level=0#被攻擊的話一次兩發子彈的能力就要關閉

        if player.health<=0:#如果生命值歸零的話
            die_sound.play()
            die = bloom(player.rect.center,"fs")#播放飛船爆炸聲音
            all_sprites群組.add(die)#飛船爆炸動畫
            player.hide()#隱藏飛船指定時間
            player.lives -= 1#生命少一條
            sp_shoot=False#失去特殊子彈的能力
            if player.lives > 0:#如果還有命的話
                player.health = 100#回復血量為100
    
    
    #掉寶碰撞事件
    hits3 = pygame.sprite.spritecollide(player,寶物群組,True,pygame.sprite.collide_circle)#玩家與加命發生碰撞
    for hit in hits3:
        #補血
        if hit.photo == "hp":
            吃心音效.play()
            吃心音效.set_volume(0.5)
            score+=10
            if  0 < player.health < 100 :   #如果生命值小於100
                player.health += 10         #增加生命值
                if player.health >= 100 :   #如果增加生命值後過100
                    player.health = 100     #把值設為100

        #一次兩發子彈            
        if hit.photo == "pro" :
            吃閃電音效.play()
            吃閃電音效.set_volume(0.5)
            if player.shoot_level==0:
                score+=15
            if player.shoot_level==1:
                score+=25            
            player.shoot_level_up()#吃到可一次發射兩發子彈

        #特別子彈
        if hit.photo == "shoot":
            吃盾牌音效.play()
            吃盾牌音效.set_volume(0.5)
            score+=30
            if  0 < player.health:#如果活著的話就可以發射特殊子彈
                sp_shoot=True

    #吃到加命    
    hits4 = pygame.sprite.spritecollide(player,加命群組,True,pygame.sprite.collide_circle)#玩家與加命發生碰撞
    for i in hits4:
        加命音效.play()
        加命音效.set_volume(0.5)
        score+=50
        if player.lives<5:
            player.lives+=1

    #更新遊戲，碰撞寫在更新遊戲顯示後才能不斷更新要顯示的物件
    all_sprites群組.update()#呼叫AbstractGroup類別中的update函式，更新數值
    #畫面顯示
    screen.blit(backround_img,(0,0))#圖片先用convert()處理過，在繪製到視窗(處理過的圖片,畫的位置(x,y))
    all_sprites群組.draw(screen)#在指定視窗中，將all_sprites群組內的所有物件繪製出來
    draw_text(screen,"score:"+str(score),18,WIDTH/2,12)#印出分數
    draw_health(screen,player.health,WIDTH/9,20)
    draw_lives(screen,player.lives,player_mini__img,WIDTH-150,10)

    #game over    
    if player.lives <= 0 and die.alive()==False:#如果完全沒命了並且撥放完飛船爆炸的動畫(顯示狀態為假)
        if score > high_score :
            high_score=score
        pygame.time.wait(1000)
        pygame.mixer.music.stop()
        show_init = True

    pygame.display.update()#更新畫面  

pygame.quit()
pygame.display.quit()
#終端機輸入auto-py-to-exe轉出exe檔