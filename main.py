# 準備
import pygame as pg
import sys
import random
import asyncio

pg.init()

screen = pg.display.set_mode((800, 600))
pg.display.set_caption("ブロック崩し")

clock = pg.time.Clock()

# サウンドデータ
hit_sound = pg.mixer.Sound("sounds/blockbreaker_hit.ogg")

# バーデータ
barrect = pg.Rect(400, 500, 80, 30)

# ボールデータ
balling = pg.image.load("images/akuma.png")
balling = pg.transform.scale(balling, (70, 70))
ballrect = pg.Rect(400, 450, 70, 70)

vx = random.choice([-5, 5])
vy = -5

# ボタンデータ
replay_img = pg.image.load("images/akuma.png")
replay_img = pg.transform.scale(replay_img, (100, 100))

# ブロックデータ
blocks = []

for yy in range(4):
    for xx in range(7):
        blocks.append(pg.Rect(50 + xx * 100, 40 + yy * 50, 80, 30))

# メインループで使う変数
pushFlag = False
page = 1
score = 0


# ボタンを押したら新しいページに飛ぶ
def button_to_jump(btn, newpage):
    global page, pushFlag

    mdown = pg.mouse.get_pressed()
    mx, my = pg.mouse.get_pos()

    if mdown[0]:
        if btn.collidepoint(mx, my) and pushFlag == False:
            hit_sound.play()
            page = newpage
            pushFlag = True
    else:
        pushFlag = False


# ゲームステージ
def gamestage():
    global vx, vy
    global page
    global score

    screen.fill(pg.Color("BLUE"))

    # バーの移動
    mx, my = pg.mouse.get_pos()
    barrect.x = mx - 40

    # バーが画面から出ないようにする
    barrect.x = max(0, min(barrect.x, 720))

    pg.draw.rect(screen, pg.Color("YELLOW"), barrect)

    # ボールの処理
    if ballrect.y < 0:
        vy = abs(vy)

    if ballrect.x < 0 or ballrect.x > 730:
        vx = -vx

    if barrect.colliderect(ballrect) and vy > 0:
        vx = int(((ballrect.x + 35) - (barrect.x + 40)) / 4)
        vy = random.randint(-10, -5)
        hit_sound.play()

    if ballrect.y > 600:
        page = 2
        hit_sound.play()

    ballrect.x += vx
    ballrect.y += vy

    screen.blit(balling, ballrect)

    # ブロックの処理
    for n, block in enumerate(blocks):
        if block.width > 0:
            pg.draw.rect(screen, pg.Color("GREEN"), block)

            # ブロックとボールがぶつかったら
            if block.colliderect(ballrect):
                vy = -vy
                blocks[n] = pg.Rect(0, 0, 0, 0)
                score += 1
                hit_sound.play()

                if score == 28:
                    page = 3

    # スコア表示
    font = pg.font.Font(None, 40)
    text = font.render("SCORE : " + str(score), True, pg.Color("WHITE"))
    screen.blit(text, (10, 550))


# データのリセット
def gamereset():
    global vx, vy
    global score
    global blocks

    vx = random.choice([-5, 5])
    vy = -5

    ballrect.x = 400
    ballrect.y = 450

    barrect.x = 400

    score = 0

    # ブロックを作り直す
    blocks = []

    for yy in range(4):
        for xx in range(7):
            blocks.append(pg.Rect(xx * 100 + 50, yy * 50 + 40, 80, 30))


# ゲームオーバー
def gameover():
    screen.fill(pg.Color("BLUE"))

    font = pg.font.Font(None, 100)
    text = font.render("GAME OVER", True, pg.Color("RED"))
    screen.blit(text, (120, 200))

    btn1 = screen.blit(replay_img, (350, 350))

    button_to_jump(btn1, 1)

    if page == 1:
        gamereset()


# ゲームクリア
def gameclear():
    screen.fill(pg.Color("GOLD"))

    font = pg.font.Font(None, 100)
    text = font.render("GAME CLEAR", True, pg.Color("RED"))
    screen.blit(text, (100, 200))

    btn1 = screen.blit(replay_img, (350, 350))

    button_to_jump(btn1, 1)

    if page == 1:
        gamereset()


# メインループ
async def main():

    while True:

        # イベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

        # ページ処理
        if page == 1:
            gamestage()

        elif page == 2:
            gameover()

        elif page == 3:
            gameclear()

        # 画面を表示する
        pg.display.update()
        clock.tick(60)

        # ブラウザに処理を渡す
        await asyncio.sleep(0)


# プログラム実行
asyncio.run(main())
