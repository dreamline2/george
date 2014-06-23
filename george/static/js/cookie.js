George = (typeof George === 'undefined') ? {} : George;

/*\
|*|
|*|  :: cookies.js ::
|*|
|*|  A complete cookies reader/writer framework with full unicode support.
|*|
|*|  https://developer.mozilla.org/en-US/docs/DOM/document.cookie
|*|
|*|  This framework is released under the GNU Public License, version 3 or later.
|*|  http://www.gnu.org/licenses/gpl-3.0-standalone.html
|*|
|*|  Syntaxes:
|*|
|*|  * Tagtoo.Cookie.setItem(name, value[, end[, path[, domain[, secure]]]])
|*|  * Tagtoo.Cookie.getItem(name)
|*|  * Tagtoo.Cookie.removeItem(name[, path], domain)
|*|  * Tagtoo.Cookie.hasItem(name)
|*|  * Tagtoo.Cookie.keys()
|*|
|*|  :: cookie Format js ::
|*|
|*|  擴充 cookie.js  setTime & getItem 直接存取 array list string 部份boolean (無法分辨數字＆部份boolean)
|*|  制定一個有限制的資料格式來達到一個較精簡的資料格式
|*|  1. 支援單層的 {} 不支援多層..
|*|  2. 支援 字串 array, 數字會被強制轉型
|*|
|*|
|*|  Syntaxes:
|*|  CookieFormat.encode(data)
|*|  CookieFormat.decode(queryString)
|*|
|*|
|*|  updated:
|*|     2014-4-7: 拔除 key name 容錯, 避免前後端溝通上問題, example
|*|         Tagtoo.Cookie.setItem('中文', "value")
|*|         這樣實際上存在 cookie 裡面的會是 %E4%B8%AD%E6%96%87=value
|*|         後端就需要用 %E4%B8%AD%E6%96%87 才能拿到 value.. 不過假如用這package 的不知道內部用 encodeURIComponent 壓過.. 那後端就永遠不知道出問題了..
|*|
\*/

(function() {
    /* moz cookie lib use cookie format */
    window.George.Cookie = {

        getItem: function(sKey) {
            return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
        },
        setItem: function(sKey, sValue, vEnd, sPath, sDomain, bSecure) {
            if (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) {
                return false;
            }
            var sExpires = "";
            if (vEnd) {
                switch (vEnd.constructor) {
                    case Number:
                        sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
                        break;
                    case String:
                        sExpires = "; expires=" + vEnd;
                        break;
                    case Date:
                        sExpires = "; expires=" + vEnd.toUTCString();
                        break;
                }
            }
            document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
            return true;
        },
        removeItem: function(sKey, sPath, sDomain) {
            if (!sKey || !this.hasItem(sKey)) {
                return false;
            }
            document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "");
            return true;
        },
        hasItem: function(sKey) {
            return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
        },
        keys: /* optional method: you can safely remove it! */ function() {
            var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
            for (var nIdx = 0; nIdx < aKeys.length; nIdx++) {
                aKeys[nIdx] = decodeURIComponent(aKeys[nIdx]);
            }
            return aKeys;
        }
    };
}());
