#!/bin/bash

# Git worktree에 gitignore된 파일들을 복사하는 스크립트
# Usage: copy_ignored_files.sh <source_dir> <target_dir> <file1> [file2 ...]

set -e

SOURCE_DIR="$1"
TARGET_DIR="$2"
shift 2
FILES_TO_COPY=("$@")

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 복사할 파일/디렉토리: ${#FILES_TO_COPY[@]}개"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

COPIED_COUNT=0
SKIPPED_COUNT=0

for item in "${FILES_TO_COPY[@]}"; do
    SOURCE_PATH="${SOURCE_DIR}/${item}"
    TARGET_PATH="${TARGET_DIR}/${item}"

    # 소스 파일/디렉토리가 존재하는지 확인
    if [ ! -e "$SOURCE_PATH" ]; then
        echo -e "${YELLOW}⏭️  건너뜀:${NC} ${item} (존재하지 않음)"
        ((SKIPPED_COUNT++))
        continue
    fi

    # 디렉토리인 경우
    if [ -d "$SOURCE_PATH" ]; then
        # 대상 디렉토리의 부모 디렉토리 생성
        mkdir -p "$(dirname "$TARGET_PATH")"

        # rsync로 디렉토리 복사 (숨김 파일 포함, .git 제외)
        if rsync -a --exclude='.git' "$SOURCE_PATH/" "$TARGET_PATH/" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} 복사 완료: ${item}/"
            ((COPIED_COUNT++))
        else
            echo -e "${RED}✗${NC} 복사 실패: ${item}/"
        fi
    # 파일인 경우
    else
        # 대상 디렉토리 생성
        mkdir -p "$(dirname "$TARGET_PATH")"

        # 파일 복사
        if cp "$SOURCE_PATH" "$TARGET_PATH" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} 복사 완료: ${item}"
            ((COPIED_COUNT++))
        else
            echo -e "${RED}✗${NC} 복사 실패: ${item}"
        fi
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ 복사 완료:${NC} ${COPIED_COUNT}개"
if [ $SKIPPED_COUNT -gt 0 ]; then
    echo -e "${YELLOW}⏭️  건너뜀:${NC} ${SKIPPED_COUNT}개"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
