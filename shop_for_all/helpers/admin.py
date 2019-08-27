from functools import reduce

from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from rest_framework.reverse import reverse


def format_choice_output(choice_output, choice):
    pk = choice[0]
    ctype = ContentType.objects.filter(pk=pk).first() if pk else None

    if ctype is None:
        return choice_output
    # ---------
    options = ",".join(
        [
            "new Option('---------', '', true)",
            *[
                f"new Option('{str(item)}', {item.pk})"
                for item in ctype.model_class().objects.all()
            ],
        ]
    )

    # noinspection PyProtectedMember
    return choice_output + f"'{pk}': [{options}],"


class ContentTypeSelect(forms.Select):
    def __init__(self, lookup_id, attrs=None, choices=()):
        self.lookup_id = lookup_id
        super(ContentTypeSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, **kwargs):
        output = super(ContentTypeSelect, self).render(name, value, attrs, **kwargs)

        output += """
            <script type="text/javascript">
                (function($) {{
                    $(document).ready(function() {{
                        function setObject(val) {{
                            var options = {id}_choice_urls[val];

                            if (options) {{
                                objectSelect.html(options);
                                objectSelect.find('option:nth-child(1)').prop('selected', true);
                                objectContainer.show();
                            }} else {{
                                objectContainer.hide();
                            }}
                        }}

                        var {id}_choice_urls = {{{choiceoutput}}};
                        var objectContainer = $('.field-{fk_id}');
                        var objectSelect = objectContainer.find('#id_{fk_id}');
                        var typeSelect = $('#{id}')
                        setObject(typeSelect.val());

                        typeSelect.change(event => 
                            setObject(event.target.value)
                        );
                    }});
                }})(django.jQuery);
            </script>
        """

        output = output.format(
            id=attrs["id"],
            fk_id=self.lookup_id,
            choiceoutput=reduce(format_choice_output, self.choices, ""),
        )

        return mark_safe(output)


class GenericForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GenericForm, self).__init__(*args, **kwargs)

        self.fields["content_type"].widget.widget = ContentTypeSelect(
            lookup_id="object_id",
            attrs=self.fields["content_type"].widget.widget.attrs,
            choices=self.fields["content_type"].widget.widget.choices,
        )

        object_id = self.fields.pop("object_id")
        object_id.widget = forms.Select()
        self.fields["object_id"] = object_id

    class Meta:
        fields = "__all__"
        labels = {"object_id": "Object"}

        readonly_fields = ("object_id",)


class GenericModelAdmin(admin.ModelAdmin):
    list_display = ("content_object", "show_content_type")
    form = GenericForm

    def content_object(self, obj):
        return obj.content_object.name

    content_object.short_description = "Name"
    content_object.admin_order_field = "content_object__name"

    def show_content_type(self, obj):
        return format_html(
            format_string='<a href="{url}">{name}</a>',
            name=obj.content_type.name,
            url=reverse(
                f"admin:{obj.content_type.app_label}_{obj.content_type.model}_changelist"
            ),
        )

    show_content_type.short_description = "Сontent type"
    show_content_type.admin_order_field = "content_type__name"
    show_content_type.allow_tags = True
