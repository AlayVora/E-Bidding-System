/*$(document).ready(function(){
	var s=10;
	var exe_flag=1;
	$(".bid_button").click(function(){
			var bid_val=$($(this).siblings(":text")[0]).val();			
			s=10;
			var that=this;
			if(exe_flag){
				exe_flag=0;
				var myVar=setInterval(function(){myTimer(that)},1000);
			}
		});

	function myTimer(that) {
	s=s-1;
	if(s<0)
	{
		$(that).attr("disabled","disabled");
		$(that).siblings("div").show();
		return;
	}
	$(that).siblings(".timer").html("00:00:"+s);
}

});
*/
//============
var arr=[];
var dict={};
var dict_countdown={};
var dict_timer={};
function Timer (that,ele_id,bid_val) {
		this.s=30;
		this.bid_val=bid_val;
		this.ref=that;
		this.max=0;
		this.ele_id=ele_id;
		this.expdatetime=$("#expdatetime_"+ele_id).val();
		this.countdown={};
	}

Timer.prototype.startTimer=function () {
			this.s=this.s-1;
			if(this.countdown.totalmin<=0)
			{
				$(this.ref).attr("disabled","disabled");
				//$(this.ref).siblings("div").show();
				this.sold();
				clearInterval(dict_timer[this.ele_id]);
				clearInterval(myVar[this.ele_id]);
				return;
			}
			if(this.s<0)
			{
			    this.s=30;
			}
			$(this.ref).siblings(".timer").html("00:00:"+this.s);
			$(this.ref).siblings(".countdown").html("  "+this.countdown.days+" Days  "+this.countdown.hours+":"+this.countdown.minutes+":"+this.countdown.seconds);

		}	
Timer.prototype.callAjax=function(ele_id,bid_val){
	//alert("customer_id="+customer_id+" ,ele_id="+ele_id+" ,bid_val="+bid_val);	
	var self=this.ref;
	 $.ajax({
				        url : post_url, // the endpoint
				        type : "POST", // http method
				        beforeSend: function(xhr, settings) {
					        if (!this.crossDomain) {
					            xhr.setRequestHeader("X-CSRFToken", csrftoken);
					        }
					    },				       
				        data : {  'product_id': ele_id,
				        		  'bid_val' : bid_val				        		  
				        	    }, // data sent with the post request

				        // handle a successful response
				        success : function(data) {
				        console.log("callAjax: data.bid_val="+data.bid_val+" ,self.max="+self.max);
				        	if(data.bid_val>self.max){
				        	self.max=data.bid_val;
				        	    self.s=30;
				        	$(self).siblings(".current_max_bid").html("");	        	
				            $(self).siblings(".current_max_bid").html(data.username+" Max Bid: "+data.bid_val); // remove the value from the input
				           	//console.log(data); // log the returned json to the console
				            console.log("success"); // another sanity check
				            }
				        },

				        // handle a non-successful response
				        error : function(xhr,errmsg,err) {
				          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
				        }
		    });

}

var callAjaxInitial=function(ele_id){
	//alert("customer_id="+customer_id+" ,ele_id="+ele_id+" ,bid_val="+bid_val);	
	
	 $.ajax({
				        url : post_url_max, // the endpoint
				        type : "POST", // http method
				        beforeSend: function(xhr, settings) {
					        if (!this.crossDomain) {
					            xhr.setRequestHeader("X-CSRFToken", csrftoken);
					        }
					    },				       
				        data : {
				         		  'product_id': ele_id
				        	    }, // data sent with the post request

				        // handle a successful response
				        success : function(data) {
				            console.log("data.bid_val="+data.bid_val+" ,dict[ele_id].max="+dict[ele_id].max);
				        	if(data.bid_val>dict[ele_id].max){
				        	dict[ele_id].max=data.bid_val;
				        	dict[ele_id].s=30;
				        	$("#"+ele_id).siblings(".current_max_bid").html("");	        	
				            $("#"+ele_id).siblings(".current_max_bid").html(data.username+" Max Bid: "+data.bid_val); // remove the value from the input
				           	//console.log(data); // log the returned json to the console
				            console.log("success"); // another sanity check
				            }
				        },

				        // handle a non-successful response
				        error : function(xhr,errmsg,err) {
				            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
				        }
		    });

}
var CurrentDateTime="";
var getDateTimeFromServer=function(ele_id){
	//alert("customer_id="+customer_id+" ,ele_id="+ele_id+" ,bid_val="+bid_val);

	 $.ajax({
				        url : getCurrentDateTimeUrl, // the endpoint
				        type : "GET", // http method
				        beforeSend: function(xhr, settings) {
					        if (!this.crossDomain) {
					            xhr.setRequestHeader("X-CSRFToken", csrftoken);
					        }
					    },
				        success : function(data) {
				            CurrentDateTime=data.CurrentDateTime;
				            $("#currenttime").html(CurrentDateTime);
				            console.log(data.CurrentDateTime);
				        },

				        // handle a non-successful response
				        error : function(xhr,errmsg,err) {
				           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
				        }
		    });

}
$(document).ready(function(){
    var datetimeInterval=setInterval(function(){
	getDateTimeFromServer();
	},1000);
setTimeout(function(){
    $(".bid_button").each(function(index){
            var ele_id=$(this).siblings(":text")[0].id;
            dict[ele_id]=new Timer(this,ele_id,0);
            dict_countdown[ele_id]=setInterval(function(){ dict[ele_id].getdateDiff()}, 1000);
            dict_timer[ele_id]=setInterval(function(){ dict[ele_id].startTimer()} ,1000);
        });

},500);


	$(".bid_button").click(function(){
			var bid_val=$($(this).siblings(":text")[0]).val();	
			var ele_id=$(this).siblings(":text")[0].id;	
			var that=this;		   
			dict[ele_id].s=30;
			dict[ele_id].callAjax(ele_id,bid_val);
		});
	
	$(".search_box").find(":text").keyup(function(){
		search();
	
	});
	
});

Timer.prototype.getdateDiff=function(){
    var d1=this.expdatetime;
    var d2=CurrentDateTime;
   // alert("d1="+d1+"     d2="+d2);
    var d1_arr=d1.split(" ");
    var d1_d_arr=d1_arr[0].split("-");
    var d1_t_arr=d1_arr[1].split(":");

    var d2_arr=d2.split(" ");
    var d2_d_arr=d2_arr[0].split("-");
    var d2_t_arr=d2_arr[1].split(":");

    var date1=new Date(d1_d_arr[0], d1_d_arr[1]-1, d1_d_arr[2],d1_t_arr[0], d1_t_arr[1], d1_t_arr[2],0);
    var date2=new Date(d2_d_arr[0], d2_d_arr[1]-1, d2_d_arr[2],d2_t_arr[0], d2_t_arr[1], d2_t_arr[2],0);

    var secondsDiff = (date1.getTime() - date2.getTime())/ 1000;
    var oDiff = {};
    if(secondsDiff<0)
    {
        oDiff.days = 0;
    oDiff.totalhours =0;      // total number of hours in difference
    oDiff.totalmin = 0;      // total number of minutes in difference
    oDiff.totalsec = 0;      // total number of seconds in difference

    secondsDiff -= oDiff.days*86400;
    oDiff.hours = Math.floor(secondsDiff/3600);     // number of hours after days

    secondsDiff -= oDiff.hours*3600;
    oDiff.minutes = Math.floor(secondsDiff/60);     // number of minutes after hours

    secondsDiff -= oDiff.minutes*60;
    oDiff.seconds = Math.floor(secondsDiff);
     this.countdown=oDiff;
    }
    else
    {


    secondsDiff = Math.abs(Math.floor(secondsDiff));

         // object that will store data returned by this function

    oDiff.days = Math.floor(secondsDiff/86400);
    oDiff.totalhours = Math.floor(secondsDiff/3600);      // total number of hours in difference
    oDiff.totalmin = Math.floor(secondsDiff/60);      // total number of minutes in difference
    oDiff.totalsec = secondsDiff;      // total number of seconds in difference

    secondsDiff -= oDiff.days*86400;
    oDiff.hours = Math.floor(secondsDiff/3600);     // number of hours after days

    secondsDiff -= oDiff.hours*3600;
    oDiff.minutes = Math.floor(secondsDiff/60);     // number of minutes after hours

    secondsDiff -= oDiff.minutes*60;
    oDiff.seconds = Math.floor(secondsDiff);     // number of seconds after minutes
    console.log(JSON.stringify(oDiff));
    this.countdown=oDiff;
    }
}

Timer.prototype.sold=function(){
var self=this.ref;
    $.ajax({
				        url : sold_url, // the endpoint
				        type : "POST", // http method
				        beforeSend: function(xhr, settings) {
					        if (!this.crossDomain) {
					            xhr.setRequestHeader("X-CSRFToken", csrftoken);
					        }
					    },
				        data : {
				         		  'product_id': this.ele_id
				        	   }, // data sent with the post request

				        // handle a successful response
				        success : function(data) {
                            if(data.hasOwnProperty('new_expdatetime'))
                            {
                                $(self).siblings("#expdatetime_"+this.ele_id).val(data['new_expdatetime']);
                            }
                            else
                            {
                                $(self).parent("div").html("<p style='color:#ff0000'><b>SOLD!</b></p>");
				                console.log("success"); // another sanity check
				            }
				        },

				        // handle a non-successful response
				        error : function(xhr,errmsg,err) {
				            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
				        }
		    });
}

