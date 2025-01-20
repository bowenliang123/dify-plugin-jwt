from collections.abc import Generator
from typing import Any

import jwt
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class JwtDecoderTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        param_jwt: str = tool_parameters.get("jwt", "{}")
        key: str = tool_parameters.get("key")
        algorithm: str = tool_parameters.get("algorithm")

        decoded_payload = jwt.decode(payload=param_jwt, key=key, algorithm=algorithm)

        yield self.create_text_message(decoded_payload)
