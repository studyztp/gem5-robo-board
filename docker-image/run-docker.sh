# Require $1 and show usage if missing
if [[ $# -lt 1 ]]; then
  echo "usage: $0 <host-workdir>" >&2
  exit 1
fi

HOST_WORKDIR=$1

if [[ ! -d $HOST_WORKDIR ]]; then
  echo "error: host workdir '$HOST_WORKDIR' does not exist" >&2
  exit 1
fi

# Canonicalize (handles symlinks; also preserves spaces)
HOST_WORKDIR="$(cd "$HOST_WORKDIR" && pwd -P)"

echo "Using host workdir: $HOST_WORKDIR"

docker run --rm -it \
  -e LOCAL_UID="$(id -u)" -e LOCAL_GID="$(id -g)" -e LOCAL_USER="$USER" \
  -v $HOST_WORKDIR:/work -w /work \
  gem5-robo-board:latest