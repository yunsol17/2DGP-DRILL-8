from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT,SDL_KEYUP, SDLK_LEFT
from state_machine import StateMachine, space_down, start_event, left_up, right_down, left_down, right_up, time_out, \
    a_down


# 상태를 클래스를 통해 정의
class Idle:
    @staticmethod #이게 있으면 객체를 찍어내는 용도가 x, 클래스 내 있는 함수를 그냥 그룹화? 시키는 개념
    def enter(boy,e):
        # 현재 시간을 저장
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1

        boy.dir = 0 #정지상태이다.
        boy.frame = 0
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT',0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

        pass
class AutoRun:
    @staticmethod
    def enter(boy, e):
        boy.dir = 1
        boy.action = 1
        boy.frame = 0
        boy.flip = False
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.x += boy.dir * 15
        boy.frame = (boy.frame + 1) % 8
        if boy.x >= 800 or boy.x <= 0:
            boy.dir *= -1
            boy.flip = not boy.flip
        if get_time() - boy.start_time > 8:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.flip:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 0, 'h', boy.x, boy.y+20, 200, 200)
        else:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y+20, 200, 200)


class Sleep:
    @staticmethod
    def enter(boy,e):
        pass
    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1: #오른쪽바라보는 상태에 눕기
            boy.image.clip_composite_draw(
                boy.frame*100,300,100,100,
                3.141592/2,
                '',# 좌우상하반전X
                boy.x -25,boy.y - 25,100,100
            )
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100,
                -3.141592 / 2,
                '',  # 좌우상하반전X
                boy.x + 25, boy.y - 25, 100, 100
            )


class Run:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):
            boy.dir=1 #오른쪽 방향
            boy.action=1
        elif left_down(e) or right_down(e):
            boy.dir = -1
            boy.action =0
        boy.frame=0

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.x+=boy.dir*5
        boy.frame = (boy.frame+1)%8
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame*100,boy.action*100,100,100,boy.x,boy.y)
        pass




class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 stateMachine 생성
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle : {right_down: Run,left_down: Run,left_up: Run,right_up: Run, time_out : Sleep,a_down: AutoRun},
                Run: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,a_down: AutoRun},
                Sleep: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down:Idle,a_down: AutoRun},
                AutoRun: { time_out : Idle}
            }
        )
    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        #event : 입력이벤트 key mouse
        #우리가 state machine 전달해줄건 ( , )
        self.state_machine.add_event(
            ('INPUT', event)
        )



    def draw(self):
        self.state_machine.draw()

