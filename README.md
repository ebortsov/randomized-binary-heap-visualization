# Very simple Treap with vizualization in python

## Example of usage:
```python
  treap = RandomizedBinaryHeap()
  treap.insert(key=10, value="abacaba")
  treap.insert(key=5, value="apricot")
  treap.insert(key=90, value=[1, 2, 3])
  with open("example.svg", mode='w') as file:
    treap.create_svg(file)
```
