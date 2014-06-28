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

        __ajax = function(d, url, succss_callback, error_callback){
            $.ajax({
                type: "get",
                data: d,
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
            height: document.documentElement.clientHeight,
            defaultUserImage: 'http://lh6.ggpht.com/S4G9Ssf-eCCGxsRqJqKEQzZSfmC4K09j0J-W7oPxePxpALU-Abgk0kOfNJowfFd54plPJYl8bRXLheMUR3t3xA'
        },

        render: function(temp, data){
            var html = temp({
                "data" : data,
                "init": George.env.init
            });
            return html;
        },



        getItemList: function(data, succss_callback,error_callback){
            var url = foodAPI + data.id +'/list';
            __ajax({size:data.size}, url, succss_callback, error_callback);
        },

        getItem: function(data, succss_callback,error_callback){
            var url = foodAPI + data.id + '/';
            __ajax({}, url, succss_callback, error_callback);
        },

        getItemTrend: function(data, succss_callback,error_callback){
            var url = foodAPI + data.id + '/trend';
            __ajax({}, url, succss_callback, error_callback);
        },



        checkUserInfo: function(data, succss_callback,error_callback){
            var url = userAPI + 'info';
            __ajax({}, url, succss_callback, error_callback);
        },

        loginUser: function(data, succss_callback,error_callback){
            var url = userAPI + 'login';
            __ajax({}, url, succss_callback, error_callback);
        },

        logoutUser: function(data, succss_callback,error_callback){
            var url = userAPI + 'logout';
            __ajax({}, url, succss_callback, error_callback);
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
        val = val.replace(/【切塊】/, '').replace('省產溫體', '').replace('當日現宰溫體', '').replace(/-.*/,'')
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
            $preIcon = $('.pre-icon'),
            desktopWidth = 960;

        if (George.env.width > desktopWidth) {
            // $img.attr('width',30);
            // $preIcon.attr('height',100);
        } else {
            // $img.attr('width',15);
            // $preIcon.attr('height',50);
        }

        // check user login status
        George.checkUserInfo({},function(res){
            if (res.name) {
                George.env.loginStatus = true;
            }

            if (George.env.loginStatus) {
                $('.people_nav,.people').attr('src','https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xfa1/t1.0-1/p160x160/10314011_10202684084237605_1762184246269689844_n.jpg');
                $('#fb_user').text(George.env.userName);
                $('#fb_login,.login_button').hide();
                $('#fb_logout,.logout_button').show();
            }else {
                $('.people_nav,.people').attr('src',George.env.defaultUserImage);
            }

        });
    },

    loginMechanism: function () {
        $('#fb_login,.login_button').on('click',function(){
            FB.login(function(response) {
                // console.log(response)
                var key = response.authResponse.accessToken;
                George.Cookie.setItem('accessToken',key);

                George.loginUser({
                    token: key
                },function(res){
                    George.env.loginStatus = true;
                    $('#fb_user').text(res.name);
                    $('.people_nav,.people').attr('src','https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xfa1/t1.0-1/p160x160/10314011_10202684084237605_1762184246269689844_n.jpg');
                    $('#fb_login,.login_button').hide();
                    $('#fb_logout,.logout_button').show();
                });

            }, {scope: 'public_profile,email'});
        });

        $('#fb_logout,.logout_button').on('click',function(){
            George.logoutUser({},function(res){
                if(res.status){
                    George.env.loginStatus = false;
                    $('#fb_user').text("訪客");
                    $('#fb_login,.login_button').show();
                    $('#fb_logout,.logout_button').hide();
                    $('.people_nav,.people').attr('src',George.env.defaultUserImage);
                }
                // George.env.loginStatus = true;

            });
          //    FB.logout(function(response) {
          //        $('#fb_user').text('訪客');
                // $('#fb_login').show();
                // $('#fb_logout').hide();
          //   });
        });
    },

    imagesLoaded: function (container, msnry) {

        // initialize Masonry after all images have loaded
        imagesLoaded( container, function() {
          msnry = new Masonry( container, {
              // options
              columnWidth: 0,
              gutter: 0,
              itemSelector: '.item'
          });
        });
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
            vAxis: {
                0: {title: '價格',minValue: 0},
                1: {title: '交易量', minValue:0}
            },
            series: {
                0: {targetAxisIndex:0},
                1: {targetAxisIndex:0},
                2: {targetAxisIndex:1}
            }
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    }
}



