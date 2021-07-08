from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
#from simple_history.models import HistoricalRecords
class Persona(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre', max_length = 100)
    apellido = models.CharField('Apellido', max_length = 200)
    #telefono = models.CharField('Telefono', max_length = 10)

    def __str__(self):
        return '{0},{1}'.format(self.apellido,self.nombre)