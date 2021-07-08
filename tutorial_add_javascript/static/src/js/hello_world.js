odoo.define('hello_world.main', function (require) {  
    const AbstractAction = require('web.AbstractAction');  
    const core = require('web.core');  
    const OurAction = AbstractAction.extend({      
        template: "hello_world.ClientAction",  
        info: "this message comes from the JS",
    });
    core.action_registry.add('hello_world.action', OurAction);
    
    var FieldChar = require('web.basic_fields').FieldChar;
    var CustomFieldChar = FieldChar.extend({
        _renderReadonly: function(){
            console.log('this is for custom field.')
        },
    });

    var fieldRegistry = require('web.field_registry');
    fieldRegistry.add('my-custom-field',CustomFieldChar);
});                    
