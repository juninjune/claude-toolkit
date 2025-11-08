#!/bin/bash

# IDE를 감지하고 실행하는 스크립트
# Usage: detect_ide.sh <directory_path>

set -e

TARGET_DIR="$1"
IDE_PREFERENCE="${2:-cursor}"  # 기본값: cursor

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Cursor 확인
if command -v cursor &> /dev/null; then
    HAS_CURSOR=true
else
    HAS_CURSOR=false
fi

# VS Code 확인
if command -v code &> /dev/null; then
    HAS_CODE=true
else
    HAS_CODE=false
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 IDE 실행"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# IDE 실행 우선순위
if [ "$IDE_PREFERENCE" = "cursor" ] && [ "$HAS_CURSOR" = true ]; then
    echo -e "${GREEN}✓${NC} Cursor로 실행 중..."
    cursor -n "$TARGET_DIR" &
    echo -e "${GREEN}✅ Cursor가 새 창에서 열렸습니다${NC}"
    echo ""
    exit 0
elif [ "$IDE_PREFERENCE" = "code" ] && [ "$HAS_CODE" = true ]; then
    echo -e "${GREEN}✓${NC} VS Code로 실행 중..."
    code -n "$TARGET_DIR" &
    echo -e "${GREEN}✅ VS Code가 새 창에서 열렸습니다${NC}"
    echo ""
    exit 0
elif [ "$HAS_CURSOR" = true ]; then
    echo -e "${YELLOW}⚠️  선호 IDE를 찾을 수 없습니다. Cursor를 대신 사용합니다${NC}"
    cursor -n "$TARGET_DIR" &
    echo -e "${GREEN}✅ Cursor가 새 창에서 열렸습니다${NC}"
    echo ""
    exit 0
elif [ "$HAS_CODE" = true ]; then
    echo -e "${YELLOW}⚠️  선호 IDE를 찾을 수 없습니다. VS Code를 대신 사용합니다${NC}"
    code -n "$TARGET_DIR" &
    echo -e "${GREEN}✅ VS Code가 새 창에서 열렸습니다${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Cursor 또는 VS Code를 찾을 수 없습니다${NC}"
    echo ""
    echo "수동으로 IDE를 실행하세요:"
    echo "  cd $TARGET_DIR"
    echo ""
    exit 1
fi
