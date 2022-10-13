from venv import create
from cv2 import rotate
import pygame, sys, random #sys để sửa lỗi:  video system not initialized

#tạo hàm cho trò chơi

def draw_floor(): #vẽ sàn
    screen.blit(floor,(floor_x_pos,650))# ox để di chuyển ngang. oy để di chuyển dọc
    screen.blit(floor,(floor_x_pos+432,650))#do chục x của display là 432, nên tạo để chục x thứ 2 kế tiếp luôn chục thứ nhất
def create_pipe(): #tạo ống
    random_pipe_pos = random.choice(pipe_heigt) # chiều cao random từ list pipe_heigt
    bottom_pipe = pipe_surface.get_rect(midtop=(500,random_pipe_pos)) #chiều cao oy random, cuối màn ox
    top_pipe = pipe_surface.get_rect(midtop=(500,random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes): #di chuyển ống
    for pipe in pipes :
        pipe.centerx -= 3 #tốc độ ống
    return pipes
def draw_pipe(pipes): #vẽ ống ra
    for pipe in pipes:
        if pipe.bottom >= 600 :
            screen.blit(pipe_surface,pipe) #pipe_surface : hình trèn vào
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            #flip để lật, false ,true để lập theo chục x hoặc y, để true ở y để lật theo oy
            screen.blit(flip_pipe,pipe)
def check_collision(pipes): #hàm sử lý va chạm
    for pipe in pipes:
        if bird_rect.colliderect(pipe): #nếu rect của chim va chạm với ống
             return True
    if bird_rect.top <=- 75 or bird_rect.bottom >= 650:
        return False
    return True 
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*4,1) #rotozoom giúp xoay, ( đối tượng, chiều xoay. scale)
    return new_bird 
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery)) #căn giữa khoảng cách 100 vs giữa trục y
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state =='main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))#chữ muốn điền vào, true or false, màu chữ
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)#vẽ giá trị lên màn hình
    if game_state =='game over': 
        score_surface = game_font.render(f'Score: {int(score)} ', True, (255,255,255))#chữ muốn điền vào, true or false, màu chữ
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)#vẽ giá trị lên màn hình


        high_score_surface = game_font.render(f'High Score: {int(high_score)} ', True, (255,255,255))#chữ muốn điền vào, true or false, màu chữ
        high_score_rect = high_score_surface.get_rect(center = (216,620))
        screen.blit(high_score_surface,high_score_rect)#vẽ giá trị lên màn hình
def update_score(score, high_score): #update điểm high_score
    if score > high_score :
        high_score = score
    return high_score
pygame.init()
screen=pygame.display.set_mode((432,768))# tạo display với kích thước kia
clock =pygame.time.Clock()#set fps
game_font = pygame.font.SysFont('04B_19.TTF',40) #font chữ down trên mạng, size 40

#tạo các biến cho trò chơi
gravity = 0.35 # thêm biến trọng lực
bird_movement = 0 # thêm biến cho sự di chuyển của chim
game_active = True
score =0
high_score =0
#chèn background+ sàn
bg = pygame.image.load('/Workspace/pygame/flbirt/FileGame/assets/background-night.png').convert()#set background, convert: đổi file ảnh thành 1 file nhẹ hơn để pygame load nhanh hơn
bg = pygame.transform.scale2x(bg) #set scale x2 so với ban đầu
floor = pygame.image.load('/Workspace/pygame/flbirt/FileGame/assets/floor.png').convert()#set sàn
floor = pygame.transform.scale2x(floor)
floor_x_pos =0 # gọi tọa độ ban đầu của floor
#tạo chim
bird_down = pygame.image.load('/Workspace/pygame/flbirt/FileGame/assets/namlol.png').convert_alpha()#convert_alpha để bỏ phần đen của rotozoom
bird_mid = pygame.image.load('/Workspace/pygame/flbirt/FileGame/assets/namlol.png').convert_alpha()
bird_up = pygame.image.load('/Workspace/pygame/flbirt/FileGame/assets/namlol.png').convert_alpha()
bird_list=[bird_down,bird_mid,bird_up] #0,1,2 : bird list chứa 3 biến
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load('/Workspace/pygame/flbirt/FileGame/assets/hiha.png').convert_alpha()
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center= (100,384)) #tạo hình chữ nhật sung quanh con chim cách chục x 100 và cách chục y 1 nửa của 768

#tạo timer cho bird
birdflap= pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
#tạo ống
pipe_surface = pygame.image.load('/Workspace/pygame/flbirt/FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] #list rỗng để chứa tất các các ống tạo ra
#tạo timer
spawnpipe=pygame.USEREVENT #để xuất hiện những ống lien tục
pygame.time.set_timer(spawnpipe,1700) #sau 1,2s thì sẽ tạo 1 ống mới

pipe_heigt = [200,230,250,270,300,340,370,400] #độ cao ống 
#tạo màn hình endgame
game_over_surface = pygame.transform.scale2x(pygame.image.load('/Workspace/pygame/flbirt/FileGame/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))
#vòng lặp frame
while True:
    for event in pygame.event.get():#replay tất cả các sự kiện diễn ra
        if event.type == pygame.QUIT: #nếu người chơi ấn phím thoát ra ngoài
            pygame.quit()
            sys.exit() # sửa lỗi : video system not initialized
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active: #khi game hoạt động
               #print("chim") test phím
               bird_movement = 0 #set về o để làm lại
               bird_movement =-11 #trừ oy đi để chim di chuyển lên trên
            if event.key == pygame.K_SPACE and game_active == False : #khi game kết thúc
                game_active = True #chơi lại
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0 #reset điểm chơi lại
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe()) #pipe_list là những list chứa ống, create_pipe: hàm để pygame biết tạo ống mới
            #nếu create_pipe return 1 cái thì dùng append, 2 cái thì đung axtend
        if event.type == birdflap:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index =0
        bird, bird_rect = bird_animation() #hàm để bird đập cánh
    screen.blit(bg,(0,0)) #áp dụng để thêm cái gì vào cửa sổ pygame, 0,0 quy định tọa độ bên cùng phía bên trái
    if game_active: #game active hoạt động thì các tính năng của chịm và ống mới hoạt động
        #chim
        bird_movement += gravity # có nghĩa là con chim càng di chuyển thì trọng lực càng tăng
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement # làm cho con chim di chuyển xuống dưới và cả hình chữ nhật xung quanh con chim đi xuống dưới
        screen.blit(rotated_bird,bird_rect)#thêm chim vào màn hình chính, với tọa độ của hình chữ nhật
        game_active = check_collision(pipe_list)
        #ống
        pipe_list = move_pipe(pipe_list)#lấy tất cả ổng vừa được tạo ra trong pipe_list , sau đó sẽ trả lại cái pipe_list mới
        draw_pipe(pipe_list)
        score +=0.006 #thời gian để cộng thêm 1 điểm
        score_display('main game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game over')
    #sàn
    floor_x_pos -=1
    #screen.blit(floor,(floor_x_pos,600)) # ox để di chuyển ngang. oy để di chuyển dọc
    # nếu như này thì floor sẽ chi chuyển liên tục lùi về phía bên trái đến khi nào hết
    draw_floor()
    if floor_x_pos <= -432: #hàm khi chạy hết display thì return lại def draw
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)#set fps
