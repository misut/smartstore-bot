from dependency_injector import containers, providers

from bot.infrastructure import ChromeSmartStoreErrander, ChromeWebDriver, SqlAccountRepository, SqlAlchemyDatabase


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(SqlAlchemyDatabase)

    driver = providers.Singleton(ChromeWebDriver)

    hidden_driver = providers.Singleton(ChromeWebDriver, hidden=True)

    accounts = providers.Singleton(SqlAccountRepository, database=database.provided)

    errander = providers.Singleton(ChromeSmartStoreErrander, driver=driver.provided.driver)

    hidden_errander = providers.Singleton(ChromeSmartStoreErrander, driver=hidden_driver.provided.driver)
