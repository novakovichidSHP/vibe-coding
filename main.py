import pygame
import sys
import threading
import time
from win10toast import ToastNotifier
from input_box import InputBox
from button import Button
from timer_colors import *

class TimerApp:
    def __init__(self):
        # Увеличиваем размер окна для лучшего дизайна
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Современный Таймер')
        self.clock = pygame.time.Clock()
        self.toaster = ToastNotifier()
        self.running = True
        self.timer_running = False
        self.timer_paused = False
        self.remaining_seconds = 0
        self.timer_thread = None

        # Центрируем элементы интерфейса
        center_x = 400
        
        # Поля ввода с лучшим расположением
        self.hours_box = InputBox(center_x - 200, 120, 80, 50)
        self.minutes_box = InputBox(center_x - 60, 120, 80, 50)
        self.seconds_box = InputBox(center_x + 80, 120, 80, 50)
        self.input_boxes = [self.hours_box, self.minutes_box, self.seconds_box]

        # Кнопки с современными цветами
        self.start_btn = Button(center_x - 200, 450, 120, 50, 'Старт', SUCCESS)
        self.pause_btn = Button(center_x - 40, 450, 120, 50, 'Пауза', WARNING)
        self.reset_btn = Button(center_x + 120, 450, 120, 50, 'Сброс', ERROR)

    def draw_gradient_background(self):
        """Рисует градиентный фон"""
        for y in range(600):
            # Создаем градиент от синего к фиолетовому
            ratio = y / 600
            r = int(GRADIENT_START[0] * (1 - ratio) + GRADIENT_END[0] * ratio)
            g = int(GRADIENT_START[1] * (1 - ratio) + GRADIENT_END[1] * ratio)
            b = int(GRADIENT_START[2] * (1 - ratio) + GRADIENT_END[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (800, y))

    def draw_card(self, x, y, width, height, color=WHITE, alpha=230):
        """Рисует карточку с тенью"""
        # Тень
        shadow_rect = pygame.Rect(x + 5, y + 5, width, height)
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=15)
        
        # Основная карточка
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, card_rect, border_radius=15)

    def draw(self):
        # Градиентный фон
        self.draw_gradient_background()
        
        # Карточка для полей ввода
        self.draw_card(200, 80, 400, 120, WHITE)
        
        # Заголовки полей
        self.screen.blit(FONT.render('Часы', True, BLACK), (320, 90))
        self.screen.blit(FONT.render('Минуты', True, BLACK), (460, 90))
        self.screen.blit(FONT.render('Секунды', True, BLACK), (600, 90))
        
        # Поля ввода
        for box in self.input_boxes:
            box.draw(self.screen)
        
        # Карточка для отображения времени
        time_card_y = 250
        self.draw_card(150, time_card_y, 500, 120, WHITE)
        
        # Отображение времени
        time_str = self.get_time_str()
        time_surface = BIG_FONT.render(time_str, True, PRIMARY)
        time_rect = time_surface.get_rect(center=(400, time_card_y + 60))
        self.screen.blit(time_surface, time_rect)
        
        # Статус таймера
        if self.timer_running:
            status_text = "Таймер работает"
            status_color = SUCCESS
        elif self.timer_paused:
            status_text = "Таймер на паузе"
            status_color = WARNING
        else:
            status_text = "Таймер готов"
            status_color = DARK_GRAY
            
        status_surface = SMALL_FONT.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(400, time_card_y + 100))
        self.screen.blit(status_surface, status_rect)
        
        # Кнопки
        self.start_btn.draw(self.screen)
        self.pause_btn.draw(self.screen)
        self.reset_btn.draw(self.screen)
        
        pygame.display.flip()

    def get_time_str(self):
        if self.timer_running or self.timer_paused:
            total = self.remaining_seconds
            h = total // 3600
            m = (total % 3600) // 60
            s = total % 60
            return f"{h:02d}:{m:02d}:{s:02d}"
        else:
            h = self.hours_box.get_value()
            m = self.minutes_box.get_value()
            s = self.seconds_box.get_value()
            return f"{h:02d}:{m:02d}:{s:02d}"

    def start_timer(self):
        if self.timer_paused:
            self.timer_running = True
            self.timer_paused = False
            self.start_btn.set_disabled(True)
            self.pause_btn.set_disabled(False)
            self.start_btn.set_text('Старт')
            self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
            self.timer_thread.start()
            return
        h = self.hours_box.get_value()
        m = self.minutes_box.get_value()
        s = self.seconds_box.get_value()
        if h == 0 and m == 0 and s == 0:
            return
        self.remaining_seconds = h * 3600 + m * 60 + s
        self.timer_running = True
        self.timer_paused = False
        self.start_btn.set_disabled(True)
        self.pause_btn.set_disabled(False)
        self.start_btn.set_text('Старт')
        self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        self.timer_thread.start()

    def timer_loop(self):
        while self.timer_running and self.remaining_seconds > 0:
            if self.timer_paused:
                break
            time.sleep(1)
            self.remaining_seconds -= 1
        if self.remaining_seconds <= 0 and self.timer_running:
            self.timer_finished()

    def pause_timer(self):
        self.timer_running = False
        self.timer_paused = True
        self.start_btn.set_disabled(False)
        self.start_btn.set_text('Продолжить')
        self.pause_btn.set_disabled(True)

    def reset_timer(self):
        self.timer_running = False
        self.timer_paused = False
        self.remaining_seconds = 0
        self.start_btn.set_disabled(False)
        self.start_btn.set_text('Старт')
        self.pause_btn.set_disabled(True)

    def timer_finished(self):
        self.timer_running = False
        self.timer_paused = False
        self.remaining_seconds = 0
        self.start_btn.set_disabled(False)
        self.start_btn.set_text('Старт')
        self.pause_btn.set_disabled(True)
        try:
            self.toaster.show_toast('Таймер завершен!', 'Время истекло!', duration=5, threaded=True)
        except Exception:
            pass

    def run(self):
        self.pause_btn.set_disabled(True)
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for box in self.input_boxes:
                    box.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_btn.is_clicked(event.pos) and (not self.timer_running or self.timer_paused):
                        self.start_timer()
                    if self.pause_btn.is_clicked(event.pos) and self.timer_running:
                        self.pause_timer()
                    if self.reset_btn.is_clicked(event.pos):
                        self.reset_timer()
            
            # Обновляем состояние наведения кнопок
            self.start_btn.update_hover(mouse_pos)
            self.pause_btn.update_hover(mouse_pos)
            self.reset_btn.update_hover(mouse_pos)
            
            for box in self.input_boxes:
                box.update()
            self.draw()
            self.clock.tick(60)  # Увеличиваем FPS для плавности
        pygame.quit()
        sys.exit() 
