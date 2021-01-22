// Frame.js -- Must be added in iframe window
function publishHeight()
{
    if (window.location.hash.length == 0) return;

    var frameId = getFrameId();

    if (frameId == '') return;

    var actualHeight = getBodyHeight();
    var currentHeight = getViewPortHeight();

    if  (Math.abs(actualHeight - currentHeight) > 15)
    {
        var hostUrl = window.location.hash.substring(1);

        hostUrl += "#";
        hostUrl += 'frameId=' + frameId;
        hostUrl += '&';
        hostUrl += 'height=' + actualHeight.toString();

        window.top.location = hostUrl;
    }
}

function getFrameId()
{
    var qs = parseQueryString(window.location.href);
    var frameId = qs["frameId"];

    var hashIndex = frameId.indexOf('#');

    if (hashIndex > -1)
    {
        frameId = frameId.substring(0, hashIndex);
    }

    return frameId;
}

function getBodyHeight()
{
    var height;
    var scrollHeight;
    var offsetHeight;

    if (document.height)
    {
        height = document.height;
    }
    else if (document.body)
    {
        if (document.body.scrollHeight)
        {
            height = scrollHeight = document.body.scrollHeight;
        }
        if (document.body.offsetHeight)
        {
            height = offsetHeight = document.body.offsetHeight;
        }

        if (scrollHeight && offsetHeight)
        {
            height = Math.max(scrollHeight, offsetHeight);
        }
    }

    return height;
}

function getViewPortHeight()
{
    var height = 0;

    if (window.innerHeight)
    {
        height = window.innerHeight - 18;
    }
    else if ((document.documentElement) && (document.documentElement.clientHeight))
    {
        height = document.documentElement.clientHeight;
    }
    else if ((document.body) && (document.body.clientHeight))
    {
        height = document.body.clientHeight;
    }

    return height;
}

function parseQueryString(url)
{
    url = new String(url);
    var queryStringValues = new Object();
    var querystring = url.substring((url.indexOf('?') + 1), url.length);
    var querystringSplit = querystring.split('&');

    for (i = 0; i < querystringSplit.length; i++)
    {
        var pair = querystringSplit[i].split('=');
        var name = pair[0];
        var value = pair[1];

        queryStringValues[name] = value;
    }

    return queryStringValues;
}