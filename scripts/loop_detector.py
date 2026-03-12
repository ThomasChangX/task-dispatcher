#!/usr/bin/env python3
"""
Loop Detector - 重复次数检测模块

用于检测任务执行循环，防止无限重试。
P0 核心功能：同一任务执行 ≤3 次安全，>3 次兜底
"""

import os
from pathlib import Path
from typing import Optional

# SESSION-STATE.md 路径
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
SESSION_STATE_FILE = WORKSPACE_DIR / "SESSION-STATE.md"


class LoopDetector:
    """任务重复执行检测器"""
    
    def __init__(self, max_retries: int = 3):
        """
        初始化检测器
        
        Args:
            max_retries: 最大重试次数，默认 3 次（安全阈值）
        """
        self.max_retries = max_retries
        self.task_history: dict[str, int] = {}  # task_id -> count
        self._load_state()
    
    def _load_state(self) -> None:
        """从 SESSION-STATE.md 加载 task_history"""
        if not SESSION_STATE_FILE.exists():
            return
        
        try:
            content = SESSION_STATE_FILE.read_text()
            # 解析 task_history 部分
            in_task_history = False
            for line in content.split('\n'):
                if line.strip() == '## Task History':
                    in_task_history = True
                    continue
                if in_task_history:
                    if line.startswith('## '):
                        break
                    if line.strip().startswith('- '):
                        # 格式: - task_id: count
                        parts = line.strip()[2:].split(':')
                        if len(parts) == 2:
                            task_id = parts[0].strip()
                            try:
                                count = int(parts[1].strip())
                                self.task_history[task_id] = count
                            except ValueError:
                                pass
        except Exception:
            pass  # 加载失败则使用空状态
    
    def _save_state(self) -> None:
        """将 task_history 写入 SESSION-STATE.md"""
        if not SESSION_STATE_FILE.exists():
            return
        
        try:
            content = SESSION_STATE_FILE.read_text()
            lines = content.split('\n')
            
            # 查找 Task History 部分
            in_task_history = False
            new_lines = []
            history_start = -1
            history_end = -1
            
            for i, line in enumerate(lines):
                if line.strip() == '## Task History':
                    in_task_history = True
                    history_start = i
                    continue
                if in_task_history and line.startswith('## '):
                    history_end = i
                    break
            
            # 构建新的 Task History 部分
            if history_start >= 0:
                # 保留前面部分
                new_lines = lines[:history_start]
                new_lines.append('## Task History')
                new_lines.append('')
                if self.task_history:
                    for task_id, count in self.task_history.items():
                        new_lines.append(f'- {task_id}: {count}')
                else:
                    new_lines.append('_（无记录）_')
                
                if history_end > 0:
                    new_lines.extend(lines[history_end:])
                else:
                    new_lines.append('')
            else:
                # 没有 Task History 部分，追加
                new_lines = lines
                new_lines.append('')
                new_lines.append('## Task History')
                new_lines.append('')
                if self.task_history:
                    for task_id, count in self.task_history.items():
                        new_lines.append(f'- {task_id}: {count}')
                else:
                    new_lines.append('_（无记录）_')
            
            SESSION_STATE_FILE.write_text('\n'.join(new_lines))
        except Exception:
            pass  # 保存失败静默处理
    
    def check(self, task_id: str) -> dict:
        """
        检查任务执行次数
        
        设计规则: ≤3 次安全，>3 次兜底
        
        Args:
            task_id: 任务唯一标识
            
        Returns:
            dict: {
                'safe': bool,      # 是否安全（未超过阈值）
                'reason': str,     # 原因说明
                'action': str,     # 建议动作
                'count': int       # 当前执行次数
            }
        """
        count = self.task_history.get(task_id, 0)
        
        if count <= self.max_retries:
            # ≤3 次都安全
            return {
                'safe': True,
                'reason': f'任务已执行 {count} 次，在安全范围内（≤{self.max_retries}）',
                'action': 'continue',
                'count': count
            }
        else:
            # >3 次兜底
            return {
                'safe': False,
                'reason': f'任务已执行 {count} 次，超过安全阈值 {self.max_retries}，进入兜底',
                'action': 'fallback',
                'count': count
            }
    
    def record(self, task_id: str) -> None:
        """
        记录任务执行
        
        Args:
            task_id: 任务唯一标识
        """
        self.task_history[task_id] = self.task_history.get(task_id, 0) + 1
        self._save_state()  # 持久化状态
    
    def reset(self, task_id: Optional[str] = None) -> None:
        """
        重置计数
        
        Args:
            task_id: 任务 ID，如果为 None 则重置所有任务
        """
        if task_id is None:
            self.task_history.clear()
        else:
            self.task_history.pop(task_id, None)
        self._save_state()  # 持久化状态
    
    def get_status(self, task_id: str) -> dict:
        """
        获取任务当前状态
        
        Args:
            task_id: 任务唯一标识
            
        Returns:
            dict: 包含执行次数和状态信息
        """
        count = self.task_history.get(task_id, 0)
        return {
            'task_id': task_id,
            'count': count,
            'max_retries': self.max_retries,
            'is_at_risk': count >= self.max_retries
        }


# 全局单例实例
_detector: Optional[LoopDetector] = None


def get_detector(max_retries: int = 3) -> LoopDetector:
    """获取全局检测器实例（单例模式）"""
    global _detector
    if _detector is None:
        _detector = LoopDetector(max_retries=max_retries)
    return _detector


def reset_detector(task_id: Optional[str] = None) -> None:
    """重置检测器"""
    global _detector
    if _detector is not None:
        _detector.reset(task_id)
