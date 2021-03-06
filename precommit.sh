#!/bin/bash

# abort on errors
set -e

check_changes() {
  if git diff --stat --cached -- "$1" | grep -E "$1"; then
    echo "run precommit for $1"
    return 0
  else
    echo "no changes found for $1"
    return 1
  fi
}

force_run_command="-f"

node_paths=("docs/quant_docs/frontend/" "docs/quant_docs/server/" "bailey/frontend")

for path in "${node_paths[@]}"
do
  if [ "$1" = "$force_run_command" ] || check_changes "$path" ; then
    npm run precommit --prefix $path
  fi
done

script_paths=("sdk" "bailey/api" "modules/weekly_report" "modules/stock_data_update" \
              "modules/stop_loss_update" "factor_model")

for path in "${script_paths[@]}"
do
  if [ "$1" = "$force_run_command" ] || check_changes "$path" ; then
    cd "$path"
    ./precommit.sh
    cd -
  fi
done

git secrets --scan

# run check for tabs precommit
cd scripts/precommit
./spaces.sh
./line_endings.sh
./check_symlinks.sh
cd -

git add -A

exit 0
