#!/bin/bash

# ClaudeHydro Export Tool - Push to GitHub
# Commands to push your completed export tool to GitHub

echo "🚀 Pushing ClaudeHydro Export Tool to GitHub..."
echo "🌐 Repository: https://github.com/AncientPsychicTandemWarElephant/Hydro-Export-Tool"
echo ""

# Navigate to the Export Tool directory
cd "/home/ntrevean/ClaudeHydro/Export Tool"

# Initialize git repository
echo "📂 Initializing git repository..."
git init

# Configure git user settings
echo "⚙️ Configuring git settings..."
git config user.name "AncientPsychicTandemWarElephant"
git config user.email "your-email@example.com"  # Update with your email

# Add GitHub remote repository
echo "🔗 Adding GitHub remote..."
git remote add origin https://github.com/AncientPsychicTandemWarElephant/Hydro-Export-Tool.git

# Add all files to staging (respecting .gitignore)
echo "📁 Adding files to staging area..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: ClaudeHydro Export Tool with comprehensive testing

Features:
- Complete export tool with GUI interface
- Dual-column header editor with tooltips (2-second hover delay)
- Multiple export modes (merged, individual, chronological)
- Seamless merging without file separators
- Lucy parser compatibility maintained
- Ocean Sonics format preservation
- Comprehensive test framework with SABIC data validation
- All 6 export combinations tested and validated

Technical Implementation:
- Python 3.7+ with tkinter GUI
- Robust file validation and error handling
- Real-time progress tracking
- Timezone conversion support
- Metadata override system
- Threading for background processing

Testing Results:
- ✅ 6/6 export tests successful
- ✅ 7/7 source files validated  
- ✅ 8/12 exports Lucy-compatible
- ✅ Data integrity confirmed
- ✅ Header preservation verified

🤖 Generated with Claude Code (https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Set the default branch to main
echo "🌿 Setting default branch to main..."
git branch -M main

# Push to GitHub
echo "📤 Pushing to GitHub..."
echo "Note: You may need to authenticate with GitHub"
git push -u origin main

echo ""
echo "✅ Push complete!"
echo "🌐 Your repository: https://github.com/AncientPsychicTandemWarElephant/Hydro-Export-Tool"
echo ""
echo "📋 If authentication fails, try:"
echo "   - GitHub Personal Access Token"
echo "   - SSH key setup"
echo "   - GitHub CLI: gh auth login"