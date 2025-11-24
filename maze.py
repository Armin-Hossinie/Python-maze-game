import turtle
import random
from collections import deque

screen = turtle.Screen()
screen.title("Maze Game - BFS Path Finding")
screen.bgcolor("white")
screen.setup(width=800, height=800)
screen.tracer(0)

CELL_SIZE = 30
MAZE_SIZE = 15

class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = [[1 for _ in range(size)] for _ in range(size)]
        self.start = (1, 1)
        self.end = (size - 2, size - 2)
        self.generate_maze()
        
    def generate_maze(self):
        stack = [self.start]
        self.maze[self.start[0]][self.start[1]] = 0
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            current = stack[-1]
            neighbors = []
            
            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 < nx < self.size - 1 and 0 < ny < self.size - 1:
                    if self.maze[nx][ny] == 1:
                        neighbors.append((nx, ny, dx//2, dy//2))
            
            if neighbors:
                nx, ny, mx, my = random.choice(neighbors)
                self.maze[nx][ny] = 0
                self.maze[current[0] + mx][current[1] + my] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        self.maze[self.start[0]][self.start[1]] = 2
        self.maze[self.end[0]][self.end[1]] = 3

    def find_path(self):
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == self.end:
                return path
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.size and 0 <= ny < self.size and 
                    (nx, ny) not in visited and self.maze[nx][ny] != 1):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        return []

class MazeDrawer:
    def __init__(self, maze):
        self.maze = maze
        self.drawer = turtle.Turtle()
        self.drawer.hideturtle()
        self.drawer.speed(0)
        self.drawer.penup()
        
        self.player = turtle.Turtle()
        self.player.shape("circle")
        self.player.color("blue")
        self.player.penup()
        self.player.speed(0)
        
        self.path_drawer = turtle.Turtle()
        self.path_drawer.hideturtle()
        self.path_drawer.speed(1)
        self.path_drawer.width(3)
        self.path_drawer.color("red")
        
        self.player_pos = list(maze.start)
        self.moves = 0
        self.game_won = False
        self.auto_solve_used = False
        
    def draw_maze(self):
        offset = -MAZE_SIZE * CELL_SIZE / 2
        
        for i in range(self.maze.size):
            for j in range(self.maze.size):
                x = offset + j * CELL_SIZE
                y = offset + (self.maze.size - 1 - i) * CELL_SIZE
                
                if self.maze.maze[i][j] == 1:
                    self.draw_cell(x, y, "black")
                elif self.maze.maze[i][j] == 2:
                    self.draw_cell(x, y, "green")
                elif self.maze.maze[i][j] == 3:
                    self.draw_cell(x, y, "gold")
                else:
                    self.draw_cell(x, y, "white", "lightgray")
    
    def draw_cell(self, x, y, fill_color, outline="black"):
        self.drawer.penup()
        self.drawer.goto(x, y)
        self.drawer.pendown()
        self.drawer.fillcolor(fill_color)
        self.drawer.pencolor(outline)
        self.drawer.begin_fill()
        for _ in range(4):
            self.drawer.forward(CELL_SIZE)
            self.drawer.left(90)
        self.drawer.end_fill()
        self.drawer.penup()
    
    def show_path(self, path):
        if not path:
            return
        
        offset = -MAZE_SIZE * CELL_SIZE / 2
        
        start_i, start_j = path[0]
        x = offset + start_j * CELL_SIZE + CELL_SIZE / 2
        y = offset + (self.maze.size - 1 - start_i) * CELL_SIZE + CELL_SIZE / 2
        
        self.path_drawer.penup()
        self.path_drawer.goto(x, y)
        self.path_drawer.pendown()
        
        for i, j in path[1:]:
            x = offset + j * CELL_SIZE + CELL_SIZE / 2
            y = offset + (self.maze.size - 1 - i) * CELL_SIZE + CELL_SIZE / 2
            self.path_drawer.goto(x, y)
            screen.update()
        
        self.path_drawer.penup()
    
    def move_player(self, i, j):
        offset = -MAZE_SIZE * CELL_SIZE / 2
        x = offset + j * CELL_SIZE + CELL_SIZE / 2
        y = offset + (self.maze.size - 1 - i) * CELL_SIZE + CELL_SIZE / 2
        self.player.goto(x, y)
        self.player_pos = [i, j]
    
    def try_move(self, direction):
        if self.game_won:
            return
        
        i, j = self.player_pos
        new_i, new_j = i, j
        
        if direction == "up":
            new_i = i - 1
        elif direction == "down":
            new_i = i + 1
        elif direction == "left":
            new_j = j - 1
        elif direction == "right":
            new_j = j + 1
        
        if (0 <= new_i < self.maze.size and 0 <= new_j < self.maze.size and 
            self.maze.maze[new_i][new_j] != 1):
            
            self.moves += 1
            self.move_player(new_i, new_j)
            self.update_stats()
            
            if (new_i, new_j) == self.maze.end:
                self.win_game()
        else:
            self.show_temp_message("Cannot move through walls!", "red")
        
        screen.update()
    
    def update_stats(self):
        self.stats_turtle.clear()
        self.stats_turtle.write(
            f"Moves: {self.moves}", 
            align="left", 
            font=("Arial", 14, "bold")
        )
    
    def win_game(self):
        self.game_won = True
        
        winner = turtle.Turtle()
        winner.hideturtle()
        winner.penup()
        winner.goto(0, 0)
        winner.color("green")
        
        bonus = "" if self.auto_solve_used else " (Without help!)"
        winner.write(
            f"Congratulations! You won!{bonus}\nTotal moves: {self.moves}", 
            align="center", 
            font=("Arial", 20, "bold")
        )
        screen.update()
    
    def show_temp_message(self, message, color="red"):
        msg = turtle.Turtle()
        msg.hideturtle()
        msg.penup()
        msg.goto(0, 0)
        msg.color(color)
        msg.write(message, align="center", font=("Arial", 14, "bold"))
        screen.update()
        screen.ontimer(msg.clear, 1000)

def main():
    maze = Maze(MAZE_SIZE)
    drawer = MazeDrawer(maze)
    drawer.draw_maze()
    
    drawer.move_player(*maze.start)
    
    drawer.stats_turtle = turtle.Turtle()
    drawer.stats_turtle.hideturtle()
    drawer.stats_turtle.penup()
    drawer.stats_turtle.goto(-MAZE_SIZE * CELL_SIZE / 2, MAZE_SIZE * CELL_SIZE / 2 + 30)
    drawer.update_stats()
    
    screen.update()
    
    def solve_maze():
        if drawer.game_won:
            return
        
        drawer.auto_solve_used = True
        path = maze.find_path()
        if path:
            drawer.show_path(path)
            text = turtle.Turtle()
            text.hideturtle()
            text.penup()
            text.goto(0, MAZE_SIZE * CELL_SIZE / 2 + 50)
            text.color("orange")
            text.write("Solution displayed! (Score reduced)", 
                      align="center", font=("Arial", 14, "bold"))
        screen.update()
    
    screen.onkey(lambda: drawer.try_move("up"), "Up")
    screen.onkey(lambda: drawer.try_move("down"), "Down")
    screen.onkey(lambda: drawer.try_move("left"), "Left")
    screen.onkey(lambda: drawer.try_move("right"), "Right")
    
    screen.onkey(lambda: drawer.try_move("up"), "w")
    screen.onkey(lambda: drawer.try_move("down"), "s")
    screen.onkey(lambda: drawer.try_move("left"), "a")
    screen.onkey(lambda: drawer.try_move("right"), "d")
    
    screen.onkey(solve_maze, "space")
    
    def restart_game():
        screen.clear()
        screen.bgcolor("white")
        main()
    
    screen.onkey(restart_game, "r")
    
    screen.listen()
    
    rules = turtle.Turtle()
    rules.hideturtle()
    rules.penup()
    rules.goto(0, -MAZE_SIZE * CELL_SIZE / 2 - 40)
  
    screen.update()
    screen.mainloop()

if __name__ == "__main__":
    main()