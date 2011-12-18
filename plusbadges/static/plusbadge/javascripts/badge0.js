// based on http://stackoverflow.com/questions/248351/how-can-i-create-a-javascript-badge-or-widget/248451#248451
// and http://alexmarandon.com/articles/web_widget_jquery/

(function(){
    // Localize jQuery variable
    var jQuery;

    /******** Load jQuery if not present *********/
        if (window.jQuery === undefined || window.jQuery.fn.jquery !== '1.4.2') {
            var script_tag = document.createElement('script');
            script_tag.setAttribute("type","text/javascript");
            script_tag.setAttribute("src",
                "http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js");
            script_tag.onload = scriptLoadHandler;
            script_tag.onreadystatechange = function () { // Same thing but for IE
                if (this.readyState == 'complete' || this.readyState == 'loaded') {
                    scriptLoadHandler();
        }
    };
    // Try to find the head, otherwise default to the documentElement
    (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
} else {
    // The jQuery version on the window is the one we want to use
    jQuery = window.jQuery;
    main();
}

    /******** Called once jQuery has loaded ******/
    function scriptLoadHandler() {
    // Restore $ and window.jQuery to their previous values and store the
    // new jQuery in our local jQuery variable
    jQuery = window.jQuery.noConflict(true);
    // Call our main function
    main(); 
}

    // create badge
    function main() {
        jQuery(document).ready(function($){
            var prefix = "com_powazord_plustoys_badge_0_";
            var tagId = prefix+"script";

            var scriptTag = document.getElementById(tagId);

            var widgetDiv = document.createElement('div');
            $.get("?embed=yes&fragment=yes", function(data){
                $(widgetDiv).html(data);
                scriptTag.parentNode.replaceChild(widgetDiv, scriptTag);
            });
        });
    }
})();
