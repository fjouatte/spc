from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field
from spc.color_parser import ColorParser
from spc.models import User


class SocialAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        cp = ColorParser()
        user = super(SocialAdapter, self).populate_user(request, sociallogin, data)
        nickname = cp.toHTML(data.get('nickname'))
        user_field(user, 'nickname', nickname)
        try:
            db_user = User.objects.get(username=user.username)
            db_user.nickname = nickname
            db_user.save()
        except User.DoesNotExist:
            return user
        return user
