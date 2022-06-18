
function getattr(url){
	result="".LoadURL(url)
	if(result!="")return JSON.parse(result)
	else return {}
}
