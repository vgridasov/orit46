from django.db import models
from django.utils import timezone
from mo.models import MOModel, MOUnitModel, StaffModel


class AROLogModel(models.Model):
    reg_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата-время записи')
    edit_datetime = models.DateTimeField(auto_now=True, verbose_name='Дата-время изменения')
    mo = models.ForeignKey(
        MOModel,
        on_delete=models.PROTECT,
        verbose_name='Организация')
    mo_unit = models.ForeignKey(
        MOUnitModel,
        on_delete=models.PROTECT,
        verbose_name='Подразделение')
    registrator = models.ForeignKey(
        StaffModel,
        on_delete=models.PROTECT,
        verbose_name='Регистратор'
    )
    mh_num = models.CharField(max_length=10, verbose_name='Номер истории болезни')
    age = models.CharField(max_length=3, verbose_name='Возраст')
    to_hosp_date = models.DateTimeField(default=timezone.now, verbose_name='Дата поступления в МО')
    to_unit_date = models.DateTimeField(default=timezone.now, verbose_name='Дата поступления в отделение')
    diagnosis = models.CharField(max_length=100, verbose_name='Основной диагноз')
    oper_date = models.DateTimeField(default=timezone.now, verbose_name='Операция (дата-время завершения)')
    oper_name = models.CharField(max_length=100, verbose_name='Операция (наименование)')

    # Степень угнетения сознания (по Коновалову)
    MIND_CHOICES = [
        ('1', 'Ясное сознание'),
        ('2', 'Умеренное оглушение'),
        ('3', 'Глубокое оглушение'),
        ('4', 'Сопор'),
        ('5', 'Умеренная кома (Кома I)'),
        ('6', 'Глубокая кома (Кома II)'),
        ('7', 'Атоническая кома (Кома III)'),
    ]
    mind = models.CharField(
        max_length=1,
        choices=MIND_CHOICES,
        verbose_name='Степень угнетения сознания (по Коновалову)'
    )

    # Статус ИВЛ
    VENT_CHOICES = [
        ('1', 'на ИВЛ'),
        ('2', 'на НИВЛ'),
        ('3', 'ВПО2'),
        ('4', 'CPAP'),
        ('5', 'O2-терапия'),
        ('6', 'нет'),
    ]
    vent = models.CharField(
        max_length=1,
        choices=VENT_CHOICES,
        default='6',
        verbose_name='ИВЛ'
    )

    # Динамика состояния
    S_DYN_CHOICES = [
        ('1', 'Поступление'),
        ('2', 'Улучшение'),
        ('3', 'Без изменений'),
        ('4', 'Ухудшение'),
    ]
    s_dyn = models.CharField(
        max_length=1,
        choices=S_DYN_CHOICES,
        default='1',
        verbose_name='Динамика состояния'
    )

    note = models.TextField(null=True, blank=True, verbose_name='Примечания')

    def __str__(self):
        return '%s: %s лет' % (self.mh_num, self.age)

    class Meta:
        ordering = ['-edit_datetime']
        verbose_name = 'Запись о пациенте'
        verbose_name_plural = 'Записи о пациентах'
