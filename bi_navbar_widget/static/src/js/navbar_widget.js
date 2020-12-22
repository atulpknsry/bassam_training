odoo.define('navbar_widget.icon', function (require) {
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    
    // Appends Icon template in system tray (navbar)
    var icon = Widget.extend({
        template:'icon',
        events: {
            'click':'clickWidget',
        },
        clickWidget: function(){

        },
    });
SystrayMenu.Items.push(icon);
});