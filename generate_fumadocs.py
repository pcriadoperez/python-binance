#!/usr/bin/env python3
"""
Custom script to generate Fumadocs JSON for python-binance package.
Works around the package name mismatch (module: binance, dist: python-binance).
"""
import json
import griffe
import sys

def generate_docs(module_name, output_file=None):
    """Generate documentation JSON for a Python module."""
    try:
        # Load the module using griffe
        loader = griffe.GriffeLoader()
        module = loader.load(module_name)

        # Get version from the module itself
        try:
            import importlib
            mod = importlib.import_module(module_name)
            version = getattr(mod, '__version__', 'unknown')
        except Exception:
            version = 'unknown'

        # Build the documentation structure
        doc_data = {
            "name": module_name,
            "version": version,
            "module": serialize_module(module)
        }

        # Write to file
        if output_file is None:
            output_file = f"{module_name}.json"

        with open(output_file, 'w') as f:
            json.dump(doc_data, f, indent=2)

        print(f"Documentation generated successfully: {output_file}")
        return True

    except Exception as e:
        print(f"Error generating documentation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def serialize_module(obj):
    """Serialize a griffe object to a dictionary."""
    if obj is None:
        return None

    result = {
        "name": obj.name,
        "kind": obj.kind.value,
        "docstring": serialize_docstring(obj.docstring),
    }

    if hasattr(obj, 'members') and obj.members:
        result["members"] = {}
        for name, member in obj.members.items():
            # Skip private members unless they're special methods
            if name.startswith('_') and not (name.startswith('__') and name.endswith('__')):
                continue
            try:
                result["members"][name] = serialize_object(member)
            except Exception as e:
                print(f"Warning: Failed to serialize {name}: {e}", file=sys.stderr)
                continue

    return result

def serialize_object(obj):
    """Serialize any griffe object."""
    if obj is None:
        return None

    result = {
        "name": obj.name,
        "kind": obj.kind.value,
        "docstring": serialize_docstring(obj.docstring),
    }

    # Add file path if available
    if hasattr(obj, 'filepath') and obj.filepath:
        result["filepath"] = str(obj.filepath)

    # Add line numbers if available
    if hasattr(obj, 'lineno'):
        result["lineno"] = obj.lineno
    if hasattr(obj, 'endlineno'):
        result["endlineno"] = obj.endlineno

    # Handle functions and methods
    if obj.kind.value in ['function', 'method']:
        result["parameters"] = serialize_parameters(obj.parameters) if hasattr(obj, 'parameters') else []
        if hasattr(obj, 'returns'):
            result["returns"] = serialize_annotation(obj.returns)

    # Handle classes
    if obj.kind.value == 'class':
        if hasattr(obj, 'bases'):
            result["bases"] = [str(base) for base in obj.bases]
        if hasattr(obj, 'members') and obj.members:
            result["members"] = {}
            for name, member in obj.members.items():
                # Skip private members
                if name.startswith('_') and not (name.startswith('__') and name.endswith('__')):
                    continue
                try:
                    result["members"][name] = serialize_object(member)
                except Exception:
                    continue

    # Handle attributes
    if obj.kind.value == 'attribute':
        if hasattr(obj, 'annotation'):
            result["annotation"] = serialize_annotation(obj.annotation)
        if hasattr(obj, 'value'):
            result["value"] = str(obj.value)

    return result

def serialize_docstring(docstring):
    """Serialize a docstring."""
    if docstring is None:
        return None
    return {
        "value": docstring.value if hasattr(docstring, 'value') else str(docstring)
    }

def serialize_parameters(parameters):
    """Serialize function parameters."""
    result = []
    for param in parameters.values():
        param_data = {
            "name": param.name,
        }
        if hasattr(param, 'annotation') and param.annotation:
            param_data["annotation"] = serialize_annotation(param.annotation)
        if hasattr(param, 'default') and param.default:
            param_data["default"] = str(param.default)
        result.append(param_data)
    return result

def serialize_annotation(annotation):
    """Serialize a type annotation."""
    if annotation is None:
        return None
    return str(annotation)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: generate_fumadocs.py <module_name> [output_file]")
        sys.exit(1)

    module_name = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    success = generate_docs(module_name, output_file)
    sys.exit(0 if success else 1)
