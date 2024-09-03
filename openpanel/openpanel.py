import asyncio
import json
import requests
from typing import Dict, Any, Optional, Callable
from threading import Thread
from queue import Queue

class OpenPanel:
    SDK_VERSION = "0.0.1"

    def __init__(self, client_id: str, client_secret: Optional[str] = None, api_url: Optional[str] = None,
                 filter: Optional[Callable[[Dict[str, Any]], bool]] = None, disabled: bool = False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url or "https://api.openpanel.dev"
        self.filter = filter
        self.disabled = disabled
        self.profile_id: Optional[str] = None
        self.global_properties: Dict[str, Any] = {}
        self.queue: Queue = Queue()
        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def _send(self, payload: Dict[str, Any]):
        if self.disabled:
            return

        if self.filter and not self.filter(payload):
            return

        headers = {
            "Content-Type": "application/json",
            "openpanel-client-id": self.client_id,
            "openpanel-sdk-name": "python",
            "openpanel-sdk-version": self.SDK_VERSION
        }

        if self.client_secret:
            headers["openpanel-client-secret"] = self.client_secret

        try:
            response = requests.post(f"{self.api_url}/track", json=payload, headers=headers)
            if response.status_code not in (200, 202):
                print(f"Error sending payload: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error sending payload: {str(e)}")

    def _queue_send(self, payload: Dict[str, Any]):
        future = asyncio.run_coroutine_threadsafe(self._send(payload), self.loop)
        future.add_done_callback(lambda f: f.exception())  # This will silently discard any exceptions

    def set_global_properties(self, properties: Dict[str, Any]):
        self.global_properties.update(properties)

    def track(self, name: str, properties: Optional[Dict[str, Any]] = None):
        merged_properties = {**self.global_properties, **(properties or {})}
        payload = {
            "type": "track",
            "payload": {
                "name": name,
                "properties": merged_properties,
                "profileId": self.profile_id or None
            }
        }
        self._queue_send(payload)

    def identify(self, profile_id: str, traits: Dict[str, Any] = None):
        self.profile_id = profile_id
        traits = traits or {}
        payload = {
            "type": "identify",
            "payload": {
                "profileId": profile_id,
                **traits,
                "properties": {**self.global_properties, **traits.get("properties", {})}
            }
        }
        self._queue_send(payload)

    def alias(self, profile_id: str, alias: str):
        payload = {
            "type": "alias",
            "payload": {
                "profileId": profile_id,
                "alias": alias
            }
        }
        self._queue_send(payload)

    def increment(self, profile_id: str, property: str, value: Optional[int] = None):
        payload = {
            "type": "increment",
            "payload": {
                "profileId": profile_id,
                "property": property,
                "value": value
            }
        }
        self._queue_send(payload)

    def decrement(self, profile_id: str, property: str, value: Optional[int] = None):
        payload = {
            "type": "decrement",
            "payload": {
                "profileId": profile_id,
                "property": property,
                "value": value
            }
        }
        self._queue_send(payload)

    def clear(self):
        self.profile_id = None
        self.global_properties.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup()

    def _cleanup(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join(timeout=5)  # Wait for up to 5 seconds for the thread to finish

        # If the thread is still alive, we need to force it to stop
        if self.thread.is_alive():
            import _thread
            _thread.interrupt_main()