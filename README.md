# Clone
via ssh:
```
git clone git@github.com:carboled/scanpostprocess.git
```
or via https:
```
git clone https://github.com/carboled/scanpostprocess.git
```

# Make environment

- move to folder
```
cd scanpostprocess
```
- make a new environment
```
python -m venv myenv
```
- UNIX: activate environmemt
```
source myenv/bin/activate
```

- WINDOWS: activate environmemt
```
source myenv/Scripts/activate
```

- Install requirements
```
pip install -r requirements.txt
```

# Usage

```
python src.py /path/to/xyz/scan
```