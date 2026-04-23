from reports.models import clasificacion, gastos, rollling


def unificar_clasificaciones(actual, hacia):
    nueva_clasificacion = clasificacion.objects.get(pk=hacia)
    clasificacion_actual = clasificacion.objects.get(pk=actual)
    #Cambio los gastos asociados de la clasificacion anterior a la nueva
    gastos_asociados = gastos.objects.filter(clasificacion=actual)
    for gasto in gastos_asociados:
        gasto.clasificacion = nueva_clasificacion
        gasto.save()
    
    #Sumo los rollings de la clasificacion anterior a la nueva y elimino los rollings
    rollings = rollling.objects.filter(clasificacion = actual)
    
    for r in rollings:
        mes  = r.mes
        annio = r.anio
        valor = r.valor
        
        r_hacia = rollling.objects.get(mes=mes, anio = annio, clasificacion = hacia)
        
        nuevo_valor = r_hacia.valor + valor
        
        
        r_hacia.valor = nuevo_valor
        r_hacia.save()
        
        r.delete()
    
    #Elimino la clasificacion
    clasificacion_actual.delete()