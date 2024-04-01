from random import choice, randint

import pygame

# Инициализация и настройка игрового окна
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
STONE_COLOR = (128, 128, 128)

SPEED = 7

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Изгиб Питона')

clock = pygame.time.Clock()


class GameObject:
    """Класс, описывающий объект на игровом поле. По умолчанию
    координаты - центр экрана, цвет фона - цвет игрового поля.
    """

    def __init__(self, position=SCREEN_CENTER,
                 body_color=BOARD_BACKGROUND_COLOR) -> None:
        """Инициализация объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Описывает отрисовку объекта, в дочерних классах
        переопределяется.
        """
        raise NotImplementedError

    def draw_cell(self):
        """Отрисовка клетки на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий объект яблока на игровом поле. Атрибуты:
    цвет яблока, координаты начального положения. При создании
    экземпляра положение определяется случайным образом.
    """

    def __init__(self, body_color=APPLE_COLOR) -> None:
        """Инициализация объекта."""
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = body_color

    def randomize_position(self, snake_positions=[]) -> tuple:
        """Метод, возвращающий случайные координаты для
        изменения положения яблока на игровом поле.
        """
        random_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                           randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        if random_position not in snake_positions:
            return random_position
        return self.randomize_position(snake_positions)

    def draw(self):
        """Метод отрисовки яблока на поле."""
        self.draw_cell()


class Snake(GameObject):
    """Класс, описывающий объект змейки на игровом поле. Атрибуты:
    начальная длина змейки, список координат сегментов, направление,
    следующее направление, цвет змейки.
    """

    def __init__(self) -> None:
        """Инициализация объекта"""
        super().__init__()
        self.reset()

    def update_direction(self):
        """Описывает изменение направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Описывает движение змейки на основании координат головы
        и направления движения.
        """
        head_w, head_h = self.get_head_position()
        direction_w, direction_h = self.direction
        new_position_width = head_w + (direction_w * 20)
        new_position_height = head_h + (direction_h * 20)
        new_position = (new_position_width % SCREEN_WIDTH,
                        new_position_height % SCREEN_HEIGHT)
        self.positions.insert(0, new_position)

    def get_head_position(self) -> tuple:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовка объекта змейки."""
        self.position = self.get_head_position()
        self.draw_cell()
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self) -> None:
        """Сбрасывает положение змейки к исходному."""
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.positions = [SCREEN_CENTER]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработка нажатий клавиш для смены напралвения
    движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    apple = Apple()
    snake = Snake()
    # Создаем объект камня
    stone = Apple(STONE_COLOR)
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.last = snake.positions[-1]
        apple.draw()
        snake.draw()
        stone.draw()
        # Если яблоко не поймано, длина не увеличивается
        if len(snake.positions) > snake.length:
            snake.last = snake.positions.pop()
        # Если яблоко поймано, длина увеличивается, яблоко появляется
        # в другом месте
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)
        # Если змейка врезалась сама в себя или в камень, возврат на исходную
        if (snake.get_head_position() in snake.positions[2:]
           or snake.get_head_position() == stone.position):
            snake.reset()
            stone.position = apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        pygame.display.update()


if __name__ == '__main__':
    main()
