from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator,
)


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        super().__init__(min_length)

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                '• کلمه عبور شما باید شامل حداقل %(min_length)d کاراکتر باشد.',
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        return super().validate(password, user)

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                '• کلمه عبور شما ساده و قابل حدس است.',
                code='password_too_common',
            )
        return super().validate(password, user)

class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                '• کلمه عبور شما نباید فقط از اعداد تشکیل شده باشد.',
                code='password_entirely_numeric',
            )
        return super().validate(password, user)

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        UserModel = get_user_model()
        user_fields = [UserModel.USERNAME_FIELD] + list(self.user_attributes)
        for field_name in user_fields:
            value = getattr(user, field_name, None)
            if value and password.lower() in str(value).lower():
                raise ValidationError(
                    '• کلمه عبور شما نباید مشابه نام کاربری شما باشد.',
                    code='password_too_similar',
                )
        return super().validate(password, user)





class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize field-specific error messages
        self.fields['username'].error_messages = {
            'required': '• نام کاربری نمی تواند خالی باشد',
        }
        self.fields['password'].error_messages = {
            'required': '• کلمه عبور نمی تواند خالی باشد',
        }

        # Customize non-field error messages
        self.error_messages = {
            'invalid_login': '• نام کاربری یا کلمه عبور شما صحیح نیست. توجه کنید که هر دو فیلد به بزرگ و کوچک بودن حروف حساس هستند.',
            'inactive': "• این حساب غیر فعال است",
        }

class CustomRegistrationForm(UserCreationForm):
    def custom_password_validator(password, user=None):
        try:
            validate_password(password, user)
        except ValidationError as e:
            raise ValidationError('• کلمه عبور اشتباه است: ' + ', '.join(e.messages))



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize field-specific error messages
        self.fields['username'].error_messages = {
            'required': '• نام کاربری نمی تواند خالی باشد',
            'unique': '• حساب کاربری دیگری با این نام کاربری وجود دارد.',
        }
        self.fields['password1'].error_messages = {
            'required': '• کلمه عبور نمی تواند خالی باشد.',
        }
        self.fields['password2'].error_messages = {
            'required': '• تکرار کلمه عبور نمی تواند خالی باشد.',
        }

        # Customize non-field error messages
        self.error_messages = {
            'password_mismatch': '• کلمه های عبور با یکدیگر تطابق ندارند.',
        }
    