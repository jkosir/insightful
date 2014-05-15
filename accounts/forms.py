from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (model.USERNAME_FIELD, )

    def __init__(self, *args, **kwargs):
        super(EmailUserCreationForm, self).__init__(*args, **kwargs)
        if 'username' not in self.Meta.fields:
            self.fields.pop('username', None)


