# Fumadocs Integration

⚠️ **Status**: The Fumadocs integration is partially complete. The source configuration works, but there is a compilation hang issue when accessing pages. Further investigation needed.

---



This project now includes [Fumadocs](https://fumadocs.vercel.app/), a modern documentation framework that generates interactive API documentation from Python code.

## What is Fumadocs?

Fumadocs is a documentation framework built on Next.js that provides:
- Automatic API documentation generation from Python docstrings
- Beautiful, interactive UI components
- Fast search functionality
- Responsive design
- MDX support for rich content

## Setup

The Fumadocs setup has been integrated into this project with the following structure:

```
python-binance/
├── app/                    # Next.js app directory
│   ├── docs/              # Documentation routes
│   ├── layout.tsx         # Root layout
│   └── global.css         # Global styles
├── content/docs/(api)/    # Generated MDX documentation
├── lib/                   # Source configuration
├── scripts/               # Build scripts
│   └── generate-docs.mjs  # JSON to MDX converter
├── next.config.mjs        # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── source.config.ts       # Fumadocs source configuration
└── package.json           # Node.js dependencies
```

## Installation

1. Install Node.js dependencies:
```bash
npm install
```

2. Install Python fumadocs package (already done):
```bash
pip install ./node_modules/fumadocs-python
```

## Generating Documentation

To regenerate the API documentation from Python source code:

1. Generate JSON from Python package:
```bash
python3 -c "
import sys
import os
sys.path.insert(0, '/home/user/python-binance')
import importlib.metadata
original_version = importlib.metadata.version
def patched_version(distribution_name):
    if distribution_name == 'binance':
        return original_version('python-binance')
    return original_version(distribution_name)
importlib.metadata.version = patched_version
from fumapy.mksource.document_module import parse_module
import griffe
import json
pkg = parse_module(griffe.load('binance'))
with open('binance.json', 'w') as f:
    json.dump(pkg, f, indent=2, default=str)
print('Documentation generated successfully')
"
```

2. Convert JSON to MDX:
```bash
npm run generate-docs
```

## Running the Documentation Site

### Development Mode
```bash
npm run dev
```

Then visit [http://localhost:3000/docs](http://localhost:3000/docs)

### Production Build
```bash
npm run build
npm start
```

## Features

- **Python API Documentation**: Automatically generated from your Python docstrings
- **Type Annotations**: Shows parameter types and return types
- **Interactive Components**: Collapsible sections, syntax highlighting, and more
- **Search**: Fast full-text search across all documentation
- **Dark Mode**: Automatic dark mode support
- **Mobile Responsive**: Works great on all devices

## Customization

### Adding Custom Content

You can add custom MDX pages to the `content/docs/` directory. For example:

```mdx
---
title: Getting Started
description: Learn how to use python-binance
---

## Introduction

Your custom content here...
```

### Styling

Styles are configured in:
- `app/global.css` - Global styles and Fumadocs presets
- `tailwind.config.js` - Tailwind CSS configuration

### Layout

Customize the documentation layout in:
- `app/docs/layout.tsx` - Docs layout configuration

## Learn More

- [Fumadocs Documentation](https://fumadocs.vercel.app/docs)
- [Fumadocs Python Support](https://fumadocs.vercel.app/docs/ui/python)
- [Next.js Documentation](https://nextjs.org/docs)

## Troubleshooting

### Build Errors

If you encounter build errors, try:
1. Delete `.next` directory: `rm -rf .next`
2. Delete `node_modules`: `rm -rf node_modules`
3. Reinstall dependencies: `npm install`
4. Rebuild: `npm run build`

### Missing Documentation

If documentation is not showing up:
1. Ensure the JSON was generated correctly: `ls -lh binance.json`
2. Check that MDX files were created: `ls content/docs/(api)/`
3. Regenerate documentation: `npm run generate-docs`
