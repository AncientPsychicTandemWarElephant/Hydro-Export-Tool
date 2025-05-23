#!/bin/bash

# ClaudeHydro Export Tool - Git Setup Script
# Run this script to initialize git repository and create initial commit

echo "🚀 Setting up git repository for ClaudeHydro Export Tool..."

# Navigate to the Export Tool directory
cd "/home/ntrevean/ClaudeHydro/Export Tool"

# Initialize git repository
echo "📂 Initializing git repository..."
git init

# Configure git user settings
echo "⚙️ Configuring git settings..."
git config user.name "ClaudeHydro Developer"
git config user.email "dev@claudehydro.local"

# Add all files to staging (respecting .gitignore)
echo "📁 Adding files to staging area..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: ClaudeHydro Export Tool with comprehensive testing

Features:
- Complete export tool with GUI interface
- Dual-column header editor with tooltips
- Multiple export modes (merged, individual, chronological)
- Seamless merging without file separators
- Lucy parser compatibility maintained
- Ocean Sonics format preservation
- Comprehensive test framework
- SABIC data validation complete

🤖 Generated with Claude Code (https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Show git status
echo "📊 Current git status:"
git status

echo "✅ Git repository setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add GitHub remote repository..."
git remote add origin https://github.com/AncientPsychicTandemWarElephant/Hydro-Export-Tool.git

echo "2. Set upstream branch and push to GitHub..."
echo "   Note: You may need to authenticate with GitHub"
echo ""
echo "🔐 GitHub Authentication Options:"
echo "   - Personal Access Token (recommended)"
echo "   - SSH key (if configured)" 
echo "   - GitHub CLI (gh auth login)"
echo ""
echo "📤 To push to GitHub, run:"
echo "   git push -u origin main"
echo ""
echo "🎉 Your ClaudeHydro Export Tool is ready for GitHub!"
echo "🌐 Repository: https://github.com/AncientPsychicTandemWarElephant/Hydro-Export-Tool"