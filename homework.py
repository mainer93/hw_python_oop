class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        """Инициализировать InfoMessage.

        Аргументы:
            training_type: Имя класса тренировки.
            duration: Длительность тренировки в часах.
            distance: Дистанция в километрах.
            speed: Средняя скорость.
            calories: Потрачено килокалорий.
        """
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть строку сообщения с данными о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
    pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    training_type: str = 'Training'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        """Инициализировать Training.

        Аргументы:
            action: Количество совершённых действий
                (число шагов при ходьбе и беге либо гребков — при плавании).
            duration: Длительность тренировки.
            weight: Вес спортсмена.
        """
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance
    pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.get_distance() / self.duration)
        return speed
    pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        data = InfoMessage(self.training_type, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return data
    pass


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    training_type: str = 'Running'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> float:
        """Инициализировать Running(Training).

        Аргументы:
            action: Число шагов при беге.
            duration: Длительность тренировки.
            weight: Вес спортсмена.
        """
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * self.duration
                    * self.MIN_IN_H)
        return calories
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100
    training_type: str = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> float:
        """Инициализировать SportsWalking(Training).

        Аргументы:
            action: Число шагов при ходьбе.
            duration: Длительность тренировки.
            weight: Вес спортсмена.
            height: Рост спортсмена.
        """
        super().__init__(action, duration, weight)
        self.height = height
    pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                    + (((self.get_mean_speed() * self.KMH_IN_MSEC)**2)
                     / (self.height / self.CM_IN_M))
                    * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                    * self.weight)
                    * (self.duration * self.MIN_IN_H))
        return calories
    pass


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    training_type: str = 'Swimming'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> float:
        """Инициализировать Swimming(Training).

        Аргументы:
            action: Число шагов при ходьбе.
            duration: Длительность тренировки.
            weight: Вес спортсмена.
            length_pool: Длина бассейна.
            count_pool: Количество переплываний бассейна пользователем.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed
    pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.CALORIES_WEIGHT_MULTIPLIER
                    * self.weight * self.duration)
        return calories
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training: dict = {'SWM': Swimming, 'RUN': Running,
                           'WLK': SportsWalking}
    while workout_type in dict_training:
        return dict_training[workout_type](*data)
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
