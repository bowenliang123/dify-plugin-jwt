from collections.abc import Generator
from typing import Any

import jwt
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils import json_utils, jwt_utils


class JwtEncoderTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        param_payload: str = tool_parameters.get("payload", "{}") or "{}"
        param_headers: str = tool_parameters.get("headers", "{}") or "{}"
        key: str = tool_parameters.get("key")
        algorithm: str = tool_parameters.get("algorithm")

        # validation
        jwt_utils.check_valid_algorithm(algorithm)
        jwt_utils.check_key_length(key, algorithm)
        jwt_utils.check_valid_json(param_payload, "payload")
        jwt_utils.check_valid_json(param_headers, "headers")

        payload: dict[str, Any] = json_utils.parse_json(param_payload)
        headers: dict[str, Any] = json_utils.parse_json(param_headers)
        result = jwt.encode(payload=payload, key=key, algorithm=algorithm, headers=headers)

        yield self.create_text_message(result)
