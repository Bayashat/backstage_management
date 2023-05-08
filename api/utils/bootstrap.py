from django import forms


class BootStrap:
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop through all the fields in the Form, and set the plug-in for each field
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            
            # If there is an attribute in the field, the original attribute will be retained; if there is no attribute, it will be added
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control", 
                    "placeholder": field.label
                }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass