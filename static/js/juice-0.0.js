/**
 * Juice is a collection of javascripts vars and methods that suits perfectly DIME-SHS projects.
 * Among others, squeeze class is an ajax sequencer call that you may find usefule (especially if your developer hasn't 
 * build a solid websocket architecture).
 */
 /* the desription*/
 var Juice = { tooltip:{} };
 
 Juice.tooltip.init = function(){
 	// $("[title]").css({cursor:"pointer"}).tooltip();// with non empy title
 }
  
 Juice.resize = function(){
 	console.log('<div>Handler for .resize() called.</div>');
 }
 /**
  * the basic tuple, suitable for sorting methds
  */
 Juice.o = function(){this.k;this.v;}
 
 /**
  * load an url using settimeout 
  */
 Juice.squeeze = function(options){var instance=this;this.__ping_timer=0;this.hasBeenKilled=false;this.settings={'named':'unnamed','url':'null','data':{},'lines':18,'dataType':"json",'timeOut':1340,'timeOutOnError':5000,'success':function(message){console.log(message)},'start':function(message,instance){console.log(message)},'error':function(message){console.log(message)},clearTimeoutOnError:true};this.kill=function(){clearTimeout(this.__ping_timer);instance.hasBeenKilled=true;}
this.update=function(updatedSettings){if(updatedSettings){$.extend(instance.settings,updatedSettings);}}
this.loop=function(){if(instance.settings.url=='null'){return instance.settings.error("pinger '"+instance.settings.named+"' settings.url is null. Check your options object");}else if(killPing){return clearTimeout(instance.__ping_timer)};if(instance.hasBeenKilled){instance.hasBeenKilled=false;clearTimeout(instance.__ping_timer);return instance.settings.error("pinger '"+instance.settings.named+"' has been killed. Call update() to restart");}
instance.settings.start("pinger '"+instance.settings.named+"' looping...");try{$.ajax({url:instance.settings.url,dataType:instance.settings.dataType,data:instance.settings.data,success:function(result){instance.settings.success(result);instance.__ping_timer=setTimeout(instance.loop,instance.settings.timeOut);},error:function(event){instance.settings.error(event);if(instance.settings.clearTimeoutOnError){clearTimeout(instance.__ping_timer);}else{console.log("pinger '"+instance.settings.named+"' error code received, settings.clearTimeoutOnError = false, then reconnect...");instance.__ping_timer=setTimeout(instance.loop,instance.settings.timeOutOnError);}}});}catch(exc){settings.error(exc);}}
if(options){$.extend(this.settings,options);}
clearTimeout(this.__ping_timer);if(this.settings.url=='null'){return this.settings.error("pinger'"+this.settings.named+"' INIT settings.url is null. Check your options object");}else this.loop();};
  
 
 
