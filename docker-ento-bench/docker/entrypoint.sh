#!/usr/bin/env bash
set -euo pipefail

# Map host UID/GID to a container user so mounted files remain owned by you.
: "${LOCAL_USER:=dev}"
: "${LOCAL_UID:=1000}"
: "${LOCAL_GID:=1000}"

# Create group if needed
if ! getent group "${LOCAL_GID}" >/dev/null 2>&1; then
  groupadd --gid "${LOCAL_GID}" "${LOCAL_USER}" || groupadd --gid "${LOCAL_GID}" hostgroup
fi

# Create user if needed (use the group we just ensured)
if ! id -u "${LOCAL_USER}" >/dev/null 2>&1; then
  useradd --create-home --home-dir "/home/${LOCAL_USER}" --shell /bin/bash \
          --uid "${LOCAL_UID}" --gid "${LOCAL_GID}" "${LOCAL_USER}"
  echo "${LOCAL_USER} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/${LOCAL_USER}"
fi

# Ensure the venv & home are writable by the mapped user
chown -R "${LOCAL_UID}:${LOCAL_GID}" "/home/${LOCAL_USER}" "/opt/venvs/entobench-ae" || true

export HOME="/home/${LOCAL_USER}"
export VIRTUAL_ENV="/opt/venvs/entobench-ae"
export PATH="${VIRTUAL_ENV}/bin:/opt/arm-gnu-toolchain/bin:${PATH}"

exec gosu "${LOCAL_USER}" "$@"
