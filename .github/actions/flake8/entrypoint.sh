#!/bin/sh -l

echo run flake8
sh -c "flake8 --config=/.flake8 $*"