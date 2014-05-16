/*
 * Copyright (C) 2014 wilson <wilson@tagtoo.org>
 *
 * Distributed under terms of the MIT license.
 */

var George = George || {};

George = (function($){

	var api = "//ad.tagtoo.co/ad/query/",

		__ajax = function(url, succss_callback, error_callback){
	        $.ajax({
        		type: "get",
        		url: url,
        		dataType: "json",
        		success: succss_callback,
        		error: error_callback
	        });
	    };

	// public method
	return {
		render: function(temp, data){
			var html = temp({
                "data" : data
            });
            document.body.innerHTML = html;
		},
		getData: function(succss_callback,error_callback){
			var url = api;
			__ajax(url, succss_callback, error_callback);
		}
	}

})(jQuery)

// George.getDate(function(res){

// })
