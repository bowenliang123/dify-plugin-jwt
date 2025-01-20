import json
from collections.abc import Generator
from typing import Any

import jwt
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils import jwt_utils


class JwtDecoderTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        param_jwt: str = tool_parameters.get("jwt")
        key: str = tool_parameters.get("key")
        algorithm: str = tool_parameters.get("algorithm")

        # validation
        jwt_utils.check_valid_algorithm(algorithm)
        if not param_jwt:
            raise ValueError("Invalid input JWT token")
        if not key:
            raise ValueError("Invalid input for decryption key")

        decoded_payload = jwt.decode(jwt=param_jwt, key=key, algorithms=[algorithm])
        payload_str = json.dumps(decoded_payload)
        yield self.create_text_message(payload_str)
