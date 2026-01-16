# === Action.py ===
from pybricks.tools import StopWatch

class Action:
    def __init__(self, robot):
        self.robot = robot
        self._started = False     # для wait()
        self._timer = None
        self._initialized = False # для отложенной инициализации (on_start)

    # -------------------------
    # Переопределяемые хуки
    # -------------------------
    def on_start(self):
        """
        Вызывается один раз перед первым update().
        Переопределяй в подклассах, если нужно получить
        актуальное состояние робота в момент запуска действия.
        """
        return None

    def update(self):
        """
        Основная логика действия — переопределяется в подклассах.
        Должна возвращать True когда действие завершено, False — если ещё выполняется.
        """
        return True

    # -------------------------
    # Вспомогательные методы
    # -------------------------
    def wait(self, duration_ms):
        """
        Удобная функция для пауз внутри update().
        Возвращает True, когда прошло >= duration_ms миллисекунд с момента первого вызова.
        """
        if not self._started:
            self._timer = StopWatch()
            self._started = True
        return self._timer.time() >= duration_ms

    def _safe_update(self):
        """
        Внутренний вызов: если действие ещё не инициализировано — вызываем on_start(),
        затем вызываем update(). Возвращает результат update().
        """
        if not self._initialized:
            try:
                self.on_start()
            except Exception as e:
                # Если on_start упала — печатаем, но продолжаем, чтобы не ломать план
                print("Action.on_start() error:", e)
            self._initialized = True
        return self.update()


# -------------------------
# Composite actions
# -------------------------
class SequentialAction(Action):
    def __init__(self, robot, actions):
        super().__init__(robot)
        # actions: список объектов Action (можно передать и "лениво" созданные)
        self.actions = actions
        self.index = 0

    def on_start(self):
        # ничего особенного при старте последовательности
        return None

    def update(self):
        # Если все под-действия выполнены — завершаем всю последовательность
        if self.index >= len(self.actions):
            return True

        current = self.actions[self.index]
        try:
            # вызываем _safe_update, а не update напрямую
            if current._safe_update():
                # текущее действие закончилось — переходим к следующему
                self.index += 1
        except Exception as e:
            # логируем ошибку, пропускаем проблемное действие
            print("SequentialAction: sub-action failed:", e)
            self.index += 1
        return False


class ParallelAction(Action):
    def __init__(self, robot, actions):
        super().__init__(robot)
        # копируем список, чтобы внешние списки не влияли
        self.actions = list(actions)

    def on_start(self):
        return None

    def update(self):
        still_running = []
        for act in self.actions:
            try:
                if not act._safe_update():
                    still_running.append(act)
            except Exception as e:
                # при падении одного действия — просто логируем и удаляем его из списка
                print("ParallelAction: sub-action failed:", e)
        self.actions = still_running
        return len(self.actions) == 0
