import os
import fnmatch

def should_exclude(path, filename):
    """Check if file/folder should be excluded based on Django project patterns"""
    exclude_patterns = [
        # Python compiled files
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '__pycache__',
        
        # Database files
        '*.sqlite3',
        '*.db',
        
        # Environment and config
        '.env',
        '.env.local',
        '.env.production',
        '*.log',
        
        # Version control
        '.git',
        '.gitignore',
        '.gitattributes',
        
        # IDEs and editors
        '.vscode',
        '.idea',
        '*.swp',
        '*.swo',
        '*~',
        '.DS_Store',
        'Thumbs.db',
        
        # Virtual environments
        'venv',
        'env',
        '*_env',
        '.venv',
        'virtualenv',
        
        # Dependencies
        'node_modules',
        'bower_components',
        
        # Media files (images, videos, etc.)
        '*.jpg',
        '*.jpeg',
        '*.png',
        '*.gif',
        '*.svg',
        '*.ico',
        '*.mp4',
        '*.avi',
        '*.mov',
        '*.wmv',
        '*.mkv',
        '*.mp3',
        '*.wav',
        '*.pdf',
        '*.doc',
        '*.docx',
        
        # Compressed files
        '*.zip',
        '*.rar',
        '*.tar',
        '*.gz',
        
        # Django specific
        'migrations',  # Will exclude migration files
        '*.pot',
        '*.mo',
        
        # Static files (if collected)
        'staticfiles',
        'collected_static',
        
        # Cache files
        '.cache',
        '*.cache',
        
        # Minified files
        '*.min.js',
        '*.min.css',
        
        # Third-party libraries
        'bootstrap*',
        'jquery*',
        'fontawesome*',
        'vendor',
        'libs',
        'libraries',
        
        # Build files
        'dist',
        'build',
        '*.egg-info',
        
        # Temporary files
        'tmp',
        'temp',
        '*.tmp',
        '*.temp',
        
        # Coverage reports
        'htmlcov',
        '.coverage',
        'coverage.xml',
        
        # Pytest
        '.pytest_cache',
        
        # Django debug toolbar
        'debug_toolbar',
        
        # Local settings that might contain secrets
        'local_settings.py',
        'settings_local.py',
    ]

    for pattern in exclude_patterns:
        if fnmatch.fnmatch(filename.lower(), pattern.lower()) or pattern.lower() in path.lower():
            return True
    
    # Also exclude specific directories
    exclude_dirs = ['__pycache__', '.git', 'node_modules', 'venv', 'env', 'media', 'static']
    if any(exclude_dir in path for exclude_dir in exclude_dirs):
        return True
        
    return False

def get_file_content(filepath):
    """Read file content with proper encoding handling"""
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                # Limit very large files
                if len(content) > 50000:  # 50KB limit
                    return content[:50000] + "\n\n[FILE TRUNCATED - Too large to display completely]"
                return content
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"Error reading file: {str(e)}"

    return "Could not read file due to encoding issues"

def is_important_file(filepath, filename):
    """Check if file is important for Django project understanding"""
    important_extensions = [
        '.py',      # Python files
        '.html',    # Templates
        '.css',     # Styles
        '.js',      # JavaScript
        '.json',    # Configuration files
        '.txt',     # Requirements, README, etc.
        '.md',      # Markdown files
        '.yml',     # YAML config
        '.yaml',    # YAML config
        '.toml',    # TOML config
        '.cfg',     # Config files
        '.ini',     # Config files
        '.conf',    # Config files
    ]
    
    important_filenames = [
        'manage.py',
        'requirements.txt',
        'requirements-dev.txt',
        'README.md',
        'README.txt',
        'Procfile',
        'runtime.txt',
        'Dockerfile',
        'docker-compose.yml',
        'setup.py',
        'setup.cfg',
        'pyproject.toml',
        '.env.example',
        'Makefile',
    ]
    
    file_ext = os.path.splitext(filename)[1].lower()
    
    return (file_ext in important_extensions or 
            filename.lower() in [f.lower() for f in important_filenames])

def generate_django_project_summary(root_dir, output_file):
    """Generate comprehensive Django project summary"""
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("="*80 + "\n")
        out.write("LEARNHUB DJANGO PROJECT - COMPLETE CODE SUMMARY\n")
        out.write("="*80 + "\n")
        out.write(f"Generated from: {root_dir}\n")
        out.write(f"Export Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write("="*80 + "\n\n")

        # Write project structure first
        out.write("📁 PROJECT STRUCTURE:\n")
        out.write("-"*60 + "\n")

        for root, dirs, files in os.walk(root_dir):
            # Filter out excluded directories early
            dirs[:] = [d for d in dirs if not should_exclude(root, d)]

            level = root.replace(root_dir, '').count(os.sep)
            indent = "  " * level
            folder_name = os.path.basename(root) if root != root_dir else "📦 LearnHub Project"
            out.write(f"{indent}📁 {folder_name}/\n")

            sub_indent = "  " * (level + 1)
            for file in sorted(files):
                if not should_exclude(root, file) and is_important_file(root, file):
                    # Add file type emoji
                    if file.endswith('.py'):
                        emoji = "🐍"
                    elif file.endswith('.html'):
                        emoji = "📄"
                    elif file.endswith(('.css', '.scss')):
                        emoji = "🎨"
                    elif file.endswith('.js'):
                        emoji = "⚡"
                    elif file.endswith(('.json', '.yml', '.yaml')):
                        emoji = "⚙️"
                    elif file.endswith('.md'):
                        emoji = "📝"
                    else:
                        emoji = "📄"
                    
                    out.write(f"{sub_indent}{emoji} {file}\n")

        out.write("\n" + "="*80 + "\n")
        out.write("📋 FILE CONTENTS:\n")
        out.write("="*80 + "\n\n")

        file_count = 0
        
        # Process all important files
        for root, dirs, files in os.walk(root_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(root, d)]

            for file in sorted(files):
                filepath = os.path.join(root, file)

                if (should_exclude(root, file) or 
                    not is_important_file(root, file)):
                    continue

                relative_path = os.path.relpath(filepath, root_dir)
                file_count += 1

                # Add file type indicator
                if file.endswith('.py'):
                    file_type = "🐍 PYTHON FILE"
                elif file.endswith('.html'):
                    file_type = "📄 HTML TEMPLATE"
                elif file.endswith('.css'):
                    file_type = "🎨 CSS STYLESHEET"
                elif file.endswith('.js'):
                    file_type = "⚡ JAVASCRIPT"
                elif file.endswith('.json'):
                    file_type = "⚙️ JSON CONFIG"
                elif file.endswith('.md'):
                    file_type = "📝 MARKDOWN"
                elif file.endswith('.txt'):
                    file_type = "📄 TEXT FILE"
                else:
                    file_type = "📄 FILE"

                out.write(f"\n{'='*70}\n")
                out.write(f"{file_type}: {relative_path}\n")
                out.write(f"{'='*70}\n")

                content = get_file_content(filepath)
                out.write(content)
                out.write("\n")

        out.write(f"\n{'='*80}\n")
        out.write(f"📊 SUMMARY: Exported {file_count} files from LearnHub Django Project\n")
        out.write(f"{'='*80}\n")

def main():
    """Main function to run the export"""
    # Get current directory (project root)
    project_root = os.getcwd()
    output_filename = "learnhub_complete_code.txt"

    print("🚀 LearnHub Project Code Exporter")
    print("="*50)
    print(f"📂 Scanning project directory: {project_root}")
    print(f"📄 Output file: {output_filename}")
    print("\n🔍 Processing files...")

    try:
        generate_django_project_summary(project_root, output_filename)
        
        # Get file size
        file_size = os.path.getsize(output_filename)
        size_mb = file_size / (1024 * 1024)
        
        print(f"\n✅ Project export completed successfully!")
        print(f"📄 File saved as: {output_filename}")
        print(f"📊 File size: {size_mb:.2f} MB")
        print(f"📁 Location: {os.path.abspath(output_filename)}")
        print(f"\n💡 You can now share this file with any AI model or developer!")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print("Please check file permissions and try again.")

if __name__ == "__main__":
    main()
