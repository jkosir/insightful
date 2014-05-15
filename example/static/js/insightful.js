
var insightful = (function () {
    'use strict';
    var apiURL,
        websiteID,
        cookiePrefix = 'i_';

    function init(options) {
        apiURL = options.url;
        websiteID = options.id;

        /*
         Load previous view data from cookie and submit pageview report
         */
        submitReport();

        /*
         Add event listeners for tracking interaction time
         */
        addEventListener(document, 'keydown', contentWatch);
        addEventListener(document, 'click', contentWatch);
        addEventListener(window, 'mousemove', contentWatch);
        addEventListener(window, 'scroll', contentWatch);

        /*
         Event listeners for specific content parts (everything with data-track-name attribute)
         Add on document.ready to ensure content has finished loading
         */
        $(document).ready(function () {
            $('[data-track-name]').each(function () {
                var events = ['click', 'mousemove', 'blur', 'focus', 'keydown', 'mouseenter'];
                for (var i = 0; i < events.length; i++) {
                    addEventListener(this, events[i], function (e) {
                        contentWatch(e, $(this).attr('data-track-name'));
                    });
                }
            })
        });

    }

    /*
     "Container" for binding throttled callbacks
     */
    function contentWatch(e, name) {
        name = name || 'active_time';
        if (typeof contentWatch[name] === 'undefined') {
            contentWatch[name] =
                throttle(function () {
                    increaseCookieValue(name);
                }, 1000);
        }
        contentWatch[name]();
    }

    /*
     Read all cookies written by self (v_ prefix)
     */
    function readOwnCookies() {
        var data = {};
        var cookies_list = docCookies.keys();
        for (var i = 0; i < cookies_list.length; i++) {
            if (cookies_list[i].slice(0, cookiePrefix.length) == cookiePrefix) {  // if startswith cookiePrefix
                data[cookies_list[i]] = readCookieValue(cookies_list[i].substring(cookiePrefix.length));
                removeCookie(cookies_list[i].substring(cookiePrefix.length));
            }
        }
        return data;
    }


    /*
     Cookie methods allow for easier changing of actual cookie handling code
     */
    function writeToCookie(key, value, prefix) {
        prefix = prefix || cookiePrefix;
        docCookies.setItem(prefix + key, value, Infinity, '/');
    }

    function readCookieValue(key, prefix) {
        prefix = prefix || cookiePrefix;
        return docCookies.getItem(prefix + key);
    }

    function removeCookie(key, prefix) {
        prefix = prefix || cookiePrefix;
        docCookies.removeItem(prefix + key, '/');
    }


    /*
     generate UUID
     Source: http://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid-in-javascript
     */
    function generateUUID() {
        var d = new Date().getTime();
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c == 'x' ? r : (r & 0x7 | 0x8)).toString(16);
        });
    }

    /*
     Get user uuid from cookie or write one if it doesn't exist yet
     */
    function getVisitorUUID() {
        var id = readCookieValue('id', 'isession_');
        if (!id) {
            id = generateUUID();
            writeToCookie('id', id, 'isession_');
        }
        return id;
    }

    /*
     Make a post request with data from cookie
     */
    function submitReport() {
        var data = {
            uuid: getVisitorUUID(),
            path: window.location.pathname,
            id: websiteID
        };
        var vData = readOwnCookies();
        for (var key in vData) {
            if (vData.hasOwnProperty(key)) {
                data[key] = vData[key];
            }
        }
        $.post(apiURL, data);
    }

    /*
     Cross-browser event listeners
     */
    function addEventListener(element, eventType, eventHandler) {
        if (element.addEventListener) {
            element.addEventListener(eventType, eventHandler, false);

            return true;
        }

        if (element.attachEvent) {
            return element.attachEvent('on' + eventType, eventHandler);
        }
        return false;
    }

    /*
     Increase cookie value by 1 or set to amount if no such key present
     */
    function increaseCookieValue(key) {
        if (readCookieValue(key)) {
            writeToCookie(key, parseInt(readCookieValue(key), 10) + 1);
        }
        else {
            writeToCookie(key, 1);
        }
    }

    /*
     Throttle function from underscore.js
     */
    function throttle(func, wait) {
        var context, args, result;
        var timeout = null;
        var previous = 0;
        var later = function () {
            previous = new Date;
            timeout = null;
            result = func.apply(context, args);
        };
        return function () {
            var now = new Date;
            if (!previous) previous = now;
            var remaining = wait - (now - previous);
            context = this;
            args = arguments;
            if (remaining <= 0) {
                clearTimeout(timeout);
                timeout = null;
                previous = now;
                result = func.apply(context, args);
            } else if (!timeout) {
                timeout = setTimeout(later, remaining);
            }
            return result;
        };
    }

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
     |*|  * docCookies.setItem(name, value[, end[, path[, domain[, secure]]]])
     |*|  * docCookies.getItem(name)
     |*|  * docCookies.removeItem(name[, path], domain)
     |*|  * docCookies.hasItem(name)
     |*|  * docCookies.keys()
     |*|
     \*/

    var docCookies = {
        getItem: function (sKey) {
            return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
        },
        setItem: function (sKey, sValue, vEnd, sPath, sDomain, bSecure) {
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
        removeItem: function (sKey, sPath, sDomain) {
            if (!sKey || !this.hasItem(sKey)) {
                return false;
            }
            document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + ( sDomain ? "; domain=" + sDomain : "") + ( sPath ? "; path=" + sPath : "");
            return true;
        },
        hasItem: function (sKey) {
            return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
        },
        keys: /* optional method: you can safely remove it! */ function () {
            var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
            for (var nIdx = 0; nIdx < aKeys.length; nIdx++) {
                aKeys[nIdx] = decodeURIComponent(aKeys[nIdx]);
            }
            return aKeys;
        }
    };

    /*
     Make init method public
     */
    return {
        init: init
    }


})();


