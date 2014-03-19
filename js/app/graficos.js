$(document).ready(function(){
	$('#controle_select option').first().remove();
});

$(document).on('change','#controle_select',function(){
	
	$('#form_busca').hide();
	
	if($(this).val() == 3){
		$('#li_municipios').hide();	
		$('#estado').trigger('click');		
	} else {
		$('#li_municipios').show();
	}
});

$(document).on('click','.mostrar',function(){
	$('#form_busca').show();
});

$(document).on('click','.teste',function(){
	$('#form_busca').hide();
});