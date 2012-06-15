#-*- coding:utf-8 -*- 
import random
import thread , time
import unittest
from Tkinter import *

'''
class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        print "jinsoo"
    def tearDown(self):
        print "zzang"
    def testAdd(self):
        self.assertEqual(2 , 1+1)

    def testSnakeMoveDown(self):
        snake = Snake([5,5],'s')
        snake.move()
        self.assertEqual(snake.body[0] , [5,6])

    def testSnakeMoveUp(self):
        snake = Snake([5,5],'n')
        snake.move()
        self.assertEqual(snake.body[0] , [5,4])

    def testSnakeMoveLeft(self):
        snake = Snake([5,5],'w')
        snake.move()
        self.assertEqual(snake.body[0] , [4,5])
    def testSnakeMoveRight(self):
        snake = Snake([5,5],'e')
        snake.move()
        self.assertEqual(snake.body[0] , [6,5])
    def testSnakeGrow(self):
        snake = Snake([4,5], 's')
        snake.grow()
        self.assertEqual(len(snake.body) , 2 )
        self.assertEqual(snake.body[1] , [4,4])
    def testDrawSnake(self):
        snake = Snake([4,5] , 's')
        snake.move()
'''        

class Snake:
    def __init__ (self , position , direction):
        self.direction = direction
        self.body = [position ,]
        self.tail = self.body[-1]
        self.head = self.body[0]
    def move(self , maps):
        if (self.direction == 's'):
            self.head = [self.body[0][0] + 1 , self.body[0][1]]
            self.tail = self.body[-1]
            self.body = [self.head] + self.body[:-1]
            try:
                if ( maps[self.head[0]][self.head[1]] == '&'):      
                    self.grow()
                elif ( maps[self.head[0]][self.head[1]] == '*'):
                    exit()
            except(IndexError):
                exit()
        elif (self.direction == 'n'):
            self.head = [self.body[0][0] - 1 , self.body[0][1]]
            self.tail = self.body[-1]
            self.body = [self.head] + self.body[:-1]
            try:
                if ( maps[self.head[0]][self.head[1]] == '&'):
                    self.grow()
                elif ( maps[self.head[0]][self.head[1]] == '*'):
                    exit()
            except(IndexError):
                exit()

        elif (self.direction == 'w'):
            self.head = [self.body[0][0] , self.body[0][1] - 1]
            self.tail = self.body[-1]
            self.body = [self.head] + self.body[:-1]
            if ( maps[self.head[0]][self.head[1]] == '&'):
                self.grow()
            elif ( maps[self.head[0]][self.head[1]] == '*'):
                exit()
                
        elif (self.direction == 'e'):
            self.head = [self.body[0][0] , self.body[0][1] + 1]
            self.tail = self.body[-1]
            self.body = [self.head] + self.body[:-1]
            if ( maps[self.head[0]][self.head[1]] == '&'):
                 self.grow()
            elif ( maps[self.head[0]][self.head[1]] == '*'):
                exit()

    def grow(self):
        if (self.direction == 's'):
            self.body.append([self.body[-1][0]-1  , self.body[-1][1]])
        elif (self.direction == 'n'):
            self.body.append([self.body[-1][0]+1  , self.body[-1][1]])
        elif (self.direction == 'w'):
            self.body.append([self.body[-1][0]  , self.body[-1][1]+1])
        elif (self.direction == 'e'):
            self.body.append([self.body[-1][0]  , self.body[-1][1]-1])



class Map:
    def __init__ (self , row, col ):
        self.size = (row,col)
        self.map = [ [''] * row for _ in [''] * col]
    def drawSnake(self , head , tail):
        self.map[head[0]][head[1]] = '*'
        self.map[tail[0]][tail[1]] = ''
    def feedSnake(self):
        while True:
            self.randomRow = random.randint(0,self.size[0]-1)
            self.randomCol = random.randint(0,self.size[1]-1)
            if (self.map[self.randomRow][self.randomCol] != "*"):
                self.map[self.randomRow][self.randomCol] = '&'
                break
        return (self.randomRow , self.randomCol)
    def printMap(self):
        self.count = 0
        for i in self.map:
            for ele in i :
                if (ele == '&'):
                    self.count += 1
        return self.count

    
class GUIMap(Map):
    def __init__(self , master, row, col):
        Map.__init__(self, row, col)
        self.w = Canvas(master , height = str(row * 15 + 30) , width = str(col * 15 + 30))
        for i in range(row):
            for j in range(col):
                self.w.create_rectangle( 15 + i * 15 ,
                                    15 + j * 15 ,
                                    15 + i * 15 + 15,
                                    15 + j * 15 + 15 , fill = 'white')
        self.w.pack()
        self.frame = Frame(master)
        self.frame.pack()
        self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.button.pack(side=LEFT)

    def drawSnake(self, head, tail):
        Map.drawSnake(self, head,tail)
        self.w.create_rectangle( 15 + head[1] * 15 ,
                            15 + head[0] * 15 ,
                            15 + head[1] * 15 + 15,
                            15 + head[0] * 15 + 15, fill = 'black')
        self.w.create_rectangle( 15 + tail[1] * 15 ,
                            15 + tail[0] * 15 ,
                            15 + tail[1] * 15 + 15,
                            15 + tail[0] * 15 + 15, fill = 'white')

    def feedSnake(self):
        randomRow , randomCol = Map.feedSnake(self)
        self.w.create_rectangle( 15 + randomCol * 15 ,
                            15 + randomRow * 15 ,
                            15 + randomCol * 15 + 15,
                            15 + randomRow * 15 + 15, fill = 'red')
        
    def printMap(self):
        self.count = Map.printMap(self)




def start():
    global snake
    snake = Snake([5,5] , 's')
    while True:
        time.sleep(1)
        guiMap.drawSnake(snake.head , snake.tail)
        snake.move(guiMap.map)
        guiMap.printMap()
        if guiMap.count == 0  :
            guiMap.feedSnake()

def key(event):
    global snake
    if (event.keysym == 'Up'):
        snake.direction = 'n'
    elif (event.keysym == 'Down'):
        snake.direction = 's'
    elif (event.keysym == 'Left'):
        snake.direction = 'w'
    elif (event.keysym == 'Right'):
        snake.direction = 'e'
    
if __name__ == '__main__':
    root = Tk()
    guiMap = GUIMap(root , 20 , 20)
    thread.start_new_thread(start , ())
    root.bind('<Left>' , key)
    root.bind('<Right>' , key)
    root.bind('<Up>' , key)
    root.bind('<Down>' , key)
                
    root.mainloop()
