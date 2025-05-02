# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Callback functions for Admission Advisor Agent."""

import logging
import time

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from typing import Any, Dict
from google.adk.tools import BaseTool
from google.adk.agents.invocation_context import InvocationContext

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RATE_LIMIT_SECS = 60
RPM_QUOTA = 10


def rate_limit_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> None:
    """Callback function that implements a query rate limit.

    Args:
      callback_context: A CallbackContext obj representing the active callback
        context.
      llm_request: A LlmRequest obj representing the active LLM request.
    """
    for content in llm_request.contents:
        for part in content.parts:
            if part.text == "":
                part.text = " "

    now = time.time()
    if "timer_start" not in callback_context.state:
        callback_context.state["timer_start"] = now
        callback_context.state["request_count"] = 1
        logger.debug(
            "rate_limit_callback [timestamp: %i, "
            "req_count: 1, elapsed_secs: 0]",
            now,
        )
        return

    request_count = callback_context.state["request_count"] + 1
    elapsed_secs = now - callback_context.state["timer_start"]
    logger.debug(
        "rate_limit_callback [timestamp: %i, request_count: %i,"
        " elapsed_secs: %i]",
        now,
        request_count,
        elapsed_secs,
    )

    if request_count > RPM_QUOTA:
        delay = RATE_LIMIT_SECS - elapsed_secs + 1
        if delay > 0:
            logger.debug("Sleeping for %i seconds", delay)
            time.sleep(delay)
        callback_context.state["timer_start"] = now
        callback_context.state["request_count"] = 1
    else:
        callback_context.state["request_count"] = request_count

    return


def before_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: CallbackContext
):
    """Callback được gọi trước khi một tool được thực thi.
    
    Args:
        tool: Tool đang được gọi
        args: Các tham số được truyền vào tool
        tool_context: Context của callback
    """
    logger.debug(f"Tool đang được gọi: {tool.name} với tham số: {args}")
    return None


def before_agent(callback_context: InvocationContext):
    """Callback được gọi trước khi agent xử lý một yêu cầu.
    
    Args:
        callback_context: Context của callback
    """
    logger.debug("Agent đang xử lý yêu cầu mới")
    return None
