from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    foto = models.ImageField()

    class Meta:
        db_table = 'usuarios'

class Curso(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombreCurso = models.CharField(max_length=100, null=False)
    creditos = models.IntegerField()
    seccion = models.CharField(max_length=10)
    usuarioId = models.ForeignKey(to=Usuario, db_column='usuario_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cursos'

class Calificacion(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    pc1 = models.FloatField()
    pc2 = models.FloatField()
    pc3 = models.FloatField()
    examenFinal = models.FloatField()
    cursoId = models.ForeignKey(to=Curso, db_column='curso_id', on_delete=models.CASCADE)
    usuarioId = models.ForeignKey(to=Usuario, db_column='calificaciones_usuarios', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'calificaciones'


class Horario(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    horaIngreso = models.TimeField()
    horaSalida = models.TimeField()
    cursoId = models.OneToOneField(to=Curso, db_column='curso_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'horarios'
