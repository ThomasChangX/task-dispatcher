#!/usr/bin/env python3
"""
Task Dispatcher V2 - Session Initialization Script

用于初始化 task-dispatcher 的会话环境。
"""

import os
import sys
from datetime import datetime

# 添加 scripts 目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

from loop_detector import get_detector, reset_detector

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SESSION_STATE_PATH = os.path.join(WORKSPACE, "SESSION-STATE.md")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")


def ensure_memory_dir():
    """确保 memory 目录存在"""
    os.makedirs(MEMORY_DIR, exist_ok=True)


def init_loop_detector():
    """初始化循环检测器"""
    reset_detector()  # 重置历史记录
    detector = get_detector(max_retries=3)
    print(f"✓ Loop Detector initialized (max_retries={detector.max_retries})")
    return detector


def create_session_state(task_description: str = None):
    """创建 SESSION-STATE.md"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    content = f"""# Session State - {date_str}

## Current Task
- **Task**: {task_description or "新任务"}
- **Started**: {datetime.now().isoformat()}
- **Status**: In Progress
- **Progress**: 0%

## Task Breakdown
- [ ] 待任务拆解后填充

## Critical Context
- 无

## Recent History
- 会话开始

## Next Steps
- [ ] 执行需求分析

## Blocker
- 无
"""
    with open(SESSION_STATE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Created SESSION-STATE.md")


def main():
    ensure_memory_dir()
    init_loop_detector()
    create_session_state()
    print("✓ Task Dispatcher V2 session initialized")


if __name__ == "__main__":
    main()
