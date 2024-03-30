from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 7

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание классов игры
class GameObject:
    """Класс, описывающий объект на игровом поле. По умолчанию
    координаты - центр экрана, цвет фона - цвет игрового поля.
    """

    position: tuple = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    body_color: tuple = BOARD_BACKGROUND_COLOR

    def __init__(self) -> None:
        """Инициализация объекта."""
        self.position = GameObject.position
        self.body_color = GameObject.body_color

    def draw(self):
        """Описывает отрисовку объекта, в дочерних классах
        переопределяется.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий объект яблока на игровом поле. Атрибуты:
    цвет яблока, координаты начального положения. При создании
    экземпляра положение определяется случайным образом.
    """

    body_color: tuple = APPLE_COLOR
    position: tuple = GameObject.position

    def __init__(self) -> None:
        """Инициализация объекта."""
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = Apple.body_color

    def randomize_position(self) -> tuple:
        """Метод, возвращающий случайные координаты для
        изменения положения яблока на игровом поле.
        """
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Метод отрисовки яблока на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий объект змейки на игровом поле. Атрибуты:
    начальная длина змейки, список координат сегментов, направление,
    следующее направление, цвет змейки.
    """

    length: int = 1
    positions: list = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    direction: tuple = RIGHT
    next_direction = None
    body_color: tuple = SNAKE_COLOR

    def __init__(self) -> None:
        """Инициализация объекта"""
        super().__init__()
        self.body_color = Snake.body_color
        self.positions = Snake.positions
        self.length = Snake.length
        self.direction = Snake.direction
        self.last = None

    def update_direction(self):
        """Описывает изменение направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Описывает движение змейки на основании координат головы
        и направления движения.
        """
        current_position = self.get_head_position()
        direction = self.direction
        new_position_width = current_position[0] + (direction[0] * 20)
        new_position_height = current_position[1] + (direction[1] * 20)
        if any([new_position_width < 0, new_position_width >= SCREEN_WIDTH]):
            new_position = (SCREEN_WIDTH - abs(new_position_width),
                            new_position_height)
        elif any([new_position_height < 0,
                  new_position_height >= SCREEN_HEIGHT]):
            new_position = (new_position_width,
                            SCREEN_HEIGHT - abs(new_position_height))
        else:
            new_position = (new_position_width, new_position_height)
        self.positions.insert(0, new_position)

    def get_head_position(self) -> tuple:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовка объекта змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
            # Отрисовка головы змейки
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
            # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self) -> None:
        """Сбрасывает положение змейки к исходному."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])


# Функция обработки действий пользователя
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
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.last = snake.positions[-1]
        apple.draw()
        snake.draw()
        # Если яблоко не поймано, длина не увеличивается
        if len(snake.positions) > snake.length:
            snake.last = snake.positions.pop()
        # Если яблоко поймано, длина увеличивается, яблоко появляется
        # в другом месте
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        # Если змейка врезалась сама в себя, возврат на исходную
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
        pygame.display.update()


if __name__ == '__main__':
    main()
