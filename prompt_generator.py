import json
import random
import time
import os

class PromptGenerator:
    def __init__(self):
        self.project_types = {
            "web": {
                "name": "Веб-приложение",
                "technologies": ["HTML/CSS/JavaScript", "React", "Vue.js", "Angular", "Node.js", "Python Flask/Django", "PHP", "Ruby on Rails"],
                "features": ["Аутентификация", "База данных", "API", "Адаптивный дизайн", "Поиск", "Пагинация", "Загрузка файлов", "Чат", "Уведомления"],
                "prompts": [
                    "Создай {technology} приложение с {feature}",
                    "Разработай веб-сайт на {technology} с функциями {feature}",
                    "Построй {technology} проект с {feature} и современным UI"
                ]
            },
            "mobile": {
                "name": "Мобильное приложение",
                "technologies": ["React Native", "Flutter", "Swift (iOS)", "Kotlin (Android)", "Xamarin", "Ionic"],
                "features": ["Push-уведомления", "Геолокация", "Камера", "Офлайн режим", "Социальные сети", "Платежи", "Анимации", "Темная тема"],
                "prompts": [
                    "Создай {technology} приложение с {feature}",
                    "Разработай мобильное приложение на {technology} с {feature}",
                    "Построй {technology} проект с {feature} и нативным UI"
                ]
            },
            "desktop": {
                "name": "Десктопное приложение",
                "technologies": ["Python (Tkinter/PyQt)", "Electron", "C# WPF", "Java Swing", "C++ Qt", "Rust Tauri"],
                "features": ["Локальная база данных", "Экспорт данных", "Печать", "Системные уведомления", "Автозапуск", "Многопоточность", "Плагины"],
                "prompts": [
                    "Создай {technology} приложение с {feature}",
                    "Разработай десктопное приложение на {technology} с {feature}",
                    "Построй {technology} проект с {feature} и кроссплатформенностью"
                ]
            },
            "game": {
                "name": "Игра",
                "technologies": ["Unity (C#)", "Unreal Engine (C++)", "Godot", "Python (Pygame)", "JavaScript (Phaser)", "C++ (SDL)"],
                "features": ["2D/3D графика", "Физика", "Звук", "Мультиплеер", "Сохранение прогресса", "ИИ противников", "Частицы", "Анимации"],
                "prompts": [
                    "Создай {technology} игру с {feature}",
                    "Разработай игру на {technology} с {feature}",
                    "Построй {technology} проект с {feature} и увлекательным геймплеем"
                ]
            },
            "ai": {
                "name": "ИИ/Машинное обучение",
                "technologies": ["Python (TensorFlow)", "Python (PyTorch)", "Python (Scikit-learn)", "R", "Julia", "JavaScript (TensorFlow.js)"],
                "features": ["Классификация", "Регрессия", "Компьютерное зрение", "Обработка текста", "Рекомендации", "Анализ данных", "Нейронные сети"],
                "prompts": [
                    "Создай {technology} модель с {feature}",
                    "Разработай ИИ проект на {technology} с {feature}",
                    "Построй {technology} систему с {feature} и высокой точностью"
                ]
            },
            "data": {
                "name": "Анализ данных",
                "technologies": ["Python (Pandas)", "Python (NumPy)", "R", "SQL", "Tableau", "Power BI", "Jupyter Notebooks"],
                "features": ["Визуализация", "Статистический анализ", "Очистка данных", "Прогнозирование", "Отчеты", "Интерактивные дашборды"],
                "prompts": [
                    "Создай {technology} анализ с {feature}",
                    "Разработай проект анализа данных на {technology} с {feature}",
                    "Построй {technology} систему с {feature} и инсайтами"
                ]
            }
        }
        
        self.complexity_levels = {
            "beginner": {
                "name": "Начинающий",
                "description": "Простые проекты для изучения основ",
                "duration": "1-2 недели",
                "team_size": "1 человек"
            },
            "intermediate": {
                "name": "Средний",
                "description": "Проекты средней сложности с несколькими функциями",
                "duration": "2-4 недели",
                "team_size": "1-2 человека"
            },
            "advanced": {
                "name": "Продвинутый",
                "description": "Сложные проекты с множеством функций",
                "duration": "1-3 месяца",
                "team_size": "2-4 человека"
            },
            "expert": {
                "name": "Эксперт",
                "description": "Крупные проекты корпоративного уровня",
                "duration": "3-6 месяцев",
                "team_size": "4+ человек"
            }
        }
        
        self.additional_features = [
            "Аутентификация и авторизация",
            "База данных (SQL/NoSQL)",
            "REST API",
            "Реальное время",
            "Кэширование",
            "Логирование",
            "Тестирование",
            "CI/CD",
            "Документация",
            "Безопасность",
            "Масштабируемость",
            "Мониторинг",
            "Бэкапы",
            "Мультиязычность",
            "Адаптивный дизайн"
        ]
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        print("=" * 60)
        print("🤖 АВТО ГЕНЕРАТОР ПРОМПТОВ ДЛЯ РАЗРАБОТКИ ПРОЕКТОВ")
        print("=" * 60)
        print()
    
    def print_menu(self):
        print("📋 МЕНЮ:")
        print("1. 🎯 Создать промпт для проекта")
        print("2. 🔧 Настроить параметры")
        print("3. 📚 Показать примеры промптов")
        print("4. 💾 Сохранить промпт в файл")
        print("5. 📖 Справка")
        print("0. 🚪 Выход")
        print()
    
    def get_user_choice(self, min_val, max_val, prompt="Выберите опцию: "):
        while True:
            try:
                choice = int(input(prompt))
                if min_val <= choice <= max_val:
                    return choice
                else:
                    print(f"❌ Пожалуйста, введите число от {min_val} до {max_val}")
            except ValueError:
                print("❌ Пожалуйста, введите корректное число")
    
    def select_project_type(self):
        print("🎯 ВЫБЕРИТЕ ТИП ПРОЕКТА:")
        print()
        
        for i, (key, project) in enumerate(self.project_types.items(), 1):
            print(f"{i}. {project['name']}")
        
        choice = self.get_user_choice(1, len(self.project_types))
        return list(self.project_types.keys())[choice - 1]
    
    def select_technology(self, project_type):
        technologies = self.project_types[project_type]["technologies"]
        
        print(f"🔧 ВЫБЕРИТЕ ТЕХНОЛОГИЮ ДЛЯ {self.project_types[project_type]['name'].upper()}:")
        print()
        
        for i, tech in enumerate(technologies, 1):
            print(f"{i}. {tech}")
        
        print(f"{len(technologies) + 1}. Случайная технология")
        
        choice = self.get_user_choice(1, len(technologies) + 1)
        
        if choice == len(technologies) + 1:
            return random.choice(technologies)
        else:
            return technologies[choice - 1]
    
    def select_features(self, project_type, count=3):
        features = self.project_types[project_type]["features"]
        
        print(f"✨ ВЫБЕРИТЕ ОСНОВНЫЕ ФУНКЦИИ (выберите {count}):")
        print()
        
        for i, feature in enumerate(features, 1):
            print(f"{i}. {feature}")
        
        selected_features = []
        for i in range(count):
            while True:
                choice = self.get_user_choice(1, len(features), f"Выберите функцию {i+1}: ")
                feature = features[choice - 1]
                if feature not in selected_features:
                    selected_features.append(feature)
                    break
                else:
                    print("❌ Эта функция уже выбрана")
        
        return selected_features
    
    def select_complexity(self):
        print("📊 ВЫБЕРИТЕ УРОВЕНЬ СЛОЖНОСТИ:")
        print()
        
        for i, (key, level) in enumerate(self.complexity_levels.items(), 1):
            print(f"{i}. {level['name']} - {level['description']}")
            print(f"   ⏱️  Длительность: {level['duration']}")
            print(f"   👥 Команда: {level['team_size']}")
            print()
        
        choice = self.get_user_choice(1, len(self.complexity_levels))
        return list(self.complexity_levels.keys())[choice - 1]
    
    def select_additional_features(self):
        print("🔧 ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ:")
        print("0. Пропустить")
        print()
        
        for i, feature in enumerate(self.additional_features, 1):
            print(f"{i}. {feature}")
        
        choice = self.get_user_choice(0, len(self.additional_features))
        
        if choice == 0:
            return []
        else:
            return [self.additional_features[choice - 1]]
    
    def generate_prompt(self, project_type, technology, features, complexity, additional_features=None):
        project_info = self.project_types[project_type]
        complexity_info = self.complexity_levels[complexity]
        
        # Выбор базового промпта
        base_prompt = random.choice(project_info["prompts"])
        
        # Формирование основного промпта
        main_features = ", ".join(features)
        prompt = base_prompt.format(technology=technology, feature=main_features)
        
        # Добавление сложности
        prompt += f"\n\n📊 Уровень сложности: {complexity_info['name']}"
        prompt += f"\n⏱️  Ожидаемая длительность: {complexity_info['duration']}"
        prompt += f"\n👥 Рекомендуемый размер команды: {complexity_info['team_size']}"
        
        # Добавление дополнительных функций
        if additional_features:
            prompt += f"\n🔧 Дополнительные функции: {', '.join(additional_features)}"
        
        # Добавление технических требований
        prompt += f"\n\n📋 ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ:"
        prompt += f"\n• Используй {technology}"
        prompt += f"\n• Реализуй функции: {main_features}"
        prompt += f"\n• Следуй лучшим практикам разработки"
        prompt += f"\n• Добавь комментарии к коду"
        prompt += f"\n• Создай README с инструкциями"
        
        # Добавление этапов разработки
        prompt += f"\n\n🚀 ЭТАПЫ РАЗРАБОТКИ:"
        prompt += f"\n1. Планирование и архитектура"
        prompt += f"\n2. Создание базовой структуры"
        prompt += f"\n3. Реализация основных функций"
        prompt += f"\n4. Тестирование и отладка"
        prompt += f"\n5. Документация и развертывание"
        
        return prompt
    
    def save_prompt_to_file(self, prompt, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"prompt_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"✅ Промпт сохранен в файл: {filename}")
        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")
    
    def show_examples(self):
        print("📚 ПРИМЕРЫ ПРОМПТОВ:")
        print("=" * 60)
        print()
        
        examples = [
            {
                "title": "Веб-приложение",
                "prompt": "Создай React приложение с аутентификацией, базой данных и API\n\n📊 Уровень сложности: Средний\n⏱️ Ожидаемая длительность: 2-4 недели\n👥 Рекомендуемый размер команды: 1-2 человека"
            },
            {
                "title": "Мобильное приложение",
                "prompt": "Разработай Flutter приложение с геолокацией и push-уведомлениями\n\n📊 Уровень сложности: Продвинутый\n⏱️ Ожидаемая длительность: 1-3 месяца\n👥 Рекомендуемый размер команды: 2-4 человека"
            },
            {
                "title": "ИИ проект",
                "prompt": "Построй Python (TensorFlow) систему с компьютерным зрением и высокой точностью\n\n📊 Уровень сложности: Эксперт\n⏱️ Ожидаемая длительность: 3-6 месяцев\n👥 Рекомендуемый размер команды: 4+ человек"
            }
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example['title']}")
            print(f"   {example['prompt']}")
            print()
        
        input("Нажмите Enter для продолжения...")
    
    def show_help(self):
        print("📖 СПРАВКА:")
        print("=" * 60)
        print()
        print("🎯 Как использовать генератор:")
        print("1. Выберите тип проекта (веб, мобильное, десктопное и т.д.)")
        print("2. Выберите технологию разработки")
        print("3. Выберите основные функции проекта")
        print("4. Выберите уровень сложности")
        print("5. При необходимости добавьте дополнительные функции")
        print("6. Получите готовый промпт для разработки")
        print()
        print("💡 Советы:")
        print("• Начинайте с простых проектов для изучения основ")
        print("• Постепенно увеличивайте сложность")
        print("• Сохраняйте промпты для будущих проектов")
        print("• Адаптируйте промпты под свои нужды")
        print()
        input("Нажмите Enter для продолжения...")
    
    def create_project_prompt(self):
        self.clear_screen()
        self.print_header()
        
        print("🎯 СОЗДАНИЕ ПРОМПТА ДЛЯ ПРОЕКТА")
        print("-" * 40)
        print()
        
        # Выбор типа проекта
        project_type = self.select_project_type()
        print()
        
        # Выбор технологии
        technology = self.select_technology(project_type)
        print()
        
        # Выбор функций
        features = self.select_features(project_type)
        print()
        
        # Выбор сложности
        complexity = self.select_complexity()
        print()
        
        # Дополнительные функции
        additional_features = self.select_additional_features()
        print()
        
        # Генерация промпта
        prompt = self.generate_prompt(project_type, technology, features, complexity, additional_features)
        
        # Вывод результата
        self.clear_screen()
        self.print_header()
        print("🎉 ГОТОВЫЙ ПРОМПТ:")
        print("=" * 60)
        print(prompt)
        print("=" * 60)
        print()
        
        # Опции сохранения
        print("💾 Сохранить промпт в файл? (y/n): ", end="")
        save_choice = input().lower()
        if save_choice in ['y', 'yes', 'да', 'д']:
            self.save_prompt_to_file(prompt)
        
        input("\nНажмите Enter для продолжения...")
    
    def run(self):
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = self.get_user_choice(0, 5)
            
            if choice == 0:
                print("👋 До свидания!")
                break
            elif choice == 1:
                self.create_project_prompt()
            elif choice == 2:
                print("🔧 Настройки пока не реализованы")
                input("Нажмите Enter для продолжения...")
            elif choice == 3:
                self.show_examples()
            elif choice == 4:
                print("💾 Сохранение промпта")
                print("Сначала создайте промпт через опцию 1")
                input("Нажмите Enter для продолжения...")
            elif choice == 5:
                self.show_help()

if __name__ == "__main__":
    generator = PromptGenerator()
    generator.run() 