from django.db import models
import datetime
from mo.models import MOUnitModel, StaffModel


class Question(models.Model):
    sn = models.CharField(max_length=10, blank=True, null=True, verbose_name='№ п/п')
    title = models.CharField(max_length=100, verbose_name='Наименование показателя')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Подчинение'
    )
    css_style = models.CharField(max_length=100, blank=True, null=True, verbose_name='Стиль строки')
    calc = models.CharField(max_length=100, blank=True, null=True, verbose_name='Вычисления')
    is_active = models.BooleanField(default=True, verbose_name='Действующий')

    def __str__(self):
        return '%s: %s' % (self.sn, self.title)

    class Meta:
        ordering = ['sn']
        verbose_name = 'Показатель'
        verbose_name_plural = 'Показатели'


class OnmkStat(models.Model):
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата-время записи')
    edit_dt = models.DateTimeField(auto_now=True, verbose_name='Дата-время изменения')
    title = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Показатель'
    )
    val = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='Значение')

    YEAR_CHOICES = [
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
        ('2030', '2030'),
        ('2031', '2031'),
        ('2032', '2032'),
    ]
    if datetime.datetime.now().strftime("%Y") in YEAR_CHOICES:
        curr_year = datetime.datetime.now().strftime("%Y")
    else:
        curr_year = YEAR_CHOICES[0]

    rep_year = models.CharField(
        max_length=4,
        choices=YEAR_CHOICES,
        default=curr_year
    )

    MONTH_CHOICES = [
        ('01', 'Январь'),
        ('02', 'Февраль'),
        ('03', 'Март'),
        ('04', 'Апрель'),
        ('05', 'Май'),
        ('06', 'Июнь'),
        ('07', 'Июль'),
        ('08', 'Август'),
        ('09', 'Сентябрь'),
        ('10', 'Октябрь'),
        ('11', 'Ноябрь'),
        ('12', 'Декабрь'),

    ]

    default_month = datetime.datetime.now()
    rep_month = models.CharField(
        max_length=3,
        choices=MONTH_CHOICES,
        default=default_month.strftime("%m")
    )

    mo_unit = models.ForeignKey(
        MOUnitModel,
        on_delete=models.PROTECT,
        verbose_name='Подразделение')

    registrator = models.ForeignKey(
        StaffModel,
        on_delete=models.PROTECT,
        verbose_name='Регистратор'
    )

    def __str__(self):
        return '%s %s: %s - %s' % (self.rep_year, self.rep_month, self.mo_unit, self.title.sn)

    class Meta:
        ordering = ['rep_year', 'rep_month', 'mo_unit']
        verbose_name = 'Запись отчета'
        verbose_name_plural = 'Записи отчета'
