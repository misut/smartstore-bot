from dependency_injector import containers, providers

from bot.infrastructure import ChromeSmartStoreErrander


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    errander = providers.Singleton(
        ChromeSmartStoreErrander,
        username=config.USERNAME,
        password=config.PASSWORD,
    )
