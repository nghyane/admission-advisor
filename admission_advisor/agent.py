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

"""Agent module for the admission advisor agent."""

import logging
import warnings
from google.adk import Agent
from .config import Config
from .prompts import INSTRUCTION
from .shared_libraries.callbacks import (
    rate_limit_callback,
    before_agent,
    before_tool,
)
from .tools import (
    get_campuses,
    get_majors_list,
    get_major_detail,
    store_student_profile,
    get_user_profile,
    get_admission_methods,
    get_dormitory_by_campus,
    get_scholarships_list,
    debug_invocation_context,  
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

configs = Config()

# configure logging __name__
logger = logging.getLogger(__name__)


root_agent = Agent(
    model=configs.agent_settings.model,
    global_instruction=INSTRUCTION,
    name=configs.agent_settings.name,
    tools=[
        get_campuses,
        get_majors_list,
        get_major_detail,
        get_admission_methods,
        store_student_profile,
        get_user_profile,
        get_dormitory_by_campus,
        get_scholarships_list,
        debug_invocation_context,  # Thêm tool mới
    ],
    before_tool_callback=before_tool,
    before_agent_callback=before_agent,
    before_model_callback=rate_limit_callback,
    generate_content_config={
        "temperature": 0.3,  
        "top_p": 0.8,  
    }
) 
