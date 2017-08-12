Running `python showerror.py` returns:

```
libc++abi.dylib: terminating with uncaught exception of type kiwi::InternalSolverError: Dual optimize failed.
```

If I change line 305 of `LayoutBox.py` to 

```
		self.solver.addConstraint((c | 'strong'))
```

the code runs.  Interestingly, even if I set it to 'required' it still works!

If I run the code with fewer subplots:

```
fig0, axs = plt.subplots(2,2)
```
it also works...

## Dependencies:

  - kiwisolver
  - numpy
  - matplotlib (>2.0?)

Note, you may need to change the matplotlib backend (`matplotlib.use()`) depending on your available backends.

