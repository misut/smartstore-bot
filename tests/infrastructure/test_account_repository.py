from bot.domain import Account, AccountRepository


def test_insert_and_select(account_repo: AccountRepository) -> None:
    accounts = [
        Account(
            id="test_select_id_1",
            password="1q2w3e4r!",
        ),
        Account(
            id="test_select_id_2",
            password="password",
        ),
        Account(
            id="test_select_id_3",
            password="1234567890-=",
        )
    ]

    with account_repo as repo:
        for account in accounts:
            repo.insert(account)
    
        assert all(account in repo.select() for account in accounts)


def test_insert_and_get(account_repo: AccountRepository) -> None:
    account = Account(
        id="test_insert_id",
        password="1q2w3e4r!",
    )

    with account_repo as repo:
        repo.insert(account)

        assert account_repo.get(account.id) == account


def test_insert_and_update_and_get(account_repo: AccountRepository) -> None:
    old_password = "1q2w3e4r!"
    new_password = "password"
    account = Account(
        id="test_update_id",
        password=old_password,
    )

    with account_repo as repo:
        repo.insert(account)
        repo.commit()

    with account_repo as repo:    
        account.password = new_password

        assert repo.get(account.id).password == old_password

        repo.update(account)
        repo.commit()

    with account_repo as repo:
        assert repo.get(account.id).password == new_password


def test_insert_and_delete_and_get(account_repo: AccountRepository) -> None:
    account = Account(
        id="test_delete_id",
        password="1q2w3e4r!",
    )

    with account_repo as repo:
        repo.insert(account)
        repo.commit()

    with account_repo as repo:
        assert repo.get(account.id) == account

        repo.delete(account.id)

        assert repo.get(account.id) is None
