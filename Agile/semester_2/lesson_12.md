# Занятие №12: Поведенческие паттерны. Состояние (State)

**Цель занятия:** Изучить паттерн State и концепцию Конечных Автоматов (FSM). Научиться управлять сложным поведением объекта, зависящим от его текущего состояния, и покрывать логику переходов модульными тестами.

**Продолжительность:** 180 минут.

---

## Часть 1. Теория и Live Coding (90 минут)

### 1. Проблема флагов (15 мин)

* **Контекст:** Персонаж может стоять, бежать, прыгать, приседать.
* **Плохое решение (Boolean Hell):**

    ```csharp
    bool isJumping;
    bool isRunning;
    bool isCrouching;

    void Update() {
        if (isJumping && !isCrouching) { ... }
        else if (isRunning && !isJumping) { ... }
        // А что если isJumping = true И isCrouching = true? Баг физики!
    }
    ```

* **Решение:** Объект может находиться только в *одном* состоянии в момент времени.

### 2. Паттерн State (30 мин)

* **Суть:** Объект меняет свое поведение в зависимости от внутреннего состояния. Извне кажется, что объект сменил свой класс.
* **UML:**
  * `Context` (Контекст): Герой (`Player`). Хранит ссылку на текущее состояние.
  * `State` (Абстрактное состояние): Интерфейс с методами действий (`HandleInput`, `Update`).
  * `ConcreteState` (Конкретные состояния): `IdleState`, `RunState`, `JumpState`.
* **Переходы:** Состояние само может решать, когда смениться на другое. (Например, `JumpState` проверяет: "Коснулся земли? -> Переход в `IdleState`").

### 3. Live Coding: Автомат героя (45 мин)

* **Задача:** Реализовать простую FSM для персонажа: Стоит -> Бежит -> Прыгает.
* **Шаг 1. Абстрактное состояние:**

    ```csharp
    public abstract class PlayerState {
        protected Player _player; // Ссылка на контекст
        
        public void SetContext(Player player) { _player = player; }

        public abstract void HandleInput(ConsoleKey key); // Реакция на нажатия
        public abstract void Update(); // Логика каждый кадр
    }
    ```

* **Шаг 2. Конкретное состояние (Idle):**

    ```csharp
    public class IdleState : PlayerState {
        public override void HandleInput(ConsoleKey key) {
            if (key == ConsoleKey.RightArrow) {
                // Переход в бег
                _player.ChangeState(new RunState()); 
            }
            else if (key == ConsoleKey.Spacebar) {
                _player.ChangeState(new JumpState());
            }
        }
        public override void Update() { Console.WriteLine("Стою и дышу..."); }
    }
    ```

* **Шаг 3. Конкретное состояние (Jump):**

    ```csharp
    public class JumpState : PlayerState {
        public override void HandleInput(ConsoleKey key) { 
            // В воздухе управление ограничено!
        }
        public override void Update() { 
            Console.WriteLine("Лечу!");
            if (_player.IsGrounded) _player.ChangeState(new IdleState());
        }
    }
    ```

* **Шаг 4. Контекст (Player):**

    ```csharp
    public class Player {
        private PlayerState _state;
        
        public void ChangeState(PlayerState newState) {
            _state = newState;
            _state.SetContext(this);
        }
        // ... проброс методов в _state
    }
    ```

---

## Часть 2. Практическое задание (Домашняя работа) (90 минут + дом)

**Тема:** Реализация Конечного Автомата (FSM).

### Задание (На выбор)

#### Вариант А: Поведение Врага (AI FSM)

1. **Состояния:** `PatrolState` (ходит туда-сюда), `ChaseState` (бежит за игроком), `AttackState` (бьет).
2. **Переходы:**
    * Patrol -> Chase (если увидел игрока).
    * Chase -> Attack (если дистанция < 1).
    * Chase -> Patrol (если игрок убежал далеко).
3. **Unit-тесты:**
    * Проверить переход из Патруля в Погоню при обнаружении игрока.
    * Проверить, что из Атаки нельзя перейти в Патруль мгновенно (нужно сначала закончить атаку или потерять цель).

#### Вариант Б: Состояние Игры (Game Loop FSM)

1. **Состояния:** `MenuState` (показывает меню), `GameState` (игровой процесс), `PauseState` (пауза), `GameOverState` (экран смерти).
2. **Переходы:**
    * Menu -> Game (Enter).
    * Game -> Pause (Esc).
    * Pause -> Game (Esc).
    * Game -> GameOver (HP <= 0).
3. **Unit-тесты:**
    * Проверить, что при нажатии Esc в игре состояние меняется на Паузу.
    * Проверить, что при смерти героя состояние меняется на GameOver.
4. **Результат работы влейте в main с коммитом "Task 12 ready."**

**Дедлайн:** 1 неделя.

---

## Критерии оценивания (Максимум 8 баллов)

| Критерий | Баллы | Описание |
| :--- | :---: | :--- |
| **Реализация State** | **2** | Выделен базовый класс/интерфейс Состояния. Контекст делегирует работу текущему состоянию. |
| **Логика переходов** | **2** | Реализовано минимум 3 состояния и корректные переходы между ними (не "все во все", а по правилам). |
| **Unit-тесты** | **2** | Написаны тесты, проверяющик смену состояния при определенном условии (Input или Game logic). Тесты проходят. |
| **Отсутствие флагов** | **1** | В классе Контекста нет переменных `bool isRunning`, `bool isDead`. Вся логика инкапсулирована в классах состояний. |
| **Качество кода** | **1** | Понятные имена классов, каждый класс в отдельном файле. |
| **Итого** | **8** | |

### Штрафы

* **Switch/Case вместо классов:** `-3 балла`. Если вместо паттерна State используется огромный `switch (currentStateEnum)` внутри метода `Update`. Это процедурный подход, а не ООП.
* **Нет тестов:** `-2 балла`. Сразу минус за отсутствие тестов, даже если код работает.
* **Жесткая связь состояний:** `-1 балл`. Если `IdleState` создает `RunState` через `new`, это допустимо, но лучше через Фабрику или Синглтон состояний (для продвинутых).

---

### Методический комментарий

* **Тестирование FSM:** Это самое приятное в паттерне State.
  * *Пример теста:*

    ```csharp
    [Fact]
    public void Player_WhenHealthZero_ShouldSwitchToDeadState() {
        var player = new Player();
        player.ChangeState(new GameState()); // Arrange
        
        player.TakeDamage(100); // Act (HP -> 0)
        
        Assert.IsType<DeadState>(player.CurrentState); // Assert
    }
    ```

  * Покажите этот пример на лекции! Это продаст идею юнит-тестов лучше любых слов.
* **Сложность:** Если студенты начнут делать иерархические автоматы (HFSM), остановите их. Пусть сделают простой плоский автомат. HFSM — это тема для отдельного курса AI.
