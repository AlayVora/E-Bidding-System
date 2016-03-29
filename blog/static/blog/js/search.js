function search(search_str)
{
    var search_val=$(".search_box").find(":text").val();
	//alert(search_val+"===="+searchUrl);
	$.ajax({
				        url : searchUrl, // the endpoint
				        type : "GET", // http method
				        beforeSend: function(xhr, settings) {
					        if (!this.crossDomain) {
					            xhr.setRequestHeader("X-CSRFToken", csrftoken);
					        }
					    },
						data:{
							'search_string':search_val

						},
				        success : function(data) {
				           // alert(JSON.stringify(data));
							$(".searchlist").empty();
							$.each(data,function(index,value){
							   	$(".searchlist").append('<li style="padding:8px 10px 8px 40px;background:#F0F0E9;color:#333;border-bottom:1px solid #ccc"><a href ="https://127.0.0.1:8000/viewproduct/'+index+'">'+value+'</a></li>');
							});


				        },

				        // handle a non-successful response
				        error : function(xhr,errmsg,err) {
				           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
				        }
		    });
}

