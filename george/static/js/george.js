/*
 * Copyright (C) 2014 wilson <wilson@tagtoo.org>
 *
 * Distributed under terms of the MIT license.
 */

window.isLogin = false;
window.fbAsyncInit = function() {
    // init the FB JS SDK
    FB.init({
        appId: '1427059277558859', // App ID from the App Dashboard
        status: true, // check the login status upon init?
        cookie: true, // set sessions cookies to allow your server to access the session?
        xfbml: true // parse XFBML tags on this page?
    });
};

// Load the SDK's source Asynchronously
// Note that the debug version is being actively developed and might
// contain some type checks that are overly strict.
// Please report such bugs using the bugs tool.
(function(d, debug) {
    var js, id = 'facebook-jssdk',
        ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement('script');
    js.id = id;
    js.async = true;
    js.src = "//connect.facebook.net/en_US/all" + (debug ? "/debug" : "") + ".js";
    ref.parentNode.insertBefore(js, ref);
}(document, /*debug*/ false));


var George = George || {};

George = (function($){

    var foodAPI = "/api/food/",
        userAPI = '/api/user/'

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

        env: {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight
        },

        render: function(temp, data){
            var html = temp({
                "data" : data,
                "init": George.env.category
            });
            return html;
        },



        getItemList: function(data, succss_callback,error_callback){
            var url = foodAPI + data.id +'/list';
            __ajax(url, succss_callback, error_callback);
        },

        getItem: function(data, succss_callback,error_callback){
            var url = foodAPI + data.id + '/';
            __ajax(url, succss_callback, error_callback);
        },

        getItemTrend: function(data, succss_callback,error_callback){
            var url = foodAPI + data.id + '/trend';
            __ajax(url, succss_callback, error_callback);
        },



        checkUserInfo: function(data, succss_callback,error_callback){
            var url = userAPI + 'info';
            __ajax(url, succss_callback, error_callback);
        },

        loginUser: function(data, succss_callback,error_callback){
            var url = userAPI + 'login';
            __ajax(url, succss_callback, error_callback);
        },

        logoutUser: function(data, succss_callback,error_callback){
            var url = userAPI + 'logout';
            __ajax(url, succss_callback, error_callback);
        },

    }

})(jQuery)

George.Utils = {

    getURLParameters: function () {
        var para = document.location.search.split(/[?&#]/g),
            data = {};

        para.shift();

        for(var i=0,l=para.length;i<l;i++) {
            data[para[i].split('=')[0]] = para[i].split('=')[1];
        }

        return data
    }
}

George.event = {

    searchIcookAPI: function  (val) {
        return 'http://icook.tw/recipes/fulltext_search?query=' + val;
    },

    detectDeviceScreen: function () {
        var $item = $('#list-dot-template section');

        if (skel.canUse('narrow')) {
            $item.removeClass('4u').addClass('6u');
        } else {
            $item.removeClass('6u').addClass('4u');
        }
    },

    initDisplay: function () {
        var $img = $('#titleBar img'),
            desktopWidth = 960;

        if (George.env.width > desktopWidth) {
            $img.attr('width',30);
        } else {
            $img.attr('width',15);
        }
    }

}

George.chart = {
    data: [['Year', '賣場價格', '盤商價格', '交易量']],
            // ['2014/02',  1000,   100,   400],
            // ['2014/03',  1170,   117,   460],
            // ['2014/04',  660,    66,    1120],
            // ['2014/05',  1030,   103,   540],
            // ['2014/06',  1000,   100,   400],
            // ['2014/07',  1170,   117,   460]

    draw: function () {
        var data = google.visualization.arrayToDataTable(George.chart.data);

        var options = {
          title: '價格比較圖',
          titleTextStyle: {fontSize: 20},
          hAxis: {titleTextStyle: {color: '#333'}},
          vAxis: {title: '',minValue: 0}
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    }
}



