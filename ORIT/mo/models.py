from django.db import models


# Create your models here.


class MOModel(models.Model):
    sn = models.CharField(max_length=10, null=True, blank=True, verbose_name='Код строки')
    name = models.CharField(max_length=100, verbose_name='Наименование МО')
    aro_available = models.BooleanField(default=False, verbose_name='АРО')
    pso_n_available = models.BooleanField(default=False, verbose_name='ПСО (Н)')
    pso_с_available = models.BooleanField(default=False, verbose_name='ПСО (К)')
    ho_available = models.BooleanField(default=False, verbose_name='ХО')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    email = models.EmailField(null=True, blank=True, verbose_name='E-mail')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    site = models.URLField(max_length=100, null=True, blank=True, verbose_name='Сайт')
    level = models.SmallIntegerField(verbose_name='Уровень')
    CRB = 'Центральные районные больницы'
    BOL = 'Больницы'
    POL = 'Поликлиники'
    STM = 'Стоматологические поликлиники'
    SMP = 'Станции скорой помощи'
    MOU = 'Медицинские колледжи'
    SAN = 'Санатории'
    DIS = 'Диспансеры'
    ROD = 'Родильные дома'
    ETC = 'Не определено'
    MO_TYPE_CHOICES = [
        (CRB, 'Центральные районные больницы'),
        (BOL, 'Больницы'),
        (POL, 'Поликлиники'),
        (STM, 'Стоматологические поликлиники'),
        (SMP, 'Станции скорой помощи'),
        (MOU, 'Медицинские колледжи'),
        (SAN, 'Санатории'),
        (DIS, 'Диспансеры'),
        (ROD, 'Родильные дома'),
        (ETC, 'Не определено')
    ]
    mo_type = models.CharField(
        max_length=3,
        choices=MO_TYPE_CHOICES,
        default=ETC,
        verbose_name='Тип МО'
    )

    def is_bol(self):
        return self.mo_type in {self.CRB, self.BOL}

    def __str__(self):
        return self.name

