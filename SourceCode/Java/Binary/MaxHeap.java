// TODO: In Java, some of these are private methods (including update)
// TODO: Need to test changes to update and modify
/* *** ODSATag: Maxheap *** */
// Max-heap implementation
class MaxHeap {
  private Comparable[] Heap; // Pointer to the heap array
  private int size;          // Maximum size of the heap
  private int n;             // Number of things now in heap

  // Constructor supporting preloading of heap contents
  MaxHeap(Comparable[] h, int num, int max)
  { Heap = h;  n = num;  size = max;  buildheap(); }

  // Return current size of the heap
  int heapsize() { return n; }

  // Return true if pos a leaf position, false otherwise
  boolean isLeaf(int pos)
  { return (pos >= n/2) && (pos < n); }

  // Return position for left child of pos
  int leftchild(int pos) {
    if (pos >= n/2) { return -1; }
    return 2*pos + 1;
  }

  // Return position for right child of pos
  int rightchild(int pos) {
    if (pos >= (n-1)/2) { return -1; }
    return 2*pos + 2;
  }

  // Return position for parent
  int parent(int pos) {
    if (pos <= 0) { return -1; }
    return (pos-1)/2;
  }

  // Insert val into heap
  void insert(int key) {
    if (n >= size) {
      System.out.println("Heap is full");
      return;
    }
    int curr = n++;
    Heap[curr] = key;  // Start at end of heap
    // Now sift up until curr's parent's key > curr's key
    while ((curr != 0) && (Heap[curr].compareTo(Heap[parent(curr)]) > 0)) {
      Swap.swap(Heap, curr, parent(curr));
      curr = parent(curr);
    }
  }

  // Heapify contents of Heap
  void buildheap()
    { for (int i=n/2-1; i>=0; i--) { siftdown(i); } }

  // Put element in its correct place
  void siftdown(int pos) {
    if ((pos < 0) || (pos >= n)) { return; } // Illegal position
    while (!isLeaf(pos)) {
      int j = leftchild(pos);
      if ((j<(n-1)) && (Heap[j].compareTo(Heap[j+1]) < 0)) {
        j++; // j is now index of child with greater value
      }
      if (Heap[pos].compareTo(Heap[j]) >= 0) { return; }
      Swap.swap(Heap, pos, j);
      pos = j;  // Move down
    }
  }

  // Remove and return maximum value
  Comparable removemax() {
    if (n == 0) { return -1; }  // Removing from empty heap
    Swap.swap(Heap, 0, --n); // Swap maximum with last value
    siftdown(0);   // Put new heap root val in correct place
    return Heap[n];
  }

  // Remove and return element at specified position
  Comparable remove(int pos) {
    if ((pos < 0) || (pos >= n)) { return -1; } // Illegal heap position
    if (pos == (n-1)) { n--; } // Last element, no work to be done
    else {
      Swap.swap(Heap, pos, --n); // Swap with last value
      update(pos);
    }
    return Heap[n];
  }

  // Modify the value at the given position
  void modify(int pos, Comparable newVal) {
    if ((pos < 0) || (pos >= n)) { return; } // Illegal heap position
    Heap[pos] = newVal;
    update(pos);
  }

  // The value at pos has been changed, restore the heap property
  void update(int pos) {
    // If it is a big value, push it up
    while ((pos > 0) && (Heap[pos].compareTo(Heap[parent(pos)]) > 0)) {
      Swap.swap(Heap, pos, parent(pos));
      pos = parent(pos);
    }
    siftdown(pos); // If it is little, push down
  }
}
/* *** ODSAendTag: Maxheap *** */
