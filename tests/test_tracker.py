import httpx
import pytest
import respx

from torrent import TorrentInfo
from tracker import HTTTPTracker, TrackerError


@pytest.mark.asyncio
async def test_http_success(respx_mock: respx.MockRouter) -> None:
    info = TorrentInfo.parse("archive.torrent")
    route = respx_mock.get(info.announce).mock(
        return_value=httpx.Response(
            200,
            content=b"d8:completei0e10:downloadedi0e10:incompletei1e8:intervali1e12:min intervali1e5:peers6:\x1f\x92\xdd\xa7\x1a\xe2e",  # noqa: E501
        )
    )

    tracker = HTTTPTracker(info)
    tracker_response = await tracker.get_info()
    await tracker.close()

    assert route.called
    assert tracker_response.complete == 0
    assert tracker_response.incomplete == 1
    assert tracker_response.interval == 1
    assert tracker_response.min_interval == 1
    assert len(tracker_response.peers) == 1


@pytest.mark.asyncio
async def test_http_success_with_failure_reason(respx_mock: respx.MockRouter) -> None:
    info = TorrentInfo.parse("archive.torrent")
    route = respx_mock.get(info.announce).mock(
        return_value=httpx.Response(
            200,
            content=b"d8:completei0e10:downloadedi0e10:incompletei1e8:intervali1e12:min intervali1e5:peers6:\x1f\x92\xdd\xa7\x1a\xe214:failure reason19:some failure reasone",  # noqa: E501
        )
    )

    tracker = HTTTPTracker(info)
    with pytest.raises(TrackerError, match=".*some failure reason.*") as _:
        await tracker.get_info()

    assert route.called
    await tracker.close()


def test_http_success_with_invalid_body() -> None:
    pass


def test_http_failure_with_error_message() -> None:
    pass


def test_http_failure_without_message() -> None:
    pass


def test_http_request_error() -> None:
    pass
