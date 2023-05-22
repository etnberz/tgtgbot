import datetime
from unittest.mock import MagicMock

import pytest

from tests.conftest import ENV_VARS, TestClient  # pylint:disable=import-error
from tgtgbot.tgtg_bot.tgtg_bot import TgtgBot

NOW = datetime.datetime(2023, 5, 18, 18)


def mock_tgtg_bot(mocker, monkeypatch):
    mocker.patch(
        "tgtg_bot.tgtg_bot.tgtg_bot.TgtgClient",
        return_value=TestClient(),
    )

    mocker.patch(
        "tgtg_bot.tgtg_bot.tgtg_bot.dt.timedelta", return_value=datetime.timedelta(seconds=1)
    )

    datetime_mock = MagicMock(wraps=datetime.datetime)
    datetime_mock.now.return_value = NOW
    monkeypatch.setattr(datetime, "datetime", datetime_mock)


@pytest.mark.parametrize(
    "items_available, expected_availability",
    [(0, False), (1, True), (100, True)],
    ids=["Item Unavailable", "One item available", "100 items available"],
)
def test_tgtgbot_is_item_available(mocker, monkeypatch, items_available, expected_availability):
    mock_tgtg_bot(mocker=mocker, monkeypatch=monkeypatch)

    get_item_mock = mocker.patch(
        "tests.conftest.TestClient.get_item", return_value={"items_available": items_available}
    )

    item_available = TgtgBot(item_id=678105).is_item_available()

    get_item_mock.assert_called_once_with(item_id=678105)
    assert item_available == expected_availability


def test_tgtgbot_send_message(mocker, monkeypatch):
    expected_url = (
        f"https://api.telegram.org/bot{ENV_VARS['TGTG_TELEGRAMBOT_TOKEN']}/sendMessage?"
        f"chat_id={ENV_VARS['TGTG_TELEGRAMBOT_CHAT_ID']}&text=scoobydoooo"
    )

    mock_tgtg_bot(mocker=mocker, monkeypatch=monkeypatch)

    mock_requests = mocker.patch("tgtg_bot.tgtg_bot.tgtg_bot.requests.get")

    TgtgBot(message="scoobydoooo").send_message()

    mock_requests.assert_called_once_with(url=expected_url, timeout=5)


def make_mock_input(generator):
    def mock_input():
        return next(generator)

    return mock_input


@pytest.mark.parametrize(
    "nb_loops, ends_with_item_availability",
    [(1, True), (6, True), (10, False)],
    ids=[
        "Item available right now",
        "Item available after 10 loops",
        "Item not available after 10 loops",
    ],
)
def test_tgtgbot_run(mocker, monkeypatch, nb_loops, ends_with_item_availability):
    mock_tgtg_bot(mocker=mocker, monkeypatch=monkeypatch)

    bot = TgtgBot()
    bot.end_time = NOW + datetime.timedelta(seconds=1)

    def datetimes_generator(dt_input):
        yield from dt_input

    dt_input = (
        [NOW for loop in range(nb_loops)]
        if ends_with_item_availability
        else [NOW for loop in range(nb_loops - 1)] + [NOW + datetime.timedelta(seconds=2)]
    )
    item_availabilities = (
        [False for loop in range(nb_loops - 1)] + [True]
        if ends_with_item_availability
        else [False for loop in range(nb_loops)]
    )

    gen = datetimes_generator(dt_input)
    datetime_now_mock = make_mock_input(gen)

    monkeypatch.setattr("datetime.datetime.now", datetime_now_mock)

    mock_is_item_available = mocker.patch(
        "tgtg_bot.tgtg_bot.tgtg_bot.TgtgBot.is_item_available",
        side_effect=item_availabilities,
    )

    mock_send_message = mocker.patch(
        "tgtg_bot.tgtg_bot.tgtg_bot.TgtgBot.send_message",
    )

    mock_time_sleep = mocker.patch(
        "tgtg_bot.tgtg_bot.tgtg_bot.time.sleep",
    )

    bot.run()

    mock_is_item_available.call_count = nb_loops
    if ends_with_item_availability:
        mock_send_message.assert_called_once()
    mock_time_sleep.call_count = nb_loops - 1
