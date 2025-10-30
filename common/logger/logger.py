# src/common/logger.py
import logging

# 기본 로깅 설정
# 포맷: [시간] - [로거 이름] - [로그 레벨] - [메시지]
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_logger(name: str) -> logging.Logger:
    """이름을 받아 로거 인스턴스를 반환합니다."""
    return logging.getLogger(name)