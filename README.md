This library is a simple wrapper around `glabels-3-batch` and `glabels-batch-qt` - extremely convenient utilities for creating labels from pre-created templates:

- Glabels-3 - https://github.com/jimevins/glabels
- Glabels-qt - https://github.com/jimevins/glabels-qt
# Installation  
  
```shell
pip install glabels
```  
  
# Usage  
### glabels-batch-qt  
  
```python  
from glabels import GLabelsBatchQT  
  
  
g = GLabelsBatchQT("/path/to/glabels-batch-qt")  
  
# If you call the function without the output parameter,  
# the output will be given in bytes as the result of execution  
out = g.run(
	template='path/to/template',
	copies=3,
)
print(out)
# b'%PDF-1.4\n%\xc3\xa2\xc3\.........'

# If you specify the path to the output file
out = g.run(
	template='path/to/template',  
	output="path/to/output",  
	copies=3,  
)  
print(out)  
# None  
  
# Instead of specifying the path to the template, 
# you can give it in bytes  
out = g.run(  
	template=b'...',  
	copies=3,  
)  
print(out)  
# b'%PDF-1.4\n%\xc3\xa2\xc3\.........'  
```

> Since `glabals-bath-qt` itself does not issue errors in `stdout`, `subprocess.Popen` cannot catch errors. (At least, I do not know how)
### glabels-3-batch

```python
from glabels import Glabels3Batch  
  
  
g = Glabels3Batch("/path/to/glabels-3-batch")  
  
# If you call the function without the output parameter,  
# the output will be given in bytes as the result of execution  
# Here you need to understand that there will be not only PDF in stdout  
out = g.run(  
	template='path/to/template',  
	copies=3,  
)  
  
print(out)  
# b'LABEL FILE = /path/to/template\n%PDF-1.4\n%\xc3\xa2\xc3\.........'  
  
# If you specify the path to the output file  
out = g.run(  
	template='path/to/template',  
	output="path/to/output",  
	copies=3,  
)  
print(out)  
# None  
  
# Instead of specifying the path to the template, you can give it in bytes  
out = g.run(  
	template=b'...',  
	copies=3,  
)  
print(out)  
# b'LABEL FILE = /path/to/template\n%PDF-1.4\n%\xc3\xa2\xc3\.........'
```