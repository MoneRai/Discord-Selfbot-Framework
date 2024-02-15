class Guild:
    __slots__ = (
        "id",
        "_guild_id",
        "name",
        "icon",
        "description",
        "splash",
        "discovery_splash",
        "features",
        "emojis",
        "banner",
        "owner_id",
        "region",
        "afk_timeout",
        "widget_enabled",
        "verification_level",
        "roles",
        "message_notifications",
        "mfa_level",
        "explicit_filter",
        "max_presences",
        "max_members",
        "vanity_url_code",
        "premium_tier",
        "premium_count",
        "system_channel_flags",
        "preferred_locale"
    )

    def __init__(self, **data):
        self.id: int = int(data.get("id", 0))
        self._guild_id: int = int(data.get("guild_id", 0))
        self.name: str = data.get("name")
        self.icon: str = data.get("icon")
        self.description = data.get("description")
        self.splash: str = data.get("splash")
        self.discovery_splash: str = data.get("discovery_splash")
        self.features: list = data.get("features")
        self.emojis: list = data.get("emojis")
        self.banner: str = data.get("banner")
        self.owner_id: int = int(data.get("owner_id", 0))
        self.region: str = data.get("region")
        self.afk_timeout: int = int(data.get("afk_timeout", 0))
        self.widget_enabled: bool = data.get("widget_enabled")
        self.verification_level: int = int(data.get("verification_level", 0))
        self.roles: list = data.get("roles")
        self.message_notifications: int = int(data.get("default_message_notifications", 0))
        self.mfa_level: int = int(data.get("mfa_level", 0))
        self.explicit_filter: int = int(data.get("explicit_content_filter", 0))
        self.max_presences: int = int(data.get("max_presences", 0))
        self.max_members: int = int(data.get("max_members", 0))
        self.vanity_url_code: str = data.get("vanity_url_code")
        self.premium_tier: int = int(data.get("premium_tier", 0))
        self.premium_count: int = int(data.get("premium_subscription_count", 0))
        self.system_channel_flags: int = int(data.get("system_channel_flags", 0))
        self.preferred_locale: str = data.get("preferred_locale")