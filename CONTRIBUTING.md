# Dealing with Agents not supported by httpagentparser

```python
import httpagentparser as hap

class JakartaHTTPClinet(hap.Browser):
    name = 'Jakarta Commons-HttpClient'
    look_for = name
    version_splitters = ["/"]

class SomeNotSoCommonClient(hap.Browser):
    name = 'NotSoCommon Client'
    look_for = 'NotSoCommon'
    def getVersion(self, agent):
        return agent.split(':')[1]

# Registering new UAs

hap.detectorshub.register(JakartaHTTPClinet())
hap.detectorshub.register(SomeNotSoCommonClient())

# Tests

s = "Jakarta Commons-HttpClient/3.1"

print(hap.detect(s))
print(hap.simple_detect(s))

s = "NotSoCommon:3.1"

print(hap.detect(s))
print(hap.simple_detect(s))
```

# Build and upload new version

1. Bump `__version__` in `httpagentparser/__init__.py`
2. Install modern build and upload tools: `python -m pip install build twine`
3. Build the package: `python -m build`
4. Upload to PyPI: `python -m twine upload dist/*`

# Test httpagentparser

- `python tests.py`
