from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class ManiaplanetOAuth2Account(ProviderAccount):
    def get_profile_url(self):
        return (self.account.extra_data
                .get('links', {})
                .get('html', {})
                .get('href'))

    def get_avatar_url(self):
        return (self.account.extra_data
                .get('links', {})
                .get('avatar', {})
                .get('href'))

    def to_str(self):
        dflt = super(ManiaplanetOAuth2Account, self).to_str()
        return self.account.extra_data.get('display_name', dflt)


class ManiaplanetOAuth2Provider(OAuth2Provider):
    id = 'maniaplanet_oauth2'
    name = 'maniaplanet'
    account_class = ManiaplanetOAuth2Account

    def extract_uid(self, data):
        return data['login']

    def extract_common_fields(self, data):
        return dict(
            name=data.get('nickname'),
        )


providers.registry.register(ManiaplanetOAuth2Provider)
