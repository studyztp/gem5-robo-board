# entobench-ae Docker image
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# gem5 deps
RUN apt -y update && apt -y upgrade && apt -y install \
    build-essential \
    scons \
    python3-dev \
    git \
    pre-commit \
    zlib1g \
    zlib1g-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libprotoc-dev \
    libgoogle-perftools-dev \
    libboost-all-dev \
    libhdf5-serial-dev \
    python3-pydot \
    python3-venv \
    python3-tk \
    mypy \
    m4 \
    libcapstone-dev \
    libpng-dev \
    libelf-dev \
    pkg-config \
    wget \
    cmake \
    doxygen
# gem5 deps end

# Core build deps + Python + helpers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake ninja-build git curl wget ca-certificates xz-utils unzip \
    python3 python3-venv python3-pip python3-dev pkg-config \
    libusb-1.0-0-dev libhidapi-dev libfuse2 udev \
    openjdk-17-jre-headless \
    sudo gosu tzdata \
 && rm -rf /var/lib/apt/lists/*

# ---- Arm GNU Toolchain (arm-none-eabi) 14.3 ----
# EntoBench pins 14.3 in its install steps; we install that exact series. 
# If Arm updates the exact tarball name, tweak the URL below accordingly.
ARG ARM_GCC_VERSION=14.3.rel1
WORKDIR /opt
RUN set -eux; \
    FILE="arm-gnu-toolchain-${ARM_GCC_VERSION}-x86_64-arm-none-eabi.tar.xz"; \
    URL="https://developer.arm.com/-/media/Files/downloads/gnu/${ARM_GCC_VERSION}/binrel/${FILE}"; \
    curl -fL "${URL}" -o "${FILE}"; \
    tar -xJf "${FILE}"; \
    ln -s "/opt/arm-gnu-toolchain-${ARM_GCC_VERSION}-x86_64-arm-none-eabi" /opt/arm-gnu-toolchain; \
    rm -f "${FILE}"
ENV PATH="/opt/arm-gnu-toolchain/bin:${PATH}"
# Reference for the download family & filenames. :contentReference[oaicite:2]{index=2}

# ---- Python virtual env mirroring scripts/install/02-setup-python-venv.sh ----
# We create the venv here; you can install project Python deps after you mount your repo.
RUN python3 -m venv /opt/venvs/entobench-ae \
 && /opt/venvs/entobench-ae/bin/pip install --upgrade pip wheel

ENV VIRTUAL_ENV=/opt/venvs/entobench-ae
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Work directory inside container
RUN mkdir -p /work
WORKDIR /work

# Minimal entrypoint to create a user matching host UID/GID
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
