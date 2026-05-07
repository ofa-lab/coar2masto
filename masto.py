from mastodon import Mastodon
from configparser import ConfigParser

CONFIG_INI = "config.ini"

def get_config(config_file=CONFIG_INI, section=None):
    config = ConfigParser()
    config.read(config_file)
    return (
        config if section is None
        else config[section] if config.has_section(section)
        else None
    )


def get_client(conf):
    return Mastodon(access_token=conf['API_TOKEN'], api_base_url=conf['API_URL'])


def toot_test():
    cfg = get_config(section='default.mastodon.api')
    m = get_client(cfg)

    msg = "test !"
    reply_to = None # 116439531486765952
    medias = [
        m.media_post("img/a.jpg"),
        m.media_post("img/b.jpg"),
        m.media_post("img/a.jpg"),
        m.media_post("img/c.jpg"),
    ] if True else None

    m.status_post(msg, in_reply_to_id=reply_to, media_ids=medias)
