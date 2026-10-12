#!/bin/sh
# UserPromptSubmit: a visual ask in the prompt loads the show skill.
grep -qiE 'montre[sz]?[- ]moi|(mani.{1,8}re|fa.{1,6}on) visuelle|visuellement|visualis|show me|visually' || exit 0
printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"The user asks for a visual answer: load the show skill before writing it."}}'
