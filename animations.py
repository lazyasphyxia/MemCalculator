from PyQt6.QtWidgets import QPushButton, QGraphicsColorizeEffect
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, Qt, pyqtProperty


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(60, 60)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Эффект осветления
        self.color_effect = QGraphicsColorizeEffect(self)
        self.color_effect.setColor(QColor(255, 255, 255))
        self.color_effect.setStrength(0.0)
        self.setGraphicsEffect(self.color_effect)

        # Внутренняя переменная масштаба
        self._scale = 1.0

        # Константы
        self.press_duration = 100
        self.release_duration = 300
        self.target_scale = 1.05
        self.color_strength = 0.3

    # Создаем свойство для анимации, чтобы Qt понимал, что такое "scale"
    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()  # Перерисовываем виджет при изменении масштаба

    def paintEvent(self, event):
        """Магия масштабирования здесь"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Сдвигаем систему координат в центр кнопки
        cx = self.width() / 2
        cy = self.height() / 2
        painter.translate(cx, cy)

        # Масштабируем
        painter.scale(self._scale, self._scale)

        # Возвращаем координаты назад
        painter.translate(-cx, -cy)

        # Рисуем стандартную кнопку в измененной системе координат
        super().paintEvent(event)

    def mousePressEvent(self, event):
        self.raise_()

        self.anim_scale_press = QPropertyAnimation(self, b"scale")
        self.anim_scale_press.setDuration(self.press_duration)
        self.anim_scale_press.setStartValue(self._scale)
        self.anim_scale_press.setEndValue(self.target_scale)
        self.anim_scale_press.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.anim_color_press = QPropertyAnimation(self.color_effect, b"strength")
        self.anim_color_press.setDuration(self.press_duration)
        self.anim_color_press.setStartValue(self.color_effect.strength())
        self.anim_color_press.setEndValue(self.color_strength)

        self.press_group = QParallelAnimationGroup()
        self.press_group.addAnimation(self.anim_scale_press)
        self.press_group.addAnimation(self.anim_color_press)
        self.press_group.start()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.anim_scale_release = QPropertyAnimation(self, b"scale")
        self.anim_scale_release.setDuration(self.release_duration)
        self.anim_scale_release.setStartValue(self._scale)
        self.anim_scale_release.setEndValue(1.0)
        self.anim_scale_release.setEasingCurve(QEasingCurve.Type.OutBack)

        self.anim_color_release = QPropertyAnimation(self.color_effect, b"strength")
        self.anim_color_release.setDuration(self.release_duration)
        self.anim_color_release.setStartValue(self.color_effect.strength())
        self.anim_color_release.setEndValue(0.0)

        self.release_group = QParallelAnimationGroup()
        self.release_group.addAnimation(self.anim_scale_release)
        self.release_group.addAnimation(self.anim_color_release)
        self.release_group.start()

        super().mouseReleaseEvent(event)