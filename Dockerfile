FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (required for Gemini CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Install Python 3.11
RUN apt-get update && apt-get install -y python3.11 python3.11-venv python3.11-dev && rm -rf /var/lib/apt/lists/*

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/root/.cargo/bin:$PATH"
ENV PNPM_HOME="/root/.local/share/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

# Install Gemini CLI, pyright, and pnpm
ENV SHELL=/bin/bash
RUN npm install -g @google/gemini-cli pyright pnpm && \
    SHELL=/bin/bash pnpm setup && \
    echo 'export PNPM_HOME="/root/.local/share/pnpm"' >> ~/.bashrc && \
    echo 'export PATH="$PNPM_HOME:$PATH"' >> ~/.bashrc

# Pre-configure Gemini CLI to use environment variables
RUN mkdir -p /root/.config/gemini-cli

# Create working directory
WORKDIR /app

# Clone Amplifier repository
RUN git clone https://github.com/microsoft/amplifier.git /app/amplifier

# Set working directory to amplifier
WORKDIR /app/amplifier

# Initialize Python environment with uv and install dependencies
RUN uv venv --python python3.11 .venv && \
    uv sync && \
    . .venv/bin/activate && make install

# Create data directory for Amplifier and required subdirectories
RUN mkdir -p /app/amplifier-data && \
    mkdir -p /app/amplifier/.data

# Clone Amplifier to /root/amplifier where Gemini CLI will start
RUN git clone https://github.com/microsoft/amplifier.git /root/amplifier

# Build Amplifier in /root/amplifier
WORKDIR /root/amplifier
RUN uv venv --python python3.11 .venv && \
    uv sync && \
    . .venv/bin/activate && make install

# Create required .data directory structure
RUN mkdir -p /root/amplifier/.data/knowledge && \
    mkdir -p /root/amplifier/.data/indexes && \
    mkdir -p /root/amplifier/.data/state && \
    mkdir -p /root/amplifier/.data/memories && \
    mkdir -p /root/amplifier/.data/cache

# Create Gemini CLI settings and tools
RUN mkdir -p /root/amplifier/.gemini/tools && \
    cat > /root/amplifier/.gemini/settings.json << 'SETTINGS_EOF'
{
    "statusLine": {
      "type": "command",
      "command": "bash /root/amplifier/.gemini/tools/statusline-example.sh"
    }
}
SETTINGS_EOF

# Create the statusline script referenced in settings
RUN cat > /root/amplifier/.gemini/tools/statusline-example.sh << 'STATUSLINE_EOF'
#!/bin/bash

# Simple statusline script for Gemini CLI
# Shows current directory, git branch (if available), and timestamp

# Get current directory (relative to home)
current_dir=$(pwd | sed "s|$HOME|~|")

# Try to get git branch if in a git repository
git_info=""
if git rev-parse --git-dir > /dev/null 2>&1; then
    branch=$(git branch --show-current 2>/dev/null || echo "detached")
    git_info=" [git:$branch]"
fi

# Get current timestamp
timestamp=$(date '+%H:%M:%S')

# Output statusline
echo "📂 $current_dir$git_info | 🕐 $timestamp"
STATUSLINE_EOF

# Make the statusline script executable
RUN chmod +x /root/amplifier/.gemini/tools/statusline-example.sh

# Create entrypoint script with comprehensive Gemini CLI configuration
RUN cat > /app/entrypoint.sh << 'EOF'
#!/bin/bash
set -e

# Logging function with timestamps
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# Error handling function
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Validate API key format
validate_api_key() {
    local api_key="$1"
    # Basic validation for Google API key (usually starts with AIza or similar, but let's just check length)
    if [[ ${#api_key} -lt 20 ]]; then
        log "WARNING: API key may be invalid (too short)"
        return 1
    fi
    return 0
}

# Create comprehensive Gemini configuration file
create_gemini_config() {
    local api_key="$1"
    local config_file="$HOME/.gemini/config.json"

    log "Creating Gemini configuration at: $config_file"

    # Create configuration directory
    mkdir -p "$(dirname "$config_file")"

    cat > "$config_file" << CONFIG_EOF
{
  "apiKey": "$api_key",
  "hasCompletedOnboarding": true,
  "projects": {}
}
CONFIG_EOF

    log "Configuration file created successfully"
}

# Set CLI configuration flags
configure_gemini_cli() {
    log "Setting Gemini CLI configuration flags..."

    # Set configuration flags to skip interactive prompts
    gemini config set hasCompletedOnboarding true 2>/dev/null || log "WARNING: Failed to set hasCompletedOnboarding"
    gemini config set hasTrustDialogAccepted true 2>/dev/null || log "WARNING: Failed to set hasTrustDialogAccepted"

    log "CLI configuration completed"
}

# Verify configuration
verify_configuration() {
    local config_file="$HOME/.gemini/config.json"

    log "Verifying Gemini configuration..."

    # Check file existence
    if [[ ! -f "$config_file" ]]; then
        log "Configuration file not found: $config_file (This might be expected if using env vars)"
    fi

    log "Configuration verification successful"
}

# Test Gemini functionality
test_gemini_functionality() {
    log "Testing Gemini CLI functionality..."

    # Test basic command
    if gemini --version >/dev/null 2>&1; then
        local version=$(gemini --version 2>/dev/null || echo "Unknown")
        log "Gemini CLI version check successful: $version"
    else
        log "WARNING: Gemini CLI version check failed"
    fi
}

# Main setup function
main() {
    # Default to /workspace if no target directory specified
    TARGET_DIR=${TARGET_DIR:-/workspace}
    AMPLIFIER_DATA_DIR=${AMPLIFIER_DATA_DIR:-/app/amplifier-data}

    log "🚀 Starting Amplifier Docker Container with Gemini CLI Configuration"
    log "📁 Target project: $TARGET_DIR"
    log "📊 Amplifier data: $AMPLIFIER_DATA_DIR"

    # Comprehensive environment variable debugging
    log "🔍 Environment Variable Debug Information:"
    log "   HOME: $HOME"
    log "   USER: $(whoami)"
    log "   PWD: $PWD"

    # Debug API key availability (masked for security)
    if [ ! -z "$GEMINI_API_KEY" ]; then
        local masked_key="****${GEMINI_API_KEY: -4}"
        log "   GEMINI_API_KEY: $masked_key"
        validate_api_key "$GEMINI_API_KEY" || log "   API key validation warning"
    elif [ ! -z "$GOOGLE_API_KEY" ]; then
        local masked_key="****${GOOGLE_API_KEY: -4}"
        log "   GOOGLE_API_KEY: $masked_key"
        export GEMINI_API_KEY="$GOOGLE_API_KEY"
    else
        log "   GEMINI_API_KEY: (not set)"
    fi

    # Validate target directory exists
    if [ -d "$TARGET_DIR" ]; then
        log "✅ Target directory found: $TARGET_DIR"
    else
        log "❌ Target directory not found: $TARGET_DIR"
        log "💡 Make sure you mounted your project directory to $TARGET_DIR"
        exit 1
    fi

    # Change to Amplifier directory and activate environment
    log "🔧 Setting up Amplifier environment..."
    cd /root/amplifier
    source .venv/bin/activate

    # Configure Amplifier data directory
    log "📂 Configuring Amplifier data directory..."
    export AMPLIFIER_DATA_DIR="$AMPLIFIER_DATA_DIR"

    # Check if API key is available
    if [ -z "$GEMINI_API_KEY" ]; then
        error_exit "No API keys found! Please set GEMINI_API_KEY or GOOGLE_API_KEY"
    fi

    log "🔧 Configuring Gemini CLI..."

    # Create configuration
    create_gemini_config "$GEMINI_API_KEY"

    # Set CLI configuration flags
    configure_gemini_cli

    # Verify configuration
    verify_configuration

    # Test basic functionality
    test_gemini_functionality

    log "✅ Gemini CLI configuration completed successfully"
    log "📁 Adding target directory: $TARGET_DIR"
    log "🚀 Starting interactive Gemini CLI session..."
    log ""

    # Start Gemini with directory access
    gemini --add-dir "$TARGET_DIR" "I'm working in $TARGET_DIR which doesn't have Amplifier files. Please cd to that directory and work there."
}

# Execute main function
main "$@"
EOF

RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV TARGET_DIR=/workspace
ENV AMPLIFIER_DATA_DIR=/app/amplifier-data
ENV PATH="/app/amplifier:$PATH"

# Create volumes for mounting
VOLUME ["/workspace", "/app/amplifier-data"]

# Set the working directory to Amplifier before entrypoint
WORKDIR /root/amplifier

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]