import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("貪吃蛇遊戲")
        
        self.game_running = True
        self.board_size = 400
        self.snake_size = 20
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.random_food_position()
        self.direction = "Right"
        
        self.canvas = tk.Canvas(root, bg="black", height=self.board_size, width=self.board_size)
        self.canvas.pack()
        
        self.root.bind("<KeyPress>", self.on_key_press)
        self.update_game()

    def random_food_position(self):
        return (random.randint(0, (self.board_size // self.snake_size) - 1) * self.snake_size,
                random.randint(0, (self.board_size // self.snake_size) - 1) * self.snake_size)

    def on_key_press(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"

    def update_game(self):
        if self.game_running:
            self.move_snake()
            self.check_collisions()
            self.redraw()
            self.root.after(100, self.update_game)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            new_head = (head_x, head_y - self.snake_size)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.snake_size)
        elif self.direction == "Left":
            new_head = (head_x - self.snake_size, head_y)
        elif self.direction == "Right":
            new_head = (head_x + self.snake_size, head_y)
        
        self.snake = [new_head] + self.snake[:-1]

        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.random_food_position()

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= self.board_size or head_y < 0 or head_y >= self.board_size:
            self.game_over()
        if len(self.snake) > 1 and (head_x, head_y) in self.snake[1:]:
            self.game_over()

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(self.board_size // 2, self.board_size // 2, text="Game Over", fill="red", font=('Helvetica', 24))

    def redraw(self):
        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + self.snake_size, segment[1] + self.snake_size, fill="green")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + self.snake_size, self.food[1] + self.snake_size, fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
