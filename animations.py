from PyQt6.QtWidgets import QPushButton, QGraphicsColorizeEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QParallelAnimationGroup, Qt


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(60, 60)
        # Отключаем стандартный фокусную рамку, чтобы не портила вид
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Эффект осветления
        self.color_effect = QGraphicsColorizeEffect(self)
        self.color_effect.setColor(QColor(255, 255, 255))  # Белый блик
        self.color_effect.setStrength(0.0)
        self.setGraphicsEffect(self.color_effect)

        # Константы для настройки "вязкости"
        self.press_duration = 70  # Быстрое нажатие (мс)
        self.release_duration = 350  # Плавный возврат (мс)
        self.scale_offset = 3  # На сколько пикселей увеличиваем
        self.color_strength = 0.4  # Сила осветления (0.0 - 1.0)

        # Переменная для хранения оригинальной геометрии
        self._orig_geometry = None

    def mousePressEvent(self, event):
        # Сохраняем оригинальный размер перед первым нажатием
        if self._orig_geometry is None:
            self._orig_geometry = self.geometry()

        # --- Анимация НАЖАТИЯ (Увеличение + Яркость) ---

        # Расширяем границы
        expanded = QRect(self._orig_geometry.x() - self.scale_offset,
                         self._orig_geometry.y() - self.scale_offset,
                         self._orig_geometry.width() + self.scale_offset * 2,
                         self._orig_geometry.height() + self.scale_offset * 2)

        # Анимация размера (быстро увеличиваем)
        self.anim_size_press = QPropertyAnimation(self, b"geometry")
        self.anim_size_press.setDuration(self.press_duration)
        self.anim_size_press.setStartValue(self.geometry())
        self.anim_size_press.setEndValue(expanded)
        # OutQuad: быстро в начале, замедляется к концу нажатия
        self.anim_size_press.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Анимация цвета (быстро осветляем)
        self.anim_color_press = QPropertyAnimation(self.color_effect, b"strength")
        self.anim_color_press.setDuration(self.press_duration)
        self.anim_color_press.setStartValue(self.color_effect.strength())
        self.anim_color_press.setEndValue(self.color_strength)

        # Запускаем группу нажатия
        self.press_group = QParallelAnimationGroup()
        self.press_group.addAnimation(self.anim_size_press)
        self.press_group.addAnimation(self.anim_color_press)
        self.press_group.start()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # --- Анимация ОТПУСКАНИЯ (Возврат к норме) ---

        # Важно: возвращаемся строго к сохраненному оригиналу
        if self._orig_geometry is None:
            self._orig_geometry = self.geometry()

        # Анимация размера (плавно возвращаем)
        self.anim_size_release = QPropertyAnimation(self, b"geometry")
        self.anim_size_release.setDuration(self.release_duration)
        self.anim_size_release.setStartValue(self.geometry())
        self.anim_size_release.setEndValue(self._orig_geometry)
        # OutElastic или OutBack дали бы "отскок", но OutCubic/OutQuint
        # дают очень гладкое, "дорогое" замедление.
        self.anim_size_release.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Анимация цвета (плавно гасим блик)
        self.anim_color_release = QPropertyAnimation(self.color_effect, b"strength")
        self.anim_color_release.setDuration(self.release_duration)
        self.anim_color_release.setStartValue(self.color_effect.strength())
        self.anim_color_release.setEndValue(0.0)
        self.anim_color_release.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Запускаем группу отпускания
        self.release_group = QParallelAnimationGroup()
        self.release_group.addAnimation(self.anim_size_release)
        self.release_group.addAnimation(self.anim_color_release)
        self.release_group.start()

        super().mouseReleaseEvent(event)