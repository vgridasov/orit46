from django.contrib.auth.models import User
from django.db import models


class MOModel(models.Model):
    sn = models.CharField(max_length=10, null=True, blank=True, verbose_name='Код строки')
    name = models.CharField(max_length=100, verbose_name='Наименование МО')
    is_active = models.BooleanField(default=True, verbose_name='Действующая')
    aro_available = models.BooleanField(default=False, verbose_name='АРО')
    pso_n_available = models.BooleanField(default=False, verbose_name='ПСО (Н)')
    pso_c_available = models.BooleanField(default=False, verbose_name='ПСО (К)')
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
        max_length=30,
        choices=MO_TYPE_CHOICES,
        default=ETC,
        verbose_name='Тип МО'
    )

    def is_bol(self):
        return self.mo_type in {self.CRB, self.BOL}

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sn', 'name']
        verbose_name = 'Мед.организация'
        verbose_name_plural = 'Мед.организации'


class MOUnitModel(models.Model):
    mo = models.ForeignKey(
        MOModel,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Организация')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Вышест.подр.'
    )
    sn = models.CharField(max_length=10, null=True, blank=True, verbose_name='Номер п/п')
    shortname = models.CharField(max_length=20, verbose_name='Сокр.наименование')
    name = models.CharField(max_length=120, verbose_name='Наименование')
    is_active = models.BooleanField(default=True, verbose_name='Действующее')

    def __str__(self):
        return '%s: %s' % (self.mo, self.shortname)

    class Meta:
        ordering = ['sn', 'name']
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class StaffModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='Должность')
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    email = models.EmailField(null=True, blank=True, verbose_name='E-mail')
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Пользователь'
    )
    mo = models.ForeignKey(
        MOModel,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Организация')
    mo_unit = models.ForeignKey(
        MOUnitModel,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Подразделение'
    )

    is_unit_only = models.BooleanField(default=True, verbose_name='Огр. отдел.')
    is_view_only = models.BooleanField(default=False, verbose_name='Анализ')
    is_active = models.BooleanField(default=True, verbose_name='Действующий')

    def __str__(self):
        return '%s: %s' % (self.title, self.fio)

    class Meta:
        ordering = ['fio']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class BedSpaceNumberModel(models.Model):
    edit_date = models.DateTimeField(auto_now=True, verbose_name='Дата изм.')
    mo = models.ForeignKey(
        MOModel,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Организация')
    mo_unit = models.ForeignKey(
        MOUnitModel,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Подразделение'
    )
    num = models.SmallIntegerField(verbose_name='Кол-во коек')
    note = models.CharField(max_length=200, default='Причина не указана!', verbose_name='Причина изменения')

    def __str__(self):
        return '%s: %s - %s' % (self.edit_date, self.mo, self.num)

    class Meta:
        ordering = ['-edit_date']
        get_latest_by = 'edit_date'
        verbose_name = 'Коечный фонд'
        verbose_name_plural = 'Коечный фонд'
