from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Curso, Usuario, Calificacion
from .serializers import CursoSerializer,CalificacionSerializer
from rest_framework import status
from django.db.models import Avg



@api_view(http_method_names=['GET','POST'])
def ControlInicial(request):
    return Response(data={
        'message':'Bienvenido a mi APi de Colegio'
    })

class CursosContorl(APIView):
    def get(self, request):
        resultado = Curso.objects.all()
        print(resultado)
        serializador = CursoSerializer(instance=resultado, many=True)
        return Response(data={
            'message':'Me hicieron get',
            'content':serializador.data
        })
    def post(self,request):
        print(request.data)
        serializador = CursoSerializer(data=request.data)
        validacion=serializador.is_valid()
        if validacion:
            serializador.save()
            return Response(data={
                'message':'Curso creado exitosamentre',
                'content': serializador.data
            }, status=status.HTTP_201_CREATED )
        else:
            return Response(data={
                'menssage':'Error al crear el curso',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class CursoControlador(APIView):
    def get(self, request, id):
            curso_encontrado = Curso.objects.filter(id = id).first()
            if not curso_encontrado:
                return Response(data={
                    'message':'No se encontro el curso'
                }, status=status.HTTP_404_NOT_FOUND)
            serializador = CursoSerializer(instance=curso_encontrado)
            return Response(data={
                    'content': serializador.data
                })
    def put(self, request, id):
            curso_encontrado = Curso.objects.filter(id = id).first()
            if not curso_encontrado:
                return Response(data={
                    'message':'No se encontro el curso'
                }, status=status.HTTP_404_NOT_FOUND)
            serializador = CursoSerializer(data = request.data)
            if serializador.is_valid():
                respuesta =  serializador.update(instance=curso_encontrado, validated_data=serializador.validated_data)
                print(respuesta)
                return Response (data={
                    'message':'El curso se actualizo corectamente'
                })

            else :
                return Response(data={
                    'message':'Error al actualizar el curso',
                    'content': serializador.errors
                }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request, id):
            curso_encontrado = Curso.objects.filter(id = id).first()
            if not curso_encontrado:
                return Response(data={
                    'message':'No se encontro el curso'
                }, status=status.HTTP_404_NOT_FOUND)
            
            Curso.objects.filter(id = id).delete()

            return Response(data={
                'message':'El curso se elimino exitosamente'
            }, status=status.HTTP_204_NO_CONTENT)

class CalificacionesController(APIView):
     def post(self, request):
          
        serializador = CalificacionSerializer(data = request.data)

        if serializador.is_valid():
            serializador.save()
            return Response({
                'message':'Calificacion ingresada correctamente',
                'content':serializador.data
            }, status=status.HTTP_201_CREATED)
        else:
             return Response({
                'message':'Error al guardar la calificaion',
                'content':serializador.errors
             }, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names = ['GET'])
def listadoDeNotas(request, id):
    calificacion_encontrada = Calificacion.objects.filter(usuarioId=id).all()
    if not calificacion_encontrada:
         return Response({
            'message':'No se encontro la calificacion'
         })
    else:
        serializador = CalificacionSerializer(instance=calificacion_encontrada, many=True)

        return Response({
             'content': serializador.data
        })


@api_view(http_method_names=['GET'])
def estadoDeAlumnos(request, id):
    # Obtener el ID del curso desde los parámetros de la URL
    
    
    # Filtrar las calificaciones para el curso dado
    notas = Calificacion.objects.filter(cursoId=id)
    
    # Verificar si hay calificaciones para el curso dado
    if notas.exists():
        # Calcular el promedio de pc1, pc2, pc3 y examenFinal
        promedio_notas = notas.aggregate(
            promedio=(Avg('pc1') + Avg('pc2') + Avg('pc3') + Avg('examenFinal')) / 4
        ).get('promedio')
        
        # Determinar el estado del alumno según el promedio
        if promedio_notas >= 12:  # Cambié el umbral a 12 según tu criterio
            estado = 'Aprobado'
        else:
            estado = 'Reprobado'
            
        return Response({
            'message': f'El alumno está {estado}',
            'promedio': promedio_notas
        })
    else:
        # No se encontraron calificaciones para el curso dado
        return Response({
            'message': 'No se encontraron calificaciones para este curso.'
        }, status=404)