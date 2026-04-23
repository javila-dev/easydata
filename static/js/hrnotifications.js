
$(document).ready(function(){
    $.ajax({
        type:'GET',
        url:'/humanresources/notifications/',
        success: function(response){
            let warnings = response.warnings;
            let errors = response.errors;
            texto_warning = ''
            texto_error = ''
            if (warnings.empalmes.length > 0){
                texto_warning += '<p class="notifications">Los siguientes empalmes están proximos a vencer:</p><ul class="notifications">'
                for (i of warnings.empalmes){
                    texto_warning += `<li>
                      El ${i.fecha_fin} finaliza el empalme entre 
                      ${i.quien_sale.primer_nombre} ${i.quien_sale.primer_apellido} (SALE) 
                      y ${i.quien_ingresa.primer_nombre} ${i.quien_ingresa.primer_apellido} (INGRESA)
                    </li>`
                }
                texto_warning += '</ul>'
            }
            if (warnings.contratos.length > 0){
                texto_warning += '<p class="notifications">Los siguientes contratos están proximos a vencer:</p><ul class="notifications">'
                for (i of warnings.contratos){
                    texto_warning += `<li>
                      ${i.trabajador.primer_nombre} ${i.trabajador.primer_apellido} el ${i.fecha_fin}
                    </li>`
                }
                texto_warning += '</ul>'
            }
            if (texto_warning != ""){
              $.toast({
                  showImage: '/static/img/just_logo_circle.png',
                  title: 'Tenemos algunas situaciones para que las tengas en cuenta:',
                  message: texto_warning,
                  closeIcon: true,
                  displayTime:0,
                  class: 'warning',

              })
            }
            
            
            if (errors.empalmes.length > 0){
              texto_error += '<p class="notifications">Los siguientes empalmes están proximos a vencer:</p><ul class="notifications">'
                for (i of errors.empalmes){
                  texto_error += `<li>
                      El ${i.fecha_fin} finalizó el empalme entre 
                      ${i.quien_sale.primer_nombre} ${i.quien_sale.primer_apellido} (SALE) 
                      y ${i.quien_ingresa.primer_nombre} ${i.quien_ingresa.primer_apellido} (INGRESA)
                      y la persona que sale aún está activa.
                    </li>`
                }
                texto_error += '</ul>'
            }
            if (errors.contratos.length > 0){
              texto_error += '<p class="notifications">Los siguientes contratos están vencidos:</p><ul class="notifications">'
                for (i of errors.contratos){
                  texto_error += `<li>
                      ${i.trabajador.primer_nombre} ${i.trabajador.primer_apellido} el ${i.fecha_fin}
                    </li>`
                }
                texto_error += '</ul>'
            }
            if (errors.cargos.length > 0){
              texto_error += '<p class="notifications">Los siguientes cargos exceden la estructura ideal:</p><ul class="notifications">'
                for (i of errors.cargos){
                  texto_error += `<li>
                      ${i.descripcion}, cantidad aprobada (${i.cantidad_aprobada}), cantidad real (${i.cantidad_real})
                    </li>`
                }
                texto_error += '</ul>'
            }
            if (texto_error != ""){
                $.toast({
                  showImage: '/static/img/just_logo_circle.png',
                  title: 'Tenemos algunas situaciones que necesitan tu atención inmediata:',
                  message: texto_error,
                  closeIcon: true,
                  displayTime:0,
                  class: 'error',
              })
            }
            

            setTimeout(function(){
              setInterval(function(){
                $('.toast-box')
                .transition({
                  animation : 'shake',
                  duration  : 800,
                  interval  : 800
                })
              },7000)
            }, 2000)
        }
    })
})